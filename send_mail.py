import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class ShutterEmail():

    def __init__(self, unit_id, acc_name, last_conn):
        self.unit_id = unit_id
        self.acc_name = acc_name
        self.last_conn = last_conn

    def email(self):
        sender_email = "ivisbi2021@gmail.com"
        receiver_email = "ivisbi2021@gmail.com"
        password = "ivis@123#"

        message = MIMEMultipart("alternative")
        message["Subject"] = "Site Offline Report"
        message["From"] = sender_email
        message["To"] = receiver_email
        now = datetime.now()

        text = '''""" \
                Hi,
                
                The below site is offline today : """+"""\
                
                Site Unit Id : """+self.unit_id+""" \
                
                Site Name : """+self.acc_name+""" \
                
                Last Connected : """+self.last_conn+"""\
                
                
                Regards,
                iVIS Support
                """ '''

        x = open('mail.html')
        id1 = self.unit_id
        id2 = self.acc_name
        id3 = self.last_conn
        html = x.read().format(p1=id1, p2=id2, p3=id3)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

