import email
import imaplib
import re
import time


class EmailVerification:
    def __init__(self, email_address, password, imap_server="imap.gmail.com"):
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.mail = None

    def connect(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def disconnect(self):
        if self.mail:
            self.mail.logout()

    def get_verification_code(self, sender_email, subject_pattern=None, timeout=60, check_interval=3):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.mail.select("inbox")
                search_criteria = f'(FROM "{sender_email}")'
                if subject_pattern:
                    search_criteria = f'(FROM "{sender_email}" SUBJECT "{subject_pattern}")'
                result, data = self.mail.search(None, search_criteria)
                if result != "OK":
                    continue
                email_ids = data[0].split()
                if email_ids:
                    latest_email_id = email_ids[-1]
                    result, email_data = self.mail.fetch(latest_email_id, "(RFC822)")
                    if result == "OK":
                        raw_email = email_data[0][1]
                        msg = email.message_from_bytes(raw_email)
                        email_text = self._extract_text_from_email(msg)
                        code = self._extract_verification_code(email_text)
                        if code:
                            return code
                time.sleep(check_interval)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(check_interval)
        return None

    def _extract_text_from_email(self, msg):
        text_parts = []
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    if content_type == "text/plain":
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        text_parts.append(payload.decode(charset, errors="ignore"))
                    elif content_type == "text/html":
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or "utf-8"
                        text_parts.append(payload.decode(charset, errors="ignore"))
        else:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or "utf-8"
            text_parts.append(payload.decode(charset, errors="ignore"))
        return "\n".join(text_parts)

    def _extract_verification_code(self, text):
        pattern = r"Your temporary password is: (.{10,20})"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
