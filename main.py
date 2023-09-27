import imaplib
import email
from email.header import decode_header
from notion_client import NotionClient  # Assume this is a library to interact with Notion

# Initialize Notion client
notion_client = NotionClient("your_notion_token")

# Email account credentials
email_accounts = [
    {"host": "imap.gmail.com", "username": "user1@gmail.com", "password": "password1"},
    # ... add other email accounts
]

def get_new_emails(host, username, password):
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    new_emails = []
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        new_emails.append(msg)
    return new_emails

def email_exists_in_notion(email_id):
    # Assume get_entries_by_email_id is a method to search entries by email ID in Notion
    entries = notion_client.get_entries_by_email_id(email_id)
    return len(entries) > 0

def add_email_to_notion(email_message):
    email_id = decode_header(email_message['Message-ID'])[0][0]
    if not email_exists_in_notion(email_id):
        # Assume add_entry is a method to add a new entry to Notion
        notion_client.add_entry({
            'email_id': email_id,
            'from': email_message['From'],
            'subject': email_message['Subject'],
            # ... add other email data as needed
        })

# Process each email account
for account in email_accounts:
    new_emails = get_new_emails(account['host'], account['username'], account['password'])
    for email_message in new_emails:
        add_email_to_notion(email_message)
