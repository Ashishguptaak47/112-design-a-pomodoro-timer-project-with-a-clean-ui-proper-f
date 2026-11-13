# Modern Pomodoro Timer

A sleek, modern Pomodoro Timer desktop application built with Python and Tkinter. Features customizable session durations, circular progress timer UI, automated workflow transitions, and persistent productivity statistics.

## Features
- 🎨 **Clean, Dark-Themed UI**: Custom canvas circular countdown timer with adaptive color schemes for Work, Short Break, and Long Break.
- ⚙️ **Customizable Settings**: Adjust Work, Short Break, and Long Break durations directly from the settings dialog.
- 📊 **Productivity Tracker**: Tracks today's finished sessions and cumulative work minutes, saved automatically to local JSON storage.
- 🔔 **Audio & Visual Alerts**: Playful timer ring animations and auditory notifications upon session completion.
- 🧪 **Unit Tested Engine**: Fully tested core timer logic and statistics manager.

## Requirements
- Python 3.8+
- Tkinter (included with standard Python installations on Windows/macOS; Linux users may need `sudo apt install python3-tk`)

## Installation & Run

1. Clone or extract the repository.
2. Install optional test dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the application:
   ```bash
   python main.py
   ```

## Running Tests

Run unit tests with `pytest`:
```bash
   pytest
   ```
