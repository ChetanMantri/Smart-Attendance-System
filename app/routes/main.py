import os
from flask import Blueprint, render_template, redirect, url_for, flash

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/photos', methods=['GET'])
def photos():
    faces_path = os.getenv('FACES_DIR', os.path.join('instance', 'faces'))
    try:
        if os.name == 'nt':  # Windows dev convenience
            os.startfile(faces_path)
    except Exception as e:
        flash(f"Unable to open folder. Error: {e}", 'error')
    return redirect(url_for('main.home'))


