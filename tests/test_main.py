import os
import tempfile
import pytest
from pomodoro.timer import PomodoroEngine, SessionType, TimerState
from pomodoro.stats import StatsManager

def test_timer_initialization():
    engine = PomodoroEngine(work_mins=25, short_break_mins=5, long_break_mins=15)
    assert engine.remaining_seconds == 25 * 60
    assert engine.current_session == SessionType.WORK
    assert engine.state == TimerState.STOPPED

def test_timer_transitions():
    engine = PomodoroEngine(work_mins=1, short_break_mins=1, long_break_mins=1, long_break_interval=2)
    engine.start()
    assert engine.state == TimerState.RUNNING

    # Fast forward work timer
    engine.remaining_seconds = 1
    finished = engine.tick()
    assert finished is True
    assert engine.completed_work_sessions == 1
    assert engine.current_session == SessionType.SHORT_BREAK

    # Fast forward short break
    engine.start()
    engine.remaining_seconds = 1
    finished = engine.tick()
    assert finished is True
    assert engine.current_session == SessionType.WORK

    # Fast forward second work session -> should trigger LONG_BREAK
    engine.start()
    engine.remaining_seconds = 1
    engine.tick()
    assert engine.completed_work_sessions == 2
    assert engine.current_session == SessionType.LONG_BREAK

def test_timer_reset_and_durations():
    engine = PomodoroEngine(work_mins=25)
    engine.start()
    engine.remaining_seconds = 100
    engine.reset()
    assert engine.state == TimerState.STOPPED
    assert engine.remaining_seconds == 25 * 60

    engine.update_durations(30, 10, 20)
    assert engine.remaining_seconds == 30 * 60

def test_stats_manager():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp_path = tmp.name

    try:
        stats = StatsManager(storage_path=tmp_path)
        assert stats.get_today_count() == 0
        assert stats.get_total_work_minutes() == 0

        stats.record_completed_session(1500) # 25 minutes
        assert stats.get_today_count() == 1
        assert stats.get_total_work_minutes() == 25

        # Test reloading
        stats_reloaded = StatsManager(storage_path=tmp_path)
        assert stats_reloaded.get_today_count() == 1
        assert stats_reloaded.get_total_work_minutes() == 25
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
