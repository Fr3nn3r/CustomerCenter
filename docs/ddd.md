# Customer Center - Backend System Detailed Design

## 1. Introduction

This document provides a detailed design of the backend system for the Customer Center, focusing on the database schema. It builds upon the requirements outlined in the [Product Requirements Document (PRD)](./prd.md).

The backend will utilize a PostgreSQL database, with the schema managed and interacted with via SQLAlchemy in the application layer.

## 2. Database Schema

The database is designed with a multi-tenant architecture from the ground up. A `tenant_id` column in most tables ensures data isolation. PostgreSQL's features like `JSONB` will be used for flexible data storage.

### 2.1. Table Overview

1.  **`tenants`**: Stores information about each client/customer account using the platform.
2.  **`users`**: Stores user accounts, linked to a tenant.
3.  **`campaigns`**: Stores details of outreach campaigns, linked to a tenant and a user.
4.  **`leads`**: Stores lead information, linked to a tenant and a campaign.
5.  **`outbound_emails`**: Tracks each individual email scheduled or sent as part of a campaign.
6.  **`email_replies`**: Stores incoming replies to sent emails and their AI classification.

### 2.2. Table Definitions

#### 2.2.1. `tenants` Table

*   **Purpose**: Manages different customers/accounts (tenants) using the platform.
*   **Columns**:
    *   `tenant_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique identifier for the tenant.
    *   `name` (VARCHAR(255), NOT NULL) - Name of the tenant/customer company.
    *   `api_key_hash` (VARCHAR(255), UNIQUE, NULLABLE) - Hashed API key for programmatic tenant access.
    *   `plan_details` (JSONB, NULLABLE) - Tenant-specific subscription plan info or feature flags.
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Timestamp of tenant creation.
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - Timestamp of last update.
*   **Indexes**:
    *   `idx_tenants_api_key_hash` ON `api_key_hash` WHERE `api_key_hash` IS NOT NULL.

#### 2.2.2. `users` Table

*   **Purpose**: Stores information about users, associated with a specific tenant.
*   **Columns**:
    *   `user_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique identifier for the user.
    *   `tenant_id` (UUID, Foreign Key references `tenants(tenant_id)`, NOT NULL) - Links user to their tenant.
    *   `username` (VARCHAR(100), NOT NULL) - User's login name.
    *   `email` (VARCHAR(255), NOT NULL) - User's email address.
    *   `password_hash` (VARCHAR(255), NOT NULL) - Hashed password for security.
    *   `full_name` (VARCHAR(255), NULLABLE) - Full name of the user.
    *   `role` (VARCHAR(50), NOT NULL, DEFAULT 'member') - Role within their tenant (e.g., 'admin', 'manager', 'member').
    *   `is_active` (BOOLEAN, NOT NULL, DEFAULT TRUE).
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
*   **Constraints**:
    *   `uq_users_tenant_username` UNIQUE (`tenant_id`, `username`).
    *   `uq_users_tenant_email` UNIQUE (`tenant_id`, `email`).
*   **Indexes**:
    *   `idx_users_tenant_id` ON `tenant_id`.
    *   `idx_users_email` ON `email`.

#### 2.2.3. `campaigns` Table

*   **Purpose**: Stores details about each client acquisition campaign, linked to a tenant.
*   **Columns**:
    *   `campaign_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique identifier for the campaign.
    *   `tenant_id` (UUID, Foreign Key references `tenants(tenant_id)`, NOT NULL) - Links campaign to a tenant.
    *   `user_id` (UUID, Foreign Key references `users(user_id)`, NOT NULL) - The user who created/manages it.
    *   `name` (VARCHAR(255), NOT NULL) - Name of the campaign.
    *   `description` (TEXT, NULLABLE) - Detailed description of the campaign.
    *   `status` (VARCHAR(50), NOT NULL, DEFAULT 'draft') - E.g., 'draft', 'active', 'paused', 'completed', 'archived'.
    *   `settings` (JSONB, NULLABLE) - Campaign-specific configurations (e.g., AI parameters, sending schedules).
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
*   **Indexes**:
    *   `idx_campaigns_tenant_id` ON `tenant_id`.
    *   `idx_campaigns_user_id` ON `user_id`.
    *   `idx_campaigns_status` ON `status`.

#### 2.2.4. `leads` Table

*   **Purpose**: Stores information about each email lead, linked to a tenant and campaign.
*   **Columns**:
    *   `lead_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique identifier for this lead entry.
    *   `tenant_id` (UUID, Foreign Key references `tenants(tenant_id)`, NOT NULL) - Links lead to a tenant.
    *   `campaign_id` (UUID, Foreign Key references `campaigns(campaign_id)`, NOT NULL) - Associates lead with a specific campaign.
    *   `email_address` (VARCHAR(255), NOT NULL) - The lead's email address.
    *   `first_name` (VARCHAR(100), NULLABLE).
    *   `last_name` (VARCHAR(100), NULLABLE).
    *   `company_name` (VARCHAR(255), NULLABLE).
    *   `title` (VARCHAR(100), NULLABLE) - Job title.
    *   `custom_fields` (JSONB, NULLABLE) - Additional structured data for personalization.
    *   `source_description` (VARCHAR(255), NULLABLE) - How this lead was obtained.
    *   `lead_batch_id` (VARCHAR(100), NULLABLE) - Identifier for a batch import.
    *   `is_validated` (BOOLEAN, NOT NULL, DEFAULT FALSE) - If the email has been validated.
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
*   **Indexes**:
    *   `idx_leads_tenant_id_campaign_id` ON (`tenant_id`, `campaign_id`).
    *   `idx_leads_email_address` ON `email_address`.
    *   `idx_leads_is_validated` ON `is_validated`.

#### 2.2.5. `outbound_emails` Table

*   **Purpose**: Tracks each individual email scheduled, sent, or interacted with. Replaces `SentEmails`.
*   **Columns**:
    *   `outbound_email_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique ID for the email.
    *   `tenant_id` (UUID, Foreign Key references `tenants(tenant_id)`, NOT NULL).
    *   `campaign_id` (UUID, Foreign Key references `campaigns(campaign_id)`, NOT NULL).
    *   `lead_id` (UUID, Foreign Key references `leads(lead_id)`, NOT NULL).
    *   `parent_outbound_email_id` (UUID, Foreign Key references `outbound_emails(outbound_email_id)`, NULLABLE) - For follow-up sequences.
    *   `subject_actual` (TEXT, NOT NULL) - Final, personalized subject line.
    *   `body_actual` (TEXT, NOT NULL) - Final, AI-personalized email body.
    *   `status` (VARCHAR(50), NOT NULL, DEFAULT 'scheduled') - E.g., 'scheduled', 'pending_personalization', 'pending_send', 'sent', 'delivered', 'bounced', 'failed', 'opened', 'clicked'.
    *   `scheduled_send_time` (TIMESTAMP WITH TIME ZONE, NULLABLE) - When the email is/was scheduled.
    *   `actual_send_time` (TIMESTAMP WITH TIME ZONE, NULLABLE) - When the email was dispatched.
    *   `opened_at` (TIMESTAMP WITH TIME ZONE, NULLABLE) - Timestamp of first open.
    *   `clicked_at` (TIMESTAMP WITH TIME ZONE, NULLABLE) - Timestamp of first click.
    *   `error_message` (TEXT, NULLABLE) - If sending/delivery failed.
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
*   **Indexes**:
    *   `idx_outbound_emails_tenant_id_campaign_id` ON (`tenant_id`, `campaign_id`).
    *   `idx_outbound_emails_lead_id` ON `lead_id`.
    *   `idx_outbound_emails_status_scheduled_time` ON (`status`, `scheduled_send_time`) WHERE `status` IN ('scheduled', 'pending_send').
    *   `idx_outbound_emails_parent_id` ON `parent_outbound_email_id`.

#### 2.2.6. `email_replies` Table

*   **Purpose**: Stores incoming replies to sent emails and their AI classification.
*   **Columns**:
    *   `reply_id` (UUID, Primary Key, DEFAULT gen_random_uuid()) - Unique identifier for the reply.
    *   `tenant_id` (UUID, Foreign Key references `tenants(tenant_id)`, NOT NULL).
    *   `outbound_email_id` (UUID, Foreign Key references `outbound_emails(outbound_email_id)`, NOT NULL) - The original sent email.
    *   `lead_id` (UUID, Foreign Key references `leads(lead_id)`, NOT NULL) - The lead who replied.
    *   `reply_received_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP) - When the reply was received.
    *   `reply_subject` (TEXT, NULLABLE).
    *   `reply_body` (TEXT, NULLABLE).
    *   `ai_classification` (VARCHAR(100), NULLABLE) - E.g., 'positive_response', 'objection', 'unsubscribe'.
    *   `classification_confidence` (FLOAT, NULLABLE) - Confidence score from AI.
    *   `classified_at` (TIMESTAMP WITH TIME ZONE, NULLABLE) - When AI classification was performed.
    *   `created_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
    *   `updated_at` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT CURRENT_TIMESTAMP).
*   **Indexes**:
    *   `idx_email_replies_tenant_id_outbound_email_id` ON (`tenant_id`, `outbound_email_id`).
    *   `idx_email_replies_lead_id` ON `lead_id`.

## 3. Data Model Considerations

*   **Multi-Tenancy**: Implemented via a `tenant_id` discriminator column in all relevant tables. Application logic MUST enforce filtering by `tenant_id` for all queries to ensure data isolation.
*   **UUIDs as Primary Keys**: Using UUIDs (`gen_random_uuid()` in PostgreSQL) helps in distributed environments and prevents ID clashes if data from different sources/tenants were ever to be merged outside the strict tenancy model (though not planned).
*   **Timestamps**: All timestamps are stored `WITH TIME ZONE` to ensure consistency across different server/user timezones. `CURRENT_TIMESTAMP` is used for defaults.
*   **JSONB for Flexibility**: Fields like `tenants.plan_details`, `campaigns.settings`, and `leads.custom_fields` use `JSONB` for storing schemaless or evolving structured data.
*   **Scalability & Performance**:
    *   Strategic indexing is crucial (see specific indexes per table). Focus is on `tenant_id`, foreign keys, status fields used in WHERE clauses, and timestamps for range queries.
    *   The application layer should encourage batch operations for data ingestion (e.g., leads) and updates.
*   **n8n / Automation Integration**:
    *   The schema supports status-driven workflows (e.g., n8n polling for `outbound_emails.status = 'scheduled'`).
    *   `campaigns.settings` can store configurations that n8n workflows read.
    *   `tenants.api_key_hash` allows for secure, tenant-specific API access if an API layer is built.

## 4. Security Considerations

*   **Data Isolation**: Strict `tenant_id` filtering in all application queries is paramount.
*   **Sensitive Data**: Passwords (`users.password_hash`) and API keys (`tenants.api_key_hash`) must be stored hashed (e.g., using bcrypt or Argon2).
*   **SQL Injection**: Use of an ORM like SQLAlchemy with parameterized queries helps prevent SQL injection vulnerabilities.
*   **Least Privilege**: Database users connecting from the application should have the minimum necessary privileges. 