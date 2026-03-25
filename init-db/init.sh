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

CREATE TABLE report_service.status (
    id SERIAL  PRIMARY KEY,
    status_code VARCHAR(2) NOT NULL,
    status_name VARCHAR(25) NOT NULL
    is_active BOOLEAN
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE report_service.event_types (
    id SERIAL  PRIMARY KEY,
    event_code VARCHAR(2) NOT NULL,
    event_name VARCHAR(25) NOT NULL
    is_active BOOLEAN
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

INSERT INTO  report_service.status(status_code, status_name)
VALUES
    ('NW', 'New'),
    ('PD', 'Pending'),
    ('DU', 'Due'),
    ('SD', 'Submitted');

INSERT INTO  report_service.event_types(event_code, event_name)
VALUES
    ('SN', 'Synchronization'),
    ('FO', 'Fore Outage'),
    ('PO', 'Planned Outage'),
    ('DN', 'Deration'),
    ('DM', 'Derating Maintenance');
EOSQL

