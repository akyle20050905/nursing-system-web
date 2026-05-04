from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

sql = """
CREATE TABLE IF NOT EXISTS patient_status_history (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    patient_id INTEGER NOT NULL, 
    status VARCHAR(50) NOT NULL, 
    remark TEXT, 
    recorded_at DATETIME, 
    recorded_by INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(patient_id) REFERENCES patients (id) ON DELETE CASCADE, 
    FOREIGN KEY(recorded_by) REFERENCES nurses (id) ON DELETE SET NULL
);
"""

with app.app_context():
    try:
        db.session.execute(text(sql))
        db.session.commit()
        print("Table patient_status_history created successfully.")
    except Exception as e:
        print("Error:", e)
