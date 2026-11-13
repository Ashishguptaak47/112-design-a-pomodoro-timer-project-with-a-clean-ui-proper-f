import json
import os
from datetime import date
from typing import Dict, Any

class StatsManager:
    def __init__(self, storage_path: str = "pomodoro_stats.json"):
        self.storage_path = storage_path
        self.data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"total_sessions": 0, "total_work_minutes": 0, "daily_history": {}}

    def save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except IOError:
            pass

    def record_completed_session(self, duration_seconds: int):
        today = str(date.today())
        minutes = round(duration_seconds / 60)
        self.data["total_sessions"] = self.data.get("total_sessions", 0) + 1
        self.data["total_work_minutes"] = self.data.get("total_work_minutes", 0) + minutes
        
        history = self.data.setdefault("daily_history", {})
        history[today] = history.get(today, 0) + 1
        self.save()

    def get_today_count(self) -> int:
        today = str(date.today())
        return self.data.get("daily_history", {}).get(today, 0)

    def get_total_sessions(self) -> int:
        return self.data.get("total_sessions", 0)

    def get_total_work_minutes(self) -> int:
        return self.data.get("total_work_minutes", 0)
