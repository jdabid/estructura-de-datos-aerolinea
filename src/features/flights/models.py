from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.shared.database import Base

class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    tax_amount = Column(Float, default=0.0)
    is_promotion = Column(Boolean, default=False) # Para el descuento del 10%
    allows_pets = Column(Boolean, default=True)  # Nuevo campo para validación

    flights = relationship("Flight", back_populates="destination")

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True)
    origin = Column(String)
    base_price = Column(Float)
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    destination = relationship("Destination", back_populates="flights")