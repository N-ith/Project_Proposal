import smtplib
import random

low =0
high = 9

verification_code= []
for i in range(0,7):
    random_number = random.randint(low,high)
    verification_code.append(random_number)
print(f"Befor: {verification_code}")
result = "".join(map(str, verification_code))
print(result)

email = "sophanithan2@gmail.com"
reciever_email = input("Reciever email: ")
link = "https://accounts.google.com/"

subject = "Security Alert!!!"
message = f"Verification code {result}"
content = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email, "google account password") 
#to get google account password: type google account password in chrome and select the second link(require the email account to have 2 step verification)
server.sendmail(email, reciever_email, content)
print("Sent successfully!")
