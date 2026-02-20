#!/usr/bin/env bash
set -euo pipefail

# WSL/리눅스 공통 사용을 위한 Day 태그 체크아웃 스크립트
DAY="${1:-day08}"

# WSL 환경 여부를 감지해 안내 메시지를 출력합니다.
if grep -qiE "microsoft|wsl" /proc/version 2>/dev/null; then
  echo "[info] WSL 환경에서 실행 중입니다."
fi

# 현재 브랜치에서 안전하게 태그/브랜치로 이동합니다.
if git rev-parse -q --verify "refs/tags/${DAY}" >/dev/null; then
  git checkout "tags/${DAY}"
else
  git checkout "$DAY"
fi

echo "Checked out ${DAY}"
