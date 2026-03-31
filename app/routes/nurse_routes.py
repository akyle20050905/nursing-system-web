from flask import Blueprint, jsonify, request, render_template
from app.controllers.nurse_controller import create_nurse, get_all_nurses

nurse_bp = Blueprint("nurse_bp", __name__, url_prefix="/nurses")

@nurse_bp.get("/ui")
def nurse_ui():
    """渲染護理師管理介面 (UI)"""
    nurses = get_all_nurses()
    return render_template("nurse_list.html", nurses=nurses)

@nurse_bp.post("/")
def add_nurse_api():
    """API: 新增護理師"""
    data = request.get_json()
    nurse = create_nurse(data.get("name"), data.get("department"), data.get("level"))
    if not nurse: return jsonify({"error": "Failed"}), 500
    return jsonify(nurse.to_dict()), 201