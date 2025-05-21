"""
CLI script to create a new campaign and return its ID.
Usage: python cli/create_campaign.py "Campaign Name" "Campaign Description"
"""

import sys
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from outreach.database import SessionLocal
from outreach.crud import create_campaign

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_new_campaign(name: str, description: str) -> str:
    """
    Create a new campaign and return its ID.

    Args:
        name: Campaign name
        description: Campaign description

    Returns:
        str: The campaign ID
    """
    try:
        db = SessionLocal()
        campaign = create_campaign(db, name=name, description=description)
        logger.info(f"Created campaign: {campaign.name}")
        return str(campaign.campaign_id)
    except Exception as e:
        logger.error(f"Error creating campaign: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            'Usage: python cli/create_campaign.py "Campaign Name" "Campaign Description"'
        )
        sys.exit(1)

    name = sys.argv[1]
    description = sys.argv[2]

    try:
        campaign_id = create_new_campaign(name, description)
        print(f"Campaign created successfully!")
        print(f"Campaign ID: {campaign_id}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
