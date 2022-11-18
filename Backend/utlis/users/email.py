from schemas.users import user
from fastapi_mail import FastMail, MessageSchema
from schemas.users.email import Email
from config.email import conf



# Send Email
async def send_mail(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="email.html")


# Send Mail to reset password
async def password_rest_email(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="password_reset.html")
