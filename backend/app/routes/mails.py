from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from app.core.deps import get_db
from app.models.mails import GeneratedEmail
from app.schemas.mails import GeneratedEmailCreate, GeneratedEmailResponse
from app.routes.auth import get_current_user_from_token
from app.services.generator import Generator
from app.services.scrape import get_webpage_text
from app.services.portfolio import Portfolio as PortfolioService

router = APIRouter()


@router.post("/generate", response_model=GeneratedEmailResponse, status_code=status.HTTP_201_CREATED)
def generate_email(
    job_url: str,
    role: str | None = None,
    organisation: str | None = None,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    content = get_webpage_text(job_url)

    generator = Generator()
    job_details = generator.extract_job_details(job_url)

    portfolio_service = PortfolioService()

    skills = []
    for job in job_details:
        skills.extend(job.get("skills", []))

    links = portfolio_service.query(skills, current_user.id)

    link_list = [link.get("links") for link in links[0]] if links else []

    role = role or "Developer"
    organisation = organisation or "Organisation"
    name = current_user.username

    description = job_details[0].get("description", "") if job_details else ""

    email_text = generator.generate_mail(description, name, role, organisation, link_list)

    email = GeneratedEmail(
        user_id=current_user.id,
        job_url=job_url,
        job_description=description,
        generated_email=email_text,
        links_used=link_list,
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    return email


@router.get("/", response_model=List[GeneratedEmailResponse])
def list_emails(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    return db.query(GeneratedEmail).filter(GeneratedEmail.user_id == current_user.id).offset(skip).limit(limit).all()


@router.get("/{email_id}", response_model=GeneratedEmailResponse)
def get_email(email_id: str, current_user=Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    try:
        eid = uuid.UUID(email_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Email not found")
    email = db.query(GeneratedEmail).filter(GeneratedEmail.id == eid, GeneratedEmail.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.delete("/{email_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email(email_id: str, current_user=Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    try:
        eid = uuid.UUID(email_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Email not found")
    email = db.query(GeneratedEmail).filter(GeneratedEmail.id == eid, GeneratedEmail.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    db.delete(email)
    db.commit()
