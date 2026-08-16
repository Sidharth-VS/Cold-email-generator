from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.mails import GeneratedEmail
from app.schemas.mails import GeneratedEmailCreate, GeneratedEmailResponse
from app.routes.auth import get_current_user_from_token
from app.services.generator import Generator
from app.services.scrape import get_webpage_text

router = APIRouter()


@router.post("/generate", response_model=GeneratedEmailResponse, status_code=status.HTTP_201_CREATED)
def generate_email(
    job_url: str,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    content = get_webpage_text(job_url)

    generator = Generator()
    job_details = generator.extract_job_details(job_url)

    portfolio_service = __import__("app.services.portfolio", fromlist=["Portfolio"]).Portfolio()

    skills = []
    for job in job_details:
        skills.extend(job.get("skills", []))

    links = portfolio_service.query(skills)

    link_list = [link.get("links") for link in links[0]] if links else []

    role = job_details[0].get("role", "")
    experience = job_details[0].get("experience", "")
    description = job_details[0].get("description", "")

    email_text = generator.generate_mail(description, current_user.username, "Developer", "Organisation", link_list)

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
    email = db.query(GeneratedEmail).filter(GeneratedEmail.id == email_id, GeneratedEmail.user_id == current_user.id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email
