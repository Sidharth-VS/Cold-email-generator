from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uuid

from app.core.deps import get_db
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate, PortfolioResponse
from app.routes.auth import get_current_user_from_token
from app.services.portfolio import Portfolio as PortfolioService

router = APIRouter()


@router.post("/", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    portfolio_in: PortfolioCreate,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    portfolio = Portfolio(
        user_id=current_user.id,
        tech_stack=portfolio_in.tech_stack,
        link=portfolio_in.link,
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    service = PortfolioService()
    chromadb_ids = service.store(portfolio.tech_stack, portfolio.link, current_user.id)
    portfolio.chromadb_ids = chromadb_ids
    db.commit()
    db.refresh(portfolio)

    return portfolio


@router.get("/", response_model=List[PortfolioResponse])
def list_portfolios(skip: int = 0, limit: int = 100, current_user=Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    return db.query(Portfolio).filter(Portfolio.user_id == current_user.id).offset(skip).limit(limit).all()


@router.get("/{portfolio_id}", response_model=PortfolioResponse)
def get_portfolio(portfolio_id: str, current_user=Depends(get_current_user_from_token), db: Session = Depends(get_db)):
    try:
        pid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolio = db.query(Portfolio).filter(Portfolio.id == pid, Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.put("/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio(
    portfolio_id: str,
    portfolio_in: PortfolioUpdate,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    try:
        pid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolio = db.query(Portfolio).filter(Portfolio.id == pid).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    update_data = portfolio_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(portfolio, field, value)

    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_portfolio(
    portfolio_id: str,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db),
):
    try:
        pid = uuid.UUID(portfolio_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolio = db.query(Portfolio).filter(Portfolio.id == pid).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    service = PortfolioService()
    service.delete(portfolio.chromadb_ids)

    db.delete(portfolio)
    db.commit()
