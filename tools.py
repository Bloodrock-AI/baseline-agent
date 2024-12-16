import uuid
from datetime import datetime

from llm_tool import tool

from typing import Dict, List

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

@tool()
def add_user(user_data: Dict[str, str]) -> str:
    """
    Adds a new user to the database and returns the user ID.

    :param user_data: dictionary containing user data. dictionary format {"name" -> "string", "age" -> "integer", "email" -> "string", "phone" -> "string", "status" -> "string"}
    :return: user ID
    """
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

@tool()
def get_user(user_id: str) -> str:
    """
    Fetches a user's details by user ID.

    :param user_id: user ID
    :return: user details
    """
    return database.get(user_id)

@tool()
def update_user(user_id: str, updates: Dict[str, str]) -> bool:
    """
    Updates a user's details with the given data.

    :param user_id: user ID
    :param updates: dictionary containing user data to update. dictionary format (only add what you need to update) {"name" -> "string", "age" -> "integer", "email" -> "string", "phone" -> "string", "status" -> "string"}
    :return: True if the user was found and updated, False otherwise
    """
    if user_id not in database:
        return False
    user = database[user_id]
    timestamp = generate_timestamp()
    for key, value in updates.items():
        if key in user:
            user[key] = value
    user["updated_at"] = timestamp
    return True

@tool()
def delete_user(user_id: str) -> bool:
    """
    Deletes a user from the database by user ID.

    :param user_id: user ID
    :return: True if the user was found and deleted, False otherwise
    """
    if user_id in database:
        del database[user_id]
        return True
    return False

@tool()
def list_users(filter_by: Dict[str, str] = None) -> List[Dict[str, str]]:
    """
    Returns a list of users, optionally filtered by specific criteria.

    :param filter_by: dictionary containing filter criteria. dictionary format {"name" -> "string", "age" -> "integer", "email" -> "string", "phone" -> "string", "status" -> "string"}
    :return: list of users
    """
    if not filter_by:
        return list(database.values())
    filtered_users = []
    for user in database.values():
        match = all(user.get(key) == value for key, value in filter_by.items())
        if match:
            filtered_users.append(user)
    return filtered_users

@tool()
def verify_user_field(user_id: str, field: str, expected_value: str) -> bool:
    """
    Verifies if a specific field in a user record matches the expected value.

    :param user_id: user ID
    :param field: field to check
    :param expected_value: expected value
    :return: True if the field matches the expected value, False otherwise
    """
    user = get_user(user_id)
    if not user:
        return False
    return user.get(field) == expected_value

@tool()
def verify_user_absent(user_id: str) -> bool:
    """
    Verifies that a user record does not exist in the database.

    :param user_id: user ID
    :return: True if the user does not exist, False otherwise
    """
    return get_user(user_id) is None

tool_definitions = [
    add_user.definition,
    get_user.definition,
    update_user.definition,
    delete_user.definition,
    list_users.definition,
    verify_user_field.definition,
    verify_user_absent.definition
]

prompts = [
    {
        "prompt": "Create a new user named 'Alice' with an age of 25. Retrieve the details of this user and confirm the age field is correct.",
    },
    {
        "prompt": "Update the email and phone number of the user with name 'Alice' to 'alice@example.com' and '555-1234', respectively. Retrieve the updated user details to ensure the changes were applied.",
        "functions": [
            'add_user({"name": "Alice", "age": 25})',
        ],
    },
    {
        "prompt": "List all users who do not have an email address. Update their profile to set the email as 'default@example.com'. Retrieve one of the updated users to confirm the change.",
        "functions": [
            'add_user({"name": "John", "age": 30, "email": None})',
            'add_user({"name": "Jane", "age": 25, "email": None})',
        ],
    },
    {
        "prompt": "Add a new user named 'Charlie' aged 40 with his status set to 'active'. Then, set his status to 'inactive'. FInally, retrieve the user details to confirm the update."
    },
    {
        "prompt": "Create a new user named 'Eve' with an age of 22. Retrieve the user details, update their email to 'eve@example.com', and finally delete the user. Confirm the deletion by trying to fetch the record.",
    }
]
# Prompt 1: "Create a new user named 'Alice' with an age of 25. Retrieve the details of this user and confirm the age field is correct."
# user_id = add_user({"name": "Alice", "age": 25, "email": None, "phone": None})
# user = get_user(user_id)
# is_age_correct = verify_user_field(user_id, "age", 25)


# Prompt 2: "Update the email and phone number of the user with ID 'user_123' to 'alice@example.com' and '555-1234', respectively. Retrieve the updated user details to ensure the changes were applied."
# user_id = add_user({"name": "Alice", "age": 25})

# update_successful = update_user(user_id, {"email": "alice@example.com", "phone": "555-1234"})
# email_correct = verify_user_field(user_id, "email", "alice@example.com")
# phone_correct = verify_user_field(user_id, "phone", "555-1234")



# Prompt 3: "List all users who do not have an email address. Update their profile to set the email as 'default@example.com'. Retrieve one of the updated users to confirm the change."
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
