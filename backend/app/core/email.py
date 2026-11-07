import asyncio
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


def is_email_configured() -> bool:
    """
    Check if the SMTP service has been configured with host details.
    """
    return bool(settings.SMTP_HOST and settings.SMTP_HOST.strip())


def _send_smtp_sync(
    to_email: str,
    subject: str,
    text_content: str,
    html_content: str,
) -> None:
    """
    Synchronous helper to dispatch an email via SMTP.
    Executed in a background thread to prevent blocking async event loop.
    """
    from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER or "noreply@interviewready.ai"
    from_header = f'"{settings.SMTP_FROM_NAME}" <{from_email}>'

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_header
    message["To"] = to_email

    # Plaintext fallback
    message.attach(MIMEText(text_content, "plain", "utf-8"))
    # HTML formatted version
    message.attach(MIMEText(html_content, "html", "utf-8"))

    server: Optional[smtplib.SMTP] = None
    try:
        if settings.SMTP_SSL:
            server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15)
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15)
            if settings.SMTP_TLS:
                server.starttls()

        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(from_email, [to_email], message.as_string())
        logger.info(f"Password recovery email successfully dispatched to {to_email}")
    except smtplib.SMTPException as exc:
        logger.error(f"SMTP delivery failed to {to_email}: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send password reset email. Please verify server SMTP configuration.",
        ) from exc
    except Exception as exc:
        logger.error(f"Unexpected error while sending email to {to_email}: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while connecting to the email service.",
        ) from exc
    finally:
        if server:
            try:
                server.quit()
            except Exception:
                pass


async def send_password_reset_email(
    to_email: str,
    recipient_name: str,
    reset_link: str,
    expires_in_minutes: int = 15,
) -> None:
    """
    Send a secure password reset link to a student's registered email address.
    """
    if not is_email_configured():
        logger.warning(
            "Password reset requested, but SMTP_HOST is not configured. Email will not be sent."
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Email delivery service is not configured on the server. "
                "Please configure SMTP credentials (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD) in the server environment (.env)."
            ),
        )

    subject = "InterviewReady AI — Reset Your Password"

    text_content = f"""Hello {recipient_name},

We received a request to reset your password for your InterviewReady AI account.

Please visit the following link to choose a new password:
{reset_link}

This link is valid for {expires_in_minutes} minutes and can only be used once.

If you did not request this password reset, you can safely ignore this email. Your existing password will remain unchanged.

Best regards,
The InterviewReady AI Team
"""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Reset Your Password</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F1F3F6; margin: 0; padding: 24px; color: #202B38; }}
    .container {{ max-width: 540px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #E5E9EF; overflow: hidden; box-shadow: 0 4px 12px rgba(18, 62, 99, 0.08); }}
    .header {{ background-color: #0D3557; padding: 28px 24px; text-align: center; }}
    .brand {{ font-size: 20px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }}
    .brand span {{ color: #F5A623; }}
    .content {{ padding: 32px 28px; line-height: 1.6; font-size: 14px; }}
    .greeting {{ font-size: 16px; font-weight: 700; color: #202B38; margin-bottom: 12px; }}
    .button-container {{ text-align: center; margin: 28px 0; }}
    .btn {{ display: inline-block; background-color: #123E63; color: #ffffff !important; text-decoration: none; font-weight: 700; font-size: 14px; padding: 13px 32px; border-radius: 10px; box-shadow: 0 2px 6px rgba(18, 62, 99, 0.2); }}
    .note {{ background-color: #FFF6E8; border-left: 4px solid #F5A623; padding: 12px 14px; font-size: 12px; color: #734800; border-radius: 6px; margin: 20px 0; }}
    .link-fallback {{ font-size: 12px; color: #8993A0; word-break: break-all; margin-top: 20px; }}
    .footer {{ background-color: #F8F9FA; padding: 18px 24px; text-align: center; font-size: 11px; color: #8993A0; border-top: 1px solid #E5E9EF; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="brand"><span>InterviewReady</span> AI</div>
    </div>
    <div class="content">
      <div class="greeting">Hello {recipient_name},</div>
      <p>We received a request to reset the password for your InterviewReady AI student preparation workspace.</p>
      
      <div class="button-container">
        <a href="{reset_link}" class="btn" target="_blank">Reset Password</a>
      </div>

      <div class="note">
        <strong>Security Notice:</strong> This password reset link is time-limited ({expires_in_minutes} minutes) and can only be used once.
      </div>

      <p class="link-fallback">
        If the button above does not work, copy and paste this URL into your browser:<br>
        <a href="{reset_link}" style="color: #123E63;">{reset_link}</a>
      </p>

      <p style="margin-top: 24px; font-size: 12px; color: #8993A0;">
        If you did not request a password reset, you can safely ignore this message. Your account remains completely secure.
      </p>
    </div>
    <div class="footer">
      InterviewReady AI &bull; AI-Powered Student Interview Preparation Platform<br>
      &copy; 2026 InterviewReady AI. All rights reserved.
    </div>
  </div>
</body>
</html>
"""

    await asyncio.to_thread(
        _send_smtp_sync,
        to_email,
        subject,
        text_content,
        html_content,
    )
