from outreach.database import SessionLocal
from outreach import crud, models

def test_create_campaign():
    session = SessionLocal()
    campaign = crud.create_campaign(session, 'Test Campaign', 'A test')
    assert campaign.name == 'Test Campaign'
    session.close()
