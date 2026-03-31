from flask import Blueprint, render_template, request, jsonify
from app.controllers.patient_controller import get_all_patients, create_patient

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