# 部署教程（中文）

## 第一步：准备三样东西

### 1. API_ID 与 API_HASH

1. 打开 https://my.telegram.org ，用你的 Telegram 手机号登录
2. 进入 **API development tools**，随便填一个应用名
3. 记下 `App api_id` 和 `App api_hash`

### 2. BOT_TOKEN

1. 在 Telegram 里找 [@BotFather](https://t.me/BotFather)
2. 发送 `/newbot`，按提示设置名字和用户名
3. 复制它给你的 Token（形如 `123456:ABC-DEF...`）

### 3. BIN_CHANNEL（存档频道 ID）

1. 新建一个频道（公开或私密都行），把你的机器人加为**管理员**
2. 在频道里随便发一条消息
3. 把这条消息转发给 [@missrose_bot](https://t.me/MissRose_bot)，然后**回复**该转发消息发送 `/id`
4. 复制其中的频道 ID（负数，形如 `-1001234567890`）

---

## 第二步：部署

### 方案 A：Render（推荐，免费额度够用）

1. 把本项目上传到你自己的 GitHub 仓库
2. 打开 https://render.com ，登录后点 **New → Web Service**，选择该仓库
3. 配置：
   - Environment：**Docker**（仓库里已带 `Dockerfile`）
   - Instance Type：Free
4. 在 **Environment Variables** 中添加：

```
API_ID=你的api_id
API_HASH=你的api_hash
BOT_TOKEN=你的bot_token
BIN_CHANNEL=-100xxxxxxxxxx
HAS_SSL=true
NO_PORT=true
KEEP_ALIVE=true
```

5. 点击 Deploy，等待构建完成
6. 复制 Render 给的域名（形如 `myapp.onrender.com`），回到环境变量再加一条：

```
FQDN=myapp.onrender.com
```

7. 保存后服务会自动重启。访问 `https://myapp.onrender.com/status` 显示运行状态即成功。

> 免费实例休眠时首个请求会慢几十秒，`KEEP_ALIVE=true` 可缓解。

### 方案 B：Koyeb（免费实例不休眠）

1. 同样先把项目推到 GitHub
2. 打开 https://app.koyeb.com ，点 **Create Web Service → GitHub**，选择仓库
3. Builder 选 **Dockerfile**
4. Instance 选 Free，Region 建议 Washington 或 Frankfurt
5. **Exposed ports**：端口填 `8080`，路径 `/`
6. 添加环境变量（同上，`HAS_SSL=true`、`NO_PORT=true`）
7. 部署完成后复制 Koyeb 域名（形如 `xxx-yyy.koyeb.app`），补上 `FQDN=xxx-yyy.koyeb.app` 并重新部署

### 方案 C：自己的服务器 / VPS

```bash
git clone <你的仓库地址>
cd TG-FileStreamBot-Telethon-modified
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 然后编辑 .env 填写变量
python -m WebStreamer
```

后台常驻运行可用 `screen`、`tmux` 或 systemd。

用 Docker 更省事：

```bash
docker build -t tg-filestream .
docker run -d --restart always --env-file .env -p 8080:8080 tg-filestream
```

---

## 第三步：验证

1. 浏览器打开 `https://你的域名/status`，应看到 `"server_status": "running"`
2. 在 Telegram 给机器人发 `/start`，应收到中文欢迎语
3. 发一个文件，应收到直链和「📥 下载」按钮；视频/音频还有「▶️ 在线播放」

---

## 常见问题

**收不到任何回复**
检查 `BOT_TOKEN` 是否正确、`NO_UPDATE` 是否被设成了 true、平台日志里有没有报错。

**报错提示频道相关 / 转存失败**
机器人必须是存档频道的管理员，且 `BIN_CHANNEL` 是以 `-100` 开头的负数 ID。

**链接打不开或地址是 `0.0.0.0`**
说明 `FQDN` 没填。填成你的域名（不带 `https://`），并设置 `HAS_SSL=true`、`NO_PORT=true`。

**播放卡顿**
把 `CACHE_CHUNK` 调到 4，或加 `MULTI_TOKEN1`、`MULTI_TOKEN2` 多机器人分流。

**启动时报语法错误**
本项目需要 Python 3.12 以上版本，Dockerfile 已固定为 3.12。

**只想自己用**
设置 `ALLOWED_USERS=你的用户ID`（可向 [@userinfobot](https://t.me/userinfobot) 查询）。
