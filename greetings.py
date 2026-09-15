import random

GREETINGS = [
    "✨ 你好呀",
    "🌞 今天很适合分享文件！",
    "👋 嗨嗨",
    "📬 有新文件要发吗",
    "🌀 在忙什么呢",
    "🌟 欢迎回来",
    "🎉 一起搞点酷东西吧",
    "🌈 哟",
    "🚀 准备好生成直链了吗",
    "💡 点亮你的文件世界！",
    "📂 是时候发点好东西了",
    "🧊 丢文件我最专业",
]

def greeting():
    return random.choice(GREETINGS)
