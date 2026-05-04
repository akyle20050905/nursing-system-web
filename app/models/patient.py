from app.extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    bed_number = db.Column(db.String(20), nullable=False) # 床號
    name = db.Column(db.String(100), nullable=False)
    medical_id = db.Column(db.String(50), unique=True, nullable=False) # 病歷號
    status = db.Column(db.String(50), default="穩定") 
    gender = db.Column(db.String(10)) # 性別
    age = db.Column(db.Integer) # 年齡
    diagnosis = db.Column(db.Text) # 主診斷
    
    # 一對多關聯：一個病人有多個任務
    tasks = db.relationship("Task", back_populates="patient", cascade="all, delete-orphan")
    
    # 關聯：狀態歷史紀錄
    status_history = db.relationship("PatientStatusHistory", back_populates="patient", cascade="all, delete-orphan", order_by="desc(PatientStatusHistory.recorded_at)")

    def to_dict(self):
        return {
            "id": self.id,
            "bed_number": self.bed_number,
            "name": self.name,
            "medical_id": self.medical_id,
            "status": self.status,
            "gender": self.gender,
            "age": self.age,
            "diagnosis": self.diagnosis
        }

class PatientStatusHistory(db.Model):
    __tablename__ = "patient_status_history"
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    remark = db.Column(db.Text, nullable=True)
    recorded_at = db.Column(db.DateTime, default=datetime.now)
    recorded_by = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=True)
    
    patient = db.relationship("Patient", back_populates="status_history")
    nurse = db.relationship("Nurse")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "remark": self.remark,
            "recorded_at": self.recorded_at.isoformat() if self.recorded_at else None,
            "recorded_by_name": self.nurse.name if self.nurse else "未知"
        }