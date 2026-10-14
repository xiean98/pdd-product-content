#!/usr/bin/env bash
# 开工前运行：拉取其他 AI / 设备最新的风格族与产品记忆
# 路径无关：自动定位到本脚本上一级（仓库根）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "[sync_pull] 仓库: $ROOT"
if [ ! -d .git ]; then
  echo "[sync_pull] 该目录不是 git 仓库，跳过（首次需在能联网的环境克隆）"
  exit 0
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "[sync_pull] 尚未配置 remote origin，跳过拉取（仅本地模式）"
  exit 0
fi
if git pull --rebase --autostash; then
  echo "[sync_pull] 已同步到最新"
else
  echo "[sync_pull] !! 拉取冲突或失败。请先解决冲突（风格族为追加式，通常保留双方），再继续；禁止强制覆盖。"
  exit 1
fi
