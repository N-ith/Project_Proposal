import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

class FileHandler:
    def __init__(self):
        """Initialize connection to the fixed user database."""
        self.json_key_path = "database key.json"
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_key_path, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet_name = 'Centralized_Authentication_System'

        # Connect to the specified spreadsheet and worksheet
        self.spreadsheet = self.client.open(self.sheet_name)
        self.worksheet = self.spreadsheet.get_worksheet(0)

    def is_username_unique(self, username):
        """Check if the username is unique."""
        return not self.worksheet.find(username.strip())
    
    def get_user_email(self, username):
        """Retrieve the email address associated with a given username."""
        try:
            user_cell = self.worksheet.find(username.strip())
            if user_cell:
                user_row = user_cell.row
                return self.worksheet.cell(user_row, 4).value.strip()  # Email is in the 4th column
            else:
                return None  # If username is not found, return None
        except Exception as e:
            print(f"Error fetching email for {username}: {e}")
            return None

    def add_user(self, username, password, ip_address, email):
        """Add a new user with the given details (username, password, IP address, email)."""
        if not self.is_username_unique(username):
            raise ValueError("Username already exists.")
        # Add user info to the spreadsheet, including email
        self.worksheet.append_row([username.strip(), password.strip(), ip_address, email])

    def verify_user(self, username, password, ip_address):
        """Validate user credentials (username, password, and IP address)."""
        try:
            user_cell = self.worksheet.find(username.strip())
            if not user_cell:
                return "Username not found."  # Username is invalid

            user_row = user_cell.row
            stored_password = self.worksheet.cell(user_row, 2).value.strip()
            stored_ip = self.worksheet.cell(user_row, 3).value.strip()

            if stored_password != password.strip():
                return "Incorrect username or password."  # Password is invalid

            if stored_ip != ip_address:
                return "IP address mismatch. Please log in from the registered location."  # IP mismatch

            return True  # Valid credentials
        except Exception as e:
            print(f"Error during verification: {e}")
            return False

    def reset_password(self, username, new_password):
        """Reset the user's password."""
        try:
            user_cell = self.worksheet.find(username.strip())
            self.worksheet.update_cell(user_cell.row, 2, new_password.strip())  # Update password
            return True
        except Exception as e:
            print(f"Error resetting password: {e}")
            return False

    def get_ip_address(self):
        """Retrieve the user's IP address."""
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=5)
            response.raise_for_status()
            return response.json().get("ip", "Unknown")
        except Exception as e:
            print(f"Error fetching IP address: {e}")
            return None
