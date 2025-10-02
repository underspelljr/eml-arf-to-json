from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class ParsedEmail(Base):
    __tablename__ = "parsed_emails"

    id = Column(Integer, primary_key=True, index=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    subject = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    sender_ip = Column(String, nullable=True)
    ollama_evaluation = Column(Text, nullable=True)

    raw_email = relationship("RawEmail", back_populates="parsed_email", uselist=False)

class RawEmail(Base):
    __tablename__ = "raw_emails"

    id = Column(Integer, primary_key=True, index=True)
    raw_content = Column(Text, nullable=False)
    parsed_email_id = Column(Integer, ForeignKey("parsed_emails.id"))

    parsed_email = relationship("ParsedEmail", back_populates="raw_email")
