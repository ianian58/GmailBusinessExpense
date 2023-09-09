import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes required for Gmail API authentication
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    """
    Authenticate the user with Gmail API and return the credentials.
    If credentials are not available or are invalid, prompt the user to log in.
    """
    creds = None
    # Check if token.pickle file exists which has stored credentials
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/Users/ian/Downloads/client_secret_1064613950676-dldu288otn9lijklupqr4otit9d38tok.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run in token.pickle
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds
