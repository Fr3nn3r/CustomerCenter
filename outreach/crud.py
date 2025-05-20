from sqlalchemy.orm import Session

from .models import Campaign, Organization, Lead


def create_campaign(session: Session, name: str, description: str, status: str = "draft") -> Campaign:
    """Create a new Campaign and persist it."""
    campaign = Campaign(name=name, description=description, status=status)
    session.add(campaign)
    session.commit()
    session.refresh(campaign)
    return campaign


def get_campaign_by_id(session: Session, campaign_id):
    """Retrieve a Campaign by its primary key."""
    return session.get(Campaign, campaign_id)


def create_organization(session: Session, **fields) -> Organization:
    """Create a new Organization using provided fields."""
    organization = Organization(**fields)
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization


def get_organization_by_domain(session: Session, domain: str) -> Organization | None:
    """Fetch an Organization by its email domain."""
    return session.query(Organization).filter_by(email_domain=domain).first()


def create_lead(session: Session, **fields) -> Lead:
    """Create a new Lead. Foreign keys must already exist."""
    lead = Lead(**fields)
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead


def get_leads_by_status(session: Session, status: str) -> list[Lead]:
    """Return all leads matching a status."""
    return session.query(Lead).filter_by(status=status).all()


def update_lead_status(session: Session, lead_id, new_status: str) -> Lead | None:
    """Update the status for a Lead."""
    lead = session.get(Lead, lead_id)
    if not lead:
        return None
    lead.status = new_status
    session.commit()
    session.refresh(lead)
    return lead
