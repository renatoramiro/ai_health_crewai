from crewai.tools import BaseTool
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community.gmail.send_message import GmailSendMessage
from typing import Optional, Literal

class SendEmailTool(BaseTool):
    name: str = "Send Email"
    description: str = """Use this tool to send an email with the exercises plan and diet plan to a user.
    The input should be a dictionary with the following keys:
    - subject: The email subject
    - message: The email body in markdown format
    - to_email: The recipient's email address
    """

    def _run(self, subject: str, message: str, to_email: str) -> str:
        try:
            # Get Gmail credentials
            credentials = get_gmail_credentials(
                token_file="token.json",
                scopes=["https://mail.google.com/"],
                client_secrets_file="credentials.json",
            )
            
            # Build Gmail service
            api_resource = build_resource_service(credentials=credentials)
            
            # Create Gmail send message tool
            gmail_sender = GmailSendMessage(api_resource=api_resource)
            
            # Send the email using invoke method
            response = gmail_sender.invoke({
                "to": to_email,
                "subject": subject,
                "message": message,
            })
            
            return f"Email sent successfully to {to_email}!"
            
        except Exception as e:
            return f"Failed to send email: {str(e)}"