# 墨影智学 - 团队协作与开发规范

## Git Flow 分支策略

本项目采用 **Git Flow** 分支模型，确保代码质量和版本稳定性。

### 分支结构

| 分支 | 命名规则 | 用途 | 保护规则 |
|------|----------|------|----------|
| `main` | `main` | 生产环境稳定分支，只接受来自 `develop` 的合并 | 禁止直接推送，强制 PR + Code Review |
| `develop` | `develop` | 日常开发集成分支，累积已完成的功能 | 禁止直接推送，强制 PR + Code Review |
| `feature/*` | `feature/<功能名>` | 功能开发分支，从 `develop` 分出 | 推送后自动触发 Code Review 请求 |
| `hotfix/*` | `hotfix/<问题描述>` | 紧急修复分支，从 `main` 分出 | 合并后同步回 `develop` |
| `release/*` | `release/<版本号>` | 发布准备分支，从 `develop` 分出 | 用于版本发布前的最终测试 |

### 分支流转图

```
main     ────●──────────────────────────●────────●── (稳定发布)
               \                         ↑        ↑
                \                     release/   hotfix/
                 \                        ↓        ↓
develop  ─────────●───●───●───●───●───●───●────────●── (开发集成)
                      ↑   ↑   ↑   ↑
                      |   |   |   |
feature/a ────●───●───●
feature/b ─────────●───●───●
feature/c ─────────────●───●───●
```

### 分支操作命令

```bash
# 1. 克隆仓库并切换到 develop 分支
git clone https://github.com/jzx-929/moying-zhixue.git
git checkout develop

# 2. 创建新的功能分支（从 develop 分出）
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# 3. 开发完成后提交代码（遵循 Conventional Commits）
git add .
git commit -m "feat(scope): 简短描述变更内容"

# 4. 推送功能分支到远程仓库
git push origin feature/your-feature-name

# 5. 在 GitHub 上创建 Pull Request: feature/* -> develop
#    PR 创建后自动进入 Code Review 流程

# 6. Code Review 通过后合并到 develop
#    使用 Squash Merge 保持提交历史整洁

# 7. develop 累积足够功能后，创建 Release PR: develop -> main
#    经最终 Review 后合并到 main 进行发布
```

---

## Code Review 流程

### 强制规则

1. **所有代码合并前必须通过 Code Review** - 无例外
2. **至少 1 位 Reviewer 审批通过** 才能合并 PR
3. **CI 检查全部通过** 后才允许合并
4. **提交信息必须遵循 Conventional Commits 规范**

### Code Review 步骤

1. **开发者** 从 `develop` 创建 `feature/*` 分支进行开发
2. **开发者** 完成开发后推送到远程并创建 PR（目标分支: `develop`）
3. **Reviewer** 收到通知后审查代码：
   - 代码逻辑是否正确
   - 是否符合项目编码规范
   - 是否有潜在的 安全/性能 问题
   - 测试覆盖是否充分
4. **Reviewer** 提出修改意见或批准通过
5. **开发者** 根据反馈修改并重新推送
6. **所有审批通过 + CI 绿色** 后合并 PR（推荐 Squash Merge）
7. **合并后** 自动删除远程 feature 分支

### PR 模板检查清单

每个 PR 自动加载 `.github/pull_request_template.md` 模板，开发者需确认：
- [ ] 提交信息遵循 Conventional Commits 规范
- [ ] 代码风格符合项目规范
- [ ] 已添加必要的注释
- [ ] 不存在硬编码的敏感信息
- [ ] 已处理边界情况和异常处理

### CODEOWNERS 自动分配

项目根目录 `.github/CODEOWNERS` 定义了各模块的负责人。当 PR 涉及对应模块时，GitHub 会自动请求相关 Reviewer 进行审查。

---

## Conventional Commits 提交规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型说明

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(ai): 添加学科问答模型推理接口` |
| `fix` | Bug 修复 | `fix(backend): 修复分页查询越界问题` |
| `docs` | 文档变更 | `docs: 更新团队协作指南` |
| `style` | 代码格式（不影响功能） | `style(frontend): 统一缩进为2空格` |
| `refactor` | 重构 | `refactor(ai): 重构模型加载逻辑` |
| `perf` | 性能优化 | `perf(backend): 优化数据库查询性能` |
| `test` | 测试相关 | `test(backend): 添加用户认证单元测试` |
| `build` | 构建/依赖变更 | `build: 升级依赖版本` |
| `ci` | CI 配置变更 | `ci: 添加 commitlint 检查工作流` |
| `chore` | 杂项 | `chore: 更新 .gitignore` |
| `revert` | 回滚 | `revert: feat(ai): 添加学科问答模型推理接口` |

### Scope 范围（可选）

| Scope | 对应模块 |
|-------|----------|
| `ai` | AI 模块 |
| `backend` | 后端模块 |
| `frontend` | 前端模块 |
| `docs` | 文档 |
| `ci` | CI/CD |
| `config` | 配置文件 |

### 提交规范验证

项目已配置以下工具自动验证提交信息：

1. **本地 Husky + Commitlint** - 提交时自动检查，不符合规范将被拒绝
2. **GitHub Actions CI** - 推送到远程后再次验证所有提交信息

### 正确示例

```
feat(ai): 添加学科知识库 RAG 检索功能

- 集成向量数据库实现语义检索
- 支持多轮对话上下文管理
- 添加检索结果相关性排序

Closes #42
```

```
fix(backend): 修复 JWT token 过期未刷新的问题

token 过期后前端未正确处理 401 响应，
导致用户需要重新登录。添加自动刷新机制。
```

### 错误示例

```
❌ 更新了代码          (缺少 type)
❌ Added new feature   (应使用中文且需 type)
❌ feat: 修复bug       (type 与描述不匹配)
❌ FEAT: 添加功能      (type 必须小写)
```

---

## 新成员快速上手

### 环境准备

```bash
# 1. 确保已安装 Git 和 Node.js (>=18)
git --version
node --version

# 2. 克隆仓库
git clone https://github.com/jzx-929/moying-zhixue.git
cd moying-zhixue

# 3. 安装依赖（包括 husky git hooks）
npm install

# 4. 切换到 develop 分支开始开发
git checkout develop
```

### 日常开发流程

```bash
# 1. 每天开始前同步最新代码
git checkout develop
git pull origin develop

# 2. 创建今日的功能分支
git checkout -b feature/today-task-name

# 3. 开发... 提交代码（规范提交信息）
git add .
git commit -m "feat(frontend): 添加学科选择组件"

# 4. 推送到远程
git push origin feature/today-task-name

# 5. 在 GitHub 创建 PR，等待 Code Review
# 6. Review 通过后合并，继续下一个任务
```

---

## 分支保护规则总结

| 规则 | main | develop | feature/* |
|------|------|---------|-----------|
| 禁止直接推送 | ✅ | ✅ | ❌ |
| 强制 PR | ✅ | ✅ | 建议 |
| 强制 Code Review | ✅ (≥1人) | ✅ (≥1人) | 建议 |
| 强制 CI 通过 | ✅ | ✅ | 建议 |
| 禁止强制推送 | ✅ | ✅ | ❌ |
| 合并后删除分支 | - | - | ✅ |
