from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from pathlib import Path
from collections import Counter
import json
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("banking_rag_api")


app = FastAPI(
    title="Banking RAG API",
    version="1.0"
)

@app.get("/api/health")
def health_check():
    dashboard_ok = DASHBOARD_FILE.exists()
    review_queue_ok = REVIEW_FILE.exists()

    dependencies = {
        "dashboard_data": dashboard_ok,
        "review_queue": review_queue_ok
    }

    overall_status = (
        "healthy"
        if all(dependencies.values())
        else "degraded"
    )

    return {
        "status": overall_status,
        "service": "Banking RAG API",
        "version": "1.0",
        "dependencies": dependencies
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DASHBOARD_FILE = Path(
    "dashboard_data.json"
)

REVIEW_FILE = Path(
    "manual_review_queue.json"
)




class ReviewResolution(BaseModel):

    decision: Literal[
        "APPROVED",
        "REJECTED"
    ]

    reviewer: str = Field(
        ...,
        min_length=1
    )

    reviewer_comment: str = Field(default="", max_length=1000)

@app.get("/")
def root():
    return {
        "application": "Banking RAG API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/reviews/pending")
def get_pending_reviews():

    if not REVIEW_FILE.exists():
        return {
            "total": 0,
            "reviews": []
        }

    try:
        with open(REVIEW_FILE, "r", encoding="utf-8") as file:
            reviews = json.load(file)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Review queue JSON is invalid."
        )

    if not isinstance(reviews, list):
        raise HTTPException(
            status_code=500,
            detail="Review queue format is invalid."
        )

    pending_reviews = [
        review
        for review in reviews
        if review.get("status") == "PENDING"
    ]

    return {
        "total": len(pending_reviews),
        "reviews": pending_reviews
    }


@app.get("/api/reviews/dashboard")
def get_review_dashboard():
    logger.info("Dashboard request received")

    if not REVIEW_FILE.exists():
        return {
            "total": 0,
            "pending": 0,
            "approved": 0,
            "rejected": 0,
            "review_reasons": {},
            "pending_reviews": []
        }

    try:
        with open(REVIEW_FILE, "r", encoding="utf-8") as file:
            reviews = json.load(file)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Review queue JSON is invalid."
        )

    if not isinstance(reviews, list):
        raise HTTPException(
            status_code=500,
            detail="Review queue format is invalid."
        )

    pending = [
        review 
        for review in reviews
        if review.get("status") == "PENDING"
    ]

    approved = [
        review for review in reviews
        if review.get("status") == "APPROVED"
    ]

    rejected = [
        review for review in reviews
        if review.get("status") == "REJECTED"
    ]

    approved_reviews = [
        review
        for review in reviews
        if review.get("status") == "APPROVED"
    ]

    rejected_reviews = [
        review
        for review in reviews
        if review.get("status") == "REJECTED"
    ]

    reasons = Counter(
        review.get("reason", "UNKNOWN")
        for review in reviews
    )

    logger.info(
        "Dashboard loaded | total=%s pending=%s approved=%s rejected=%s",
        len(reviews),
        len(pending),
        len(approved),
        len(rejected)
    )

    return {
        "total": len(reviews),
        "pending": len(pending),
        "approved": len(approved),
        "rejected": len(rejected),
        "review_reasons": dict(reasons),
        "pending_reviews": pending,
        "approved_reviews": approved_reviews,
        "rejected_reviews": rejected_reviews
    }


@app.get("/api/reviews/{review_id}")
def get_review(review_id: str):

    if not REVIEW_FILE.exists():

        raise HTTPException(
            status_code=404,
            detail="Review queue not found."
        )

    try:

        with open(
            REVIEW_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            reviews = json.load(file)

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="Review queue JSON is invalid."
        )

    for review in reviews:

        if review.get("review_id") == review_id:

            return review

    raise HTTPException(
        status_code=404,
        detail="Review ID not found."
    )

@app.post("/api/reviews/{review_id}/resolve")
def resolve_review_api(
    review_id: str,
    resolution: ReviewResolution
):
    reviews = load_reviews()

    review = next(
        (r for r in reviews if r.get("review_id") == review_id),
        None
    )

    if review is None:
        logger.warning(
            "Review not found | review_id=%s",
            review_id
        )
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    if review.get("status") != "PENDING":
        logger.warning(
            "Attempt to resolve non-pending review | review_id=%s status=%s",
            review_id,
            review.get("status")
        )
        raise HTTPException(
            status_code=400,
            detail="Review has already been resolved"
        )

    logger.info(
        "Review resolution started | review_id=%s decision=%s reviewer=%s",
        review_id,
        resolution.decision,
        resolution.reviewer
    )

    review["status"] = resolution.decision
    review["reviewer"] = resolution.reviewer
    review["reviewer_comment"] = resolution.reviewer_comment
    review["resolved_at"] = datetime.utcnow().isoformat()

    review["resolution"] = {
        "decision": resolution.decision,
        "reviewer": resolution.reviewer,
        "comment": resolution.reviewer_comment,
        "resolved_at": review["resolved_at"]
    }

    save_reviews(reviews)

    logger.info(
        "Review resolved | review_id=%s status=%s",
        review_id,
        resolution.decision
    )

    return {
        "success": True,
        "review_id": review_id,
        "status": review["status"]
    }


