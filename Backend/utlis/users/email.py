from fastapi_mail import FastMail, MessageSchema
from config.email import conf



# Send Email for successful signup
async def account_purchased(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="accountPurchased.html")

# Send Email after invoice generation
async def account_paid_for(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="accountPaidFor.html")


# Send Email for account confirmation
async def account_confirmation(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="purchasedConfirmation.html")


# Send Email for account setup
async def account_setup(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="purchasedSetup.html")


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

async def admin_invite(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="admin_invite.html")


async def rejected_payment_email(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="rejected_payment.html")

async def upgrade_request(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="upgradeRequest.html")


async def upgrade_request_processing(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="upgradeRequestProcessing.html")


async def upgrade_request_completed(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="upgradeRequestConfirmation.html")


async def upgrade_request_rejected(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="rejectedUpgrade.html")


async def scale_request(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="scaleRequest.html")


async def scale_request_processing(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="scaleRequestProcessing.html")



async def scale_request_completed(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="scaleRequestConfirmation.html")


async def scale_request_rejected(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="rejectedScale.html")


async def payout_request(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="payoutRequest.html")


async def payout_request_processing(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="payoutRequestProcessing.html")


async def payout_request_confirmation(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="payoutRequestConfirmation.html")


async def payout_request_rejected(subject: str, email_to: str, body:dict):
    message= MessageSchema(
        subject=subject,
        recipients= [email_to],
        template_body= body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="rejectedPayout.html")
