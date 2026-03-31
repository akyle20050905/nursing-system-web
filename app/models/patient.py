from app.extensions import db

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