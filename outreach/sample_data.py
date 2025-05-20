
from outreach.database import SessionLocal
from outreach.models import Campaign, Organization, Lead
import uuid
from datetime import datetime

def create_sample_data():
    session = SessionLocal()

    # Create campaigns
    camp1 = Campaign(
        campaign_id=uuid.uuid4(),
        name="Cold Email Blitz",
        description="January push to cold leads",
        status="draft",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    camp2 = Campaign(
        campaign_id=uuid.uuid4(),
        name="Swiss Law Outreach",
        description="Targeting law firms in Switzerland",
        status="active",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add_all([camp1, camp2])

    # Create organizations
    org1 = Organization(
        organization_id=uuid.uuid4(),
        name="Acme Corp",
        email_domain="acme.com",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    org2 = Organization(
        organization_id=uuid.uuid4(),
        name="Initech",
        email_domain="initech.io",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    org3 = Organization(
        organization_id=uuid.uuid4(),
        name="Stark Industries",
        email_domain="starkindustries.com",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    session.add_all([org1, org2, org3])

    # Create leads
    leads = [
        Lead(
            lead_id=uuid.uuid4(),
            campaign_id=camp1.campaign_id,
            company_id=org1.organization_id,
            first_name="Alice",
            last_name="Anderson",
            email="alice@acme.com",
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Lead(
            lead_id=uuid.uuid4(),
            campaign_id=camp1.campaign_id,
            company_id=org2.organization_id,
            first_name="Bob",
            last_name="Brown",
            email="bob@initech.io",
            status="emailed",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Lead(
            lead_id=uuid.uuid4(),
            campaign_id=camp1.campaign_id,
            company_id=org3.organization_id,
            first_name="Charlie",
            last_name="Chaplin",
            email="charlie@starkindustries.com",
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Lead(
            lead_id=uuid.uuid4(),
            campaign_id=camp2.campaign_id,
            company_id=org1.organization_id,
            first_name="Diana",
            last_name="Daniels",
            email="diana@acme.com",
            status="emailed",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        Lead(
            lead_id=uuid.uuid4(),
            campaign_id=camp2.campaign_id,
            company_id=org3.organization_id,
            first_name="Eve",
            last_name="Evans",
            email="eve@starkindustries.com",
            status="replied",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]
    session.add_all(leads)

    session.commit()
    print("✅ Sample data created successfully.")

if __name__ == "__main__":
    create_sample_data()
