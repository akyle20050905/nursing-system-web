from app.extensions import db
from app.models.nurse import Nurse
from app.models.patient import Patient
from app.models.task import Task
from datetime import datetime, timedelta

def create_nurse(name, department, level, password="123456"):
    """新增護理師"""
    try:
        nurse = Nurse(name=name, department=department, level=level, password=password)
        db.session.add(nurse)
        db.session.commit()
        return nurse
    except Exception as e:
        db.session.rollback()
        print(f"Error creating nurse: {e}")
        return None

def get_all_nurses():
    """取得所有護理師"""
    return Nurse.query.all()

def get_nurse_by_id(nurse_id):
    """透過 ID 取得單一護理師"""
    return db.session.get(Nurse, nurse_id)

def login_nurse(nurse_id, password):
    """護理師登入驗證"""
    nurse = db.session.get(Nurse, nurse_id)
    if nurse and nurse.password == password:
        return nurse
    return None

def update_nurse(nurse_id, name=None, department=None, level=None):
    """更新護理師資料"""
    try:
        nurse = db.session.get(Nurse, nurse_id)
        if not nurse:
            return None
        if name: nurse.name = name
        if department: nurse.department = department
        if level: nurse.level = level
        db.session.commit()
        return nurse
    except Exception as e:
        db.session.rollback()
        return None

def delete_nurse(nurse_id):
    """刪除護理師"""
    try:
        nurse = db.session.get(Nurse, nurse_id)
        if not nurse:
            return None
        db.session.delete(nurse)
        db.session.commit()
        return nurse
    except Exception as e:
        db.session.rollback()
        return None

def seed_hospital_data():
    """
    初始資料植入 (Seed)
    """
    try:
        # 1. 檢查並植入護理師
        if Nurse.query.count() == 0:
            n1 = Nurse(name="王小美", department="ICU", level="N2", password="123456")
            n2 = Nurse(name="陳雅婷", department="ER", level="N3", password="123456")
            db.session.add_all([n1, n2])
            db.session.flush()

            # 2. 檢查並植入病人
            if Patient.query.count() == 0:
                p1 = Patient(
                    bed_number="701-1", 
                    name="張大山", 
                    medical_id="A123", 
                    status="穩定", 
                    gender="男", 
                    age=65, 
                    diagnosis="肺炎"
                )
                db.session.add(p1)
                db.session.flush()

                # 3. 建立初始測試任務
                t1 = Task(
                    patient_id=p1.id, 
                    creator_id=n1.id, 
                    content="14:00 測量生命徵象並記錄", 
                    priority="High", 
                    processing_order="First", 
                    category="一般照護",
                    due_time=datetime.now() + timedelta(hours=2)
                )
                db.session.add(t1)

        db.session.commit()
        print("Initial data seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Seed error: {e}")