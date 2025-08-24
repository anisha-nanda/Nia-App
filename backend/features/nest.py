from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Numeric
from sqlalchemy.orm import relationship
from db import get_db
from models import NestCuisine
from models import House, Reservation
from typing import Optional
from authen import get_current_user 

router = APIRouter(prefix="/nest", tags=["Nest"])


@router.get("/cuisines")
def get_cuisines(db: Session = Depends(get_db)):
    return db.query(NestCuisine).all()

#Add new cuisine
@router.post("/cuisines")
def add_cuisine(name: str, id: int = None, db: Session = Depends(get_db)):
    cuisine = NestCuisine(name=name, description=description)
    db.add(cuisine)
    db.commit()
    db.refresh(cuisine)
    return cuisine

#HOOUSE SEARCH AND FILTERING


@router.get("/houses")
def search_houses(
    location: Optional[str] = None,
    room_type: Optional[str] = None,
    women_only: Optional[bool] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None,
    special_assistance: Optional[bool] = None,
    dietary_preference: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(House)

    if location:
        query = query.filter(House.location.ilike(f"%{location}%"))
    if room_type:
        query = query.filter(House.room_type == room_type)
    if women_only is not None:
        query = query.filter(House.women_only == women_only)
    if min_budget:
        query = query.filter(House.budget_min >= min_budget)
    if max_budget:
        query = query.filter(House.budget_max <= max_budget)
    if special_assistance is not None:
        query = query.filter(House.special_assistance == special_assistance)
    if dietary_preference:
        query = query.filter(House.dietary_preference == dietary_preference)

    return query.all()



# 2. Get all houses (search results list)
@router.get("/houses/all")
def list_houses(db: Session = Depends(get_db)):
    houses = db.query(House).all()

    results = []
    for h in houses:
        results.append({
            "id": h.id,
            "name": h.location,   
            "price": f"₹ {h.budget_min}/month",  
            "distance": "1 km",   
            "image": h.images.split(",")[0] if h.images else None
        })

    return results




# Get single house details
@router.get("/houses/{house_id}")
def get_house(house_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == house_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    return {
        "id": house.id,
        "name": house.location,   
        "address": house.location, 
        "dietary_preference": "Food Available" if house.dietary_preference else "No Food",
        "women_only": "Women-Only" if house.women_only else "Open to All",
        "room_type": house.room_type,
        "rent": f"₹{house.budget_min} monthly",
        "reservation_deposit": 1000.0,  
        "image": house.images.split(",")[0] if house.images else None
    }




# ✅ 4. Create reservation and update resevation table instant


router = APIRouter()


@router.post("/reserve")
def reserve_house(user_id: int, property_id: int, db: Session = Depends(get_db)):
    house = db.query(House).filter(House.id == property_id).first()
    if not house:
        raise HTTPException(status_code=404, detail="House not found")

    # expiry 7 days
    expiry = datetime.utcnow() + timedelta(days=7)

    reservation = Reservation(
        user_id=user_id,
        property_id=property_id,
        status="confirmed",
        deposit_paid=1000.0,
        expiry_time=expiry
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return {
        "message": "Reservation Confirmed!",
        "residence": house.location,
        "date": reservation.timestamp,
        "amount_paid": reservation.deposit_paid,
        "expiry": reservation.expiry_time,
        "reservation_id": reservation.id
    }


# View reservations for a house particular to that user

@router.get("/my_reservations")
def my_reservations(user_id: int, db: Session = Depends(get_db)):
    reservations = (
        db.query(Reservation, House)
        .join(House, Reservation.property_id == House.id)
        .filter(Reservation.user_id == user_id)
        .all()
    )

    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")

    result = []
    for res, house in reservations:
        result.append({
            "reservation_id": res.id,
            "residence": house.location,
            "status": res.status,
            "deposit_paid": res.deposit_paid,
            "date": res.timestamp,
            "expiry": res.expiry_time,
            "rent": house.budget_range,
            "room_type": house.room_type,
            "dietary_preference": house.dietary_preference,
            "women_only": house.women_only,
            "special_assistance": house.special_assistance
        })

    return {"my_reservations": result}


