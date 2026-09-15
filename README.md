# Telegram 文件直链机器人（中文版）

把 Telegram 里的任意文件变成可以直接播放/下载的网页直链，无需先把文件下载下来。

- 机器人所有提示语、按钮均已汉化
- 支持视频、音频在线播放（浏览器 / 播放器直接打开）
- 支持 Render、Koyeb、VPS、Docker 部署

> 需要 Python 3.12 或更高版本。

## 快速部署

详细中文步骤见 [docs/INSTALL.md](docs/INSTALL.md)。

## 必填环境变量

| 变量 | 说明 |
| --- | --- |
| `API_ID` | 在 https://my.telegram.org 获取 |
| `API_HASH` | 在 https://my.telegram.org 获取 |
| `BOT_TOKEN` | 向 [@BotFather](https://t.me/BotFather) 申请机器人后获得 |
| `BIN_CHANNEL` | 存档频道的 ID（负数，形如 `-1001234567890`） |

## 常用可选变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `FQDN` | 绑定地址 | 你的域名，例如 `myapp.onrender.com`，部署完成后必须填写 |
| `HAS_SSL` | `false` | 设为 `true` 时生成 https 链接（Render/Koyeb 都要设为 true） |
| `NO_PORT` | `false` | 设为 `true` 时链接里不显示端口（Render/Koyeb 都要设为 true） |
| `PORT` | `8080` | 网页服务端口，平台通常会自动注入 |
| `ALLOWED_USERS` | 空 | 允许使用的用户 ID，逗号分隔；留空表示所有人可用 |
| `BLOCKED_USERS` | 空 | 禁止使用的用户 ID，逗号分隔，优先级最高 |
| `KEEP_ALIVE` | `false` | 设为 `true` 时定时自我访问，防止免费实例休眠 |
| `PING_INTERVAL` | `600` | 自我访问间隔（秒） |
| `REQUEST_LIMIT` | `5` | 单个 IP 同时允许的请求数 |
| `CHUNK_SIZE` | `1048576` | 每次向 Telegram 请求的分块大小（字节） |
| `CACHE_SIZE` | `128` | 每个客户端缓存的文件信息条数 |
| `CACHE_CHUNK` | `2` | 预读的分块数量，越大越流畅、越占内存 |
| `CONNECTION_LIMIT` | `20` | 到单个 Telegram 数据中心的最大连接数 |
| `HASH_LENGTH` | `6` | 链接校验串长度（6–63），越长越难被猜到 |
| `NO_UPDATE` | `false` | 设为 `true` 时机器人不回复任何消息（仅做网页服务） |
| `MULTI_TOKEN1`, `MULTI_TOKEN2`… | 空 | 额外的机器人 Token，用于多号分流提速 |

## 使用方式

1. 给机器人发送 `/start`
2. 直接把文件发给它
3. 它会回复直链，视频/音频还会附带「▶️ 在线播放」按钮

## 状态检查

访问 `https://你的域名/status` 可以查看运行状态与在线时长。

## 致谢

基于 [SpringsFern/TG-FileStreamBot](https://github.com/SpringsFern/TG-FileStreamBot)、
[EverythingSuckz/TG-FileStreamBot](https://github.com/EverythingSuckz/TG-FileStreamBot) 与
[tulir/TGFileStream](https://github.com/tulir/TGFileStream)。
