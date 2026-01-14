import smtplib
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, sender_email, app_password):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465  # SSL
        self.sender_email = sender_email
        self.app_password = app_password

    def load_template(self, template_path="email_template.html"):
        """Load the HTML email template from file."""
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def build_email_body(self, user_message, template_path="email_template.html"):
        """Insert the user's message into the HTML template."""
        template = self.load_template(template_path)
        return template.replace("{{message}}", user_message)

    def send_email(self, to_email, user_message, subject="Overdue Balance Reminder"):
        """Send a styled HTML email using Gmail SMTP."""
        html_body = self.build_email_body(user_message)

        msg = MIMEText(html_body, "html")
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = to_email

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            return True, "Email sent successfully"

        except Exception as e:
            return False, f"Failed to send email: {e}"
