import os
import resend


class Mail:
    def __init__(self) -> None:
        pass

    def send(self, recipient, content, subject):
        resend.api_key = "re_YMSPgaL3_GLZpdEjGkzTctiTPhiyPypXu"

        r = resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": recipient,
                "subject": subject,
                "text": content,
            }
        )

        return r
