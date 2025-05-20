# Customer Center - Backend System Detailed Design

## 1. Introduction

This document provides a detailed design of the backend system for the Customer Center, focusing on the database schema. It builds upon the requirements outlined in the [Product Requirements Document (PRD)](./prd.md).

The backend utilizes a PostgreSQL database with SQLAlchemy ORM for schema management and data access. The system is designed with a focus on scalability, maintainability, and integration with automation platforms like n8n.

## 2. Database Schema

The database is implemented using PostgreSQL with the following key features:
- UUID primary keys for distributed-friendly identifiers
- JSONB for flexible data storage
- Timestamps with timezone support
- Strategic indexing for performance
- SQLAlchemy ORM for type-safe database access

### 2.1. Table Overview

1. **`campaigns`**: Core table for managing outreach campaigns
2. **`organizations`**: Stores company information for leads
3. **`leads`**: Stores lead information and campaign associations

### 2.2. Table Definitions

#### 2.2.1. `campaigns` Table

* **Purpose**: Manages outreach campaigns
* **Columns**:
    * `campaign_id` (UUID, Primary Key) - Unique identifier
    * `name` (String, NOT NULL) - Campaign name
    * `description` (Text, NULLABLE) - Campaign description
    * `status` (String, NOT NULL) - Campaign status
    * `created_at` (DateTime with timezone) - Creation timestamp
    * `updated_at` (DateTime with timezone) - Last update timestamp
* **Relationships**:
    * One-to-many with `leads` table
* **Indexes**:
    * `idx_outreach_campaign_status` on `status`

#### 2.2.2. `organizations` Table

* **Purpose**: Stores company information
* **Columns**:
    * `organization_id` (UUID, Primary Key) - Unique identifier
    * `name` (String, NOT NULL) - Company name
    * `email_domain` (String, NOT NULL) - Company email domain
    * `external_id` (String, NULLABLE) - External system ID
    * `external_source` (String, NULLABLE) - Source system
    * `website_url` (String, NULLABLE) - Company website
    * `linkedin_url` (String, NULLABLE) - LinkedIn profile
    * `estimated_num_employees` (Integer, NULLABLE) - Company size
    * `website_summary_data` (JSONB, NULLABLE) - Processed website data
    * `website_raw_data` (JSONB, NULLABLE) - Raw website data
    * `country` (String, NULLABLE) - Company location
    * `language` (String, NULLABLE) - Primary language
    * `time_zone` (String, NULLABLE) - Company timezone
    * `source` (String, NULLABLE) - Data source
    * `formatted_organization_name` (String, NULLABLE) - Normalized name
    * `raw_address` (String, NULLABLE) - Company address
    * `created_at` (DateTime with timezone) - Creation timestamp
    * `updated_at` (DateTime with timezone) - Last update timestamp
* **Relationships**:
    * One-to-many with `leads` table
* **Indexes**:
    * `idx_outreach_organization_email_domain` on `email_domain`

#### 2.2.3. `leads` Table

* **Purpose**: Stores lead information and campaign associations
* **Columns**:
    * `lead_id` (UUID, Primary Key) - Unique identifier
    * `campaign_id` (UUID, Foreign Key) - Associated campaign
    * `company_id` (UUID, Foreign Key) - Associated organization
    * `first_name` (String, NULLABLE) - Lead's first name
    * `last_name` (String, NULLABLE) - Lead's last name
    * `email` (String, NOT NULL) - Lead's email address
    * `external_id` (String, NULLABLE) - External system ID
    * `title` (String, NULLABLE) - Job title
    * `headline` (String, NULLABLE) - Professional headline
    * `linkedin_url` (String, NULLABLE) - LinkedIn profile
    * `email_verification_status` (String, NULLABLE) - Email validation status
    * `email_verification_message` (String, NULLABLE) - Validation details
    * `email_icebreaker` (String, NULLABLE) - AI-generated icebreaker
    * `status` (String, NOT NULL) - Lead status
    * `language` (String, NULLABLE) - Preferred language
    * `source` (String, NULLABLE) - Lead source
    * `email_sent_at` (DateTime with timezone, NULLABLE) - Last email sent
    * `reply_received_at` (DateTime with timezone, NULLABLE) - Last reply received
    * `last_contacted_at` (DateTime with timezone, NULLABLE) - Last contact
    * `created_at` (DateTime with timezone) - Creation timestamp
    * `updated_at` (DateTime with timezone) - Last update timestamp
* **Relationships**:
    * Many-to-one with `campaigns` table
    * Many-to-one with `organizations` table
* **Indexes**:
    * `ix_leads_email` on `email`
    * `idx_outreach_lead_status` on `status`

## 3. Data Model Considerations

* **Scalability & Performance**:
    * Strategic indexing on frequently queried fields
    * JSONB for flexible data storage (website data, enrichment)
    * UUID primary keys for distributed-friendly identifiers
    * Timestamps with timezone for consistent time tracking

* **Integration Support**:
    * Schema designed to support n8n automation workflows
    * Status fields for workflow state management
    * External IDs for system integration
    * Flexible data storage for enrichment data

* **Data Quality**:
    * Email validation tracking
    * Source tracking for data provenance
    * Status tracking for campaign progress
    * Timestamps for activity tracking

## 4. Security Considerations

* **Data Access**:
    * SQLAlchemy ORM for safe query construction
    * Parameterized queries to prevent SQL injection
    * Type-safe database access through ORM models

* **Data Integrity**:
    * Foreign key constraints for referential integrity
    * NOT NULL constraints on required fields
    * Indexes for performance and data integrity

* **Configuration**:
    * Environment-based configuration
    * Secure database URL handling
    * Connection pooling through SQLAlchemy

## 5. Future Considerations

* **Multi-tenancy Implementation**:
    * Add tenant_id to all tables
    * Implement tenant isolation
    * Add tenant-specific API keys

* **User Management**:
    * Add users table
    * Implement role-based access control
    * Add authentication system

* **Email Management**:
    * Add outbound_emails table
    * Add email_replies table
    * Implement email tracking

* **Analytics**:
    * Add campaign performance metrics
    * Implement reporting views
    * Add data aggregation tables 