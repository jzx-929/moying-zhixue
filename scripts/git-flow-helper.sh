#!/usr/bin/env bash
#
# Git Flow 辅助脚本
# 快速创建和管理 Git Flow 分支
#
# 用法:
#   ./scripts/git-flow-helper.sh feature <功能名>   # 创建功能分支
#   ./scripts/git-flow-helper.sh hotfix <问题描述>   # 创建热修复分支
#   ./scripts/git-flow-helper.sh release <版本号>    # 创建发布分支
#   ./scripts/git-flow-helper.sh finish              # 完成当前分支（推送+提示创建PR）
#   ./scripts/git-flow-helper.sh sync                # 同步 develop 最新代码

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}Git Flow 辅助脚本${NC}"
    echo ""
    echo "用法:"
    echo "  $0 feature <功能名>    从 develop 创建功能分支 feature/<功能名>"
    echo "  $0 hotfix <问题描述>   从 main 创建热修复分支 hotfix/<问题描述>"
    echo "  $0 release <版本号>    从 develop 创建发布分支 release/<版本号>"
    echo "  $0 finish              推送当前分支到远程并提示创建 PR"
    echo "  $0 sync                同步 develop 分支最新代码"
    echo ""
    echo "示例:"
    echo "  $0 feature rag-search"
    echo "  $0 hotfix login-crash"
    echo "  $0 release v1.0.0"
}

create_feature() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}错误: 请提供功能名称${NC}"
        echo "  用法: $0 feature <功能名>"
        exit 1
    fi

    echo -e "${BLUE}从 develop 创建功能分支: feature/${name}${NC}"
    git checkout develop
    git pull origin develop
    git checkout -b "feature/${name}"
    echo -e "${GREEN}✓ 已创建并切换到 feature/${name}${NC}"
    echo -e "${YELLOW}提示: 开发完成后运行 '$0 finish' 推送并创建 PR${NC}"
}

create_hotfix() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}错误: 请提供问题描述${NC}"
        echo "  用法: $0 hotfix <问题描述>"
        exit 1
    fi

    echo -e "${BLUE}从 main 创建热修复分支: hotfix/${name}${NC}"
    git checkout main
    git pull origin main
    git checkout -b "hotfix/${name}"
    echo -e "${GREEN}✓ 已创建并切换到 hotfix/${name}${NC}"
    echo -e "${YELLOW}提示: 修复完成后合并到 main 和 develop${NC}"
}

create_release() {
    local version=$1
    if [ -z "$version" ]; then
        echo -e "${RED}错误: 请提供版本号${NC}"
        echo "  用法: $0 release <版本号>"
        exit 1
    fi

    echo -e "${BLUE}从 develop 创建发布分支: release/${version}${NC}"
    git checkout develop
    git pull origin develop
    git checkout -b "release/${version}"
    echo -e "${GREEN}✓ 已创建并切换到 release/${version}${NC}"
    echo -e "${YELLOW}提示: 发布准备完成后合并到 main，再同步回 develop${NC}"
}

finish_branch() {
    local branch=$(git branch --show-current)

    if [ "$branch" = "main" ] || [ "$branch" = "develop" ]; then
        echo -e "${RED}错误: 不能在 main/develop 分支上执行此操作${NC}"
        exit 1
    fi

    echo -e "${BLUE}当前分支: ${branch}${NC}"

    # 检查是否有未提交的更改
    if [ -n "$(git status --porcelain)" ]; then
        echo -e "${RED}错误: 有未提交的更改，请先提交${NC}"
        git status --short
        exit 1
    fi

    # 推送到远程
    echo -e "${BLUE}推送 ${branch} 到远程仓库...${NC}"
    git push -u origin "$branch"
    echo -e "${GREEN}✓ 已推送到远程${NC}"

    # 提示创建 PR
    local remote_url=$(git remote get-url origin)
    local pr_url="${remote_url%.git}/compare/develop...${branch}?expand=1"

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  分支已推送，请创建 Pull Request${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo -e "${YELLOW}PR 链接: ${pr_url}${NC}"
    echo -e "${YELLOW}目标分支: develop${NC}"
    echo -e "${YELLOW}请确保 PR 标题遵循 Conventional Commits 规范${NC}"
    echo -e "${YELLOW}格式: <type>(<scope>): <subject>${NC}"
}

sync_develop() {
    echo -e "${BLUE}同步 develop 分支最新代码...${NC}"
    git checkout develop
    git pull origin develop
    echo -e "${GREEN}✓ develop 分支已更新${NC}"
}

# 主逻辑
case "$1" in
    feature)
        create_feature "$2"
        ;;
    hotfix)
        create_hotfix "$2"
        ;;
    release)
        create_release "$2"
        ;;
    finish)
        finish_branch
        ;;
    sync)
        sync_develop
        ;;
    *)
        print_usage
        ;;
esac
