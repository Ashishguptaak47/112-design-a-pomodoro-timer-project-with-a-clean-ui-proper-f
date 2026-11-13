from enum import Enum, auto
from typing import Dict, Callable, Optional

class SessionType(Enum):
    WORK = "Work"
    SHORT_BREAK = "Short Break"
    LONG_BREAK = "Long Break"

class TimerState(Enum):
    STOPPED = auto()
    RUNNING = auto()
    PAUSED = auto()

class PomodoroEngine:
    def __init__(
        self,
        work_mins: int = 25,
        short_break_mins: int = 5,
        long_break_mins: int = 15,
        long_break_interval: int = 4
    ):
        self.durations: Dict[SessionType, int] = {
            SessionType.WORK: work_mins * 60,
            SessionType.SHORT_BREAK: short_break_mins * 60,
            SessionType.LONG_BREAK: long_break_mins * 60,
        }
        self.long_break_interval = long_break_interval
        self.completed_work_sessions = 0
        self.current_session = SessionType.WORK
        self.state = TimerState.STOPPED
        self.remaining_seconds = self.durations[self.current_session]

    def update_durations(self, work_mins: int, short_break_mins: int, long_break_mins: int):
        self.durations[SessionType.WORK] = work_mins * 60
        self.durations[SessionType.SHORT_BREAK] = short_break_mins * 60
        self.durations[SessionType.LONG_BREAK] = long_break_mins * 60
        if self.state == TimerState.STOPPED:
            self.remaining_seconds = self.durations[self.current_session]

    def get_total_duration(self) -> int:
        return self.durations[self.current_session]

    def start(self):
        self.state = TimerState.RUNNING

    def pause(self):
        self.state = TimerState.PAUSED

    def reset(self):
        self.state = TimerState.STOPPED
        self.remaining_seconds = self.durations[self.current_session]

    def switch_session(self, session_type: SessionType):
        self.current_session = session_type
        self.state = TimerState.STOPPED
        self.remaining_seconds = self.durations[session_type]

    def tick(() -> bool:
        """Decrements remaining time if running. Returns True if current session finished."""
        if self.state == TimerState.RUNNING and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            if self.remaining_seconds == 0:
                self._on_session_finished()
                return True
        return False

    def _on_session_finished(self):
        self.state = TimerState.STOPPED
        if self.current_session == SessionType.WORK:
            self.completed_work_sessions += 1
            if self.completed_work_sessions % self.long_break_interval == 0:
                self.current_session = SessionType.LONG_BREAK
            else:
                self.current_session = SessionType.SHORT_BREAK
        else:
            self.current_session = SessionType.WORK
        self.remaining_seconds = self.durations[self.current_session]
