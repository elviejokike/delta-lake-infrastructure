import os

import logging
import sqlparse
import trino
from config import TRINO_CONFIG, MIGRATIONS_PATH

logger = logging.getLogger("migration")
logging.basicConfig(level=logging.INFO)

# Create Trino connection
def get_trino_connection():
    return trino.dbapi.connect(
        host=TRINO_CONFIG["host"],
        port=TRINO_CONFIG["port"],
        user=TRINO_CONFIG["user"],
        catalog=TRINO_CONFIG["catalog"],
        schema=TRINO_CONFIG["schema"],
    )

# Get applied migrations from Trino
def get_applied_migrations(cursor):
    cursor.execute("SELECT version FROM icebergnessie.test.schema_migrations")
    return {row[0] for row in cursor.fetchall()}

# Apply a migration file
def apply_migration(cursor, migration_file, version):
    print(f"Applying migration: {migration_file}")
    with open(migration_file, "r") as f:
        sql_content = f.read()
        statements = [stmt.strip().rstrip(";") for stmt in sqlparse.split(sql_content) if stmt.strip()]
        for statement in statements:
            logger.info(f"Executing: {statement}")
            cursor.execute(statement)

        cursor.execute(
            "INSERT INTO icebergnessie.test.schema_migrations (version, file) VALUES (?,?)", [version, migration_file]
        )

# Main migration function
def run_migrations():
    conn = get_trino_connection()
    cursor = conn.cursor()

    # Ensure the migrations table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS icebergnessie.test.schema_migrations (
            version VARCHAR,
            file VARCHAR,
            applied_at TIMESTAMP
        )
    """)

    applied_migrations = get_applied_migrations(cursor)

    # Sort migration files (ensures proper order)
    migration_files = sorted(os.listdir(MIGRATIONS_PATH))
    logger.info("List of found migration files" + str(migration_files))

    try:

        for file in migration_files:
            if file.endswith(".sql"):
                version = file.split("__")[0]  # Extract version from filename
                if version not in applied_migrations:
                    apply_migration(cursor, os.path.join(MIGRATIONS_PATH, file), version)
                    logger.info(version + " applied successfully ✅")
                else:
                    logger.info(version + " already applied ❌")

        logger.info("✅ All migrations applied successfully!")
    except Exception as e:
        logger.error("❌ DataMigrationFailed An error occurred while applying migrations")
        logger.error(e)

if __name__ == "__main__":
    run_migrations()