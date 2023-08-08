#graphes_links 
Live_session = {
'AppSrv01_live_session':'https://presentation.egyptpost.local/#/monitors/501948+295968/1/perfOverviewTab',
'AppSrv02_live_session':'https://presentation.egyptpost.local/#/monitors/501948+296299/1/perfOverviewTab',
'AppSrv03_live_session':'https://presentation.egyptpost.local/#/monitors/501948+296660/1/perfOverviewTab',
'AppSrv04_live_session':'https://presentation.egyptpost.local/#/monitors/501948+296798/1/perfOverviewTab',
'AppSrv05_live_session':'https://presentation.egyptpost.local/#/monitors/501948+296295/1/perfOverviewTab',
'AppSrv06_live_session':'https://presentation.egyptpost.local/#/monitors/501948+296411/1/perfOverviewTab'
}

Availability = {
'AppSrv01_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139310/1/perfOverviewTab',
'AppSrv02_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139304/1/perfOverviewTab',
'AppSrv03_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139299/1/perfOverviewTab',
'AppSrv04_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139296/1/perfOverviewTab',
'AppSrv05_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139301/1/perfOverviewTab',
'AppSrv06_Availability':'https://presentation.egyptpost.local/#/monitors/501988+139298/1/perfOverviewTab'
}

Oracle = {
'Appsrv01_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296087/1/perfOverviewTab',
'Appsrv02_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296414/1/perfOverviewTab',
'Appsrv03_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296720/1/perfOverviewTab',
'Appsrv04_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296038/1/perfOverviewTab',
'Appsrv05_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296352/1/perfOverviewTab',
'Appsrv06_Oracle':'https://presentation.egyptpost.local/#/monitors/501940+296566/1/perfOverviewTab'
}


Thread_Pool = {
'Appsrv01_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+296103/1/perfOverviewTab',
'Appsrv02_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+296339/1/perfOverviewTab',
'Appsrv03_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+296684/1/perfOverviewTab',
'Appsrv04_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+295877/1/perfOverviewTab',
'Appsrv05_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+296185/1/perfOverviewTab',
'Appsrv06_Thread_Pool':'https://presentation.egyptpost.local/#/monitors/501930+296467/1/perfOverviewTab'
}

Memory = {
'Appsrv01_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296154/1/perfOverviewTab',
'Appsrv02_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296426/1/perfOverviewTab',
'Appsrv03_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296725/1/perfOverviewTab',
'Appsrv04_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296044/1/perfOverviewTab',
'Appsrv05_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296241/1/perfOverviewTab',
'Appsrv06_Memory':'https://presentation.egyptpost.local/#/monitors/501978+296617/1/perfOverviewTab'
}

import os
import smtplib
from email.message import EmailMessage

def send_email(body_message, folder_path):
    # Email configuration
    smtp_host = 'mail.egyptpost.org'
    smtp_port = 25  # Update the port if necessary
    sender_email = 'W_Abdelrahman.Ataa@EgyptPost.Org'
    recipient_emails = ['W_Abdelrahman.Ataa@EgyptPost.Org',
                         'w_soc_team@egyptpost.org',
                         'SOC_supervisors@EgyptPost.Org']
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
