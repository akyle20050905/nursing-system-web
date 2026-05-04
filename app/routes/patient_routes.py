from flask import Blueprint, render_template, request, jsonify, session
from app.controllers.patient_controller import get_all_patients, create_patient, update_patient_status

# 確保 url_prefix 為 /patients
patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patients")

@patient_bp.get("/")
def list_patients_view():
    """【修正】新增 UI 路由，渲染病人管理頁面"""
    patients = get_all_patients()
    return render_template("patient_list.html", patients=patients)

@patient_bp.post("/api")
def add_patient_api():
    data = request.get_json()
    result, status_code = create_patient(
        name=data.get("name"),
        bed_number=data.get("bed_number"),
        medical_id=data.get("medical_id"),
        gender=data.get("gender"),
        age=data.get("age"),
        diagnosis=data.get("diagnosis")
    )
    return jsonify(result), status_code

@patient_bp.put("/<int:patient_id>/status")
def update_status_api(patient_id):
    """更新病患狀態 API"""
    data = request.get_json()
    nurse_id = session.get("nurse_id")
    if not nurse_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    result, status_code = update_patient_status(
        patient_id=patient_id,
        status=data.get("status"),
        remark=data.get("remark"),
        nurse_id=nurse_id
    )
    return jsonify(result), status_code