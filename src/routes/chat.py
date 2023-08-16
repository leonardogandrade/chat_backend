"""
    Sentence Module docstring
"""


from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.chat import Item, Chat
from classes.chat_gpt import ChatGpt
from classes.mail import Mail


chat = APIRouter()
mail = Mail()
gpt = ChatGpt()


@chat.post("/chat")
async def chat_interation(chat: Chat):
    """Method docstring"""

    new_chat = []

    if len(chat.messages) < 2:
        new_chat.append(gpt.config)

    for item in chat.messages:
        new_chat.append(jsonable_encoder(item))

    gpt.messages = new_chat

    if len(gpt.messages) > 2 and gpt.messages[-1]["content"].find("#send_mail") == -1:
        last_gpt_interaction = gpt.call_chatGPT(messages=gpt.messages, temperature=0.0)
        gpt.messages.append(jsonable_encoder(last_gpt_interaction))

    if gpt.messages[-1]["content"].find("Subject:") != -1:
        gpt.info["sender_name"] = gpt.messages[1]["content"].split(" ")[1]
        mail_formated = gpt.mail_formater(
            gpt.messages[-1]["content"], gpt.info["sender_name"]
        )
        gpt.messages.pop()
        gpt.messages.append({"role": "assistant", "content": mail_formated})

    if gpt.messages[-1]["content"].find("#send_mail") != -1:
        gpt.info["recipient"] = gpt.get_mail()
        mail.send(
            gpt.info["recipient"], gpt.messages[-2]["content"], gpt.info["subject"]
        )

    return JSONResponse(
        content=jsonable_encoder(gpt.messages), status_code=status.HTTP_200_OK
    )
