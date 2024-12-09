import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from Database import FileHandler  # Assuming FileHandler is in a separate file
from OTP_Email import OTPHandler  # Import the OTPHandler class

class AuthApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the FileHandler class
        self.file_handler = FileHandler()
        self.otp_handler = OTPHandler()  # Create an instance of OTPHandler

        # Set up the UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Authentication System')
        self.setGeometry(100, 100, 400, 500)  # Adjusted window size
        self.setStyleSheet("background-color: #e9f1f7;")  # Light blue background

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("Login to Your Account", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #3b5998; margin-top: 30px;")
        self.main_layout.addWidget(self.title_label)

        # Placeholder for dynamic content
        self.dynamic_content_layout = QVBoxLayout()
        self.main_layout.addLayout(self.dynamic_content_layout)

        # Set the layout
        self.setLayout(self.main_layout)

        # Start with login view
        self.username_input = None
        self.password_input = None
        self.otp_input = None
        self.otp_sent = False  # Track if OTP has been sent
        self.show_login_view()

    def show_login_view(self):
        """Switch to login view."""
        # Clear existing layout
        self.clear_dynamic_content()

        self.title_label.setText("Login to Your Account")

        # Add fields for login view
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.dynamic_content_layout.addWidget(self.username_input)
        self.dynamic_content_layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton('Log In', self)
        self.login_button.clicked.connect(self.verify_user)
        self.dynamic_content_layout.addWidget(self.login_button)

        # Forgot Password link
        self.forgot_password_label = QLabel('<a href="#">Forgotten password?</a>', self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setStyleSheet(""" 
            font-size: 14px;
            color: #3b5998;
            text-decoration: underline;
            margin-top: 10px;
        """)
        self.forgot_password_label.linkActivated.connect(self.show_reset_password_view)
        self.dynamic_content_layout.addWidget(self.forgot_password_label)

        # Register button
        self.register_button = QPushButton('Sign Up', self)
        self.register_button.clicked.connect(self.show_signup_view)
        self.dynamic_content_layout.addWidget(self.register_button)

    def verify_user(self):
        """Verify the user credentials."""
        username = self.username_input.text()
        password = self.password_input.text()
        ip_address = self.file_handler.get_ip_address()

        if username and password:
            result = self.file_handler.verify_user(username, password, ip_address)

            if result == True:
                self.show_message('Success', f'User verified successfully.')
            elif isinstance(result, str):  # IP mismatch or other error
                self.show_message('Error', result)
            else:
                self.show_message('Error', f'Incorrect username or password.')
        else:
            self.show_message('Error', 'Please enter both username and password.')

    def show_signup_view(self):
        """Switch to sign up view."""
        # Clear existing layout
        self.clear_dynamic_content()
        self.title_label.setText("Sign Up for an Account")

        # Add fields for sign-up view
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter username")
        
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Add email field
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter email")

        self.dynamic_content_layout.addWidget(self.username_input)
        self.dynamic_content_layout.addWidget(self.password_input)
        self.dynamic_content_layout.addWidget(self.email_input)

        self.signup_button = QPushButton('Sign Up', self)
        self.signup_button.clicked.connect(self.sign_up)
        self.dynamic_content_layout.addWidget(self.signup_button)

        # Add back button to login view
        self.back_to_login_button = QPushButton('Back to Login', self)
        self.back_to_login_button.clicked.connect(self.show_login_view)
        self.dynamic_content_layout.addWidget(self.back_to_login_button)

    def sign_up(self):
        """Sign up new user."""
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()  # Get email from input field

        # Get IP address using the FileHandler method
        ip_address = self.file_handler.get_ip_address()

        if username and password and email and ip_address:
            if not self.file_handler.is_username_unique(username):
                self.show_message('Error', 'Username already exists. Please choose a different username.')
                return
            try:
                # Pass the IP address along with the other details to add_user
                self.file_handler.add_user(username, password, ip_address, email)
                self.show_message('Success', 'User registered successfully.')
                self.show_login_view()
            except ValueError:
                self.show_message('Error', 'Registration failed. Please try again later.')
        else:
            self.show_message('Error', 'Please fill in all fields.')

    def show_reset_password_view(self):
            """Switch to forgot password view."""
            self.clear_dynamic_content()
            self.title_label.setText("Reset Your Password")

            self.otp_sent = False
            self.otp = None

            self.username_input = QLineEdit(self)
            self.username_input.setPlaceholderText("Enter username")
            self.password_input = QLineEdit(self)
            self.password_input.setPlaceholderText("Enter new password")
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.otp_input = QLineEdit(self)
            self.otp_input.setPlaceholderText("Enter OTP")

            self.dynamic_content_layout.addWidget(self.username_input)
            self.dynamic_content_layout.addWidget(self.password_input)
            self.dynamic_content_layout.addWidget(self.otp_input)

            self.send_otp_button = QPushButton('Send OTP', self)
            self.send_otp_button.clicked.connect(self.send_otp)
            self.dynamic_content_layout.addWidget(self.send_otp_button)

            self.reset_password_button = QPushButton('Reset Password', self)
            self.reset_password_button.clicked.connect(self.reset_password)
            self.dynamic_content_layout.addWidget(self.reset_password_button)

            self.go_back_button = QPushButton('Back to Login', self)
            self.go_back_button.clicked.connect(self.show_login_view)
            self.dynamic_content_layout.addWidget(self.go_back_button)

    def send_otp(self):
        """Send OTP to the user's email."""
        if self.otp_sent:
            self.show_message('Error', 'OTP has already been sent. Please check your inbox and enter the OTP to reset your password.')
            return

        username = self.username_input.text()
        if username:
            email = self.file_handler.get_user_email(username)
            if email:
                # Use OTPHandler to send OTP
                self.otp_sent = True
                self.otp_handler.send_verification_email(email)  # Send OTP
                self.show_message('OTP Sent', f'OTP has been sent to {email}. Please check your inbox.')
            else:
                self.show_message('Error', 'No user found with that username.')
        else:
            self.show_message('Error', 'Please provide username.')

    def reset_password(self):
        """Reset the password after verifying OTP."""
        username = self.username_input.text()
        new_password = self.password_input.text()
        entered_otp = self.otp_input.text()

        if not self.otp_sent:
            self.show_message('Error', 'Please send OTP first by clicking "Send OTP".')
            return

        if self.otp_handler.verify_otp(entered_otp):  # Check OTP using OTPHandler
            if self.file_handler.reset_password(username, new_password):
                self.show_message('Success', 'Password reset successfully.')
                self.show_login_view()
            else:
                self.show_message('Error', 'Error resetting password. Please try again.')
        else:
            self.show_message('Error', 'Invalid OTP. Please try again.')

    def clear_dynamic_content(self):
        """Clear the dynamic fields for each view."""
        for i in range(self.dynamic_content_layout.count()):
            widget = self.dynamic_content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def show_message(self, title, message):
        """Displays a message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStyleSheet("QMessageBox { font-size: 16px; }")
        msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AuthApp()
    ex.show()
    sys.exit(app.exec_())
