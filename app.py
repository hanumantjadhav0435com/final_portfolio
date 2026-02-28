import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configure logging
logging.basicConfig(level=logging.DEBUG)

from extensions import db

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(app.instance_path, 'portfolio.db')}")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Ensure the instance folder exists for SQLite
    os.makedirs(app.instance_path, exist_ok=True)
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    db.create_all()

@app.route('/')
def index():
    """Main portfolio page"""
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Create contact record
        contact_record = models.Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        db.session.add(contact_record)
        db.session.commit()
        
        # Send email notifications (Combined for speed)
        try:
            send_combined_emails(name, email, subject, message)
            flash('Thank you for your message! I will get back to you soon.', 'success')
        except Exception as e:
            app.logger.error(f"Email sending failed: {e}")
            # Message is already saved in database, so we can still flash success or a warning
            flash('Your message was saved, but email notification failed. Please check email settings.', 'warning')
        
        return redirect(url_for('index') + '#contact')
        
    except Exception as e:
        app.logger.error(f"Contact form error: {e}")
        flash('Something went wrong. Please try again later.', 'error')
        return redirect(url_for('index') + '#contact')

def send_combined_emails(name, visitor_email, subject, message):
    """Sends both notification to owner AND auto-reply to visitor in ONE SMTP session."""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL", "")
    sender_password = os.environ.get("SENDER_PASSWORD", "")
    recipient_email = os.environ.get("RECIPIENT_EMAIL", sender_email)
    
    if not all([sender_email, sender_password, recipient_email]):
        app.logger.warning("Email configuration incomplete. Skipping notifications.")
        return

    # 1. Create message for YOU (The Portfolio Owner)
    msg_to_owner = MIMEMultipart()
    msg_to_owner['From'] = f"{name} (Portfolio) <{sender_email}>"
    msg_to_owner['To'] = recipient_email
    msg_to_owner['Subject'] = f"New Portfolio Message: {subject}"
    msg_to_owner.add_header('Reply-To', visitor_email)
    
    owner_body = f"From: {name}\nEmail: {visitor_email}\nSubject: {subject}\n\nMessage:\n{message}"
    msg_to_owner.attach(MIMEText(owner_body, 'plain'))

    # 2. Create auto-reply for the VISITOR
    msg_to_visitor = MIMEMultipart()
    msg_to_visitor['From'] = f"Hanumant Jadhav <{sender_email}>"
    msg_to_visitor['To'] = visitor_email
    msg_to_visitor['Subject'] = f"Re: {subject} - Thank you for reaching out!"
    
    visitor_body = f"Hello {name},\n\nThank you for your message. I've received it and will get back to you shortly.\n\nBest regards,\nHanumant Jadhav"
    msg_to_visitor.attach(MIMEText(visitor_body, 'plain'))

    # 3. Connect ONCE and send BOTH
    try:
        # Set a 30-second timeout to prevent the app from hanging forever
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send one by one via the same connection
        server.sendmail(sender_email, recipient_email, msg_to_owner.as_string())
        server.sendmail(sender_email, visitor_email, msg_to_visitor.as_string())
        
        server.quit()
    except Exception as e:
        app.logger.error(f"Combined mail sending failed: {e}")
        raise e

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
