from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Artisan(Base):
    __tablename__ = "artisans"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    state = Column(String, nullable=False)
    cluster = Column(String, nullable=False)
    craft_type = Column(String, nullable=False)
    scheme_id = Column(String, nullable=True) # PM Vishwakarma / PM-DAKSH
    created_at = Column(DateTime, default=datetime.utcnow)
    products = relationship("Product", back_populates="artisan")

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    artisan_id = Column(String, ForeignKey("artisans.id"), nullable=False)
    title_en = Column(String, nullable=False)
    title_hi = Column(String, nullable=False)
    craft_type = Column(String, nullable=False)
    material = Column(String, nullable=True)
    story_en = Column(Text, nullable=True)
    bullet_points = Column(Text, nullable=True)
    status = Column(String, default="PUBLISHED")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    artisan = relationship("Artisan", back_populates="products")
    media = relationship("ProductMedia", back_populates="product", uselist=False)
    pricing = relationship("ProductPricing", back_populates="product", uselist=False)

class ProductMedia(Base):
    __tablename__ = "product_media"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    original_url = Column(String, nullable=False)
    enhanced_studio_url = Column(String, nullable=False)
    product = relationship("Product", back_populates="media")

class ProductPricing(Base):
    __tablename__ = "product_pricing"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    cost_floor = Column(Float, nullable=False)
    recommended_retail_price = Column(Float, nullable=False)
    wholesale_b2b_price = Column(Float, nullable=False)
    guaranteed_labor_wage = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    product = relationship("Product", back_populates="pricing")

class B2BEnquiry(Base):
    __tablename__ = "b2b_enquiries"
    id = Column(String, primary_key=True, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    buyer_name = Column(String, nullable=False)
    organization = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    contact_email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
