import os
import sys
import time
import re
import openai
from fastapi.encoders import jsonable_encoder


class ChatGpt:
    def __init__(self) -> None:
        self.api_key = os.environ["GPT_API_KEY"]
        self.model_id = "gpt-3.5-turbo"
        self.regex_mail = re.compile(
            r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        )
        self.messages = []
        self.info = {}
        self.config = {
            "role": "assistant",
            "content": "Assistant is an intelligent chatbot designed to help people to write an email.\
                                    Instructions:\
                                    - ask for the recipient's name.\
                                    - if recipient email address wasn't provided ask for it.\
                                    - ask for appointment's date wasn't provided ask for it.\
                                    - if it is a formal a formal email, write this way, otherwise write informal.",
        }

    def get_subject(self, content):
        return content.split("\n\n")[0].replace("Subject:", "").strip()

    def get_sender(self, content):
        re.fullmatch(self.regex_mail, content)

    def get_mail(self):
        mail = ""
        for message in self.messages:
            if re.fullmatch(self.regex_mail, message["content"]):
                mail = message["content"]
        return mail

    def mail_formater(self, mail, sender_name):
        subject_flag = False
        sentence_array = mail.split("\n")
        remove_range = []

        for idx, line in enumerate(mail.split("\n")):
            if line.find("Subject:") != -1:
                subject_flag = True
                self.info["subject"] = (
                    line.split("\n\n")[0].replace("Subject:", "").strip()
                )

            if line.find("[Your Name]") != -1:
                line = line.replace("[Your Name]", sender_name)
                remove_range.append(line)
                break

            if subject_flag == True and line.find("Subject:") == -1:
                remove_range.append(line)

        final_mail = "\n".join(remove_range)

        return final_mail

    def call_chatGPT(self, messages, temperature):
        print("CALL GPT")
        openai.api_key = self.api_key
        completion = openai.ChatCompletion.create(
            model=self.model_id, messages=messages, temperature=temperature
        )
        return {"role": "assistant", "content": completion.choices[0].message.content}

    # try:
    #     print("CALL GPT")
    #     openai.api_key = self.api_key
    #     completion = openai.ChatCompletion.create(
    #         model=self.model_id, messages=self.messages, temperature=0.0
    #     )
    #     return completion.choices[0].message.content

    # except:
    #     print("error")
    #     raise Exception(
    #         "chatGPT rate reached the limit of 3 requests, wait 20s and try again."
    #     )


# gpt = ChatGpt()

# sentence = "Thank you for providing the date and time of your upcoming bridal shower party. Now, I will draft an email to your sister, Jack, asking her to create a guest list for the party.\nSubject: Bridal Shower Guest ListHi Jack,\nI hope this email finds you well. I wanted to reach out to you regarding my upcoming bridal shower party. As you know, the party will be held on October 21st at 3PM.\n\nI would greatly appreciate it if you could take on the task of creating a guest list for the event. It would be wonderful if you could gather the names and contact information of all the guests I should invite.\n\nPlease let me know if you have any questions or need any further information. Thank you so much for your help!\n\nBest regards,\n[Your Name]\n\nFeel free to make any changes or additions as needed. Let me know if you need any further assistance!"

# final = gpt.mail_formater(sentence, "Emily")
# print(final)

# email my friend inviting him to my birthday party
# Email my sister to create a guest list for my upcoming bridal shower party
# if it is a formal a formal email, write this way, otherwise write informal.
