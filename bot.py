import telebot
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

# ===================== 🤖 بوت تيليجرام =====================
TOKEN = '8961192435:AAE8MPkOoYUJsnirvTwpuztLFmnKkU9GQes'
bot = telebot.TeleBot(TOKEN)

# ===================== 🔧 إعدادات الإيميل =====================
EMAIL_CONFIG = {
    "sender": "8ep999@gmail.com",           
    "password": "hstkjxizrhlanzbq",            # استخدم كلمة السر العادية هنا
    "receiver": "security@mail.instagram.com", 
}

# نص الاستئناف
APPEAL_REASON = """My account has been disabled without a clear reason, despite my full compliance with all platform policies and guidelines.
I have not engaged in any violating activity and use my account normally, so I believe this may have been a mistake or an inaccurate review.
I kindly request a thorough review of my case and the restoration of my account as soon as possible."""

# ===================== 💌 دالة إرسال الإيميل (مع التعديل السحري) =====================
def send_appeal_email(target_username):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG["sender"]
        msg['To'] = EMAIL_CONFIG["receiver"]
        msg['Subject'] = f"URGENT: Appeal Request for Account @{target_username}"

        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🔒 Instagram Appeal Request</h2>
            <p><strong>Username:</strong> @{target_username}</p>
            <p><strong>Contact Email:</strong> {EMAIL_CONFIG['sender']}</p>
            <h3>Reason:</h3>
            <p>{APPEAL_REASON}</p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(email_body, 'html'))

        # ===== التعديل السحري هنا لجعل جوجل يقبل كلمة السر =====
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # استخدمنا المنفذ 465 و SSL
        server.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
        server.send_message(msg)
        server.quit()

        return True, "✅ تم إرسال الاستئناف بنجاح!"

    except Exception as e:
        return False, f"❌ فشل الإرسال: {str(e)}"

# ===================== 📱 أوامر تيليجرام =====================
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحباً! أرسل `/appeal` واسم المستخدم.\nمثال: `/appeal vicxii6`")

@bot.message_handler(commands=['appeal'])
def appeal(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ اكتب الأمر هكذا: `/appeal اسم_المستخدم`")
            return
        target = parts[1].strip()
        bot.reply_to(message, f"⏳ جارٍ الإرسال لـ @{target}...")
        success, result = send_appeal_email(target)
        bot.reply_to(message, result)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

# ===================== 🚀 تشغيل البوت =====================
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(5)
