from flask import Blueprint, render_template, request, redirect, url_for, flash
from db_connection import get_db_connection
from app.services.capture_service import capture_images

bp = Blueprint('users', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        parents_no = request.form['parents_no']

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, parents_no) VALUES (%s, %s, %s)",
                (name, email, parents_no)
            )
            connection.commit()
            user_id = cursor.lastrowid

            folder_path = capture_images(user_id, name, email, parents_no)

            cursor.execute(
                "UPDATE users SET face_data=%s WHERE user_id=%s",
                (folder_path, user_id)
            )
            connection.commit()

            flash(f"Student {name} added and images captured successfully!")
        except Exception as e:
            connection.rollback()
            flash(f"Registration failed: {e}", 'error')
        finally:
            cursor.close()
            connection.close()

        return redirect(url_for('users.register'))

    return render_template('register.html')


