import imaplib
import email
from typing import Any
from dataclasses import dataclass, field
from email.utils import parseaddr
from email.header import Header, decode_header
from email.message import Message

@dataclass
class Mail:
    uid: str
    sender: str
    subject: str
    body: str


class MailDecoder:
    @staticmethod
    def decode_mail(uid: str, message_data: list[Any]) -> Mail | None:
        message = MailDecoder.decode_message(message_data)
        if message is None:
            return None
        sender = MailDecoder.sender(message)
        subject = MailDecoder.subject(message)
        body = MailDecoder.body(message)
        return Mail(uid, sender, subject, body)
    
    @staticmethod
    def decode_message(message_data: list[Any]) -> Message | None:
        raw_email = next((item[1] for item in message_data if isinstance(item, tuple)), None)
        if not raw_email:
            return None
        return email.message_from_bytes(raw_email)
    
    @staticmethod
    def text(value: Header | str) -> str:
        if not value:
            return ""

        result = []
        for part, encoding in decode_header(value):
            if isinstance(part, bytes):
                part = part.decode(encoding or "utf-8", errors="replace")
            result.append(str(part))

        return "".join(result)

    @staticmethod
    def sender(message: Message) -> str:
        sender_name, sender_address = parseaddr(message.get("From", ""))
        sender_name = MailDecoder.text(sender_name)
        return f"{sender_name} <{sender_address}>" if sender_name else sender_address

    @staticmethod
    def subject(message: Message) -> str:
        return MailDecoder.text(message.get("Subject", "(No subject)"))

    @staticmethod
    def body(message: Message) -> str:
        parts = message.walk() if message.is_multipart() else [message]
        body = ""

        for part in parts:
            if part.get_content_type() != "text/plain":
                continue
            if "attachment" in str(part.get("Content-Disposition", "")).lower():
                continue
            payload = part.get_payload(decode=True)
            if payload:
                charset = part.get_content_charset() or "utf-8"
                body += payload.decode(charset, errors="replace")

        return body


@dataclass
class MailServiceConfiguration:
    mail_address: str
    password: str
    imap_server: str
    imap_port: int

class MailService:
    def __init__(self, configuration: MailServiceConfiguration):
        self.server = configuration.imap_server
        self.port = configuration.imap_port
        self.address = configuration.mail_address
        self.password = configuration.password

    def connect_to_mail_service(self) -> imaplib.IMAP4_SSL:
        print("Connecting to mail service...")
        service = imaplib.IMAP4_SSL(self.server, self.port)
        service.login(self.address, self.password)
        print("Connected.")
        return service

    def dispose_mail_service(self, service: imaplib.IMAP4_SSL) -> None:
        service.close()
        service.logout()

    def get_unread_emails(self, ignore_uid: list[str]) -> list[Mail]:
        service = None
        try:
            service = self.connect_to_mail_service()
            return self._get_unread_emails(service, ignore_uid)
        except imaplib.IMAP4.error as e:
            print(f"Yahoo IMAP error: {e}")
        except Exception as e:
            print(f"Error while checking email: {e}")
        finally:
            if service:
                self.dispose_mail_service(service)
        return []

    def _get_unread_emails(self, service: imaplib.IMAP4_SSL, ignore_uid: list[str]) -> list[Mail]:
        status: str
        status, _ = service.select("INBOX", readonly=True)
        if status != "OK":
            return []
        
        data : list[bytes]
        status, data = service.uid("search", None, "UNSEEN")
        if status != "OK":
            return []

        mails :list[Mail]= []
        for uid_bytes in data[0].split():
            uid = uid_bytes.decode()
            if uid in ignore_uid:
                continue

            status, message_data = service.uid("fetch", uid_bytes, "(RFC822)")
            if status != "OK":
                continue

            mail = MailDecoder.decode_mail(uid, message_data)
            if mail is None:
                continue

            mails.append(mail)
        return mails

@dataclass
class MailCheckerConfiguration:
    keywords: list[str] = field(default_factory=list)
    search_in: list[str] = field(default_factory=lambda: ["subject", "sender", "body"])
    notify_only_once: bool = False

class MailChecker:
    def __init__(self, configuration: MailCheckerConfiguration, mail_service: MailService, notified_uids: list[str]):
        self.mail_service = mail_service
        self.search_in = configuration.search_in
        self.keywords = configuration.keywords
        self.notified_uids = notified_uids
        self.notify_only_once = configuration.notify_only_once

    def has_matching_keyword(self, mail: Mail) -> bool:
        fields = []
        if "subject" in self.search_in:
            fields.append(mail.subject)
        if "sender" in self.search_in:
            fields.append(mail.sender)
        if "body" in self.search_in:
            fields.append(mail.body)
        combined_text = "\n".join(fields).casefold()

        for keyword in self.keywords:
            if keyword.casefold() in combined_text:
                return True
        return False

    def retrieve_mails_passing_filter(self) -> list[Mail]:
        passing_mails :list[Mail]= []
        uids_to_ignore :list[str]= self.notified_uids if self.notify_only_once else []

        mails = self.mail_service.get_unread_emails(uids_to_ignore)
        for mail in mails:
            if self.has_matching_keyword(mail):
                passing_mails.append(mail)

        return passing_mails