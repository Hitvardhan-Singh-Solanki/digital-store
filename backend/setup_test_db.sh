#!/bin/bash
# Wait for PostgreSQL to be ready
until psql "$DATABASE_URL" -c '\q' 2>/dev/null; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Create test database if it doesn’t exist
psql "$DATABASE_URL" -c "CREATE DATABASE digital_store_test;" || true

# Run pytest
exec pytest -v