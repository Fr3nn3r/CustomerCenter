
# 📦 Alembic Workflow & Best Practices

This document explains how to manage database schema changes using **Alembic**.

---

## 🚀 Why Use Alembic?

Alembic is a database migration tool that works with SQLAlchemy. It lets you:
- Track and apply schema changes safely
- Keep local, staging, and production DBs in sync
- Roll back changes if needed

---

## 🔧 Setup (One-Time)

1. Initialize Alembic in your project root:
   ```bash
   alembic init alembic
   ```

2. Edit `alembic.ini`:
   - Leave `sqlalchemy.url` empty (we'll set it dynamically from `.env`)

3. Edit `alembic/env.py`:
   - Load the DB URL from `.env` using `dotenv`
   - Import your Base metadata (`from outreach.models import Base`)
   - Replace `run_migrations_online()` with:

   ```python
   def run_migrations_online():
       connectable = create_engine(DATABASE_URL)
       with connectable.connect() as connection:
           context.configure(connection=connection, target_metadata=Base.metadata)
           with context.begin_transaction():
               context.run_migrations()
   ```

---

## 🔄 How to Create and Apply Migrations

1. ✅ Make changes in your `models.py` (e.g. add a new column)

2. ✅ Generate a new migration script:
   ```bash
   alembic revision --autogenerate -m "Describe your change here"
   ```

3. ✅ Apply the migration to your DB:
   ```bash
   alembic upgrade head
   ```

---

## 💡 Best Practices

| Rule | Why |
|------|-----|
| ✅ All schema changes must go through Alembic | Keeps schema consistent across environments |
| 🚫 Never manually edit old migration scripts | Avoid breaking environments already migrated |
| ✅ Use `--autogenerate` with each model change | Ensures Alembic reflects actual model state |
| ✅ Commit migration files to Git | Team members stay in sync |
| 🚫 Don't run manual SQL like `ALTER TABLE` | You’ll bypass Alembic tracking |

---

## 🧪 Example Workflow

1. Add a new field to `Lead` in `models.py`:
   ```python
   priority = Column(String, nullable=True)
   ```

2. Generate migration:
   ```bash
   alembic revision --autogenerate -m "Add priority to lead"
   ```

3. Apply migration:
   ```bash
   alembic upgrade head
   ```

---

## 🧼 Helpful Commands

- View history:
  ```bash
  alembic history
  ```

- Show current DB version:
  ```bash
  alembic current
  ```

- Downgrade one step:
  ```bash
  alembic downgrade -1
  ```

- Re-apply everything (for testing):
  ```bash
  alembic downgrade base
  alembic upgrade head
  ```

---

Happy migrating! 🧙‍♂️
