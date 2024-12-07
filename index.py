import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from Database import FileHandler  # Assuming FileHandler is in a separate file

class AuthApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the FileHandler class
        self.file_handler = FileHandler()

        # Set up the UI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Authentication System')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #e9f1f7;")  # Light blue background

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Title label (large and centered)
        self.title_label = QLabel("Login to Your Account", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 26px; font-weight: bold; color: #3b5998; margin-top: 30px;")
        self.main_layout.addWidget(self.title_label)

        # Username/Email input (updated prompt)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter email or username")
        self.username_input.setStyleSheet("""
            padding: 15px;
            font-size: 14px;
            border: 1px solid #ccd0d5;
            border-radius: 25px;
            background-color: #fff;
            margin: 10px 0;
        """)
        self.main_layout.addWidget(self.username_input)

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 15px;
            font-size: 14px;
            border: 1px solid #ccd0d5;
            border-radius: 25px;
            background-color: #fff;
            margin: 10px 0;
        """)
        self.main_layout.addWidget(self.password_input)

        # Login button (blue background, white text)
        self.login_button = QPushButton('Log In', self)
        self.login_button.setStyleSheet("""
            background-color: #3b5998;  /* Blue background */
            color: white;               /* White text */
            padding: 15px;
            font-size: 16px;
            border: none;
            border-radius: 25px;
        """)
        self.login_button.clicked.connect(self.verify_user)
        self.main_layout.addWidget(self.login_button)

        # Forgot Password link
        self.forgot_password_label = QLabel('<a href="#">Forgotten password?</a>', self)
        self.forgot_password_label.setAlignment(Qt.AlignCenter)
        self.forgot_password_label.setStyleSheet("""
            font-size: 14px;
            color: #3b5998;
            text-decoration: underline;
        """)
        self.forgot_password_label.linkActivated.connect(self.show_reset_password)  # Fix: link to show_reset_password
        self.main_layout.addWidget(self.forgot_password_label)

        # Register new account button
        self.register_button = QPushButton('Sign Up', self)
        self.register_button.setStyleSheet("""
            background-color: #42b72a;
            color: white;
            padding: 15px;
            font-size: 16px;
            border: none;
            border-radius: 25px;
            margin-top: 15px;
        """)
        self.register_button.clicked.connect(self.add_user)
        self.main_layout.addWidget(self.register_button)

        # Set the main layout to the window
        self.setLayout(self.main_layout)

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Check if both username and password are entered
        if username and password:
            # Check if the username already exists
            if self.file_handler.verify_user(username, None):  # Check if the username exists
                self.show_message('Error', 'Username already exists. Please choose a different one.')
            else:
                self.file_handler.add_user(username, password)
                self.show_message('Success', f'User added successfully.')
        else:
            self.show_message('Error', 'Please enter both username and password.')

    def verify_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            if self.file_handler.verify_user(username, password):
                self.show_message('Success', f'User verified successfully.')
            else:
                self.show_message('Error', f'Incorrect username or password.')
        else:
            self.show_message('Error', 'Please enter both username and password.')

    def show_reset_password(self):
        """Switch to the reset password view"""
        self.title_label.setText("Reset Your Password")
        self.username_input.setPlaceholderText("Enter your username")
        self.password_input.setPlaceholderText("Enter new password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button.setText("Reset Password")
        self.login_button.clicked.disconnect()  # Disconnect previous click event
        self.login_button.clicked.connect(self.reset_password)  # Connect to reset password method

        # Update forgot password link to "Log In"
        self.forgot_password_label.setText('<a href="#">Log In</a>')
        self.forgot_password_label.linkActivated.connect(self.reset_to_login_view)

        # Change "Sign Up" button to "Go to Sign Up"
        self.register_button.setText("Sign Up")
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.reset_to_register_view)

    def reset_password(self):
        username = self.username_input.text()
        new_password = self.password_input.text()

        if username and new_password:
            if self.file_handler.reset_password(username, new_password):
                self.show_message('Success', f'Password reset successfully.')
                self.reset_to_login_view()  # Reset to login view after success
            else:
                self.show_message('Error', f'Username not found.')
        else:
            self.show_message('Error', 'Please enter both username and new password.')

    def reset_to_login_view(self):
        """Reset to the login view after password reset"""
        self.title_label.setText("Login to Your Account")
        self.username_input.setPlaceholderText("Email or Phone")
        self.password_input.setPlaceholderText("Password")
        self.login_button.setText("Log In")
        self.login_button.clicked.disconnect()  # Disconnect from reset password
        self.login_button.clicked.connect(self.verify_user)  # Reconnect to login verification

        # Update forgot password link to "Forgotten password?"
        self.forgot_password_label.setText('<a href="#">Forgotten password?</a>')
        self.forgot_password_label.linkActivated.connect(self.show_reset_password)

        # Change "Go to Sign Up" back to "Sign Up"
        self.register_button.setText("Sign Up")
        self.register_button.clicked.disconnect()
        self.register_button.clicked.connect(self.add_user)

    def reset_to_register_view(self):
        """Go back to the register view"""
        self.title_label.setText("Create a New Account")
        self.username_input.setPlaceholderText("Email or Phone")
        self.password_input.setPlaceholderText("Password")
        self.login_button.setText("Sign Up")
        self.login_button.clicked.disconnect()  # Disconnect from login
        self.login_button.clicked.connect(self.add_user)  # Reconnect to sign-up

    def show_message(self, title, message):
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
