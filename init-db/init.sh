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
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE report_service.status (
    id SERIAL  PRIMARY KEY,
    status_code VARCHAR(2) NOT NULL DEFAULT 'N/A',
    status_name VARCHAR(25) NOT NULL DEFAULT 'N/A',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE report_service.event_types (
    id SERIAL  PRIMARY KEY,
    event_code VARCHAR(2) NOT NULL DEFAULT 'N/A',
    event_name VARCHAR(25) NOT NULL DEFAULT 'N/A',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE report_service.operating_units (
    id SERIAL  PRIMARY KEY,
    resource_name VARCHAR(15) NOT NULL DEFAULT 'N/A',
    name VARCHAR(25) NOT NULL DEFAULT 'zzUnit test',
    facility_id INTEGER NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE approval_service.approval_hierarchy (
    id SERIAL PRIMARY KEY,
    status VARCHAR(100) NULL, 
    rolename VARCHAR(100) NULL,
    approval_level INTEGER NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE approval_service.approval_status (
    id SERIAL  PRIMARY KEY,
    status_name VARCHAR(100) NOT NULL DEFAULT 'N/A',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
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

INSERT INTO report_service.status(status_code, status_name)
VALUES
    ('NW', 'New'),
    ('PD', 'Pending'),
    ('DU', 'Due'),
    ('SD', 'Submitted');

INSERT INTO report_service.event_types(event_code, event_name)
VALUES
    ('SN', 'Synchronization'),
    ('FO', 'Force Outage'),
    ('PO', 'Planned Outage'),
    ('DN', 'Deration'),
    ('DM', 'Derating Maintenance');

INSERT INTO report_service.operating_units(resource_name, name, facility_id)
VALUES
    ('01FHRI_G01', 'Fontaine Renewable Unit 1', 54),
    ('01FHRI_G02', 'Fontaine Renewable Unit 2', 54),
    ('01FHRI_G03', 'Fontaine Renewable Unit 3', 54),
    ('01FHRI_G04', 'Fontaine Renewable Unit 4', 54);

INSERT INTO approval_service.approval_hierarchy(status, rolename, approval_level)
VALUES
    ('Rejected', NULL, -1),
    ('Return to Submitter', NULL, 0),
    ('Pending with the Senior Energy Trader', 'Senior Energy Trader', 1),
    ('Pending with the Team Leader', 'Team Leader', 2),
    ('Pending with the VP of the Market Operations', 'Vice President Market Operations', 3),
    ('Closed', NULL, 4);

INSERT INTO approval_service.approval_status(status_name)
VALUES
    ('New'),
    ('Completed'),
    ('Updated'),
    ('Rejected'),
    ('Return to Submitter');
EOSQL

