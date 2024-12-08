from Database import FileHandler  # Ensure this imports your FileHandler class

class Login:
    def __init__(self):
        # Initialize FileHandler for accessing the Google Sheet
        self.file_handler = FileHandler()

    def login(self):
        """
        Prompts the user to log in by verifying username, email, and password.
        """
        while True:
            # Prompt user for username and email
            username = input("Username: ").strip()
            email = input("Email: ").strip()

            # Fetch all user data from Google Sheet
            user_data = self.file_handler.worksheet.get_all_records()  # List of dictionaries

            # Check if the username and email match any record
            user_record = next((user for user in user_data if user['Username'] == username and user['Email'] == email), None)

            if not user_record:
                # If no matching record is found
                print("This username and email combination is not registered.")

                # Offer registration or return to menu
                choice = input("Would you like to register an account? (yes/no): ").strip().lower()
                if choice == "yes":
                    self.register()
                else:
                    print("Returning to the main menu.")
                    break
            else:
                # Username and email exist, proceed to password check
                for _ in range(3):  # Allow 3 attempts for password
                    password = input("Password: ").strip()

                    # Compare entered password with the stored password
                    if password == user_record['Password']:
                        print("Login successful!")
                        return  # Exit the login function
                    else:
                        print("Incorrect password. Try again.")
                
                # If all attempts fail
                print("Too many failed attempts. Returning to the menu.")
                break

    def register(self):
        """
        Registers a new user by adding their details to the Google Sheet.
        """
        username = input("Enter a username: ").strip()
        email = input("Enter an email: ").strip()
        password = input("Enter a password: ").strip()

        # Add the new user to the Google Sheet
        self.file_handler.add_user(username, email, password)
        print("Registration successful! You can now log in.")

# Example Usage
if __name__ == "__main__":
    login_system = Login()
    login_system.login()
