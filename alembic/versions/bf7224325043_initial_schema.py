"""initial schema

Revision ID: bf7224325043
Revises: 
Create Date: 2025-03-30 00:01:30.652359

"""
from alembic import op
import sqlalchemy as sa
import csv
import os

# revision identifiers, used by Alembic.
revision = 'data_migration_001'
down_revision = 'bf7224325043' # Revision ID
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()

def load_csv_and_insert(table_name, csv_filename, columns):
    """
    Loads CSV data from the given file and inserts each row into the specified table.
    :param table_name: Name of the table in SQLite.
    :param csv_filename: CSV file exported from H2.
    :param columns: List of column names to read from the CSV.
    """
    if not os.path.exists(csv_filename):
        print(f"CSV file {csv_filename} not found!")
        return
        
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter only the required columns from the CSV row
            data = {col: row[col] for col in columns if col in row}
            # Build an INSERT statement with named parameters
            sql = sa.text(
                f"INSERT INTO {table_name} ({', '.join(data.keys())}) "
                f"VALUES ({', '.join(':' + key for key in data.keys())})"
            )
 
    # Migrate data for each table using the exported CSV files
    load_csv_and_insert(
        table_name="users",
        csv_filename="users.csv",
        columns=["id", "username", "hashed_password"]
    )
    load_csv_and_insert(
        table_name="exercises",
        csv_filename="exercises.csv",
        columns=["id", "name", "description", "difficulty", "is_public", "owner_id"]
    )
    load_csv_and_insert(
        table_name="favorites",
        csv_filename="favorites.csv",
        columns=["id", "user_id", "exercise_id"]
    )
    load_csv_and_insert(
        table_name="saved",
        csv_filename="saved.csv",
        columns=["id", "user_id", "exercise_id"]
    )
    load_csv_and_insert(
        table_name="ratings",
        csv_filename="ratings.csv",
        columns=["id", "user_id", "exercise_id", "rating"]
    )
    print("Data migration completed.")

def downgrade():
    connection = op.get_bind()
    # Remove all rows inserted during upgrade (for rollback purposes)
    for table in ["ratings", "saved", "favorites", "exercises", "users"]:
        connection.execute(sa.text(f"DELETE FROM {table}"))
    print("Data migration rolled back.")