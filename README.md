# telegram01_bot

一个用 Python 编写的简单 Telegram 机器人，支持内联按钮菜单、时间查询、笑话、掷骰子和简单计算等功能。

## 功能

| 命令 | 说明 |
|------|------|
| `/start` | 开始对话，显示功能菜单（内联按钮） |
| `/help` | 显示所有可用命令 |
| `/echo <文字>` | 回显指定文字 |
| `/time` | 显示当前时间 |
| `/joke` | 随机讲一个程序员笑话 |
| `/dice` | 掷一个骰子（1-6） |
| `/calc <表达式>` | 计算数学表达式，例如 `/calc 1+2*3` |

直接发送任意文字，机器人会原文回复。

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Guyi888/telegram01_bot.git
cd telegram01_bot
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 Token

打开 `bot.py`，将第 12 行的 `YOUR_BOT_TOKEN_HERE` 替换为你的 Bot Token：

```python
BOT_TOKEN = "你的Token"
```

> 通过 Telegram 中的 [@BotFather](https://t.me/BotFather) 创建机器人并获取 Token。

### 4. 运行

```bash
python bot.py
```

## 项目结构

```
telegram01_bot/
├── bot.py           # 主程序
├── requirements.txt # 依赖列表
└── README.md        # 说明文档
```

## 依赖

- Python 3.8+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) 21.9
