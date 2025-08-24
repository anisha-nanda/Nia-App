#register page input and login page input

from pydantic import BaseModel
from db import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer,Text, String, Float, ForeignKey, DateTime, Boolean,Enum
from sqlalchemy.sql import func

class reg_users(BaseModel):

    name: str
    id:str
    phone: int
    location:str
    password: str

class login_users(BaseModel):

    name: str
    id:str
    password: str    


class login_sellers(BaseModel): 
    name:str
    seller_id:str
    password:str   
    phone:int

class reg_sellers(BaseModel): 
    name:str
    seller_id:str
    password:str
    location:str  



#NEST FRONT
class NestCuisine(Base):
    __tablename__ = "cuisines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class House(Base):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, nullable=False)
    location = Column(String, index=True)
    room_type = Column(String)   # shared/private
    budget_min = Column(Float)
    budget_max = Column(Float)
    accessibility_features = Column(Text)
    images = Column(Text)   # store image URLs as JSON/text
    women_only = Column(Boolean, default=False)
    house_rules = Column(Text)
    special_assistance = Column(Boolean, default=False)
    dietary_preference = Column(String)   # veg / non-veg / any


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    status = Column(String, default="confirmed")
    deposit_paid = Column(Float, default=1000.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    expiry_time = Column(DateTime(timezone=True))
    house = relationship("House", back_populates="reservations")




# to specify that each user can make its specific reservation only


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="user")
       
#STUDIO


# ---------------- Studio Houses ----------------
class StudioHouse(Base):
    __tablename__ = "studio_houses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)

    posts = relationship("StudioPost", back_populates="house")


# ---------------- Studio Posts ----------------
class StudioPost(Base):
    __tablename__ = "studio_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    house_id = Column(Integer, ForeignKey("studio_houses.id"))

    house = relationship("StudioHouse", back_populates="posts")


#TRIBE
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# ---------------- Tribe Jobs ----------------
class TribeJob(Base):
    __tablename__ = "tribe_jobs"

    id = Column(Integer, primary_key=True, index=True)
    lister_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # who posted
    title = Column(String, nullable=False)
    pay = Column(Integer, nullable=False)
    location = Column(String, nullable=True)
    job_lat = Column(Float, nullable=True)
    job_long = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    ratings = Column(Float, nullable=True)

    applications = relationship("TribeApplication", back_populates="job")


# ---------------- Tribe Applications ----------------
#upon clicking apply option
class TribeApplication(Base):
    __tablename__ = "tribe_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))   # assumes users table
    job_id = Column(Integer, ForeignKey("tribe_jobs.id"))
    status = Column(String, default="applied")          # applied/accepted/rejected
    applied_date = Column(DateTime, default=datetime.utcnow)

    job = relationship("TribeJob", back_populates="applications")


#STUDIO
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base


# Main Category (e.g., Tech Devices, Wearables, Home & Living, Financing Options)
class StudioCategory(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, unique=True, nullable=False)

    # One-to-many relationship
    products = relationship("StudioProduct", back_populates="category")


# Product model (items displayed in Search Results)
class StudioProduct(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    subcategory = Column(String, nullable=False)          
    price = Column(Float, nullable=False)           
    description = Column(String, nullable=True)    
    condition = Column(String, nullable=False)     
    financing_available = Column(Boolean, default=False)

    # Link to Category (Tech Devices, etc.)
    category_id = Column(Integer, ForeignKey("products.id"))
    category = relationship("StudioCategory", back_populates="products")

    # Device type within category (e.g., Smartphone, Laptop under Tech Devices)
    device_type = Column(String, nullable=True)


#for further payemnts and reservations
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from db import Base


# ------------------------
# ENUMS
# ------------------------
class PaymentStatus(enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"


# ------------------------
# STUDIO MODELS
# ------------------------

class StudioHouse(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    price_per_night = Column(Float, nullable=False)
    description = Column(String)

    reservations = relationship("StudioReservation", back_populates="house")


class StudioReservation(Base):
    __tablename__ = "studio_reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)   # Could be FK if you have user table
    house_id = Column(Integer, ForeignKey("studio_houses.id"))
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    is_confirmed = Column(Boolean, default=False)

    house = relationship("StudioHouse", back_populates="reservations")
    order = relationship("StudioOrder", back_populates="reservation", uselist=False)


class StudioOrder(Base):
    __tablename__ = "studio_orders"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("studio_reservations.id"))
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reservation = relationship("StudioReservation", back_populates="order")
    payment = relationship("StudioPayment", back_populates="order", uselist=False)


class StudioPayment(Base):
    __tablename__ = "studio_payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("studio_orders.id"))
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    transaction_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("StudioOrder", back_populates="payment")


    






