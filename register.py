from pwinput import pwinput
import OTP_Email

class Register:

    def header(self):
        print("*************************")
        print("*                       *")
        print("*       REGISTER        *")
        print("*                       *")
        print("*************************")

    def open_file_append(self, file_name, append):
        with open(file_name, 'a') as file:
            file.write(append)
    
    # split each line of the database 
    def split_line(self, file_name):
        line = []
        # break each line of the database(username, gmail, password) and store it temporary into a list called "line"
        with open(file_name) as file:
            for each_line in file.readlines():
                line.append(each_line.strip())
        # return the list of each line of the database
        return line
    
    def check_username(self):
        username = input("Enter your username: ")
        # path to file that store username
        file_name = "database/username.txt"
        # variable for each line of username
        usernames = self.split_line(file_name)
        # check if username is already exists and let user input another username untill they put the unique one
        while True:
            if (username in usernames):
                username = input(f"!!Alert: {username} has already registered.\nPlease choose another username: ")
            else:
                # return the username to append it into the file in function "register" when the process end
                return username
        
    def check_email(self):
        fail = "not success!"
        # user .lower() at the end to convert the string to lowercase 
        gmail = input("Enter your Gmail: ").lower()
        # it can also replace with: gmail = gmail.lower()
        print("Operation is running. Please wait...")
        file_name = "database/gmail.txt"
        gmails = self.split_line(file_name)
        verify = gmail[-10:]
        while True:
            # check if gmail has "@gmail.com" at the end of it
            if (verify != "@gmail.com"):
                gmail = input(f"Alert!!: {gmail} is not valid.\nGmail should has \"@gmail.com\" in it.\nEnter your Gmail: ").lower()
            
            else:
                # check if that gmail has not yet been registered over 5 times
                # 1 gmail can only use to register for 5 accounts maximum
                maximum = 0
                for i in range (0, len(gmails)):
                    if(gmail == gmails[i]):
                        maximum+=1
                if(maximum < 5):
                    otp = OTP_Email.send_otp(gmail)
                    verify_otp = input("Enter your verification code: ")
                    for attempt in range (0,4):
                        if (verify_otp == otp):
                            print("success")
                            return gmail
                        elif (attempt == 0):
                            print("This is your second try! You have 2 last tries left.")
                            verify_otp = input("Enter your verification code: ")
                        elif (attempt == 1):
                            print("This is your third try! You have 1 last try left.")
                            verify_otp = input("Enter your verification code: ")
                        elif (attempt == 2):
                            print("This is your last try")
                            verify_otp = input("Enter your verification code: ")
                        else:
                            print("We suspect that you are not the owner of the gamil.\n!We decide to end your process here.\nThank you for using our service.\nExiting register section...")
                            return fail

                else:
                    print(f"{gmail} has already reached the maximum.\nNote: 1 Gmail can only register for 5 accounts.")
                    return fail
                    
    def check_password(self):
        # while inputing the password it shows in "*" format
        while True:
            password = pwinput("Enter your password: ", '*')
            strength = self.check_password_strength(password)
            if strength == "strong":
                return password
            else:
                print("Your password need to contain lower case, upper case, a number and a special character, \nPlease enter a new password...")

    def check_password_strength(self, password):
        has_upper = False
        has_lower = False
        has_digit = False
        has_symbol = False

        for c in password:
            if c.isupper():
                has_upper = True
            if c.islower():
                has_lower = True
            if c.isdigit():
                has_digit = True
            if c in ("!@#$%^&*()"):
                has_symbol = True

        if len(password) < 8:
            pass
        elif len(password) > 7 and has_upper and has_lower and has_digit and has_symbol:
            return "strong"
        else:
            pass

    def register(self):
        self.header()
        username = self.check_username()
        gmail = self.check_email()
        if (gmail == "not success!"):
            print("Registering unsuccessful!")
            return
        password = self.check_password()
        self.open_file_append("database/username.txt", username)
        self.open_file_append("database/gmail.txt", gmail)
        self.open_file_append("database/password.txt", password)
        with open("database/user_account.txt", 'a') as file:
            file.write("Username: "+ username + ', ')
            file.write("Gmail: "+ gmail + ', ')
            file.write("Password: "+ password + '\n')


register_obj = Register()

register_obj.register()
