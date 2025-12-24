import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# البوت هيجيب التوكن من Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ID الجروب اللي هيستقبل الطلبات
GROUP_ID = -6240305292  # غيره لو عندك ID مختلف

# رسالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك في بوت *في الدار*\n"
        "📦 ابعت /order علشان تبعت طلبك",
        parse_mode="Markdown"
    )

# أمر /order للعميل يرسل طلب للجروب
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # أزرار القبول والرفض لأصحاب المحلات
    keyboard = [
        [
            InlineKeyboardButton("✅ قبول", callback_data=f"accept_{user.id}"),
            InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user.id}")
        ]
    ]

    # إرسال الطلب للجروب
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=(
            f"📥 *طلب جديد*\n\n"
            f"👤 الاسم: {user.full_name}\n"
            f"🆔 ID: `{user.id}`"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

    # تأكيد للعميل
    await update.message.reply_text("✅ تم إرسال طلبك، انتظر الرد")

# التعامل مع الردود من أصحاب المحلات
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, user_id = query.data.split("_")
    user_id = int(user_id)

    if action == "accept":
        text = "✅ تم قبول طلبك"
    else:
        text = "❌ تم رفض طلبك"

    # إرسال الرد للعميل
    await context.bot.send_message(chat_id=user_id, text=text)

    # تعديل رسالة الجروب بعد الضغط على الزر
    await query.edit_message_text("✔️ تم الرد على الطلب")

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))
    app.add_handler(CallbackQueryHandler(handle_response))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

