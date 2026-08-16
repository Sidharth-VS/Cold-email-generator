from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class PortfolioBase(BaseModel):
    tech_stack: str
    link: str


class PortfolioCreate(PortfolioBase):
    user_id: uuid.UUID


class PortfolioUpdate(BaseModel):
    tech_stack: str | None = None
    link: str | None = None


class PortfolioResponse(PortfolioBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
