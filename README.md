# gohanpass-web-monitor

`go.hanpass` 자동화의 Notion Raw data를 읽어 KPI, 현재 상태, 최근 실패, 반복 실패, 버전별 상태, 실행 기록을 보여주는 경량 모니터입니다.

## What It Serves

- `/` : 일반 대시보드
- `/embed` : Notion 임베드용 대시보드
- `/api/monitor` : 모니터 집계 JSON
- `/health` : 헬스체크

## Requirements

- Python 3.11+
- Notion integration token
- Notion database id

기본 대상 DB:

```text
5ad73fbd195182bcb4b201fb9d76815f
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

`.env`가 없으면 `.env.example`를 fallback으로 읽습니다.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py
```

접속:

```text
http://127.0.0.1:8080
http://127.0.0.1:8080/embed
```

## Data Behavior

- Notion API 조회 성공 시 실데이터를 표시합니다.
- Notion 조회 실패 시 샘플 데이터로 fallback 합니다.
- 화면 상단 배지로 `Notion Live` 또는 `샘플 데이터`를 구분합니다.

## Notion Schema Recommendation

| 컬럼명 | 타입 | 설명 |
| --- | --- | --- |
| 제목 | title | 실행 리포트명 |
| 버전 | rich_text 또는 select | 릴리즈/빌드 버전 |
| 플랫폼 | select | `WEB_CHROME_SERVER` |
| PASS | number | 통과 TC 수 |
| FAIL | number | 실패 TC 수 |
| N/A | number | 제외/미실행 TC 수 |
| Total | number | 전체 TC 수 |
| 상태 | status 또는 select | 성공/실패/실행중 |
| 테스트 결과 | select | 테스트 성공/테스트 실패 |
| 결과 | rich_text | 원본 실행 로그 |
| 등록일 | date | 실행 시각 |
| 스냅샷 | files | 실패/최신 화면 이미지 |

## Notes

- GitHub Pages만으로는 Notion secret을 안전하게 보관할 수 없습니다.
- 외부 공개 시에는 인증 또는 사내망 제한이 필요합니다.

## 의존성 보안 점검 (2026-10-22)

기존 FastAPI 스택을 유지하면서 공개 보안 권고가 있는 고정 의존성을 수정 버전으로 갱신했습니다. FastAPI/Starlette의 보안 수정과 함께 사용 중인 패키지만 업데이트하며, `pip check`와 기존 테스트 또는 로컬 smoke 검증을 수행했습니다. 정확한 버전은 `requirements.txt`를 따릅니다. 새 환경에서 다시 설치한 뒤 배포하세요.
