import email
import imaplib
from email.header import decode_header


class EmailFetcher:

    def __init__(self, imap_server, imap_port, email_address, password, mailbox):
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.email_address = email_address
        self.password = password
        self.mailbox = mailbox

    def connect_server(self):
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
        except Exception as error:
            return str(error)

    def login(self):
        try:
            self.imap.login(self.email_address, self.password)
        except imaplib.IMAP4.error:
            return "LOGIN FAILED!!!"

    def select_mailbox(self):
        self.imap.select(self.mailbox)

    def fetch_mailbox_emails(self):
        status, email_ids = self.imap.search(None, 'ALL')
        for email_id in email_ids[0].split():
            self.fetch_email_data(email_id)

    def fetch_email_data(self, email_id):
        status, email_data = self.imap.fetch(email_id, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)
        self.print_email_details(email_message)

    @staticmethod
    def print_email_details(email_message):
        from_header = email_message['From']
        dh = decode_header(from_header)
        default_charset = dh[0][1] or "ASCII"
        from_decoded = dh[0][0].decode(default_charset)

        print(f"From: {from_decoded}")
        print(f"To: {email_message['To']}")
        print(f"Subject: {email_message['Subject']}")
        print(f"Date: {email_message['Date']}")
        print("-----------------------------------")
        EmailFetcher.iterate_email_parts(email_message)

    @staticmethod
    def iterate_email_parts(email_message):
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            content_type = part.get_content_type()

            if content_type == 'text/plain':
                charset = part.get_content_charset()
                email_body = part.get_payload(decode=True).decode(charset, errors='ignore')
                print(email_body)
            else:
                content_disposition = part.get('Content-Disposition')
                if content_disposition is not None:
                    filename = part.get_filename()
                    if 'attachment' in content_disposition or 'inline' in content_disposition:
                        try:
                            with open(filename, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                            print(f"File {filename} saved.")
                        except Exception as e:
                            print(f"Error during saving a file: {str(e)}")

    def starter(self):
        self.connect_server()
        self.login()
        self.select_mailbox()
        self.fetch_mailbox_emails()
        self.logout()

    def logout(self):
        self.imap.logout()


email_fetcher = EmailFetcher('outlook.office365.com', 993, 'ikvictp7@outlook.com', 'Somepassword123', 'INBOX')
# email_fetcher.connect_server()
# email_fetcher.login()
# email_fetcher.select_mailbox()
# email_fetcher.fetch_mailbox_emails()
# email_fetcher.logout()

email_fetcher.starter()
