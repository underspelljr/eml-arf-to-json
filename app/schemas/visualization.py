from pydantic import BaseModel
import datetime

class ParsedEmail(BaseModel):
    id: int
    from_address: str
    to_address: str
    subject: str
    date: datetime.datetime
    sender_ip: str | None
    ollama_evaluation: str | None
    raw_email_id: int | None

    class Config:
        orm_mode = True

class RawEmail(BaseModel):
    id: int
    raw_content: str
    parsed_email_id: int

    class Config:
        orm_mode = True

class VisualizationData(BaseModel):
    parsed_emails: list[ParsedEmail]
    raw_emails: list[RawEmail]
