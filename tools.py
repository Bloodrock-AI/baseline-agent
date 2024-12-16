import uuid
from datetime import datetime

# {
#   "id": "string",            // Unique identifier for the user (e.g., "user_123").
#   "name": "string",          // Full name of the user.
#   "age": "integer",          // Age of the user in years.
#   "email": "string",         // Email address (nullable if not set).
#   "phone": "string",         // Phone number (nullable if not set).
#   "status": "string",        // Status of the user (e.g., "active", "inactive", "minor").
#   "created_at": "string",    // Timestamp for when the user was created (ISO 8601 format).
#   "updated_at": "string"     // Timestamp for the last update to the user's record (ISO 8601 format).
# }


# In-memory database for user records
database = {}

def generate_timestamp():
    """Generates the current timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + "Z"

def add_user(user_data):
    """Adds a new user to the database and returns the user ID."""
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    timestamp = generate_timestamp()
    new_user = {
        "id": user_id,
        "name": user_data.get("name"),
        "age": user_data.get("age"),
        "email": user_data.get("email"),
        "phone": user_data.get("phone"),
        "status": user_data.get("status", "active"),
        "created_at": timestamp,
        "updated_at": timestamp
    }
    database[user_id] = new_user
    return user_id

def get_user(user_id):
    """Fetches a user's details by user ID."""
    return database.get(user_id)

def update_user(user_id, updates):
    """Updates a user's details with the given data."""
    if user_id not in database:
        return False
    user = database[user_id]
    timestamp = generate_timestamp()
    for key, value in updates.items():
        if key in user:
            user[key] = value
    user["updated_at"] = timestamp
    return True

def delete_user(user_id):
    """Deletes a user from the database by user ID."""
    if user_id in database:
        del database[user_id]
        return True
    return False

def list_users(filter_by=None):
    """Returns a list of users, optionally filtered by specific criteria."""
    if not filter_by:
        return list(database.values())
    filtered_users = []
    for user in database.values():
        match = all(user.get(key) == value for key, value in filter_by.items())
        if match:
            filtered_users.append(user)
    return filtered_users

def verify_user_field(user_id, field, expected_value):
    """Verifies if a specific field in a user record matches the expected value."""
    user = get_user(user_id)
    if not user:
        return False
    return user.get(field) == expected_value

def verify_user_absent(user_id):
    """Verifies that a user record does not exist in the database."""
    return get_user(user_id) is None



# Prompt 1: "Create a new user named 'Alice' with an age of 25. Retrieve the details of this user and confirm the age field is correct."
# user_id = add_user({"name": "Alice", "age": 25, "email": None, "phone": None})
# user = get_user(user_id)
# is_age_correct = verify_user_field(user_id, "age", 25)


# Prompt 2: "Update the email and phone number of the user with ID 'user_123' to 'alice@example.com' and '555-1234', respectively. Retrieve the updated user details to ensure the changes were applied."
# user_id = add_user({"name": "Alice", "age": 25})
# update_successful = update_user(user_id, {"email": "alice@example.com", "phone": "555-1234"})
# email_correct = verify_user_field(user_id, "email", "alice@example.com")
# phone_correct = verify_user_field(user_id, "phone", "555-1234")



# Prompt 3: "List all users who do not have an email address. Update their profile to set the email as 'default@example.com'. Retrieve one of the updated users to confirm the change."add_user({"name": "John", "age": 30, "email": None})
# add_user({"name": "John", "age": 30, "email": None})
# add_user({"name": "Jane", "age": 25, "email": None})

# users_without_email = list_users({"email": None})
# for user in users_without_email:
#     update_user(user["id"], {"email": "default@example.com"})
# email_correct = verify_user_field(users_without_email[0]["id"], "email", "default@example.com")


# Prompt 4: "Add a new user named 'Charlie' aged 40 with his status set to "active". Then, set his status to 'inactive'. FInally, retrieve the user details to confirm the update."
# user_id = add_user({"name": "Charlie", "age": 40})
# update_user(user_id, {"status": "inactive"})
# status_correct = verify_user_field(user_id, "status", "inactive")


# Prompt 5: "Create a new user named 'Eve' with an age of 22. Retrieve the user details, update their email to 'eve@example.com', and finally delete the user. Confirm the deletion by trying to fetch the record."
# user_id = add_user({"name": "Eve", "age": 22})
# user = get_user(user_id)
# update_user(user_id, {"email": "eve@example.com"})
# delete_successful = delete_user(user_id)
# user_absent = verify_user_absent(user_id)
