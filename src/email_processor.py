import time
import re

from .gmail_client import Email, GmailClientInterface


class EmailProcessor:
    def __init__(self, gmail_client: GmailClientInterface):
        self.gmail_client = gmail_client
        self.required_keywords = ["pseudo", "internship", "interest"]
        # Pre-compile regex patterns for better performance
        self.name_patterns = [
            re.compile(r"Best regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Sincerely,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Thanks,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Best,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Thank you,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
            re.compile(r"Kind regards,\s*([A-Za-z\s]+)", re.IGNORECASE | re.MULTILINE),
        ]

    def filter_emails(self, emails: list[Email]) -> list[Email]:
        # implement filtering logic based on required keywords
        filtered = []
        for email in emails:
            subject_lower = email.subject.lower()
            # Check if all required keywords are present in the subject
            if all(keyword in subject_lower for keyword in self.required_keywords):
                filtered.append(email)
        return filtered

    def extract_name_from_email(self, email_body: str) -> str | None:
        # implement name extraction logic
        for pattern in self.name_patterns:
            match = pattern.search(email_body)
            if match:
                name = match.group(1).strip()
                if name:  # Make sure we have a non-empty name
                    return name

        return None

    # Use this method. Do not modify it.
    def generate_response(self, name: str | None) -> str:
        if name:
            return f"""Dear {name},

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""
        else:
            return """Dear Applicant,

Thank you for your interest in our pseudo internship program. We have received your application and will review it carefully.

We will get back to you within 5-7 business days with an update on your application status.

Best regards,
Hiring Team"""

    def process_emails(self) -> dict:
        # Do not modify this block
        emails = []
        filtered_emails = []
        responses_sent = 0
        # end of non-modifiable block

        # implement email processing logic.
        # 1. Fetch emails from the gmail client
        emails = self.gmail_client.fetch_emails()

        # 2. Filter emails based on required keywords
        filtered_emails = self.filter_emails(emails)

        # 3. Process each filtered email: extract name, generate response, send email
        for email in filtered_emails:
            # Extract name from email body
            name = self.extract_name_from_email(email.body)

            # Generate response based on extracted name
            response_body = self.generate_response(name)

            # Create reply subject
            reply_subject = f"Re: {email.subject}"

            # Send response email
            if self.gmail_client.send_email(email.sender, reply_subject, response_body):
                responses_sent += 1

        # Do not modify this block
        return {
            "total_emails": len(emails),
            "filtered_emails": len(filtered_emails),
            "responses_sent": responses_sent,
        }
        # end of non-modifiable block
