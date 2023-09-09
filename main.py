from authentication import authenticate
import email_handling as eh
import ocr_handling as oh

def main():
    """
    Main function to process unread emails and extract text from their attachments.
    """
    # Authenticate and get the Gmail API service
    creds = authenticate()
    service = eh.get_service(creds)
    
    try:  # Handle potential connectivity or other unexpected issues
        # Fetch unread emails
        messages = eh.get_unread_emails(service)
        if not messages:
            print("No unread messages found.")
        else:
            for message in messages:
                # Fetch email data
                email_data = eh.get_email_data(service, message['id'])
                
                # Extract and print the subject of the email
                headers = email_data['payload']['headers']
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                print("Subject:", subject)
                
                # Extract text from the attachments and print
                attachments = eh.get_email_attachments(service, email_data)
                for attachment in attachments:
                    try:  # Handle potential Tesseract errors
                        extracted_text = oh.get_text_from_image(attachment)
                        print("Extracted Text:", extracted_text)
                        print("===================================")
                    except oh.TesseractError as te:
                        print(f"Error processing image with Tesseract: {te}")
                        continue  # Continue to next attachment or email
                
                # Mark the email as read
                eh.mark_email_as_read(service, message['id'])
    except Exception as e:
        print(f"Error encountered: {e}")
        # For connectivity issues, you might want to retry or prompt the user
        # to check their connection.

if __name__ == '__main__':
    main()