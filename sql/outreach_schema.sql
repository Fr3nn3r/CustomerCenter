-- SQL migration to create outreach schema and tables
-- Uses UUID primary keys and jsonb enrichment data
-- Safe to run in production; only creates schema and tables if they do not exist

-- Create schema
CREATE SCHEMA IF NOT EXISTS outreach;

-- Campaign table
CREATE TABLE IF NOT EXISTS outreach.campaign (
    campaign_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Organization table
CREATE TABLE IF NOT EXISTS outreach.organization (
    organization_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email_domain TEXT,
    external_id TEXT,
    external_source TEXT,
    website_url TEXT,
    linkedin_url TEXT,
    estimated_num_employees INT,
    website_summary_data JSONB,
    website_raw_data JSONB,
    country TEXT,
    language TEXT,
    time_zone TEXT,
    source TEXT,
    formatted_organization_name TEXT,
    raw_address TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Lead table
CREATE TABLE IF NOT EXISTS outreach.lead (
    lead_id UUID PRIMARY KEY,
    campaign_id UUID REFERENCES outreach.campaign(campaign_id),
    company_id UUID REFERENCES outreach.organization(organization_id),
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    title TEXT,
    headline TEXT,
    linkedin_url TEXT,
    email_verification_status TEXT,
    email_verification_message TEXT,
    email_icebreaker TEXT,
    status TEXT,
    language TEXT,
    source TEXT,
    email_sent_at TIMESTAMP,
    reply_received_at TIMESTAMP,
    last_contacted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_outreach_lead_email ON outreach.lead(email);
CREATE INDEX IF NOT EXISTS idx_outreach_lead_status ON outreach.lead(status);
CREATE INDEX IF NOT EXISTS idx_outreach_campaign_status ON outreach.campaign(status);
CREATE INDEX IF NOT EXISTS idx_outreach_organization_email_domain ON outreach.organization(email_domain);
