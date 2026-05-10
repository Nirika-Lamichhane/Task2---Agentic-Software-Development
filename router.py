from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
import crud, schemas, database
from logger import get_logger
import time
import asyncio
from fastapi.concurrency import run_in_threadpool
from database import SessionLocal


def get_count_safely(count_function):
    db = SessionLocal()

    try:
        return count_function(db)

    finally:
        db.close()

logger = get_logger("router")
router = APIRouter()

# --- TASK 3: INDIVIDUAL COUNT ENDPOINTS (MODULAR) ---
# NOTE: These are placed at the top to avoid path conflicts (like the 422 error)

@router.get("/customers/count")
def read_customers_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /customers/count")
    try:
        count = crud.get_customers_count(db)
        logger.info(f"Response Status: Success - Customers Count: {count}")
        return {"table": "customers", "count": count}
    except Exception as e:
        logger.error(f"Failed to fetch customer count: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/orders/count")
def read_orders_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /orders/count")
    count = crud.get_orders_count(db)
    return {"table": "orders", "count": count}

@router.get("/products/count")
def read_products_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /products/count")
    count = crud.get_products_count(db)
    return {"table": "products", "count": count}

@router.get("/employees/count")
def read_employees_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /employees/count")
    count = crud.get_employees_count(db)
    return {"table": "employees", "count": count}

@router.get("/offices/count")
def read_offices_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /offices/count")
    count = crud.get_offices_count(db)
    return {"table": "offices", "count": count}

@router.get("/payments/count")
def read_payments_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /payments/count")
    count = crud.get_payments_count(db)
    return {"table": "payments", "count": count}

@router.get("/orderdetails/count")
def read_orderdetails_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /orderdetails/count")
    count = crud.get_orderdetails_count(db)
    return {"table": "orderdetails", "count": count}

@router.get("/productlines/count")
def read_productlines_count(db: Session = Depends(database.get_db)):
    logger.info("Incoming Request: /productlines/count")
    count = crud.get_productlines_count(db)
    return {"table": "productlines", "count": count}


# --- TASK 3: AGGREGATED ENDPOINT (CONCURRENCY - FACTOR VIII) ---

@router.get("/overall_counts")
async def read_overall_counts():
    logger.info("Incoming Request: /overall_counts (Aggregated Dashboard)")
    start_time = time.time()

    # Define the tasks to be run in parallel
    logger.info("Starting 8 database tasks simultaneously...")
    tasks = [
    run_in_threadpool(get_count_safely, crud.get_customers_count),
    run_in_threadpool(get_count_safely, crud.get_orders_count),
    run_in_threadpool(get_count_safely, crud.get_products_count),
    run_in_threadpool(get_count_safely, crud.get_employees_count),
    run_in_threadpool(get_count_safely, crud.get_offices_count),
    run_in_threadpool(get_count_safely, crud.get_payments_count),
    run_in_threadpool(get_count_safely, crud.get_orderdetails_count),
    run_in_threadpool(get_count_safely, crud.get_productlines_count),
]

    # Execute all queries concurrently
    results = await asyncio.gather(*tasks)
    logger.info("asyncio.gather() completed successfully")

    total_duration = time.time() - start_time
    logger.info(f"Total response time for /overall_counts: {total_duration:.4f}s")

    return {
        "counts": {
            "customers": results[0],
            "orders": results[1],
            "products": results[2],
            "employees": results[3],
            "offices": results[4],
            "payments": results[5],
            "orderdetails": results[6],
            "productlines": results[7]
        },
        "performance": {
            "total_time": f"{total_duration:.4f}s",
            "method": "concurrent_processing"
        }
    }


# --- EXISTING CUSTOMER CRUD OPERATIONS ---

@router.get("/customers/", response_model=List[schemas.CustomerOut])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    logger.info("API Request: List Customers")
    return crud.get_customers(db, skip=skip, limit=limit)

@router.get("/customers/{customer_id}", response_model=schemas.CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"API Request: Get Customer {customer_id}")
    db_customer = crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Customer not found: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.post("/customers/", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    logger.info("API Request: Create Customer")
    return crud.create_customer(db=db, customer=customer)

@router.put("/customers/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(database.get_db)):
    logger.info(f"API Request: Update Customer {customer_id}")
    updated_customer = crud.update_customer(db, customer_id, customer)
    if updated_customer is None:
        logger.warning(f"Customer not found for update: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer

@router.delete("/customers/{customer_id}", response_model=schemas.CustomerOut)
def delete_customer(customer_id: int, db: Session = Depends(database.get_db)):
    logger.info(f"API Request: Delete Customer {customer_id}")
    deleted_customer = crud.delete_customer(db, customer_id)
    if deleted_customer is None:
        logger.warning(f"Customer not found for delete: {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return deleted_customer