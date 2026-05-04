from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE nurses ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT '123456';"))
        db.session.commit()
        print("Successfully added password column.")
    except Exception as e:
        print("Column may already exist or error occurred:", e)
