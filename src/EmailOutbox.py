import smtplib, ssl
from src import Configurations, DataBridgeAbs

class EmailOutbox():
    """Outgoing email, encapsulates the process of sending an email"""

    def __init__ (self, conf: Configurations, databridge: DataBridgeAbs):
        self._smtp_server      = conf["smtp_server"]
        self._email_address    = conf["sender_email_address"]
        self._send_to          = conf["send_email_to"]
        self._smtp_port        = conf["smtp_port"]
        self._pass             = conf["pass"]
        self._databridge       = databridge

    def sendEmailAndRecord(self, message_text, subject):
        message = self._buildMessage(message_text, subject)

        secure_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port, context=secure_context) as email_server:
            email_server.login(self._email_address, self._pass)
            email_server.sendmail(self._email_address, self._send_to.split(";"), message)

        self._databridge.recordOutgoingEmail(self._send_to)

    def _buildMessage(self, message_text, subject):
        new_email_id = self._databridge.getNewEmailId()
        email_id_part = f"\n\n\n\n\n#sys[EmailId:{new_email_id}]"

        return f"Subject: {subject}\n\n{message_text}{email_id_part}"



