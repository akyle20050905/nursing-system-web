from app.extensions import db
from datetime import datetime

class HandoverLog(db.Model):
    __tablename__ = "handover_logs"
    
    id = db.Column(db.Integer, primary_key=True)
    from_nurse_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=False)
    to_nurse_id = db.Column(db.Integer, db.ForeignKey("nurses.id"), nullable=False)
    shift_type = db.Column(db.String(20)) # 白班, 小夜, 大夜
    summary = db.Column(db.Text) # 交班摘要
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "from_nurse": self.from_nurse_id,
            "to_nurse": self.to_nurse_id,
            "shift_type": self.shift_type,
            "summary": self.summary,
            "timestamp": self.created_at.isoformat()
        }