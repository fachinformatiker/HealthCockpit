import os
from app import app, db
from sqlalchemy import text

def run_migration(sql):
    try:
        print(f"Running migration: {sql}")
        db.session.execute(text(sql))
        db.session.commit()
        print("Success")
    except Exception as e:
        db.session.rollback()
        print(f"Skipped/Error: {e}")

with app.app_context():
    cols = [
        ("fat_percentage", "FLOAT"), ("bmi", "FLOAT"), ("skeletal_muscle", "FLOAT"),
        ("muscle_mass", "FLOAT"), ("protein", "FLOAT"), ("bmr", "FLOAT"),
        ("fat_free_mass", "FLOAT"), ("subcutaneous_fat", "FLOAT"), ("visceral_fat", "FLOAT"),
        ("body_water", "FLOAT"), ("bone_mass", "FLOAT")
    ]
    for col_name, col_type in cols:
        run_migration(f"ALTER TABLE weight_entry ADD COLUMN IF NOT EXISTS {col_name} {col_type}")
    
    run_migration("ALTER TABLE medication ADD COLUMN IF NOT EXISTS unit VARCHAR(50)")
    run_migration("ALTER TABLE medication ADD COLUMN IF NOT EXISTS common_dose VARCHAR(100)")
    run_migration("ALTER TABLE profile ADD COLUMN IF NOT EXISTS target_weight FLOAT")
    
    db.create_all()
    print("Database initialization complete.")
