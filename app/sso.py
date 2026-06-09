from __future__ import annotations

from html import escape
import time

from itsdangerous import BadSignature, URLSafeSerializer

from app.config import QA_CONSOLE_ALLOWED_ORIGIN, QA_CONSOLE_SHARED_SECRET


SSO_SALT = "qa-console-sso-v1"
TARGET = "regression"


def validate_sso_token(token: str) -> tuple[dict | None, str | None]:
    if not token:
        return None, "missing"
    if not QA_CONSOLE_SHARED_SECRET:
        return None, "disabled"

    try:
        payload = URLSafeSerializer(QA_CONSOLE_SHARED_SECRET, salt=SSO_SALT).loads(token)
    except BadSignature:
        return None, "invalid"

    if not isinstance(payload, dict):
        return None, "invalid"
    if payload.get("source") != "qa-console":
        return None, "invalid"
    if payload.get("target") != TARGET:
        return None, "invalid"

    expires_at = int(payload.get("exp", 0))
    if expires_at <= int(time.time()):
        return None, "expired"

    return payload, None


def is_allowed_console_referer(referer: str | None) -> bool:
    if not referer:
        return False
    return referer.startswith(QA_CONSOLE_ALLOWED_ORIGIN)


def launch_failure_html(reason: str) -> str:
    safe_reason = escape(reason or "invalid")
    return f"""<!doctype html>
<html lang="ko">
  <head><meta charset="utf-8" /><title>QA Console SSO</title></head>
  <body>
    <script>
      window.location.replace("/?auth_error={safe_reason}");
    </script>
  </body>
</html>"""


def launch_success_html() -> str:
    return """<!doctype html>
<html lang="ko">
  <head><meta charset="utf-8" /><title>QA Console SSO</title></head>
  <body>
    <script>
      window.name = "qa-console-sso";
      window.location.replace("/");
    </script>
  </body>
</html>"""


def logout_cleanup_html() -> str:
    return """<!doctype html>
<html lang="ko">
  <head><meta charset="utf-8" /><title>QA Console Logout</title></head>
  <body>
    <script>
      window.name = "";
      document.body.textContent = "logout";
    </script>
  </body>
</html>"""
