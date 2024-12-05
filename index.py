import os
import login
import register
import pass_recovery


class UserAuthentication:
    def __init__(self) -> None:
        pass
    def menu(self):
        print("****************")
        print("*****      *****")
        print("***   MENU   ***")
        print("*****      *****")
        print("****************")
        print("1. Register\n2. Login\n3. Password Recovery\n0. Exit")
    def register(self):
        pass
    def login(self):
        pass
    def pass_recovery(self):
        pass

def main():
    user_auth = UserAuthentication()
    while True:
        user_auth.menu()
        mode = int(input("Choose a mode by it's number(0-3): "))
        os.system('cls')
        if mode in range(0,4):
            if mode == 0:
                print("Exiting the program...")
                break
            if mode == 1:
                user_auth.register()
            if mode == 2:
                user_auth.login()
            if mode == 3:
                user_auth.register()
        else:
            print(f"{mode} is not on the list.")

main()