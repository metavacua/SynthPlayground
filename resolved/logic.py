# Component B: Stance: Safety


def get_user_name(user_data):
    """
    This is the robust, "Safety"-focused implementation.
    It validates its input to prevent runtime errors.
    """
    if isinstance(user_data, dict) and "name" in user_data and user_data["name"]:
        return user_data["name"]
    else:
        # Return a safe default value if the data is invalid.
        return "Anonymous"
