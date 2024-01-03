import os
import smtplib
from email.message import EmailMessage

def send_email(body_message, folder_path):
    # Email configuration
    smtp_host = 'mail.egyptpost.org'
    smtp_port = 25  # Update the port if necessary
    sender_email = 'mohamedgamal@EgyptPost.Org'
    recipient_emails = ['W_Abdelrahman.Ataa@EgyptPost.Org'
                         ]
    subject = 'Graphes status'

    # Create the email message
    message = EmailMessage()
    message.set_content(body_message, subtype='html')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = ', '.join(recipient_emails)

    # Attach images from the specified folder if it's not empty
    if os.listdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # Add more extensions if needed
                image_path = os.path.join(folder_path, filename)
                with open(image_path, 'rb') as image_file:
                    image_data = image_file.read()
                    image_type = filename.split('.')[-1]  # Get the file extension
                    message.add_attachment(image_data, maintype='image', subtype=image_type, filename=filename)

    # Create the SMTP connection
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.set_debuglevel(1)  # Enable debug output for troubleshooting
        server.ehlo()
        server.sendmail(sender_email, recipient_emails, message.as_string())



content = f"test test"
send_email(content, "/home/kyo/Desktop/abdelrahman/Test_side/test2")               