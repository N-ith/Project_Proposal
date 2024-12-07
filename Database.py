import gspread
from oauth2client.service_account import ServiceAccountCredentials

class FileHandler:
    def __init__(self):
        """
        Initializes the connection to the centralized Google Sheet.
        This version only includes functions to add a user, verify a user, and reset a user's password.
        """
        # Define the scope for Google Sheets and Drive API
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Path to your service account JSON key file and sheet name
        self.json_key_path = 'database key.json'  # Replace with actual file path
        self.sheet_name = 'Centralized_Authentication_System'  # Replace with the name of your sheet

        # Authenticate using service account credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_key_path, self.scope)
        self.client = gspread.authorize(self.credentials)

        try:
            # Try to open the specified Google Sheet
            self.spreadsheet = self.client.open(self.sheet_name)
            print(f"Spreadsheet '{self.sheet_name}' found.")
        except gspread.exceptions.SpreadsheetNotFound:
            # If the sheet does not exist, create a new one
            print(f"Spreadsheet '{self.sheet_name}' not found. Creating it.")
            self.spreadsheet = self.client.create(self.sheet_name)
            print(f"Spreadsheet '{self.sheet_name}' created.")
        
        # Access the first worksheet
        self.worksheet = self.spreadsheet.get_worksheet(0)  # Access the first sheet
        print(f"Accessing worksheet: {self.worksheet.title}")

    def add_user(self, username, password):
        """
        Adds a new user to the Google Sheet.

        :param username: The username to add
        :param password: The password to add
        """
        existing_users = self.worksheet.col_values(1)  # Get all usernames from the first column
        if username in existing_users:
            print(f"Username '{username}' already exists.")
            return False
        # Append the new user's username and password to the sheet
        self.worksheet.append_row([username, password])
        print(f"User '{username}' added successfully.")
        return True

    def verify_user(self, username, password=None):
        """
        Verifies if the provided username and password match.

        :param username: The username to verify
        :param password: The password to verify (optional for existence check)
        :return: True if the username and password match, False otherwise
        """
        try:
            # Find the row with the given username
            user_row = self.worksheet.find(username).row

            if password:  # If password is provided, check it
                stored_password = self.worksheet.cell(user_row, 2).value  # Get the stored password from the second column
                if stored_password == password:
                    return True  # Password matches
                else:
                    return False  # Password does not match
            else:
                return True  # If no password is provided, only check if the username exists

        except gspread.exceptions.CellNotFound:
            # If the username is not found
            return False

    def reset_password(self, username, new_password):
        """
        Resets the password for a given username.

        :param username: The username to reset
        :param new_password: The new password to set
        :return: True if the password is successfully reset, False otherwise
        """
        try:
            # Try to find the row containing the username
            user_row = self.worksheet.find(username).row
            # Update the password in the second column
            self.worksheet.update_cell(user_row, 2, new_password)  
            print(f"Password for '{username}' reset successfully.")
            return True
        except gspread.exceptions.CellNotFound:
            # If the username is not found, handle the exception
            print(f"Username '{username}' not found.")
            return False

            
# Test the code
if __name__ == "__main__":
    file_handler = FileHandler()
    
    # Add a user
    file_handler.add_user('test_user', 'test_password')

    # Verify the user
    file_handler.verify_user('test_user', 'test_password')

    # Reset password for the user
    file_handler.reset_password('test_user', 'new_password')

    # Verify the user after password reset
    file_handler.verify_user('test_user', 'new_password')
