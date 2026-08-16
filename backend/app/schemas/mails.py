from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class GeneratedEmailBase(BaseModel):
    job_url: str | None = None
    job_description: str | None = None
    generated_email: str
    links_used: list | None = None


class GeneratedEmailCreate(GeneratedEmailBase):
    user_id: uuid.UUID


class GeneratedEmailUpdate(BaseModel):
    job_url: str | None = None
    job_description: str | None = None
    generated_email: str | None = None
    links_used: list | None = None


class GeneratedEmailResponse(GeneratedEmailBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
