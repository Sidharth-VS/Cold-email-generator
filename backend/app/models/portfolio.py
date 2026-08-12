import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Portfolio(Base):
    __tablename__ = "portfolio"
    id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True), nullable=False)
    tech_stack: Mapped[str] = mapped_column(String(255), nullable=False)
    link: Mapped[str] = mapped_column(String(255), nullable=False)