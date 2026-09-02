import uuid
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime

from .base import Base


class GeneratedEmail(Base):
    __tablename__ = "generated_emails"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_email: Mapped[str] = mapped_column(Text, nullable=False)
    links_used: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
