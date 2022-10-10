


from pydantic import BaseModel


class MailBase(BaseModel):
    subject: str
    body: str
