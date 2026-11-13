import tkinter as tk
from tkinter import messagebox, ttk
from pomodoro.timer import PomodoroEngine, SessionType, TimerState
from pomodoro.stats import StatsManager

PALETTE = {
    "bg": "#1E1E2E",
    "card": "#2A2A3C",
    "text": "#F8F8F2",
    "subtext": "#A6ADC8",
    "work": "#FF5555",
    "short_break": "#50FA7B",
    "long_break": "#8BE9FD",
    "button_bg": "#44475A",
    "button_hover": "#6272A4"
}

class PomodoroApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("420x580")
        self.root.configure(bg=PALETTE["bg"])
        self.root.resizable(False, False)

        self.engine = PomodoroEngine()
        self.stats = StatsManager()

        self.theme_color = PALETTE["work"]
        self._setup_ui()
        self._update_display()
        self._schedule_tick()

    def _setup_ui(self):
        # Header / Navigation tabs
        self.nav_frame = tk.Frame(self.root, bg=PALETTE["bg"], pady=15)
        self.nav_frame.pack()

        self.mode_buttons = {}
        for session_type in SessionType:
            btn = tk.Button(
                self.nav_frame,
                text=session_type.value,
                font=("Helvetica", 10, "bold"),
                bg=PALETTE["button_bg"],
                fg=PALETTE["text"],
                activebackground=PALETTE["button_hover"],
                activeforeground=PALETTE["text"],
                bd=0, padx=10, pady=5,
                cursor="hand2",
                command=lambda s=session_type: self._switch_mode(s)
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.mode_buttons[session_type] = btn

        # Canvas Arc Timer
        self.canvas_frame = tk.Frame(self.root, bg=PALETTE["bg"])
        self.canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, width=240, height=240, bg=PALETTE["bg"], highlightthickness=0)
        self.canvas.pack()

        self.circle_bg = self.canvas.create_oval(15, 15, 225, 225, outline=PALETTE["card"], width=12)
        self.circle_progress = self.canvas.create_arc(15, 15, 225, 225, start=90, extent=0, outline=self.theme_color, width=12, style=tk.ARC)
        self.time_text = self.canvas.create_text(120, 110, text="25:00", fill=PALETTE["text"], font=("Helvetica", 36, "bold"))
        self.status_text = self.canvas.create_text(120, 150, text="WORK", fill=PALETTE["subtext"], font=("Helvetica", 12, "bold"))

        # Controls
        self.controls_frame = tk.Frame(self.root, bg=PALETTE["bg"], pady=15)
        self.controls_frame.pack()

        self.start_pause_btn = tk.Button(
            self.controls_frame, text="START", font=("Helvetica", 12, "bold"),
            bg=PALETTE["work"], fg=PALETTE["bg"], activebackground=PALETTE["text"],
            bd=0, width=10, pady=8, cursor="hand2", command=self._toggle_timer
        )
        self.start_pause_btn.pack(side=tk.LEFT, padx=8)

        self.reset_btn = tk.Button(
            self.controls_frame, text="RESET", font=("Helvetica", 12, "bold"),
            bg=PALETTE["button_bg"], fg=PALETTE["text"], activebackground=PALETTE["button_hover"],
            bd=0, width=8, pady=8, cursor="hand2", command=self._reset_timer
        )
        self.reset_btn.pack(side=tk.LEFT, padx=8)

        # Footer Stats & Settings button
        self.footer_frame = tk.Frame(self.root, bg=PALETTE["card"], pady=15)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.stats_label = tk.Label(
            self.footer_frame, text="", bg=PALETTE["card"], fg=PALETTE["text"], font=("Helvetica", 10)
        )
        self.stats_label.pack(side=tk.LEFT, padx=20)

        self.settings_btn = tk.Button(
            self.footer_frame, text="⚙ Settings", bg=PALETTE["button_bg"], fg=PALETTE["text"],
            activebackground=PALETTE["button_hover"], bd=0, padx=8, pady=4, cursor="hand2",
            command=self._open_settings
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=20)

        self._update_stats_display()

    def _switch_mode(self, session_type: SessionType):
        self.engine.switch_session(session_type)
        self._update_display()

    def _toggle_timer(self):
        if self.engine.state == TimerState.RUNNING:
            self.engine.pause()
        else:
            self.engine.start()
        self._update_display()

    def _reset_timer(self):
        self.engine.reset()
        self._update_display()

    def _schedule_tick(self):
        finished = self.engine.tick()
        if finished:
            self.root.bell()
            if self.engine.current_session != SessionType.WORK:
                # Previous session was work
                prev_duration = self.engine.durations[SessionType.WORK]
                self.stats.record_completed_session(prev_duration)
                self._update_stats_display()
            messagebox.showinfo("Pomodoro", f"Session complete! Next: {self.engine.current_session.value}")

        self._update_display()
        self.root.after(1000, self._schedule_tick)

    def _update_display(self):
        # Update colors
        color_map = {
            SessionType.WORK: PALETTE["work"],
            SessionType.SHORT_BREAK: PALETTE["short_break"],
            SessionType.LONG_BREAK: PALETTE["long_break"]
        }
        self.theme_color = color_map[self.engine.current_session]

        # Remaining Time
        mins, secs = divmod(self.engine.remaining_seconds, 60)
        self.canvas.itemconfig(self.time_text, text=f"{mins:02d}:{secs:02d}")
        self.canvas.itemconfig(self.status_text, text=self.engine.current_session.value.upper(), fill=self.theme_color)

        # Ring extent calculate
        total = self.engine.get_total_duration()
        fraction = (self.engine.remaining_seconds / total) if total > 0 else 0
        extent = -360 * fraction
        self.canvas.itemconfig(self.circle_progress, extent=extent, outline=self.theme_color)

        # Button Labels
        if self.engine.state == TimerState.RUNNING:
            self.start_pause_btn.config(text="PAUSE", bg=PALETTE["button_bg"], fg=PALETTE["text"])
        else:
            self.start_pause_btn.config(text="START", bg=self.theme_color, fg=PALETTE["bg"])

        # Highlight Active Nav Button
        for stype, btn in self.mode_buttons.items():
            if stype == self.engine.current_session:
                btn.config(bg=self.theme_color, fg=PALETTE["bg"])
            else:
                btn.config(bg=PALETTE["button_bg"], fg=PALETTE["text"])

    def _update_stats_display(self):
        today = self.stats.get_today_count()
        total_mins = self.stats.get_total_work_minutes()
        self.stats_label.config(text=f"Today: {today} completed | Total Focus: {total_mins} mins")

    def _open_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("280x220")
        dialog.configure(bg=PALETTE["bg"])
        dialog.transient(self.root)
        dialog.grab_set()

        fields = [
            ("Work (mins):", self.engine.durations[SessionType.WORK] // 60),
            ("Short Break (mins):", self.engine.durations[SessionType.SHORT_BREAK] // 60),
            ("Long Break (mins):", self.engine.durations[SessionType.LONG_BREAK] // 60)
        ]

        entries = {}
        for i, (label_text, default_val) in enumerate(fields):
            lbl = tk.Label(dialog, text=label_text, bg=PALETTE["bg"], fg=PALETTE["text"], font=("Helvetica", 10))
            lbl.grid(row=i, column=0, padx=15, pady=10, sticky="w")
            ent = tk.Entry(dialog, width=8)
            ent.insert(0, str(default_val))
            ent.grid(row=i, column=1, padx=15, pady=10)
            entries[label_text] = ent

        def save():
            try:
                w = int(entries["Work (mins):"].get())
                sb = int(entries["Short Break (mins):"].get())
                lb = int(entries["Long Break (mins):"].get())
                if w > 0 and sb > 0 and lb > 0:
                    self.engine.update_durations(w, sb, lb)
                    self._update_display()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Values must be positive integers.", parent=dialog)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integers.", parent=dialog)

        save_btn = tk.Button(dialog, text="Save", bg=PALETTE["work"], fg=PALETTE["bg"], bd=0, padx=15, pady=5, command=save)
        save_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)
