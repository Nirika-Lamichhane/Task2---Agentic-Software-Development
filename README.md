# ClassicModels: High-Performance Concurrent API

A professional-grade FastAPI implementation of the ClassicModels database. This project serves as a technical demonstration of **The Twelve-Factor App** methodology, specifically focusing on **Factor VIII (Concurrency)** and **Modularity**.

## 🚀 Features

* **Concurrent Data Aggregation**: Implements `asyncio.gather` and `run_in_threadpool` to query 8 different database tables simultaneously, drastically reducing response latency.
* **Twelve-Factor Architecture**: 
    * **Factor III (Config)**: Centralized configuration management for database connections.
    * **Factor VIII (Concurrency)**: Scale-out capability via asynchronous task coordination.
    * **Factor XI (Logs)**: Structured logging for deep observability and performance tracking.
* **Modular CRUD Layer**: Decoupled business logic where every database entity has independent operations, ensuring a clean and maintainable codebase.

## 🛠️ Tech Stack

* **Framework**: FastAPI (Python)
* **ORM**: SQLAlchemy
* **Database**: PostgreSQL
* **Concurrency**: Asyncio & Multi-threading
* **Containerization**: Docker & Docker Compose

## ⚙️ Installation & Setup (Docker Workflow)

1.  **Clone the Repository**:
    ```bash
    git clone <use this repo link>
    cd classicmodels-api
    ```

2.  **Database Seeding**:
    Ensure the `seed.sql` file is in your root directory. This script will automatically initialize the PostgreSQL schema and populate the tables when the container starts.

3.  **Launch with Docker Compose**:
    This command builds the FastAPI image and starts the PostgreSQL container:
    ```bash
    docker-compose up --build
    ```

4.  **Access the API**:
    * **Interactive Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * **Base URL**: `http://127.0.0.1:8000`

## 📊 Performance & Concurrency (Factor VIII)

The hallmark of this project is the `/overall_counts` endpoint.

### How it Works:
By utilizing `asyncio.gather`, the API triggers 8 queries in parallel. Instead of waiting for each count to finish one-by-one, the total response time is governed only by the single slowest query.

### Verification through Logs:
You can verify the concurrent execution in your Docker logs:
- `INFO: Starting 8 database tasks simultaneously...`
- `INFO: asyncio.gather() completed successfully`
- `INFO: Total response time for /overall_counts: 0.05xxs`

## 🛣️ API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/overall_counts` | **Aggregated concurrent count** of all tables. |
| `GET` | `/customers/count` | Individual customer count. |
| `GET` | `/customers/` | List all customers with pagination. |
| `POST` | `/customers/` | Create a new customer record. |
| `GET` | `/customers/{id}` | Retrieve specific customer details by ID. |

## 👨‍💻 Author
**Nirika Lamichhane** Engineering Student | IOE Thapathali Campus
