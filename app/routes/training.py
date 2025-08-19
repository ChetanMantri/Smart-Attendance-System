from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.training_service import train_model

bp = Blueprint('training', __name__)


@bp.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        try:
            train_model()
            flash('Training completed successfully.', 'success')
        except Exception as e:
            flash(f'Error training model: {e}', 'error')
        return redirect(url_for('training.train'))
    return render_template('train.html')


