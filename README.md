## Smart Attendance System

A Flask web app to register students, capture faces via webcam, train an LBPH recognizer (OpenCV), recognize faces to mark attendance in MySQL, and optionally send weekly WhatsApp summaries to parents using Twilio.

## Prerequisites
- Python 3.10+
- MySQL Server
- Webcam

## Install (Windows PowerShell)
1) Activate the virtual environment and install dependencies 
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

2) Create a .env file in the project root (required)
```env
SECRET_KEY=key
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=attendance_system

# Optional (for WhatsApp messages via Twilio)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM=whatsapp:+11xxxxxxxxx

# Optional (storage locations; defaults shown)
FACES_DIR=instance/faces
MODEL_PATH=instance/trained_model.yml
```

3) Prepare the database
- Create database `attendance_system`
- Create tables `users` and `attendance` with the columns used by the code

## Run
```powershell
python run.py
```
Open `http://127.0.0.1:5000` in your browser.

## Project layout (key parts)
```
app/
  __init__.py          # App factory and setup
  routes/              # Blueprints (pages/endpoints)
  services/            # Capture, training, recognition
  templates/           # HTML templates
static/                # CSS/Images
instance/              # Faces and trained model (created on first run)
run.py                 # App entrypoint
```

Notes
- LBPH comes from `opencv-contrib-python` (already in requirements).
- Faces default to `instance/faces`, model to `instance/trained_model.yml`.
- Attendance timestamps are stored in UTC.
