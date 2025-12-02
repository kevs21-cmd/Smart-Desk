from website import mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email

def send_password_reset_email(user_email):
    token = generate_reset_token(user_email)
    reset_url = f"http://localhost:5000/reset_password/{token}"  # Change domain in production

    msg = Message(
        subject="Password Reset Request",
        recipients=[user_email],
        sender=current_app.config['MAIL_USERNAME']
    )
    msg.body = f"""\
Hello,

To reset your password, please visit the following link:

{reset_url}

If you did not request a password reset, please ignore this email.

Thanks,
PGPC Support
"""
    try:
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending password reset email: {e}")
        raise e


from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app, url_for, render_template
from website import mail  # import your Mail instance

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
        return email
    except Exception:
        return False

def send_verification_email(email, token):
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('email/verify_email.html', confirm_url=confirm_url)
    msg = Message("Verify Your Email Address", recipients=[email], html=html)
    mail.send(msg)
