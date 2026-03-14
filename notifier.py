import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER

def create_email_body(problems_with_solutions):
    """
    Creates an HTML body for the email.
    """
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; }}
            .container {{ max-width: 800px; margin: auto; padding: 20px; }}
            .problem {{ border-bottom: 2px solid #eee; margin-bottom: 30px; padding-bottom: 20px; }}
            .link {{ font-size: 18px; font-weight: bold; margin-bottom: 15px; }}
            .solution {{ background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; font-family: 'Courier New', Courier, monospace; white-space: pre-wrap; }}
            .footer {{ margin-top: 50px; font-size: 12px; color: #95a5a6; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Daily LeetCode Practice</h1>
    """
    
    for p in problems_with_solutions:
        html += f"""
        <div class="problem">
            <div class="link">
                <a href="https://leetcode.com/problems/{p['titleSlug']}">Problem: {p['title']}</a>
            </div>
            <h3>Python Solution</h3>
            <div class="solution">{p['solution']}</div>
        </div>
        """
        
    html += """
            <div class="footer">
                Automated Daily LeetCode Solver &copy; 2026
            </div>
        </div>
    </body>
    </html>
    """
    return html

def send_email(subject, body, is_html=True):
    """
    Sends an email using the SMTP settings from config.
    """
    if not all([EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER]):
        print("Error: Email credentials not fully configured in environment.")
        return False

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Mock test (won't send without credentials)
    test_problems = [
        {
            "title": "Two Sum",
            "titleSlug": "two-sum",
            "difficulty": "Easy",
            "content": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            "solution": "def twoSum(nums, target):\n    # implementation"
        }
    ]
    body = create_email_body(test_problems)
    # print(body[:500])
    # send_email("Test LeetCode Daily", body)
