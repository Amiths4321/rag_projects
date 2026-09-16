from request_id import generate_request_id


request_id_1 = generate_request_id()
request_id_2 = generate_request_id()

print("Request ID 1:")
print(request_id_1)

print("\nRequest ID 2:")
print(request_id_2)

print("\nIDs are different:")
print(request_id_1 != request_id_2)