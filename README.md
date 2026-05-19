# gohanpass-web-monitor

`go.hanpass` 자동화 Notion Raw data를 표시하는 모니터입니다.

## URLs

GitHub Pages:

```text
https://mhjang-qa.github.io/gohanpass-web-monitor/index.html
https://mhjang-qa.github.io/gohanpass-web-monitor/embed.html
```

Notion 임베드용은 `embed.html`을 사용합니다.

## Important

GitHub Pages는 정적 호스팅이므로 Notion API를 직접 호출하지 않습니다.  
실데이터를 바로 보이게 하려면 공개 HTTPS 백엔드가 필요합니다.

## Backend Setup

이 저장소에는 Render 배포용 [render.yaml](/private/tmp/gohanpass-web-monitor/render.yaml) 이 포함되어 있습니다.

배포 후 예시 백엔드 URL:

```text
https://YOUR-BACKEND-DOMAIN
```

헬스체크:

```text
https://YOUR-BACKEND-DOMAIN/health
```

API:

```text
https://YOUR-BACKEND-DOMAIN/api/monitor
```

## How To Make Embed Work Immediately

루트 [config.js](/private/tmp/gohanpass-web-monitor/config.js) 에 백엔드 주소를 넣습니다.

```js
window.MONITOR_API_BASE = "https://YOUR-BACKEND-DOMAIN";
```

그러면 아래 URL을 Notion에 바로 임베드할 수 있습니다.

```text
https://mhjang-qa.github.io/gohanpass-web-monitor/embed.html
```

또는 query parameter 방식도 가능합니다.

```text
https://mhjang-qa.github.io/gohanpass-web-monitor/embed.html?api=https://YOUR-BACKEND-DOMAIN
```

## Local Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py
```

로컬 접속:

```text
http://127.0.0.1:8080
http://127.0.0.1:8080/embed
```

## Environment

`.env` 또는 `.env.example`:

```env
NOTION_TOKEN=secret_xxx
NOTION_DB_ID=5ad73fbd195182bcb4b201fb9d76815f
TIMEZONE=Asia/Seoul
HOST=0.0.0.0
PORT=8080
```
