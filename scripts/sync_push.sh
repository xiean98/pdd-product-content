#!/usr/bin/env bash
# 收工前运行：提交并推送本次回写的风格族 / 产品记忆 / 经验
# 用法: bash scripts/sync_push.sh "本次改动说明"
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MSG="${1:-update: 回写产品经验与风格记忆 $(date +%Y-%m-%d_%H%M)}"
if [ ! -d .git ]; then
  echo "[sync_push] 该目录不是 git 仓库，跳过"
  exit 0
fi
git add -A
if git diff --cached --quiet; then
  echo "[sync_push] 无改动，跳过"
  exit 0
fi
git commit -m "$MSG"
if git remote get-url origin >/dev/null 2>&1; then
  if git push; then
    echo "[sync_push] 已提交并推送：$MSG"
  else
    echo "[sync_push] 已本地提交，但 push 失败（检查网络/凭证）。请在能联网环境执行 git push。"
    exit 1
  fi
else
  echo "[sync_push] 已本地提交（尚无 remote，未推送）：$MSG"
fi
