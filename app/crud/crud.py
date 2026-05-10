from sqlalchemy.orm import Session
from app.models import models
from app import schemas
from app.config.logger import get_logger

logger = get_logger("crud")

# customer
def get_customers_count(db:Session):
    logger.info("Executing count query for customers")
    return db.query(models.Customer).count()

# orders
def get_orders_count(db:Session):
    logger.info("Executing count query for orders")
    return db.query(models.Order).count()

# products
def get_products_count(db:Session):
    logger.info("Executing count query for products")
    return db.query(models.Product).count()

# employee
def get_employees_count(db:Session):
    logger.info("Executing count query for employees")
    return db.query(models.Employee).count()

# offices
def get_offices_count(db:Session):
    logger.info("Executing count query for offices")
    return db.query(models.Office).count()

# payments
def get_payments_count(db:Session):
    logger.info("Executing count query for payments")
    return db.query(models.Payment).count()

# order details
def get_orderdetails_count(db:Session):
    logger.info("Executing count query for order details")
    return db.query(models.OrderDetail).count()

# product lines
def get_productlines_count(db:Session):
    logger.info("Executing count query for product lines")
    return db.query(models.ProductLine).count()



def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers (skip={skip}, limit={limit})")
    return db.query(models.Customer).offset(skip).limit(limit).all()



def get_customer(db: Session, customer_id: int):
    logger.info(f"Searching customer ID: {customer_id}")
    return db.query(models.Customer).filter(
        models.Customer.customerNumber == customer_id
    ).first()



def create_customer(db: Session, customer: schemas.CustomerCreate):
    logger.info(f"Creating customer: {customer.customerName}")

    try:
        db_customer = models.Customer(**customer.model_dump())

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return db_customer

    except Exception as e:
        db.rollback()
        logger.error(f"Create customer failed: {e}")
        raise



def update_customer(db: Session, customer_id: int, updated_data: schemas.CustomerUpdate):
    logger.info(f"Updating customer ID: {customer_id}")

    db_customer = db.query(models.Customer).filter(
        models.Customer.customerNumber == customer_id
    ).first()

    if not db_customer:
        logger.warning(f"Customer not found: {customer_id}")
        return None

    update_dict = updated_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_customer, key, value)

    try:
        db.commit()
        db.refresh(db_customer)

        logger.info(f"Customer updated successfully: {customer_id}")
        return db_customer

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating customer {customer_id}: {e}")
        raise



def delete_customer(db: Session, customer_id: int):
    logger.info(f"Deleting customer ID: {customer_id}")

    db_customer = db.query(models.Customer).filter(
        models.Customer.customerNumber == customer_id
    ).first()

    if not db_customer:
        logger.warning(f"Customer not found: {customer_id}")
        return None

    try:
        db.delete(db_customer)
        db.commit()

        logger.info(f"Customer deleted successfully: {customer_id}")
        return db_customer

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting customer {customer_id}: {e}")
        raise
