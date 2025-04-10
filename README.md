# Digital Game Store

A full-stack application for a digital game store where users can browse items, make purchases, and view their purchase history. The backend handles API requests, webhook processing, and database management, while the frontend provides a user-friendly interface.

---

## Project Structure

```
digital-store/
├── backend/                # Backend application (FastAPI)
│   ├── app/                # Application code
│   │   ├── routes/         # API routes
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── main.py         # FastAPI entry point
│   │   ├── database.py     # Database configuration
│   │   ├── state.py        # WebSocket state management
│   ├── tests/              # Unit and integration tests
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Dockerfile for backend
│   ├── docker-compose.yml  # Backend-specific Docker Compose
├── frontend/               # Frontend application (Vue.js)
│   ├── src/                # Application code
│   │   ├── components/     # Vue components
│   │   ├── pages/          # Vue pages
│   │   ├── router.ts       # Vue Router configuration
│   │   ├── main.ts         # Vue entry point
│   ├── Dockerfile          # Dockerfile for frontend
│   ├── docker-compose.yml  # Frontend-specific Docker Compose
│   ├── package.json        # Node.js dependencies
├── scripts/                # Utility scripts
│   ├── simulate_webhook.py # Webhook simulation script
│   ├── Dockerfile          # Dockerfile for webhook simulator
├── docker-compose.yml      # Main Docker Compose file
├── docker-compose.base.yml # Base services (Redis, Postgres)
└── README.md               # Project documentation
```

---

## Prerequisites

- **Docker**: Ensure Docker is installed and running.
- **Node.js**: Required for frontend development (Node.js 20+ recommended).
- **Python**: Required for backend development (Python 3.9+ recommended).

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd digital-store
```

### 2. Build and Start the Application

Run the following command to build and start all services:

```bash
docker-compose up --build
```

This will start the following services:
- **Backend**: Accessible at `http://localhost:8000`
- **Frontend**: Accessible at `http://localhost:5173`
- **Redis**: Used for caching
- **Postgres**: Used for database storage
- **Webhook Simulator**: Simulates webhook requests

### 3. Create Sample Items

Run the following command to populate the database with sample items:

```bash
docker-compose exec backend python app/scripts/create_example_items.py
```

---

## How to Test

### 1. Backend Tests

Run the backend tests using the following command:

```bash
docker-compose -f backend/docker-compose.test.yml up --build
```

This will execute all unit and integration tests for the backend.

### 2. Frontend Development

To run the frontend in development mode:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## Webhook Simulation

The webhook simulator sends simulated payment notifications to the backend.

### Steps to Run the Webhook Simulator

1. Ensure the backend is running.
2. Start the webhook simulator:

```bash
docker-compose -f scripts/docker-compose.webhook.yml up --build
```

The simulator will send webhook requests to the backend every 3 seconds.

---

## API Endpoints

### Backend API

- **GET /api/items**: Retrieve all available items.
- **GET /api/purchases?user_id=<user_id>**: Retrieve purchases for a specific user.
- **POST /api/webhooks/payment**: Handle payment confirmation webhooks.

### WebSocket

- **ws://localhost:8000/ws**: WebSocket endpoint for real-time notifications.

---

## Environment Variables

### Backend

- `XSOLLA_WEBHOOK_SECRET`: Shared secret for webhook signature verification.
- `DATABASE_URL`: Database connection string.
- `REDIS_URL`: Redis connection string.

### Frontend

- `CHOKIDAR_USEPOLLING`: Enables polling for file changes during development.

---

## Troubleshooting

### Common Issues

1. **Docker Build Fails**:
   - Ensure all paths in Dockerfiles are correct.
   - Verify that required files (e.g., `requirements.txt`) exist in the build context.

2. **Database Connection Issues**:
   - Ensure the `DATABASE_URL` environment variable is correctly configured.
   - Check if the Postgres service is running.

3. **Webhook Signature Verification Fails**:
   - Verify that the `XSOLLA_WEBHOOK_SECRET` matches between the backend and simulator.

---

## Future Improvements

- Add pagination and filtering to API endpoints.
- Enhance frontend UI/UX.
- Implement CI/CD pipelines for automated testing and deployment.

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Xsolla Webhooks](https://developers.xsolla.com/webhooks/overview/)

---

## Database Table Structure

### Items Table
| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| `id`        | Integer | Primary key                    |
| `name`      | String  | Name of the item               |
| `description` | String | Description of the item        |
| `price`     | Float   | Price of the item              |

### Users Table
| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| `id`        | String  | Primary key (UUID)             |
| `username`  | String  | Unique username                |
| `password`  | String  | Hashed password                |

### Purchases Table
| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| `id`        | Integer | Primary key                    |
| `user_id`   | String  | Foreign key referencing `users` |
| `item_id`   | Integer | Foreign key referencing `items` |
| `timestamp` | DateTime| Timestamp of the purchase       |
| `order_id`  | String  | Unique order identifier         |

### Pending Purchases Table
| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| `id`        | Integer | Primary key                    |
| `user_id`   | String  | Foreign key referencing `users` |
| `item_id`   | Integer | Foreign key referencing `items` |
| `timestamp` | DateTime| Timestamp of the pending purchase |
| `order_id`  | String  | Unique order identifier         |