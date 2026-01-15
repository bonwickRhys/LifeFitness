from emailClient import EmailService
from database import Database

def send_all_reminders():
    db = Database()

    emailer = EmailService(
        sender_email="lifefitnessautomatic@gmail.com",
        app_password=""
    )

    overdue_rows = db.query("SELECT * FROM overdue")

    for row in overdue_rows:
        name = row["name"]
        amount = row["amount"]
        to_email = row["email"]

        # Default message that goes inside {{message}}
        custom_message = (
            "This is a friendly reminder that your membership account currently has an "
            "outstanding balance. Please arrange payment at your earliest convenience or "
            "contact us if you believe this is an error. We appreciate your cooperation."
        )

        success, msg = emailer.send_email(
            to_email=to_email,
            name=name,
            amount=amount,
            user_message=custom_message
        )

        print(f"{name} → {to_email} → {msg}")

if __name__ == "__main__":
    send_all_reminders()
