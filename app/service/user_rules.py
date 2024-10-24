from typing import Dict
from app.model.models import User

class UserRules:
    """Business rules related to users."""

    @staticmethod
    def validate_user_age(user: User) -> bool:
        """Validate if the user's age meets the required service rule."""
        if user.age < 18:
            return False
        return True

    @staticmethod
    def generate_user_profile(user: User) -> Dict[str, str]:
        """Generate a user profile summary."""
        return {
            "name": user.name,
            "profile_summary": f"{user.name}, aged {user.age}, lives in {user.city}."
        }
