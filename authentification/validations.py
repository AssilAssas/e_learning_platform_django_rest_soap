import re
from email_validator import validate_email, EmailNotValidError


class ValidationData:
    @staticmethod
    def validate_email(email):
        """
        Validate email format using the email_validator library.
         """
        try:
            # Validate and get info
            v = validate_email(email)

            # Get a normalized version of the email address
            email = v["email"]
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            raise ValueError(str(e))

    @staticmethod
    def validate_password(password):
        """
        Validate password strength.
        """
        # Customize this function based on your password requirements
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # You can add more conditions for password strength as needed

        # Example: Check for at least one digit
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")

        # Example: Check for at least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")

        # Example: Check for at least one special character
        special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?"
        if not any(char in special_characters for char in password):
            raise ValueError("Password must contain at least one special character")

    
