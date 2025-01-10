from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def is_debug_mode():
    """
    Utility function to check if the application is in DEBUG mode.

    Returns:
        bool: True if DEBUG is set to True in the .env file, False otherwise.
    """
    return os.getenv('DEBUG', 'False').lower() in ['true', '1', 'yes']
