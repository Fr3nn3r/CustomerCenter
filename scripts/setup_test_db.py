"""
Script to set up the test database schema and populate it with sample data.
Run this script to initialize your test database with sample data.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from outreach import models
from outreach.crud import create_campaign, create_organization, create_lead
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test database configuration
TEST_DATABASE_URL = (
    "postgresql+psycopg2://owluser:owlsrock@localhost:5432/owlai_test_db"
)


def setup_test_database():
    """Set up the test database schema and populate it with sample data."""
    try:
        # Create engine and session
        engine = create_engine(TEST_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        # Create all tables
        logger.info("Creating database tables...")
        models.Base.metadata.drop_all(bind=engine)  # Drop existing tables
        models.Base.metadata.create_all(bind=engine)

        # Create a session
        db = SessionLocal()

        try:
            # Create sample campaigns
            logger.info("Creating sample campaigns...")
            campaign1 = create_campaign(
                db, "Q1 Outreach", "First quarter outreach campaign"
            )
            campaign2 = create_campaign(
                db, "Enterprise Focus", "Targeting enterprise companies"
            )

            # Create sample organizations
            logger.info("Creating sample organizations...")
            org1 = create_organization(
                db,
                name="TechCorp Inc",
                email_domain="techcorp.com",
                website_url="https://techcorp.com",
                linkedin_url="https://linkedin.com/company/techcorp",
            )
            org2 = create_organization(
                db,
                name="DataFlow Systems",
                email_domain="dataflow.com",
                website_url="https://dataflow.com",
                linkedin_url="https://linkedin.com/company/dataflow",
            )

            # Create sample leads
            logger.info("Creating sample leads...")
            lead1 = create_lead(
                db,
                campaign_id=campaign1.campaign_id,
                company_id=org1.organization_id,
                email="john.doe@techcorp.com",
                first_name="John",
                last_name="Doe",
                title="CTO",
                status="new",
            )

            lead2 = create_lead(
                db,
                campaign_id=campaign1.campaign_id,
                company_id=org2.organization_id,
                email="jane.smith@dataflow.com",
                first_name="Jane",
                last_name="Smith",
                title="VP of Engineering",
                status="contacted",
            )

            lead3 = create_lead(
                db,
                campaign_id=campaign2.campaign_id,
                company_id=org1.organization_id,
                email="bob.wilson@techcorp.com",
                first_name="Bob",
                last_name="Wilson",
                title="CEO",
                status="new",
            )

            # Commit all changes
            db.commit()
            logger.info("Sample data created successfully!")

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating sample data: {e}")
            raise
        finally:
            db.close()

    except Exception as e:
        logger.error(f"Error setting up test database: {e}")
        raise


if __name__ == "__main__":
    setup_test_database()
