from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
from app.controllers.task_controller import (
    create_task, update_task_status, get_pending_tasks_for_handover, process_task_for_handover
)
from app.models.patient import Patient
from app.models.nurse import Nurse
from app.models.task import Task
from app.extensions import db

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.get("/dashboard")
def shift_dashboard():
    """渲染看板：修正注入 Nurses 列表供交班選擇"""
    # 登入檢查：如果沒有登入則強制轉跳到登入頁面
    if "nurse_id" not in session:
        return redirect(url_for("nurse_bp.login_ui"))

    tasks, _ = get_pending_tasks_for_handover()
    patients = Patient.query.all()
    nurses = Nurse.query.all() # 注入護理師清單，讓前端交班彈窗可以參考 ID
    return render_template("dashboard.html", 
                         tasks=tasks, 
                         patients=patients, 
                         nurses=nurses, 
                         current_user_id=session.get("nurse_id"),
                         current_user_name=session.get("nurse_name"))

@task_bp.get("/patient/<int:patient_id>/details")
def patient_task_details(patient_id):
    """【修正】補齊原本缺失的路由，讓 patient_list.html 能跳轉過來"""
    patient = db.session.get(Patient, patient_id)
    if not patient:
        return "Patient not found", 404
        
    tasks = [t.to_dict() for t in patient.tasks]
    status_history = [h.to_dict() for h in patient.status_history]
    
    return render_template("patient_details.html", patient=patient, tasks=tasks, status_history=status_history)

@task_bp.post("/")
def create_task_api():
    data = request.get_json()
    result, status_code = create_task(
        patient_id=data.get("patient_id"),
        creator_id=data.get("creator_id"),
        content=data.get("content"),
        priority=data.get("priority", "Normal"),
        category=data.get("category"),
        processing_order=data.get("processing_order", "Normal"),
        due_time=data.get("due_time")
    )
    return jsonify(result), status_code

@task_bp.put("/<int:task_id>/status")
def update_status_api(task_id):
    data = request.get_json()
    result, status_code = update_task_status(task_id, data.get("executor_id"), data.get("status"))
    return jsonify(result), status_code

@task_bp.put("/<int:task_id>/handover")
def handle_task_handover_api(task_id):
    """交班接口：增加對 next_executor_id 的校驗"""
    data = request.get_json()
    next_id = data.get("next_executor_id")
    
    if not next_id:
        return jsonify({"error": "必須指定接班護理師 ID"}), 400
        
    result, status_code = process_task_for_handover(
        task_id, 
        data.get("current_user_id"), 
        data.get("action"), 
        data.get("summary"), 
        next_id
    )
    return jsonify(result), status_code