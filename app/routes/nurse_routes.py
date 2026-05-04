from flask import Blueprint, jsonify, request, render_template, redirect, url_for, session, flash
from app.controllers.nurse_controller import create_nurse, get_all_nurses, login_nurse

nurse_bp = Blueprint("nurse_bp", __name__, url_prefix="/nurses")

@nurse_bp.get("/login")
def login_ui():
    """渲染登入與註冊介面"""
    return render_template("login.html")

@nurse_bp.post("/login")
def login_api():
    """處理登入邏輯"""
    data = request.get_json()
    nurse_id = data.get("nurse_id")
    password = data.get("password")
    
    nurse = login_nurse(nurse_id, password)
    if nurse:
        session["nurse_id"] = nurse.id
        session["nurse_name"] = nurse.name
        return jsonify({"message": "Login successful", "redirect": url_for("task_bp.shift_dashboard")}), 200
    else:
        return jsonify({"error": "Invalid Nurse ID or Password"}), 401

@nurse_bp.get("/ui")
def nurse_ui():
    """渲染護理師管理介面 (UI)"""
    nurses = get_all_nurses()
    return render_template("nurse_list.html", nurses=nurses)

@nurse_bp.post("/")
def add_nurse_api():
    """API: 新增(註冊)護理師"""
    data = request.get_json()
    password = data.get("password", "123456") # 預設密碼 fallback
    nurse = create_nurse(data.get("name"), data.get("department"), data.get("level"), password)
    if not nurse: return jsonify({"error": "Failed"}), 500
    return jsonify(nurse.to_dict()), 201