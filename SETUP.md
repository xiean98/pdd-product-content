# 新设备 / 新 AI 接入指南

本 skill 通过 GitHub 私有仓库在多台设备、多个 AI 之间共享同一份记忆（风格库、产品档案、经验）。仓库地址（私有）：

```
https://github.com/xiean98/pdd-product-content
```

> 给 AI 的话：以下命令请在“当前环境”真实执行；路径按本环境实际情况定位，不要照抄示例路径。

---

## 一、首次接入（有终端、能装/用 git 与 gh）

1. 确认工具：
   ```bash
   git --version && gh --version
   ```
   没有 `gh` 也可，见“三、只有 git 没有 gh”。

2. 登录 GitHub（设备码方式，不需要把密码贴进对话）：
   ```bash
   gh auth login --hostname github.com --web
   # 按提示打开 https://github.com/login/device，输入一次性码并 Authorize
   gh auth setup-git        # 让 git 复用 gh 的凭证
   ```

3. 定位本环境的用户技能目录（结尾为 `workspace/.user_skills`），进入它：
   ```bash
   # 常见位置：~/.doubao/agent_mode/workspace/.user_skills 或同类 agent 工作区
   cd <workspace>/.user_skills
   ```

4. 克隆仓库（目录名即技能名）：
   ```bash
   git clone https://github.com/xiean98/pdd-product-content.git
   ```
   若该目录已存在旧副本（如曾用 zip 放入）：先备份/删除旧目录再 clone，或进入目录执行 `git init && git remote add origin <url> && git fetch && git reset --hard origin/main`。

5. 验证：
   ```bash
   cd pdd-product-content && bash scripts/sync_pull.sh
   ```

---

## 二、日常使用（每次会话）

- 开工第一步：`bash scripts/sync_pull.sh`
- 收工最后一步：`bash scripts/sync_push.sh "feat(<产品>): 改了什么"`
- 这两步已写进 `SKILL.md`，AI 应自动执行，无需用户提醒。

---

## 三、只有 git、没有 gh（用个人访问令牌 PAT）

1. 在 GitHub：Settings → Developer settings → Personal access tokens → 生成勾选 `repo` 权限的令牌。
2. 克隆/推送时用该令牌（更安全的做法是用 credential helper，不要把令牌写进仓库或命令历史）：
   ```bash
   git clone https://github.com/xiean98/pdd-product-content.git
   git -C pdd-product-content push   # 用户名填 GitHub 用户名，密码粘贴 PAT
   ```

---

## 四、只有网页对话的 AI（无终端）

- 让它产出：在仓库页面 **Code → Download ZIP** 下载最新版喂给它。
- 回写：让它输出需要新增/修改的文件，由你或有终端的 AI 合并后提交；或在支持的 AI 上接 **GitHub MCP** 直接读写仓库。

---

## 五、常见问题

- **pull 冲突**：在风格族/产品记忆的追加式改动上，通常保留双方；`git pull --rebase` 后手动解决再 `git rebase --continue`，禁止 `push -f` 强制覆盖。
- **push 要求登录 / 403**：重新 `gh auth login` 或更新 PAT；确认账号对私有仓库有写权限。
- **网络**：GitHub 不通时可临时改用 Gitee 镜像；无网络时先本地完成，在能联网环境补跑 `sync_push.sh`。
- **图片/成品图不进 Git**：仓库只存文本记忆；原图、成品图、压缩包放飞书云盘/项目空间（见 `.gitignore`）。
