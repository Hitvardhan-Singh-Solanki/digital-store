# Digital Game Store

A full-stack application for a digital game store where users can browse items, make purchases, and receive real-time purchase notifications. The backend handles API requests, secure webhook processing, and database management, while the frontend provides a modern, reactive user interface.

---

## Table of Contents

- [Digital Game Store](#digital-game-store)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Architecture Overview](#architecture-overview)
  - [Project Structure](#project-structure)
  - [Setup \& Installation](#setup--installation)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Items](#items)
    - [Purchases](#purchases)
    - [Webhooks](#webhooks)
    - [WebSocket](#websocket)
  - [Database relations](#database-relations)
  - [Architecture flow](#architecture-flow)
  - [Testing](#testing)
    - [Backend Tests](#backend-tests)
    - [Frontend Testing](#frontend-testing)
  - [Environment Variables](#environment-variables)
    - [Backend (.env)](#backend-env)
    - [Frontend](#frontend)
  - [Troubleshooting](#troubleshooting)
  - [Future Improvements](#future-improvements)
  - [References](#references)

---

## Features

- **User Management**: Register, login, and manage user accounts.
- **Item Catalog**: Browse, search, and buy digital game items.
- **Real-Time Notifications**: WebSocket-based notifications for successful purchases.
- **Secure Payments and Webhooks**: HMAC-based webhook verification and asynchronous payment intent processing.
- **Database Integration**: PostgreSQL for persistent data and SQLAlchemy ORM.
- **Caching**: Redis caching to optimize item retrieval performance.

---

## Architecture Overview

- **Backend:** Built with FastAPI. Implements RESTful endpoints, webhook processing, and WebSocket communication.
- **Frontend:** Developed in Vue.js with Vite. Provides a reactive SPA with state management and routing.
- **Payment Simulation:** A dedicated microservice that simulates third-party payment confirmations via webhooks.
- **Data Storage:** PostgreSQL for relational data and Redis for caching.
- **Containerization:** All services are containerized using Docker and coordinated with Docker Compose.

---

## Project Structure

```
digital-store/
├── backend/                
│   ├── app/                
│   │   ├── routes/         # API routes (items, purchases, users, webhooks)
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── main.py         # FastAPI application entry point
│   │   ├── database.py     # Database configuration and Redis setup
│   │   ├── state.py        # WebSocket state management
│   │   └── payment/        # Payment module (async payment intent processing)
│   ├── tests/              # Unit and integration tests for backend
│   ├── requirements.txt    
│   ├── Dockerfile          
│   └── docker-compose.yml  
├── frontend/               
│   ├── src/                
│   │   ├── components/     # Vue components
│   │   ├── pages/          # Page components
│   │   ├── router.ts       # Vue Router configuration
│   │   ├── main.ts         # Vue application entry point
│   ├── package.json        
│   ├── Dockerfile          
│   └── docker-compose.yml  
├── scripts/                
│   ├── simulate_webhook.py # Script to simulate payment webhooks
│   ├── Dockerfile          # Dockerfile for webhook simulator
│   └── docker-compose.yml  # Docker Compose for webhook simulator
├── docker-compose.yml      # Main Docker Compose file orchestrating all services
├── docker-compose.base.yml # Base services (Redis, Postgres)
└── README.md               
```

---

## Setup & Installation

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.9+ (for backend development)
- Git

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Hitvardhan-Singh-Solanki/digital-store
   cd digital-store
   ```

2. **Configure Environment Variables**

   Create a `.env` file in the `backend` folder with:
   ```bash
   DATABASE_URL=postgresql://postgres:postgres@postgres:5432/digital_store
   REDIS_URL=redis://redis:6379/0
   XSOLLA_WEBHOOK_SECRET=your_secure_secret_here
   ```

   Ensure the `scripts/.env` file contains:
   ```bash
   XSOLLA_WEBHOOK_SECRET=your_secure_secret_here
   ```

3. **Build and Run the Application**

   ```bash
   docker-compose up --build
   ```

   This starts all services:
   - **Backend** at `http://localhost:8000`
   - **Frontend** at `http://localhost:5173`
   - **Redis** and **Postgres**
   - **Webhook Simulator** (sends simulated payment notifications)

4. **Populate Sample Data**

   ```bash
   docker-compose exec backend python app/scripts/create_example_items.py
   ```

---

## Usage

- **Access Frontend**: http://localhost:5173
- **Access Backend API**: http://localhost:8000
- **WebSocket Endpoint**: ws://localhost:8000/ws

---

## API Endpoints

### Authentication
- **POST** `/api/users`: Create a new user.
- **POST** `/api/users/login`: Login a user.

### Items
- **GET** `/api/items`: Retrieve a list of available items.
- **POST** `/api/items`: Create a new game item.

### Purchases
- **GET** `/api/purchases?user_id=<user_id>`: Retrieve purchases for a specific user.
- **POST** `/api/purchases`: Initiate a purchase.

### Webhooks
- **POST** `/api/webhooks/payment`: Endpoint to receive payment confirmation webhooks.

### WebSocket
- **WS** `/ws`: Receive real-time notification messages.

---

## Database relations

![Mermaid](image.png)

---

## Architecture flow

![Mermaid](image-1.png)

---

## Testing

### Backend Tests

Run tests via Docker Compose:

```bash
docker-compose -f backend/docker-compose.test.yml up --build
```

### Frontend Testing

For local frontend tests:

```bash
cd frontend
npm run test
```

---

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string.
- `REDIS_URL`: Redis connection URL.
- `XSOLLA_WEBHOOK_SECRET`: Secret used for HMAC webhook signature verification.

### Frontend
- `CHOKIDAR_USEPOLLING`: Set to `true` to enable file polling for hot reloading during development.

---

## Troubleshooting

- **Docker Build Issues**: Verify file paths and environment variable files.
- **Database Connection**: Ensure the `DATABASE_URL` variable is correct.
- **Webhook Signature Fails**: Confirm the `XSOLLA_WEBHOOK_SECRET` matches across backend and scripts.
- **Clearing Cache**:
  ```bash
  docker-compose exec redis redis-cli FLUSHALL
  ```

- **Rebuild Services**:
  ```bash
  docker-compose up --build --force-recreate
  ```

---

## Future Improvements

- Add pagination and filters to API endpoints.
- Enhance frontend UI/UX with more detailed product views and animations.
- Implement CI/CD pipelines for automated testing and deployment.
- Improve logging and monitoring across services.

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Xsolla Webhooks](https://developers.xsolla.com/webhooks/overview/)