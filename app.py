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

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
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
        
        # Send email notification to portfolio owner
        try:
            send_email_notification(name, email, subject, message)
            
            # Send auto-reply back to the visitor
            try:
                send_auto_reply(name, email, subject)
            except Exception as e:
                app.logger.error(f"Auto-reply email sending failed to {email}: {e}")
                
            flash('Thank you for your message! I will get back to you soon.', 'success')
        except Exception as e:
            app.logger.error(f"Email sending failed: {e}")
            flash('Your message was saved, but email notification failed. Please check email settings.', 'error')
        
        return redirect(url_for('index') + '#contact')
        
    except Exception as e:
        app.logger.error(f"Contact form error: {e}")
        flash('Something went wrong. Please try again later.', 'error')
        return redirect(url_for('index') + '#contact')

def send_email_notification(name, email, subject, message):
    """Send email notification for new contact"""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL", "")
    sender_password = os.environ.get("SENDER_PASSWORD", "")
    recipient_email = os.environ.get("RECIPIENT_EMAIL", sender_email)
    
    if not all([sender_email, sender_password, recipient_email]):
        app.logger.warning(
            "Email configuration incomplete. "
            "Set SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, and optionally RECIPIENT_EMAIL."
        )
        raise RuntimeError("Email configuration incomplete")
    
    msg = MIMEMultipart()
    # Format the From header to show the visitor's name, but use your authenticated email to prevent spam issues
    msg['From'] = f"{name} (Portfolio Contact) <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = f"Portfolio Contact: {subject}"
    # Add Reply-To so that when you hit 'Reply', it replies to the visitor's email
    msg.add_header('Reply-To', email)
    
    body = f"""
    New contact form submission:
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)
    server.quit()

def send_auto_reply(name, visitor_email, subject):
    """Send an auto-reply confirmation email to the visitor"""
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    sender_email = os.environ.get("SENDER_EMAIL", "")
    sender_password = os.environ.get("SENDER_PASSWORD", "")
    
    if not all([sender_email, sender_password]):
        return
        
    msg = MIMEMultipart()
    msg['From'] = f"Hanumant Jadhav <{sender_email}>"
    msg['To'] = visitor_email
    msg['Subject'] = f"Re: {subject} - Thank you for reaching out!"
    
    body = f"""Hello {name},

Thank you for contacting me! I have received your message regarding "{subject}" and will get back to you as soon as possible.

Best regards,
Hanumant Jadhav
Portfolio: http://app.it3213.com (Your portfolio link)
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, visitor_email, text)
    server.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
