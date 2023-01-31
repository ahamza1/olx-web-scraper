import base64
import datetime
import os.path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from jinja2 import Environment, FileSystemLoader


class MailSender:
    def __init__(self) -> None:
        super().__init__()

    def send_articles_notification(self, recipient, articles):
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("mail.html")

        html_template_string = template.render(
            article_count=len(articles),
            articles=articles,
            version_date=datetime.datetime.utcnow()
        )

        self.send_notification(recipient, html_template_string)

    def send_notification(self, recipient, body):
        sender = os.getenv("EMAIL_SENDER")

        try:
            creds = self.google_authenticate()
            service = build('gmail', 'v1', credentials=creds)
            message = MIMEMultipart('alternative')

            message['To'] = recipient
            message['From'] = sender
            message['Subject'] = 'New Articles Digest'
            message.attach(MIMEText(body, 'html'))

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                'raw': encoded_message
            }

            # pylint: disable=E1101
            send_message = (service.users().messages().send(
                userId="me",
                body=create_message
            ).execute())

            print(F'Message Id: {send_message["id"]}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        return send_message

    @staticmethod
    def google_authenticate():
        # If modifying these scopes, delete the file token.json.
        scopes = ['https://mail.google.com/']

        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                creds = flow.run_local_server(port=61642)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds
