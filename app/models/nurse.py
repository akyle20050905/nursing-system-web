from app.extensions import db
from datetime import datetime

class Nurse(db.Model):
    __tablename__ = "nurses"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False) # N1, N2...
    update_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 關聯：建立的任務與執行的任務
    created_tasks = db.relationship("Task", foreign_keys="Task.creator_id", back_populates="creator")
    executed_tasks = db.relationship("Task", foreign_keys="Task.executor_id", back_populates="executor")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "level": self.level,
            "update_date": self.update_date.isoformat() if self.update_date else None
        }

    def __repr__(self):
        return f"<Nurse {self.name}>"