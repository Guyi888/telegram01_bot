import logging
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

JOKES = [
    "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25。",
    "一个SQL语句走进酒吧，走向两张桌子问道：我可以JOIN你们吗？",
    "程序员的老婆让他去买一升牛奶，如果看到鸡蛋就买12个。程序员回来后买了12升牛奶。",
    "为什么程序员喜欢黑色主题？因为 light 吸引 bug。",
    "递归是什么？请参考"递归"。",
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    keyboard = [
        [
            InlineKeyboardButton("获取时间", callback_data="time"),
            InlineKeyboardButton("讲个笑话", callback_data="joke"),
        ],
        [
            InlineKeyboardButton("掷骰子", callback_data="dice"),
            InlineKeyboardButton("帮助", callback_data="help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"你好，{user.first_name}！我是你的 Telegram 机器人。\n"
        "选择下方功能，或输入 /help 查看所有命令。",
        reply_markup=reply_markup,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "可用命令：\n"
        "/start  - 开始对话（显示菜单按钮）\n"
        "/help   - 查看帮助\n"
        "/echo   - 回显你的消息\n"
        "/time   - 显示当前时间\n"
        "/joke   - 随机讲一个笑话\n"
        "/dice   - 掷一个骰子\n"
        "/calc   - 简单计算（例：/calc 1+2*3）\n\n"
        "也可以直接发送文字，我会鹦鹉学舌地重复给你。"
    )
    await update.message.reply_text(text)


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else "你没有输入任何内容。"
    await update.message.reply_text(f"Echo: {text}")


async def time_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"当前时间：{now}")


async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(random.choice(JOKES))


async def dice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = random.randint(1, 6)
    faces = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
    await update.message.reply_text(f"掷骰子结果：{faces[result]}（点数：{result}）")


async def calc_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    expr = " ".join(context.args)
    if not expr:
        await update.message.reply_text("用法：/calc <表达式>\n示例：/calc 1+2*3")
        return
    # 只允许数字和基本运算符，防止代码注入
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expr):
        await update.message.reply_text("只支持基本数学运算（+ - * / 括号）。")
        return
    try:
        result = eval(expr, {"__builtins__": {}})
        await update.message.reply_text(f"{expr} = {result}")
    except Exception:
        await update.message.reply_text("表达式有误，请检查后重试。")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "time":
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await query.edit_message_text(f"当前时间：{now}")
    elif query.data == "joke":
        await query.edit_message_text(random.choice(JOKES))
    elif query.data == "dice":
        result = random.randint(1, 6)
        await query.edit_message_text(f"掷骰子结果：点数 {result}")
    elif query.data == "help":
        await query.edit_message_text(
            "可用命令：\n"
            "/start /help /echo /time /joke /dice /calc"
        )


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("echo", echo_command))
    app.add_handler(CommandHandler("time", time_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("dice", dice_command))
    app.add_handler(CommandHandler("calc", calc_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    logger.info("Bot 已启动，按 Ctrl+C 停止。")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
