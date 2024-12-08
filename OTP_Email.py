import smtplib
import random

# Check line 10 and 12
def send_otp(reciever_gmail):
    # low, high can be modified depend on the range of your OTP
    low = 0
    high = 9

    # enter your gmail (host gmail/ sender gmail)
    gmail = "sophanithan2@gmail.com"
    # enter your google app password
    google_app_password = "google app password"
    # ctrl+click on this link to get google account password: https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&followup=https%3A%2F%2Fmyaccount.google.com%2Fapppasswords&ifkv=AcMMx-egbmBzat9KbYWtPtQad408VvqcOQifFoQAQgLmDOZJJCqHIv0GUoFtTQ6mppxnvNt67m8FiA&osid=1&passive=1209600&rart=ANgoxcfjlkg4rAxvilJQI3Z5FGJCjwAwAe55A3VIxMVdeA2_1vY0D-zqFBiZzdUY1StBoPG5Gc0P0hedpLl59xUDplFhWd78YHTH53c7wpOb48nx63xHxWc&service=accountsettings&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1140668789%3A1733653089952120&ddm=1

    # to store the OTP code
    verification_code= []
    # random OTP
    for i in range(0,6):
        random_number = random.randint(low,high)
        verification_code.append(random_number)
    result = "".join(map(str, verification_code))

    email = gmail
    reciever_email = reciever_gmail

    #subject, message and content can be modify
    subject = "Security Alert!!!"
    message = f"Verification code: {result}"
    content = f"Subject: {subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(email, google_app_password) 
    
    server.sendmail(email, reciever_email, content)
    print(f"Verification code sent to {reciever_gmail}")

    return result
