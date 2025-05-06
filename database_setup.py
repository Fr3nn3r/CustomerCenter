import sqlalchemy
from sqlalchemy import (
    create_engine,
    Column,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Text,
    Index,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import (
    func as sqlfunc,
)  # Import func from sqlalchemy.sql for server-side defaults like CURRENT_TIMESTAMP

import uuid  # For client-side default UUIDs if needed, though server-side is preferred for PG

# Database connection URL (replace with your actual connection string)
# Example: "postgresql://user:password@host:port/database"
DATABASE_URL = "postgresql://user:password@localhost/customer_center_db"

Base = declarative_base()

# --- Table Definitions ---


class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    name = Column(String(255), nullable=False)
    api_key_hash = Column(
        String(255), unique=True, nullable=True
    )  # Store hashed API keys
    plan_details = Column(JSONB, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    users = relationship("User", back_populates="tenant")
    campaigns = relationship("Campaign", back_populates="tenant")
    leads = relationship("Lead", back_populates="tenant")
    outbound_emails = relationship("OutboundEmail", back_populates="tenant")
    email_replies = relationship("EmailReply", back_populates="tenant")

    __table_args__ = (
        Index(
            "idx_tenants_api_key_hash",
            "api_key_hash",
            unique=True,
            postgresql_where=api_key_hash.isnot(None),
        ),
    )

    def __repr__(self):
        return f"<Tenant(tenant_id={self.tenant_id}, name='{self.name}')>"


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False
    )
    username = Column(String(100), nullable=False)
    email = Column(
        String(255), nullable=False
    )  # Consider adding index if frequently queried directly
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(
        String(50), nullable=False, default="member"
    )  # E.g., 'admin', 'manager', 'member'
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    campaigns_created = relationship("Campaign", back_populates="creator")

    __table_args__ = (
        UniqueConstraint("tenant_id", "username", name="uq_users_tenant_username"),
        UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),
        Index("idx_users_tenant_id", "tenant_id"),
        Index("idx_users_email", "email"),  # Added for potential direct email lookups
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', tenant_id={self.tenant_id})>"


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )  # User who created the campaign
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        String(50), nullable=False, default="draft"
    )  # E.g., 'draft', 'active', 'paused', 'completed'
    settings = Column(JSONB, nullable=True)  # For AI params, schedule hints, etc.
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="campaigns")
    creator = relationship("User", back_populates="campaigns_created")
    leads = relationship("Lead", back_populates="campaign")
    outbound_emails = relationship("OutboundEmail", back_populates="campaign")

    __table_args__ = (
        Index("idx_campaigns_tenant_id", "tenant_id"),
        Index("idx_campaigns_user_id", "user_id"),
        Index("idx_campaigns_status", "status"),
    )

    def __repr__(self):
        return f"<Campaign(campaign_id={self.campaign_id}, name='{self.name}')>"


class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False
    )
    campaign_id = Column(
        UUID(as_uuid=True), ForeignKey("campaigns.campaign_id"), nullable=False
    )
    email_address = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company_name = Column(String(255), nullable=True)
    title = Column(String(100), nullable=True)
    custom_fields = Column(JSONB, nullable=True)
    source_description = Column(String(255), nullable=True)
    lead_batch_id = Column(String(100), nullable=True)
    is_validated = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="leads")
    campaign = relationship("Campaign", back_populates="leads")
    outbound_emails = relationship("OutboundEmail", back_populates="lead")
    email_replies = relationship("EmailReply", back_populates="lead")

    __table_args__ = (
        Index("idx_leads_tenant_id_campaign_id", "tenant_id", "campaign_id"),
        Index("idx_leads_email_address", "email_address"),
        Index("idx_leads_is_validated", "is_validated"),
    )

    def __repr__(self):
        return f"<Lead(lead_id={self.lead_id}, email='{self.email_address}')>"


class OutboundEmail(Base):
    __tablename__ = "outbound_emails"

    outbound_email_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False
    )
    campaign_id = Column(
        UUID(as_uuid=True), ForeignKey("campaigns.campaign_id"), nullable=False
    )
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.lead_id"), nullable=False)
    parent_outbound_email_id = Column(
        UUID(as_uuid=True),
        ForeignKey("outbound_emails.outbound_email_id"),
        nullable=True,
    )

    subject_actual = Column(Text, nullable=False)
    body_actual = Column(Text, nullable=False)
    status = Column(
        String(50), nullable=False, default="scheduled"
    )  # 'scheduled', 'pending_send', 'sent', 'delivered', 'bounced', 'failed', 'opened', 'clicked'
    scheduled_send_time = Column(DateTime(timezone=True), nullable=True)
    actual_send_time = Column(DateTime(timezone=True), nullable=True)
    opened_at = Column(DateTime(timezone=True), nullable=True)
    clicked_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="outbound_emails")
    campaign = relationship("Campaign", back_populates="outbound_emails")
    lead = relationship("Lead", back_populates="outbound_emails")
    replies = relationship("EmailReply", back_populates="original_email")

    # Self-referential relationship for follow-ups
    parent_email = relationship(
        "OutboundEmail", remote_side=[outbound_email_id], backref="follow_up_emails"
    )

    __table_args__ = (
        Index("idx_outbound_emails_tenant_id_campaign_id", "tenant_id", "campaign_id"),
        Index("idx_outbound_emails_lead_id", "lead_id"),
        Index(
            "idx_outbound_emails_status_scheduled_time",
            "status",
            "scheduled_send_time",
            postgresql_where=sqlalchemy.text("status IN ('scheduled', 'pending_send')"),
        ),
        Index("idx_outbound_emails_parent_id", "parent_outbound_email_id"),
    )

    def __repr__(self):
        return f"<OutboundEmail(outbound_email_id={self.outbound_email_id}, lead_id={self.lead_id}, status='{self.status}')>"


class EmailReply(Base):
    __tablename__ = "email_replies"

    reply_id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=sqlfunc.gen_random_uuid()
    )
    tenant_id = Column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False
    )
    outbound_email_id = Column(
        UUID(as_uuid=True),
        ForeignKey("outbound_emails.outbound_email_id"),
        nullable=False,
    )
    lead_id = Column(
        UUID(as_uuid=True), ForeignKey("leads.lead_id"), nullable=False
    )  # Denormalized for easier access, but linked through outbound_email

    reply_received_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    reply_subject = Column(Text, nullable=True)
    reply_body = Column(Text, nullable=True)
    ai_classification = Column(String(100), nullable=True)
    classification_confidence = Column(sqlalchemy.Float, nullable=True)
    classified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=sqlfunc.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=sqlfunc.now(),
        onupdate=sqlfunc.now(),
        nullable=False,
    )

    # Relationships
    tenant = relationship("Tenant", back_populates="email_replies")
    original_email = relationship("OutboundEmail", back_populates="replies")
    lead = relationship("Lead", back_populates="email_replies")

    __table_args__ = (
        Index(
            "idx_email_replies_tenant_id_outbound_email_id",
            "tenant_id",
            "outbound_email_id",
        ),
        Index("idx_email_replies_lead_id", "lead_id"),
    )

    def __repr__(self):
        return f"<EmailReply(reply_id={self.reply_id}, original_email_id={self.outbound_email_id})>"


# --- Main script to create tables ---
def create_tables(engine):
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created (if they didn't exist).")


if __name__ == "__main__":
    # This is just an example. In a real application, you would get the
    # DATABASE_URL from environment variables or a config file.
    print(f"Attempting to connect to database: {DATABASE_URL}")

    # For PostgreSQL, ensure the database exists before running this script.
    # You might need to create it manually: CREATE DATABASE customer_center_db;
    try:
        engine = create_engine(DATABASE_URL)

        # Test connection (optional, but good for immediate feedback)
        with engine.connect() as connection:
            print("Successfully connected to the database.")

        create_tables(engine)

        # Example of how to create a session and add some data (optional)
        # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # db = SessionLocal()
        # try:
        #     # Add sample data here if needed for testing
        #     # new_tenant = Tenant(name="Test Tenant Inc.")
        #     # db.add(new_tenant)
        #     # db.commit()
        #     # print(f"Added tenant: {new_tenant}")
        #     pass
        # finally:
        #     db.close()

    except sqlalchemy.exc.OperationalError as e:
        print(f"Error connecting to the database or database does not exist: {e}")
        print("Please ensure PostgreSQL is running and the database exists.")
        print(f"DATABASE_URL used: {DATABASE_URL}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
