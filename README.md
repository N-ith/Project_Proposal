--->On Mac might pop up this message: 'cls' is not recognized as an internal or external command, operable program or batch file.
    #Solve it by changing os.system('cls') on line 29 to os.system('clear')
    
---------------------------------------------------------------------------------------------------------------
library to install: 
  - pip install smtplib
  - pip install pyqt5
  - pip install gspread
  - pip install oauth2client

Register:
+ Username: check for uniqueness
+ Email: check for valid like having @ and . in the string. OPTIONAL: send an email with OTP to that email then let the user enter the OTP and check if these 2 OTP are matched then let the user enter password, if not let them enter again for 2 more times. If it still doesn't match shows the menu and let them choose the mode again.
+ Password: check for strength

#recommendation: username, email, password should be stored in a dicitonary that has a structure of user_account = {username:{email:password}} then store it into the database (user_management.txt)
--------------------------------------------------------------------------------------------------------------------

Login:
+ Username/Email:
    - check if user enter username or email
    - check if that username or email is in the data base or not

    #Condition 1(username/email is not in the database):
      - tell them their username or email has not been registered yet then ask them to register an account or show the menu

    #Condition 2(username/email is in the database):
      - go to check password
      
+ Password: check if that password matches to the password that stores with in that username or email

--------------------------------------------------------------------------------------------------------------------

Recovery password:
+ Username/Email:
  - check if user enter username or email
  - check if that username or email is in the data base or not
  #Condition 1 (username/email is not in the data base):
    - if not tell them their username or email has not been registered yet then ask them to register an account or show the menu
  #Condition 2 (username/email in the data base):
    - Send OPT email to the email with timeout for 2mns
    - check if the OPTs are matched
    - go to create new password
+ Create new password:
  - let the user enter a new password and check for password strength
    
 
