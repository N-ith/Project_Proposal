import gspread
from oauth2client.service_account import ServiceAccountCredentials

class FileHandler:
    def __init__(self):
        """
        Initializes the connection to the centralized Google Sheet.
        This version does not require user input for JSON key or sheet name.
        """
        # Define the scope for Google Sheets and Drive API
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Path to your service account JSON key file and sheet name
        self.json_key_path = 'database key.json'  # Replace with actual file path
        self.sheet_name = 'Centralized_Authentication'  # Replace with the name of your sheet

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

    def get_password(self, username):
        """
        Retrieves the password for a given username.

        :param username: The username to find
        :return: The password if found, else None
        """
        try:
            user_row = self.worksheet.find(username).row  # Find the row containing the username
            password = self.worksheet.cell(user_row, 2).value  # Get the password from the second column
            return password
        except gspread.exceptions.CellNotFound:
            print(f"Username '{username}' not found.")
            return None

    def update_password(self, username, new_password):
        """
        Updates the password for a given username.

        :param username: The username to update
        :param new_password: The new password to set
        """
        try:
            user_row = self.worksheet.find(username).row  # Find the row containing the username
            self.worksheet.update_cell(user_row, 2, new_password)  # Update the password in the second column
            print(f"Password for '{username}' updated successfully.")
        except gspread.exceptions.CellNotFound:
            print(f"Username '{username}' not found.")


