/**
 * Commitlint 配置 - Conventional Commits 规范
 *
 * 提交信息格式: <type>(<scope>): <subject>
 *   <body>
 *   <footer>
 *
 * type 类型说明:
 *   feat     - 新功能
 *   fix      - Bug 修复
 *   docs     - 文档变更
 *   style    - 代码格式（不影响功能）
 *   refactor - 重构（既不是新功能也不是修复）
 *   perf     - 性能优化
 *   test     - 测试相关
 *   build    - 构建系统或外部依赖变更
 *   ci       - CI 配置变更
 *   chore    - 其他杂项（不修改源码也不修改测试）
 *   revert   - 回滚之前的提交
 */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // type 枚举值
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert',
      ],
    ],
    // type 不能为空
    'type-empty': [2, 'never'],
    // type 必须小写
    'type-case': [2, 'always', 'lower-case'],
    // subject 不能为空
    'subject-empty': [2, 'never'],
    // subject 不超过 72 个字符
    'subject-max-length': [2, 'always', 72],
    // subject 不以句号结尾
    'subject-full-stop': [0],
    // header 不超过 100 个字符
    'header-max-length': [2, 'always', 100],
    // body 每行不超过 100 个字符
    'body-max-line-length': [2, 'always', 100],
    // footer 每行不超过 100 个字符
    'footer-max-line-length': [2, 'always', 100],
  },
};
