from datetime import datetime
from app.extensions import db
from app.models.task import Task
from app.models.handover_log import HandoverLog

def create_task(patient_id, creator_id, content, priority='Normal', category=None, processing_order='Normal', due_time=None):
    """建立新任務：強化時間格式兼容性"""
    try:
        if isinstance(due_time, str):
            # 處理前端常見的日期格式
            try:
                dt_obj = datetime.fromisoformat(due_time.replace('Z', '+00:00'))
            except ValueError:
                dt_obj = datetime.now()
        else:
            dt_obj = due_time if due_time else datetime.now()

        new_task = Task(
            patient_id=patient_id, 
            creator_id=creator_id, 
            content=content,
            priority=priority, 
            category=category, 
            processing_order=processing_order,
            due_time=dt_obj, 
            status='Pending'
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {"error": f"Database Error: {str(e)}"}, 500

def update_task_status(task_id, executor_id, status):
    """更新任務狀態"""
    try:
        task = db.session.get(Task, task_id)
        if not task: 
            return {"error": "Task not found"}, 404
            
        task.status = status
        task.executor_id = executor_id
        
        if status == 'Completed':
            task.completed_time = datetime.now()
            
        db.session.commit()
        return task.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def process_task_for_handover(task_id, current_user_id, action, summary, next_executor_id=None):
    """處理任務交班：修正負責人變更邏輯"""
    try:
        task = db.session.get(Task, task_id)
        if not task: 
            return {"error": "Task not found"}, 404
        
        task.handoff_summary = summary
        
        if action == 'completed':
            task.status = 'Completed'
            task.executor_id = current_user_id
            task.completed_time = datetime.now()
        elif action == 'handover':
            # 工程師修正：交班時應將當前負責人改為下一位，並標註狀態
            task.status = 'Pending'
            task.is_handed_over = True
            task.executor_id = next_executor_id # 更新當前負責人
            task.next_executor_id = next_executor_id
            
            # 寫入交班日誌
            log = HandoverLog(
                from_nurse_id=current_user_id,
                to_nurse_id=next_executor_id if next_executor_id else 0,
                summary=f"任務 ID {task.id} 轉交：{summary}",
                shift_type="系統轉交"
            )
            db.session.add(log)
            
        db.session.commit()
        return task.to_dict(), 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_pending_tasks_for_handover():
    """取得待處理任務：已修改為回傳所有任務以配合前端過濾器"""
    tasks = Task.query.order_by(Task.priority.desc(), Task.due_time.asc()).all()
    return [t.to_dict() for t in tasks], 200