import os
import uuid
import pytest

# Configure database URL before importing database module
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from outreach import models, crud
from outreach.database import SessionLocal, engine

# Ensure tables are created for tests
models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def session():
    # Start with a clean database for each test
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()


def test_create_and_get_campaign(session):
    campaign = crud.create_campaign(session, "Test Campaign", "Testing")
    fetched = crud.get_campaign_by_id(session, campaign.campaign_id)
    assert fetched is not None
    assert fetched.name == "Test Campaign"


def test_create_and_get_organization(session):
    org = crud.create_organization(session, name="Acme Inc.", email_domain="acme.com")
    fetched = crud.get_organization_by_domain(session, "acme.com")
    assert fetched is not None
    assert fetched.organization_id == org.organization_id


def test_create_lead_and_query(session):
    camp = crud.create_campaign(session, "Camp", "desc")
    org = crud.create_organization(session, name="Org", email_domain="org.com")
    lead = crud.create_lead(
        session,
        campaign_id=camp.campaign_id,
        company_id=org.organization_id,
        email="user@org.com",
        status="new",
    )
    leads = crud.get_leads_by_status(session, "new")
    assert len(leads) == 1
    assert leads[0].lead_id == lead.lead_id


def test_update_lead_status(session):
    camp = crud.create_campaign(session, "Camp2", "desc")
    org = crud.create_organization(session, name="Org2", email_domain="org2.com")
    lead = crud.create_lead(
        session,
        campaign_id=camp.campaign_id,
        company_id=org.organization_id,
        email="jane@org2.com",
        status="new",
    )
    updated = crud.update_lead_status(session, lead.lead_id, "contacted")
    assert updated.status == "contacted"
    leads = crud.get_leads_by_status(session, "contacted")
    assert len(leads) == 1
    assert leads[0].lead_id == lead.lead_id
