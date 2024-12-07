import gspread
from oauth2client.service_account import ServiceAccountCredentials

class FileHandler:
    def __init__(self):
        """
        Initializes the connection to the centralized Google Sheet.
        """
        # Define the scope for Google Sheets and Drive API
        self.scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

        # Hardcoded JSON credentials (use your actual credentials)
        self.credentials_info = {
            "type": "service_account",
            "project_id": "authentication-system-database",
            "private_key_id": "e7d3cbf7b1cb19e89450156ba091c7b0ef5fa84f",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVjJO1Je73EKKR\n5gfa3Myfx3yIt5t1zaQBb5saYekEnrIPZ1W0BppZIY2/Ygz6FUKBjt+zyXtq6gr4\n7CAzlVxBvxy/8MzXNMbFYrgB2kazUwn8o04LeiciOJDX1kPPiv9DCuPYi4wxfpk0\nHGRee7h9ARoadk4znT8j8He/e5TOTwY3/wH3a8mSUzzduEwHekGW9q4Bc3RlcBsD\nkM/EIb99pkmVneIs3sN5YJJrRYsSXvjWmDAMcSQqlKvUFuq3vWwq8whBOp2jT+fJ\nDgrHZRzuBPbZYT5ZmPZEHK2/9aoUBwDB3cSaXc9z4gF5AWbiN9idIHVVR9PmNtuf\no58QdvOPAgMBAAECggEAOGfJyhLLdFHeBviCAaLJn7iC4d/RfcPD+qceilDrSg+a\ny6vJPORzl3Bf7vm4oMPFzc/NscDZywsnu8ku1kEw3aLbtq0lhgCIMjHZlY+wlgQs\ngqEl560rsgPL6l7LiYHW28AAH734WUhtshB/yF8Yg1grq2qtTD/QIi+NibPcQcOt\nBdHSg/JLBEffsm8F2LNg9mbommizh00l2Z+l59GhgRV+5EScRNtt7yG09VNdGILu\nUIm/VOqIBMOJpp/UU4exXRCEQAEilMeOvEPSo15PIrihplac/smBnwAWqlC0Zri/\n9ZSZkvveagQXzT2eqklxT8sf4ZH3CrgzQ8KS3ymeNQKBgQD5LFA0MaVakpfjDbLk\npmJCQmFNE7i7YZYasrX67pdZofc3aD41oaPnU663h9QKwFLD1ZXsHeVo98UlR8qB\nSVQN1TMHtWAnblmFc3gGdJmhHvKT4uu7tSIhWHGo5aZy26yXg6SXwbC6SCYtdlhh\nGThkeWI9Q1Dv4m2i8D6tYOnDQwKBgQDbZmYqAXrg7DZdGTjT0lPcE82vwzb4k68Y\n0RSSz3gk0lR7rQ83KLCWrSZd145Nrau2mQ7eBTgM30aZIK5q2H+GCA1IhcyRBSQe\nNJHAdIdYNkVZsrNd15qA4jUivBr8dVFBFFVcNLyXFX+vZ0TeEGVrnio5zhJb6z96\nxscUfMv7xQKBgQCUmh33EsinvJeC3Q+cl7IwDACVhDZ+4hMwNvabAaIX3aVfUPcQ\n6yah9mFTqVkHVG3Hx2CTIb1IncPgmPEnq8DKQyUc6sm+mmwfT578Upuw4JERK5sl\nJkCFnIakkNl01JgZAHSv4N7yKcdDA7pvpifgnBe/q57ggaybKSZoJk0jmwKBgBgz\nYl+NzD0VMSXxy0fqMl/bO1wA34Zp2+2T2n4bLnh5TuJZg40lCt2D+fBt/39oAcHh\nfjdVQgqBcmsfpL2aZe6l4rk2MQtqEsLWL6GX+Pns+pdbU9etGZjP2uaa8ysX0b+o\n+4VxN8A+mdgCPyFzk4xcZPH9Xh8PgvALDxieb221AoGAYiD4KafDwy+1f5rwQRH5\nT03f2sfUbXfWGlIHxx/0KnwGLX1oxWn4tU6SKRTXjuvG3QObpOL/wZHX6uTUM7k/\nrdZaxqgwSeJuEX2/YXXJk/08IE+7xW1i9RVeoyuct0cOH0ZB02L9pBp+RAIWs58n\nZU5Q+gCbeegeX2ffiZDJIAY=\n-----END PRIVATE KEY-----\n",
            "client_email": "python-database@authentication-system-database.iam.gserviceaccount.com",
            "client_id": "109527905347608125590",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/python-database%40authentication-system-database.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            }

        # Define the name of your sheet
        self.sheet_name = 'Centralized_Authentication_System'  # Replace with your actual sheet name

        # Authenticate using the hardcoded credentials
        self.credentials = ServiceAccountCredentials.from_json_keyfile_dict(self.credentials_info, self.scope)
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
