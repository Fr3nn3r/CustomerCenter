import logging
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

logger = logging.getLogger(__name__)


class TestBase(DeclarativeBase):
    """Base class for all test schema ORM models."""

    __abstract__ = True
    __table_args__ = {"schema": "test_schema"}


class TestCampaign(TestBase):
    __tablename__ = "campaigns"

    campaign_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    leads: Mapped[list["TestLead"]] = relationship(
        "TestLead", back_populates="campaign", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TestCampaign id={self.campaign_id} name={self.name}>"


class TestOrganization(TestBase):
    __tablename__ = "organizations"

    organization_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email_domain: Mapped[str] = mapped_column(String, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True)
    external_source: Mapped[str | None] = mapped_column(String, nullable=True)
    website_url: Mapped[str | None] = mapped_column(String, nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String, nullable=True)
    estimated_num_employees: Mapped[int | None] = mapped_column(Integer, nullable=True)
    website_summary_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    website_raw_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    country: Mapped[str | None] = mapped_column(String, nullable=True)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    time_zone: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    formatted_organization_name: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    raw_address: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    leads: Mapped[list["TestLead"]] = relationship(
        "TestLead", back_populates="organization", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TestOrganization id={self.organization_id} name={self.name}>"


class TestLead(TestBase):
    __tablename__ = "leads"

    lead_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    campaign_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("test_schema.campaigns.campaign_id"),
        nullable=False,
    )
    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("test_schema.organizations.organization_id"),
        nullable=False,
    )
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    external_id: Mapped[str | None] = mapped_column(String, nullable=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    headline: Mapped[str | None] = mapped_column(String, nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String, nullable=True)
    linkedin_data: Mapped[str | None] = mapped_column(String, nullable=True)
    email_verification_status: Mapped[str | None] = mapped_column(String, nullable=True)
    email_verification_message: Mapped[str | None] = mapped_column(
        String, nullable=True
    )
    email_icebreaker: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
    language: Mapped[str | None] = mapped_column(String, nullable=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    email_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    reply_received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_contacted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    campaign: Mapped[TestCampaign] = relationship(
        "TestCampaign", back_populates="leads"
    )
    organization: Mapped[TestOrganization] = relationship(
        "TestOrganization", back_populates="leads"
    )

    def __repr__(self) -> str:
        return f"<TestLead id={self.lead_id} email={self.email}>"
