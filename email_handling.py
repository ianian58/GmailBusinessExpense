from googleapiclient.discovery import build
import base64

def get_service(creds):
    """
    Return the Gmail API service.
    """
    return build('gmail', 'v1', credentials=creds)

def get_unread_emails(service):
    """
    Fetch and return unread emails.
    """
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    return results.get('messages', [])

def mark_email_as_read(service, message_id):
    """
    Mark a specific email as read.
    """
    service.users().messages().modify(userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()

def get_email_data(service, message_id):
    """
    Fetch and return data of a specific email.
    """
    return service.users().messages().get(userId='me', id=message_id).execute()

def get_email_attachments(service, email_data):
    """
    Extract and return attachments from an email.
    """
    attachments = []
    for part in email_data['payload']['parts']:
        if part['filename']:
            if 'data' in part['body']:
                file_data = base64.urlsafe_b64decode(part['body']['data'].encode('UTF-8'))
            else:
                attachment_id = part['body']['attachmentId']
                attachment = service.users().messages().attachments().get(userId='me', messageId=email_data['id'], id=attachment_id).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
            attachments.append(file_data)
    return attachments
