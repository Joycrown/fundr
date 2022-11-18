from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.environ import settings








conf = ConnectionConfig (
    MAIL_USERNAME = settings.email,
    MAIL_PASSWORD =settings.email_password,
    MAIL_FROM = settings.email,
    MAIL_PORT = settings.email_port,
    MAIL_SERVER = settings.email_server,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER="utlis/templates"
)