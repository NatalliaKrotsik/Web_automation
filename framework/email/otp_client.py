import email
import imaplib
import os
import re
import time

from framework.logger.logger import Logger


class OtpEmailClient:
    """Gmail IMAP client for retrieving OTP codes from example@gmail.com."""

    IMAP_SERVER = "imap.gmail.com"
    IMAP_PORT = 993

    def __init__(self, gmail_user: str = None, app_password: str = None):
        self.gmail_user = gmail_user or os.environ.get("AQA_GMAIL_ADDRESS", "example@gmail.com")
        self.app_password = app_password or os.environ.get("GMAIL_APP_PASSWORD")
        if not self.app_password:
            raise ValueError("GMAIL_APP_PASSWORD environment variable is required")

    def wait_for_otp(self, recipient: str, timeout: int = 60, interval: int = 5) -> str:
        deadline = time.time() + timeout
        while time.time() < deadline:
            otp = self._find_latest_otp()
            if otp:
                Logger.debug(f"[OtpEmailClient] OTP found for {recipient}")
                return otp
            Logger.debug(f"[OtpEmailClient] OTP not yet received for {recipient}, retrying...")
            time.sleep(interval)
        raise TimeoutError(f"OTP email was not received for {recipient} within {timeout} seconds")

    def _find_latest_otp(self) -> str | None:
        try:
            with imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT) as mail:
                mail.login(self.gmail_user, self.app_password)
                for folder in ["INBOX", "[Gmail]/Spam"]:
                    mail.select(folder)
                    _, message_ids = mail.search(None, "UNSEEN")
                    ids = message_ids[0].split()
                    if not ids:
                        continue
                    for msg_id in reversed(ids):
                        otp = self._fetch_otp_from_message(mail, msg_id)
                        if otp:
                            mail.store(msg_id, "+FLAGS", "\\Seen")
                            return otp
        except Exception as e:
            Logger.error(f"[OtpEmailClient] IMAP error: {e}")
        return None

    def _fetch_otp_from_message(self, mail: imaplib.IMAP4_SSL, msg_id: bytes) -> str | None:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        if not msg_data or not msg_data[0]:
            return None
        msg = email.message_from_bytes(msg_data[0][1])
        body = self._extract_body(msg)
        match = re.search(r"\b(\d{6})\b", body)
        return match.group(1) if match else None

    def _extract_body(self, msg: email.message.Message) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        return payload.decode(part.get_content_charset() or "utf-8", errors="ignore")
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(msg.get_content_charset() or "utf-8", errors="ignore")
        return ""
