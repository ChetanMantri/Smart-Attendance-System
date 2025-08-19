from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.recognition_service import recognize_faces

bp = Blueprint('recognition', __name__)


@bp.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'POST':
        message, _ = recognize_faces()
        flash(message)
        return redirect(url_for('recognition.recognize'))
    return render_template('recognize.html')


