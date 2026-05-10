from sqlalchemy import Column, Integer, String, TEXT, Numeric, ForeignKey, Date, SmallInteger
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True, autoincrement=True)

    customerName = Column(String(100), nullable=False)
    contactLastName = Column(String(100), nullable=False)
    contactFirstName = Column(String(100), nullable=False)

    phone = Column(String(30), nullable=False)

    addressLine1 = Column(String(255), nullable=False)

    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

class ProductLine(Base):
    __tablename__ = "productlines"
    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(TEXT)


class Product(Base):
    __tablename__ = "products"
    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(String(50), ForeignKey("productlines.productLine"), nullable=False)

class Office(Base):
    __tablename__ = "offices"
    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    employeeNumber = Column(Integer, primary_key=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    officeCode = Column(String(10), ForeignKey("offices.officeCode"), nullable=False)

class Payment(Base):
    __tablename__ = "payments"
    # Primary Key is composite in your SQL: ("customerNumber", "checkNumber")
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber = Column(String(50), primary_key=True)
    amount = Column(Numeric(10, 2), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    orderNumber = Column(Integer, primary_key=True)
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), nullable=False)

class OrderDetail(Base):
    __tablename__ = "orderdetails"
    # Primary Key is composite: ("orderNumber", "productCode")
    orderNumber = Column(Integer, ForeignKey("orders.orderNumber"), primary_key=True)
    productCode = Column(String(15), ForeignKey("products.productCode"), primary_key=True)
    

