from Database import FileHandler  # Ensure this imports your FileHandler class
import register  # Import your registration logic

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

            # Check if the email matches the stored email for the username
            stored_email = self.file_handler.get_user_email(username)
            if not stored_email or stored_email != email:
                print("This username and email combination is not registered.")
                # choice = input("Would you like to register an account? (yes/no): ").strip().lower()
                # if choice == "yes":
                #     register()  # Call the registration logic
                # else:
                #     print("Returning to the main menu.")
                #     break
            else:
                # Username and email exist, proceed to password check
                for _ in range(3):  # Allow 3 attempts for password
                    password = input("Password: ").strip()

                    # Validate the user's credentials
                    ip_address = self.file_handler.get_ip_address()
                    result = self.file_handler.verify_user(username, password, ip_address)

                    if result is True:
                        print("Login successful!")
                        return  # Exit the login function
                    else:
                        print(result)  # Display error message (e.g., incorrect password)
                
                # If all attempts fail
                print("Too many failed attempts. Returning to the menu.")
                break



# Example Usage
if __name__ == "__main__":
    login_system = Login()
    login_system.login()
