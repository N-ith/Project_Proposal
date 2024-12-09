import smtplib
import random

class OTPHandler:
    def __init__(self):
        self.verification_code = None

    def generate_otp(self):
        """Generate a 7-digit OTP."""
        self.verification_code = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        print(f"Generated OTP: {self.verification_code}")  # Debugging line
        return self.verification_code

    def send_verification_email(self, receiver_email):
        """Send the OTP to the user's email."""
        if self.verification_code is None:
            self.generate_otp()

        # No-reply email account configuration
        email = "buthdavid25@gmail.com"  # Replace with your no-reply email address

        # Read app password from a file
        password_file = "gmail password.txt"  # Name of the file containing the password
        try:
            with open(password_file, "r") as file:
                app_password = file.read().strip()  # Read and strip any extra whitespace
        except FileNotFoundError:
            print(f"Error: Password file '{password_file}' not found.")
            exit()
        except Exception as e:
            print(f"Error reading password file: {e}")
            exit()

        # Email content
        subject = "Security Alert!!!"
        message = f"Your verification code is: {self.verification_code}"
        content = f"Subject: {subject}\n\n{message}"

        # Set up the SMTP server
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
            server.starttls()  # Start TLS encryption
            server.login(email, app_password)
            server.sendmail(email, receiver_email, content)
            print("Verification email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            server.quit()

    def verify_otp(self, entered_otp):
        """Verify the entered OTP against the generated one."""
        if self.verification_code == entered_otp:
            return True
        return False
