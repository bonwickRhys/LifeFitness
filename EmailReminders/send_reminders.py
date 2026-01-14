from emailClient import EmailService
from database import Database

def send_all_reminders():
    db = Database()
    emailer = EmailService(
        sender_email="lifefitnessautomatic@gmail.com",
        app_password="YOUR_APP_PASSWORD"
    )

    rows = db.query("SELECT * FROM overdue")

    for row in rows:
        message = f"Hello {row['name']}, this is a reminder that you owe £{row['amount']}."
        emailer.send_email(
            to_email=row["email"],
            user_message=message,
            amount=row["amount"]
        )

if __name__ == "__main__":
    send_all_reminders()
