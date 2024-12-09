import os
import OTP_Email
from pwinput import pwinput

def check():
    fail = "failed"
    # input gmail
    gmail = input("Enter you Gmail: ").lower()
    # list of gmail in database
    gmails = split_line("database/gmail.txt")
    if (gmail in gmails):
        verify = gmail[-10:]
        if (verify == "@gmail.com"):
            username = input("Enter your Usernmae: ")
            # list of username in database
            usernames = split_line("database/username.txt")
            check = 0
            for i in range (0, len(usernames)):
                if ((username == usernames[i]) and (gmail == gmails[i])):
                    index = i
                    check = 1
            if check != 1:
                print(f"\"{gmail}\" did not register with username \"{username}\" ")
                return fail
            otp = OTP_Email.send_otp(gmail)
            print("Operation is in process. Please wait...")
            verify_otp = input("Enter verification code: ")
            for attempt in range(0,4):
                if (verify_otp == otp):
                    while True:
                        new_password = pwinput("New password: ")
                        strength = check_password_strength(new_password)
                        if (strength == "strong"):
                            while True:
                                confirm_new_password = pwinput("Re-Enter new password: ")
                                if (confirm_new_password == new_password):
                                    passwords = split_line("database/password.txt")
                                    passwords[index] = new_password
                                    return passwords
                                else:
                                    print("Password miss matched.")
                        else:
                            print("Password need to contain lower case, upper case, a number and a special character.")
                elif (attempt == 0):
                    print("Verification code does not matched! You have 2 more tries left.")
                    verify_otp = input("Enter your verification code: ")
                elif (attempt == 1):
                    print("Verification code does not matched! You have 1 more try left.")
                    verify_otp = input("Enter your verification code: ")
                elif (attempt == 2):
                    print("Verification code does not matched! This is your last try")
                    verify_otp = input("Enter your verification code: ")
                else:
                    os.system('cls')
                    print("We suspect that you are not the owner of the gamil.\nWe decide to end your process here.\nThank you for using our service.\nExiting register section...")
                    return fail
        else:
            print(f"{gmail} is not valid.\nGmail should has \"@gmail.com\" at the end")
            return fail
    else:
        print(f"{gmail} is not in the database.")
        return fail

def check_password_strength(password):
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

# split each line of the database 
def split_line(file_name):
    line = []
    # break each line of the database(username, gmail, password) and store it temporary into a list called "line"
    with open(file_name) as file:
        for each_line in file.readlines():
            line.append(each_line.strip())
    # return the list of each line of the database
    return line

def reset_password():
    new_passwords = check()
    if (new_passwords == "failed"):
        print("Password recovery is not success.\nExiting password recovery...")
        return
    with open("database/password.txt", 'w') as file:
        for new_password in new_passwords:
            file.write(new_password+"\n")

reset_password()