from Database import FileHandler
class Login:
    def __init__(self):
        self.fileHandler = FileHandler()
    def login(self,username,email,password):
        while True:
         # Prompt user for username and email
         username = input("Username: ").strip()
         email = input("Email: ").strip()

        
         # Check if username/email exists in the database
         if username and email not in self.database:
            print("This username and email is not registered.")
            
            # Ask if they want to register or show the menu
            choice = input("Would you like to register an account? (yes/no): ").strip().lower()
            if choice == "yes":
                self.register()
            else:
                print("Returning to the main menu.")
                break
         else:
            # Username exists, proceed to check password
            for _ in range(3):  # Allow 3 attempts for password
                password = input("Password: ").strip()
                
                # Check if the entered password matches
                if password == self.database[username] and self.database[email]:
                    print("Login successful!")
                    return  # Exit the login function
                else:
                    print("Incorrect password. Try again.")
            
         # If all attempts fail
         print("Too many failed attempts. Returning to the menu.")
         break

login = Login()
login.login()        



