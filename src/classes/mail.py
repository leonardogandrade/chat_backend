import os
import resend


class Mail:
    def __init__(self) -> None:
        pass

    def send(self, recipient, content, subject):
        resend.api_key = os.getenv["RESEND_API_KEY"]

        r = resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": recipient,
                "subject": subject,
                "text": content,
            }
        )

        return r
