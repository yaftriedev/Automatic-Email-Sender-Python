import smtplib
import ssl
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(message_file, recipients_file, subject, sender_email, password, smtp_server, smtp_port):
    # Load the email content (HTML)
    with open(message_file, 'r', encoding='utf-8') as file:
        email_content = file.read()

    # Load the list of recipient email addresses
    with open(recipients_file, 'r', encoding='utf-8') as file:
        recipients = [line.strip() for line in file if line.strip()]

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message.attach(MIMEText(email_content, "html"))  # Attach content as HTML

    # Set up SSL context for secure connection
    context = ssl.create_default_context()
    
    # Connect to SMTP server and send the email
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(sender_email, password)
            for recipient in recipients:
                message["To"] = recipient
                server.sendmail(sender_email, recipient, message.as_string())
                print(f"Email sent to: {recipient}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Send bulk HTML emails using SMTP.")
    parser.add_argument("message_file", help="Path to the file containing the HTML email content.")
    parser.add_argument("recipients_file", help="Path to the file containing recipient email addresses.")
    parser.add_argument("subject", help="Subject of the email.")
    parser.add_argument("sender_email", help="Your email address.")
    parser.add_argument("password", help="Your email account password.")
    parser.add_argument("smtp_server", help="SMTP server address (e.g., smtp.gmail.com).")
    parser.add_argument("smtp_port", type=int, help="SMTP server port (e.g., 465 for SSL).")

    args = parser.parse_args()
    send_email(args.message_file, args.recipients_file, args.subject, args.sender_email, args.password, args.smtp_server, args.smtp_port)
