from app.extensions import db
from app.models.patient import Patient, PatientStatusHistory

def get_all_patients():
    """取得所有病人資料"""
    return Patient.query.all()

def create_patient(name, bed_number, medical_id, gender, age, diagnosis):
    """資料庫新增病人邏輯"""
    try:
        new_patient = Patient(
            name=name,
            bed_number=bed_number,
            medical_id=medical_id,
            gender=gender,
            age=age,
            diagnosis=diagnosis
        )
        db.session.add(new_patient)
        db.session.commit()
        return new_patient.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def update_patient_status(patient_id, status, remark=None, nurse_id=None):
    """更新並記錄病人狀態"""
    try:
        patient = db.session.get(Patient, patient_id)
        if not patient:
            return {"error": "Patient not found"}, 404
            
        patient.status = status
        
        history = PatientStatusHistory(
            patient_id=patient_id,
            status=status,
            remark=remark,
            recorded_by=nurse_id
        )
        db.session.add(history)
        db.session.commit()
        return {"message": "Status updated successfully", "status": status}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500