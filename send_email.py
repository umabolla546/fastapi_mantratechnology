import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.templating import Jinja2Templates

# Initialize Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_email(receiver_email, subject, employee_name, template_name, num_days, sender_email, sender_password):
    # Read and render the email template
    try:
        message = templates.get_template(template_name).render(employee_name=employee_name, num_days=num_days)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'html'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        logger.info("Email sent successfully to %s", receiver_email)
    except smtplib.SMTPAuthenticationError as e:
        logger.error("SMTP Authentication Error: %s", str(e))
        logger.error("Make sure your Gmail credentials are correct and less secure apps are allowed.")
    except Exception as e:
        logger.error("Error sending email: %s", str(e))


