import uuid

id1 = "REV-" + str(uuid.uuid4())
id2 = "REV-" + str(uuid.uuid4())

print("Review ID 1:", id1)
print("Review ID 2:", id2)
print("Are they same?:", id1 == id2)