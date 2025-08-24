import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import TribeJob,TribeApplication
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Numeric
from sqlalchemy.orm import relationship
from database import get_db

router = APIRouter()

# Utility function → Haversine Distance (km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c


# Create Job
@router.post("/jobs/")
def create_job(
    lister_id: int,
    title: str,
    pay: float,
    location: str,
    job_lat: float,
    job_long: float,
    description: str,
    ratings: float = None,
    db: Session = Depends(get_db)
):
    job = TribeJob(
        lister_id=lister_id,
        title=title,
        pay=pay,
        location=location,
        job_lat=job_lat,
        job_long=job_long,
        description=description,
        ratings=ratings
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# Get All Jobs (with distance from user)
@router.get("/jobs/")
def get_jobs(user_lat: float, user_long: float, db: Session = Depends(get_db)):
    jobs = db.query(TribeJob).all()
    results = []

    for job in jobs:
        distance_km = None
        if job.job_lat and job.job_long:
            distance_km = calculate_distance(user_lat, user_long, job.job_lat, job.job_long)

        results.append({
            "id": job.id,
            "title": job.title,
            "pay": f"₹ {job.pay}/day",
            "location": job.location,
            "description": job.description,
            "ratings": job.ratings,
            "distance": f"{distance_km:.1f} km away" if distance_km else "N/A"
        })

    return results


# Get Single Job (with distance from user)
@router.get("/jobs/{job_id}")
def get_job(job_id: int, user_lat: float, user_long: float, db: Session = Depends(get_db)):
    job = db.query(TribeJob).filter(TribeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    distance_km = None
    if job.job_lat and job.job_long:
        distance_km = calculate_distance(user_lat, user_long, job.job_lat, job.job_long)

    return {
        "id": job.id,
        "title": job.title,
        "pay": f"₹ {job.pay}/day",
        "location": job.location,
        "description": job.description,
        "ratings": job.ratings,
        "distance": f"{distance_km:.1f} km away" if distance_km else "N/A"
    }







#after clicking on apply option for a job
@router.post("/jobs/{job_id}/apply")
def apply_for_job(job_id: int, user_id: int, db: Session = Depends(get_db)):
    # Check if job exists
    job = db.query(TribeJob).filter(TribeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if already applied
    existing_app = db.query(TribeApplication).filter(
        TribeApplication.job_id == job_id,
        TribeApplication.user_id == user_id
    ).first()

    if existing_app:
        raise HTTPException(status_code=400, detail="Already applied for this job")

    # Create new application
    application = TribeApplication(
        user_id=user_id,
        job_id=job_id,
        status="applied",
        applied_date=datetime.utcnow()
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {"message": "Application submitted successfully", "application_id": application.id}

#   TO VIEW APPLICATION FOR A PARTICULAR USER
@router.get("/users/{user_id}/applications")
def view_applications(user_id: int, db: Session = Depends(get_db)):
    apps = db.query(TribeApplication).filter(TribeApplication.user_id == user_id).all()
    return apps


@router.put("/applications/{application_id}/status")
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db)):
    app = db.query(TribeApplication).filter(TribeApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    if status not in ["applied", "accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    app.status = status
    db.commit()
    db.refresh(app)
    return {"message": "Status updated", "application_id": app.id, "new_status": app.status}

#view all application for a job(for lister)
@router.get("/jobs/{job_id}/applications")
def get_job_applications(job_id: int, db: Session = Depends(get_db)):
    job = db.query(TribeJob).filter(TribeJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job.applications
