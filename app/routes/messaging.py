import os
from flask import Blueprint, render_template
from flask import request, redirect, url_for, flash
from db_connection import get_db_connection
from twilio.rest import Client

bp = Blueprint('messaging', __name__)


@bp.route('/send_message_home', methods=['GET'])
def send_message_home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, parents_no FROM users")
        users = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
    return render_template('send_message_home.html', users=users)


@bp.route('/send_message/<int:user_id>', methods=['POST'])
def send_message(user_id: int):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, parents_no FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.execute(
            """
            SELECT COUNT(*) AS days_present
            FROM attendance
            WHERE user_id = %s AND status = 'present'
              AND timestamp >= DATE_SUB(UTC_TIMESTAMP(), INTERVAL 7 DAY)
            """,
            (user_id,)
        )
        attendance = cursor.fetchone()

        message_body = (
            f"Hello, this is a weekly attendance update for {user['name']}. "
            f"Attendance in the last week: {attendance['days_present']} days."
        )

        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_whatsapp = os.getenv('TWILIO_FROM')

        client = Client(account_sid, auth_token)
        client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=f"whatsapp:{user['parents_no']}"
        )

        flash("Message sent successfully!")
    except Exception as e:
        flash(f"Failed to send message: {e}")
    finally:
        cursor.close()
        connection.close()
    return redirect(url_for('messaging.send_message_home'))


