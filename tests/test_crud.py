import os

# Configure database to use local SQLite file for testing before importing DB module
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from outreach.database import SessionLocal, engine
from outreach import crud, models
import pytest


@pytest.fixture(scope="function")
def session():
    # Start each test with a clean database
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_and_get_campaign(session):
    campaign = crud.create_campaign(session, "Test Campaign", "Testing...")
    fetched = crud.get_campaign_by_id(session, campaign.campaign_id)
    assert fetched is not None
    assert fetched.name == "Test Campaign"
    assert fetched.description == "Testing..."


def test_organization_crud(session):
    org = crud.create_organization(session, name="Acme Inc", email_domain="acme.com")
    fetched = crud.get_organization_by_domain(session, "acme.com")
    assert fetched is not None
    assert fetched.organization_id == org.organization_id
    assert fetched.name == "Acme Inc"


def test_lead_crud(session):
    campaign = crud.create_campaign(session, "Camp", "Desc")
    org = crud.create_organization(session, name="Org", email_domain="org.com")
    lead = crud.create_lead(
        session,
        campaign_id=campaign.campaign_id,
        company_id=org.organization_id,
        email="john@example.com",
        status="new",
    )

    leads = crud.get_leads_by_status(session, "new")
    assert len(leads) == 1
    assert leads[0].lead_id == lead.lead_id

    updated = crud.update_lead_status(session, lead.lead_id, "contacted")
    assert updated.status == "contacted"
    # Verify retrieval
    assert crud.get_leads_by_status(session, "contacted")[0].lead_id == lead.lead_id
