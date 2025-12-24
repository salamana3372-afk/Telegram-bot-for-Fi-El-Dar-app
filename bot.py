from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
import time

# =========================
# إعدادات أساسية
# =========================
BOT_TOKEN = "8542250749:AAFG3PwuPUqv3yqsXMg-pbxiYAsEnYPLE58"
GROUP_ID = -1003686549523
APP_NAME = "في الدار"

# =========================
# تخزين الطلبات (مؤقت)
# =========================
orders = {}  
# order_id : {
#   user_id,
#   status,
#   created_at
# }

# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 أهلاً بيك في {APP_NAME}\n\n"
        "🛒 اطلب كل اللي محتاجه وانت في مكانك\n\n"
        "📦 ابعت /order علشان تعمل طلب"
    )

# =========================
# /order
# =========================
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    order_id = str(int(time.time()))
    orders[order_id] = {
        "user_id": user.id,
        "status": "pending",
        "created_at": time.time()
    }

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ قبول الطلب", callback_data=f"accept|{order_id}"),
            InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject|{order_id}")
        ]
    ])

    text = (
        f"🛒 طلب جديد - {APP_NAME}\n\n"
        f"👤 العميل: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"📦 رقم الطلب: {order_id}"
    )

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=text,
        reply_markup=keyboard
    )

    await update.message.reply_text(
        "✅ تم إرسال طلبك بنجاح\n"
        "⏳ في انتظار رد أقرب محل"
    )

# =========================
# أزرار القبول / الرفض
# =========================
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, order_id = query.data.split("|")

    if order_id not in orders:
        await query.edit_message_text("⚠️ الطلب غير موجود")
        return

    if orders[order_id]["status"] != "pending":
        await query.edit_message_text("⚠️ تم التعامل مع الطلب بالفعل")
        return

    user_id = orders[order_id]["user_id"]
    admin = query.from_user.full_name

    if action == "accept":
        orders[order_id]["status"] = "accepted"

        await query.edit_message_text(
            f"✅ تم قبول الطلب\n\n"
            f"👨‍🍳 بواسطة: {admin}\n"
            f"📦 رقم الطلب: {order_id}"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"🎉 {APP_NAME}\n\n"
                "✅ تم قبول طلبك\n"
                "🚚 جاري التجهيز والتوصيل"
            )
        )

    elif action == "reject":
        orders[order_id]["status"] = "rejected"

        await query.edit_message_text(
            f"❌ تم رفض الطلب\n\n"
            f"👨‍🍳 بواسطة: {admin}\n"
            f"📦 رقم الطلب: {order_id}"
        )

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"{APP_NAME}\n\n"
                "❌ للأسف لم يتم قبول الطلب\n"
                "🔁 حاول مرة أخرى"
            )
        )

# =========================
# تشغيل البوت
# =========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    print(f"🤖 {APP_NAME} Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
