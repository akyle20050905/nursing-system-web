from app.extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('High', 'Normal', 'Low', name='priority_enum'), default='Normal')
    status = db.Column(db.Enum('Pending', 'In_Progress', 'Completed', 'Abnormal', name='status_enum'), default='Pending')
    category = db.Column(db.String(50)) 
    processing_order = db.Column(db.Enum('Normal', 'First', 'Last', name='order_enum'), default='Normal')
    due_time = db.Column(db.DateTime)
    completed_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    handoff_summary = db.Column(db.Text, nullable=True)
    is_handed_over = db.Column(db.Boolean, default=False)
    next_executor_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=True) 

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=False)
    executor_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=True)

    patient = db.relationship("Patient", back_populates="tasks")
    creator = db.relationship("Nurse", foreign_keys=[creator_id], back_populates="created_tasks")
    executor = db.relationship("Nurse", foreign_keys=[executor_id], back_populates="executed_tasks")
    next_executor = db.relationship("Nurse", foreign_keys=[next_executor_id])

    def to_dict(self):
        """資深工程師修正：回傳更多欄位以便 UI 判斷"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "patient_bed": self.patient.bed_number if self.patient else "N/A",
            "patient_name": self.patient.name if self.patient else "Unknown",
            "content": self.content,
            "priority": self.priority,
            "status": self.status,
            "category": self.category,
            "due_time": self.due_time.strftime('%Y-%m-%d %H:%M') if self.due_time else None,
            "processing_order": self.processing_order,
            "handoff_summary": self.handoff_summary,
            "is_handed_over": self.is_handed_over,
            "executor_id": self.executor_id
        }