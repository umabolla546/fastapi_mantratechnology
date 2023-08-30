
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from send_email import send_email
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Read the Excel sheet and extract employee attendance data
file_path = 'data/employee_attendance.xlsx'
df = pd.read_excel(file_path)

# Define email templates
candidate_email_template = "candidate_email_template.html"
employer_email_template = "employer_email_template.html"

# Set up Gmail account
sender_email = 'umamaheswararao546@gmail.com'
sender_password = 'vkgcyesicqfkkkbk'

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/process_attendance")
def process_attendance(request: Request):
    try:
        absent_candidates = df[df['Attendance'] == 'A'].groupby('E.Name').filter(lambda x: len(x) >= 2)

        for employee_name, group in absent_candidates.groupby('E.Name'):
            if len(group) == 2:
                subject = "Leave Notification for {}".format(employee_name)
                send_email('umabolla28@gmail.com', subject, employee_name, candidate_email_template, len(group),sender_email, sender_password)
            elif len(group) >= 3:
                subject = "Leave Notification for {}".format(employee_name)
                send_email('umabolla28@gmail.com', subject, employee_name, candidate_email_template, len(group), sender_email, sender_password)

                send_email('umabolla0546@gmail.com', subject, employee_name, employer_email_template,len(group), sender_email, sender_password)

        success_message = "Attendance processing and emails sent."
        logger.info(success_message)
    except Exception as e:
        success_message = f"Error processing attendance: {str(e)}"
        logger.error(success_message)

    return templates.TemplateResponse("success_message.html", {"request": request, "message": success_message})


