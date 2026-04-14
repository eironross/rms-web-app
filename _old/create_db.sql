CREATE DATABASE rms_db;

CREATE SCHEMA user_service;
CREATE SCHEMA report_service;
CREATE SCHEMA notification_service;
CREATE SCHEMA audit_service;
CREATE SCHEMA approval_service;

CREATE TABLE user_service.user_roles (
    id SERIAL  PRIMARY KEY,
    role VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NULL

);

INSERT INTO user_service.user_roles (role)
VALUES
   	('admin'),
	('manager'),
	('regulatory'),
	('trader');