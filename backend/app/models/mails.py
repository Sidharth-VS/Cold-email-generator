import uuid
from sqlalchemy import Date, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Mails(Base):
    __tablename__ = "mails"
    id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), nullable=False)
    mail_content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
