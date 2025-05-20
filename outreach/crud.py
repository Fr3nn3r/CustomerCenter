"""CRUD operations for Outreach tables."""

from sqlalchemy.orm import Session

from . import models


def create_campaign(session: Session, name: str, description: str | None, status: str = "draft") -> models.Campaign:
    """Create a new Campaign and return it."""
    campaign = models.Campaign(name=name, description=description, status=status)
    session.add(campaign)
    session.commit()
    session.refresh(campaign)
    return campaign


def get_campaign_by_id(session: Session, campaign_id):
    """Retrieve a Campaign by its ID."""
    return session.query(models.Campaign).filter(models.Campaign.campaign_id == campaign_id).first()


def create_organization(session: Session, **fields) -> models.Organization:
    """Create an Organization using provided fields."""
    org = models.Organization(**fields)
    session.add(org)
    session.commit()
    session.refresh(org)
    return org


def get_organization_by_domain(session: Session, domain: str):
    """Retrieve an Organization by its email domain."""
    return session.query(models.Organization).filter(models.Organization.email_domain == domain).first()


def create_lead(session: Session, **fields) -> models.Lead:
    """Create a Lead using provided fields."""
    lead = models.Lead(**fields)
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead


def get_leads_by_status(session: Session, status: str) -> list[models.Lead]:
    """Return all leads with the given status."""
    return session.query(models.Lead).filter(models.Lead.status == status).all()


def update_lead_status(session: Session, lead_id, new_status: str):
    """Update the status for a Lead and return the updated object."""
    lead = session.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()
    if lead:
        lead.status = new_status
        session.commit()
        session.refresh(lead)
    return lead
