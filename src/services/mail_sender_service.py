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

from src import config


class MailSenderService:
    def __init__(self) -> None:
        self.scopes = config.MAIL_SCOPES
        self.token_file = config.MAIL_TOKEN_FILE
        self.credentials_file = config.MAIL_CREDENTIALS_FILE
        self.local_port = config.MAIL_LOCAL_PORT

        self.templates_folder = config.TEMPLATES_FOLDER
        self.mail_template = config.MAIL_TEMPLATE
        self.mail_subject = config.MAIL_SUBJECT

        super().__init__()

    def send_articles_notification(self, recipient, articles):
        environment = Environment(loader=FileSystemLoader(self.templates_folder))
        template = environment.get_template(self.mail_template)

        html_template_string = template.render(
            article_count=len(articles),
            articles=articles,
            version_date=datetime.datetime.utcnow()
        )

        return self.send_notification(recipient, html_template_string)

    def send_notification(self, recipient, body):
        sender = os.getenv("EMAIL_SENDER")

        try:
            creds = self.google_authenticate()
            service = build("gmail", "v1", credentials=creds)
            message = MIMEMultipart("alternative")

            message["To"] = recipient
            message["From"] = sender
            message["Subject"] = self.mail_subject
            message.attach(MIMEText(body, "html"))

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                .decode()

            create_message = {
                "raw": encoded_message
            }

            # pylint: disable=E1101
            send_message = (service.users().messages().send(
                userId="me",
                body=create_message
            ).execute())

        except HttpError as error:
            print(f"An unexpected error occurred: { error }")
            send_message = None
        return send_message

    def google_authenticate(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes)
                creds = flow.run_local_server(port=self.local_port)

            with open(self.token_file, "w") as token:
                token.write(creds.to_json())

        return creds
