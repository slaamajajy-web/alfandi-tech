import telebot, requests, os
from config import Config

# استخراج التوكن الحقيقي من النسخة المشفرة في الذاكرة
TOKEN = Config.get_token()
if not TOKEN:
    print("خطأ: لم يتم العثور على التوكن المشفر أو مفتاح Fernet!")
    exit()

bot = telebot.TeleBot(TOKEN)
API_URL = Config.API_URL

@bot.message_handler(commands=['start'])
def send_welcome(m):
    bot.reply_to(m, "مرحباً بك في نظام الفندي TechHunter التقنية\nاستخدم الأمر /buy لشراء رخصة جديدة.")

@bot.message_handler(commands=['buy'])
def buy_menu(m):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("باقة Basic (أداة واحدة)", callback_data="basic"))
    markup.add(telebot.types.InlineKeyboardButton("باقة Pro (5 أدوات)", callback_data="pro"))
    markup.add(telebot.types.InlineKeyboardButton("باقة Sovereign (الكل)", callback_data="sovereign"))
    bot.send_message(m.chat.id, "اختر الباقة المناسبة لك:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    tier = call.data
    bot.answer_callback_query(call.id, "جاري معالجة الطلب...")
    try:
        headers = {"X-SECURE-KEY": Config.HANDSHAKE}
        response = requests.post(
            f"{API_URL}/generate_license", 
            json={"tier": tier}, 
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            license_key = response.json().get("key")
            msg = f"✅ تم شراء باقة {tier.upper()} بنجاح!\n\nرخصة التشغيل الخاصة بك هي:\n`{license_key}`\n\n*ملاحظة: هذه الرخصة تعمل على جهاز واحد فقط.*"
            bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")
            bot.send_message(Config.ADMIN_ID, f"💰 عملية بيع جديدة!\nالباقة: {tier}\nالمفتاح: {license_key}")
        else:
            bot.send_message(call.message.chat.id, "❌ عذراً، حدث خطأ في الاتصال بالسيرفر.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"⚠️ خطأ تقني: {str(e)}")

if __name__ == "__main__":
    print("البوت السيادي يعمل الآن...")
    bot.infinity_polling()
