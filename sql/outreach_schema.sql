-- SQL migration to create outreach schema and tables
-- Uses UUID primary keys, jsonb for enrichment data
-- Safe to run in production; only creates schema and tables if they do not exist

-- Create schema
CREATE SCHEMA IF NOT EXISTS outreach;

-- campaign table
CREATE TABLE IF NOT EXISTS outreach.campaign (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- organization table
CREATE TABLE IF NOT EXISTS outreach.organization (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain TEXT NOT NULL,
    metadata JSONB,
    enrichment JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- lead table
CREATE TABLE IF NOT EXISTS outreach.lead (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES outreach.campaign(id),
    organization_id UUID NOT NULL REFERENCES outreach.organization(id),
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT,
    status TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Useful indexes
CREATE INDEX IF NOT EXISTS idx_outreach_campaign_status ON outreach.campaign(status);
CREATE INDEX IF NOT EXISTS idx_outreach_organization_domain ON outreach.organization(domain);
CREATE INDEX IF NOT EXISTS idx_outreach_lead_email ON outreach.lead(email);
CREATE INDEX IF NOT EXISTS idx_outreach_lead_status ON outreach.lead(status);

