#!/usr/bin/env bash
# IndexNow ping — submits every URL in sitemap.xml to the IndexNow endpoint.
# HONEST NOTE: Google does NOT participate in IndexNow. This nudges Bing,
# Yandex, Seznam and Naver only. Google discovery relies on sitemap + GSC.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KEYFILE="$(ls "$ROOT"/work/.indexnow-key 2>/dev/null)"
KEY="$(tr -d '[:space:]' < "$KEYFILE")"
HOST="brycespatios.work"
MAP="$ROOT/sitemap.xml"

if [ -z "$KEY" ] || [ ! -f "$ROOT/$KEY.txt" ]; then
  echo "IndexNow: key file missing ($KEY.txt). Aborting." >&2
  exit 1
fi

URLS=$(python3 - "$MAP" <<'PY'
import re, sys
x = open(sys.argv[1], encoding="utf-8").read()
print("\n".join(re.findall(r"<loc>(.*?)</loc>", x)))
PY
)
COUNT=$(printf '%s\n' "$URLS" | grep -c .)
JSON=$(python3 - <<PY
import json
urls = """$URLS""".split()
print(json.dumps({
  "host": "$HOST",
  "key": "$KEY",
  "keyLocation": "https://$HOST/$KEY.txt",
  "urlList": urls,
}))
PY
)
echo "IndexNow: submitting $COUNT urls to api.indexnow.org"
curl -sS -o /tmp/indexnow-out.txt -w 'HTTP %{http_code}\n' \
  -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  --data "$JSON"
echo "body: $(cat /tmp/indexnow-out.txt)"
