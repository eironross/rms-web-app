#!/bin/bash
set -e

# --- Configuration ---
DB_USER="admin"
DB_NAME="rms_db"

# Create schemas inside the new database
echo "Creating schemas in '$DB_NAME'..."

psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "postgres" -c "CREATE DATABASE $DB_NAME;"
psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    CREATE SCHEMA IF NOT EXISTS user_service;
    CREATE SCHEMA IF NOT EXISTS report_service;
    CREATE SCHEMA IF NOT EXISTS notification_service;
    CREATE SCHEMA IF NOT EXISTS approval_service;
    CREATE SCHEMA IF NOT EXISTS audit_service;
EOSQL

echo "Creating initial table in the db"
psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    CREATE TABLE user_service.user_roles (
    id SERIAL  PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NULL
);
EOSQL

echo "Inserting initial roles into '$DB_NAME'..."
psql -v ON_ERROR_STOP=1 -U "$DB_USER" -d "$DB_NAME" <<-EOSQL
    INSERT INTO user_service.user_roles (role)
    VALUES
        ('admin'),
        ('manager'),
        ('regulatory'),
        ('trader');
EOSQL

