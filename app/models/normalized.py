from sqlalchemy import Column, Date, Enum, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Sale(Base):
    __tablename__ = 'sale'
    id = Column('id', Integer, primary_key=True)
    product_id = Column('product_id', Integer, ForeignKey(
        "product.id"), nullable=False)
    product = relationship("Product")
    date_id = Column('date_id', Integer, ForeignKey("date.id"), nullable=False)
    date = relationship("Date")
    revenue = Column('revenue', Float, nullable=False)
    quantity = Column('quantity', Integer, nullable=False)
    gross_margin = Column('gross_margin', Float, nullable=False)

class Date(Base):
    __tablename__ = 'date'
    id = Column('id', Integer, primary_key=True)
    year = Column('year', Date, nullable=False)
    quarter = Column('quarter', Enum('1', '2', '3', '4'), nullable=False)
    __table_args__ = (UniqueConstraint('year', 'quarter', name='_year_quarter_uc'),)

class Country(Base):
    __tablename__ = 'country'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), unique=True, nullable=False)

class Product(Base):
    __tablename__ = 'product'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False)

class ProductLine(Base):
    __tablename__ = 'product_line'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False)

class ProductType(Base):
    __tablename__ = 'product_type'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False)

class OrderType(Base):
    __tablename__ = 'order_type'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False)

class RetailerType(Base):
    __tablename__ = 'retailer_type'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(250), nullable=False)
