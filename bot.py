import telebot
import os
from dotenv import load_dotenv

# بارگذاری مقادیر .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_BASE = os.getenv("SITE_BASE", "https://nimv.ir")
ADMIN_ID = os.getenv("ADMIN_ID")

# ساخت ربات
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# --- فرمان /start ---
@bot.message_handler(commands=['start'])
def start(message):
    first = message.from_user.first_name or ""
    text = f"🌙 <b>نــیمــا</b>\nبه پرتال من خوش اومدی 👋\nاز دکمه‌های زیر استفاده کن ↓"

    buttons = telebot.types.InlineKeyboardMarkup(row_width=1)
    buttons.add(
        telebot.types.InlineKeyboardButton("🌐 پرتال من", url=SITE_BASE),
        telebot.types.InlineKeyboardButton("🛡️ خرید VPN", url="https://t.me/iliiyo"),
        telebot.types.InlineKeyboardButton("✉️ تماس با من", callback_data="contact"),
        telebot.types.InlineKeyboardButton("🆘 راهنما", callback_data="help")
    )

    bot.send_message(message.chat.id, text, reply_markup=buttons)


# --- دکمه‌های اینلاین ---
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "help":
        msg = (
            "🆘 <b>راهنما</b>\n\n"
            "🌐 پرتال من — باز کردن سایت من\n"
            "🛡 خرید VPN — ارتباط مستقیم با پشتیبانی\n"
            "✉ تماس با من — ارسال پیام مستقیم"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=msg, reply_markup=main_menu(), parse_mode="HTML")

    elif call.data == "contact":
        bot.send_message(call.message.chat.id, "✉️ لطفاً پیامت رو بنویس تا برام بفرسته 📩")
        bot.register_next_step_handler(call.message, get_contact_message)


def get_contact_message(message):
    """پیام کاربر رو برای ادمین ارسال می‌کنه"""
    user = message.from_user
    text = f"📩 <b>پیام جدید از {user.first_name}</b>\n\n{message.text}\n\n🆔 @{user.username or '---'}"
    if ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, text)
            bot.reply_to(message, "✅ پیامت ارسال شد! 🙌")
        except Exception as e:
            bot.reply_to(message, f"⚠️ ارسال پیام به ادمین انجام نشد.\n{e}")
    else:
        bot.reply_to(message, "ادمین تعریف نشده!")


def main_menu():
    """منوی اصلی دوباره"""
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("🌐 پرتال من", url=SITE_BASE),
        telebot.types.InlineKeyboardButton("🛡️ خرید VPN", url="https://t.me/iliiyo"),
        telebot.types.InlineKeyboardButton("✉️ تماس با من", callback_data="contact"),
        telebot.types.InlineKeyboardButton("🆘 راهنما", callback_data="help")
    )
    return markup


# --- اجرای ربات (Polling برای Render) ---
if __name__ == "__main__":
    print("🚀 Bot is running ...")
    bot.infinity_polling(skip_pending=True, timeout=30)