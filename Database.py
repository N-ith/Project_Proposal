import gspread
from oauth2client.service_account import ServiceAccountCredentials

class FileHandler:
    def __init__(self):
        """
        Initializes the connection to the centralized Google Sheet.
        """
        # Define the scope for Google Sheets and Drive API
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        self.credentials_file = "database key.json"

        # Define the name of your sheet
        self.sheet_name = 'Centralized_Authentication_System'  # Replace with your actual sheet name
        # Authenticate using the hardcoded credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials_file, self.scope)
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
        self.worksheet.append_row([username, password])  # Add a new row with the username and password
        print(f"User '{username}' added successfully.")

    def verify_user(self, username, password):
        """
        Verifies if the provided username and password match.

        :param username: The username to verify
        :param password: The password to verify
        :return: True if the username and password match, False otherwise
        """
        try:
            # Find the row with the given username
            user_row = self.worksheet.find(username).row
            stored_password = self.worksheet.cell(user_row, 2).value  # Get the password from the second column

            # Check if the provided password matches the stored password
            if stored_password == password:
                print(f"User '{username}' verified successfully.")
                return True
            else:
                print(f"Incorrect password for '{username}'.")
                return False
        except ValueError:
            # If the username is not found
            print(f"Username '{username}' not found.")
            return False

    def reset_password(self, username, new_password):
        """
        Resets the password for a given username.

        :param username: The username to reset the password for
        :param new_password: The new password to set
        :return: True if the password is successfully reset, False otherwise
        """
        try:
            # Find the row with the given username
            user_row = self.worksheet.find(username).row

            # Update the password in the second column
            self.worksheet.update_cell(user_row, 2, new_password)  # Update password in the 2nd column
            print(f"Password for '{username}' reset successfully.")
            return True
        except ValueError:
            # If the username is not found
            print(f"Username '{username}' not found.")
            return False