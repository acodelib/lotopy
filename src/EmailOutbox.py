import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from src import Configurations, DataBridgeAbs


class EmailOutbox():
    """Outgoing email, encapsulates the process of sending an email"""
    EMAIL_HTML = 1
    EMAIL_TXT = 2

    def __init__(self, conf: Configurations, databridge: DataBridgeAbs):
        self._smtp_server = conf["smtp_server"]
        self._email_address = conf["sender_email_address"]
        self._send_to = conf["send_email_to"]
        self._smtp_port = conf["smtp_port"]
        self._pass = conf["pass"]
        self._databridge = databridge

    def sendEmailAndRecord(self, message_content, subject, message_format=EMAIL_HTML):
        """1 or EMAIL_HTML when passing message_content as HTML
           2 or EMAIL_TXT when passing message_content as plain text"""

        if message_format == EmailOutbox.EMAIL_HTML:
            message = self._buildHtmlMessage(message_content, subject)
        elif message_format == EmailOutbox.EMAIL_TXT:
            message = self._buildTextMessage(message_content, subject)

        secure_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port, context=secure_context) as email_server:
            email_server.login(self._email_address, self._pass)
            email_server.sendmail(self._email_address, self._send_to.split(";"), message.as_string())

        self._databridge.recordOutgoingEmail(self._send_to)

    def _buildHtmlMessage(self, message_text, subject):
        new_email_id = self._databridge.getNewEmailId()
        email_id_part = f"\n<br><br><br><br>#sys[EmailId:{new_email_id}]"
        header = """\
        <html>
            <head></head>
                <body>
        """
        footer = f"""\
                {email_id_part}
            </body>
        </html>
        """
        full_html_msg = header + "\n" + message_text + "\n" + footer
        message = MIMEMultipart('alternative')
        message["Subject"] = subject
        message_content = MIMEText(full_html_msg, 'html')
        message.attach(message_content)

        return message

    def _buildTextMessage(self, message_text, subject):
        new_email_id = self._databridge.getNewEmailId()
        email_id_part = f"\n\n\n\n\n#sys[EmailId:{new_email_id}]"

        return f"Subject: {subject}\n\n{message_text}{email_id_part}"