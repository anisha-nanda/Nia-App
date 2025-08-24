from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import StudioCategory, StudioItem

router = APIRouter(prefix="/studio", tags=["Studio"])




@router.get("/categories", response_model=List[dict])
def get_categories(db: Session = Depends(get_db)):
    
    categories = db.query(StudioCategory).all()
    return [c.__dict__ for c in categories]




@router.get("/categories/{category_id}/items", response_model=List[dict])
def get_items_in_category(
    category_id: int,
    db: Session = Depends(get_db),
    condition: str = Query(None, description="Filter by condition (New/Used)"),
    min_price: float = Query(0, description="Minimum budget"),
    max_price: float = Query(999999, description="Maximum budget"),
    financing: bool = Query(None, description="Filter by financing availability"),
):
    """Fetch items under a specific category with optional filters"""
    query = db.query(StudioItem).filter(StudioItem.category_id == category_id)

    if condition:
        query = query.filter(StudioItem.condition.ilike(condition))
    if financing is not None:
        query = query.filter(StudioItem.financing_available == financing)

    query = query.filter(StudioItem.price >= min_price, StudioItem.price <= max_price)

    items = query.all()
    if not items:
        raise HTTPException(status_code=404, detail="No items found")

    return [item.__dict__ for item in items]
