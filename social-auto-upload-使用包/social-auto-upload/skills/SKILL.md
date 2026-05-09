# social-auto-upload 多平台社媒发布

当 agent 需要通过 CLI 将视频或图文发布到抖音、快手、小红书、B站、Kingsway 等社交平台时使用这个 skill。

**前提**：social-auto-upload 已安装，sau 命令可用。

## 支持平台

| 平台 | 视频 | 图文 | 定时发布 | 登录方式 | 详情 |
|------|:----:|:----:|:--------:|----------|------|
| 抖音 | YES | YES | YES | Cookie | douyin-upload/SKILL.md |
| 快手 | YES | YES | YES | Cookie | kuaishou-upload/SKILL.md |
| 小红书 | YES | YES | YES | Cookie | xiaohongshu-upload/SKILL.md |
| B站 | YES | NO | YES | Cookie | bilibili-upload/SKILL.md |
| Kingsway | YES | NO | YES | API Key | kingsway-upload/SKILL.md |

## 默认工作流

1. sau --help 确认命令可用
2. sau <platform> check --account <name> 确认登录状态
3. 未登录则引导登录
4. 执行上传命令
5. 检查返回结果

## 视频上传模板

sau <platform> upload-video --account <name> --file <path> --title "标题" --desc "描述" --tags "tag1,tag2"

描述含引号用 --desc-file 避免 shell 问题

## 图文上传模板

sau <platform> upload-note --account <name> --images img1.png img2.png --title "标题" --note "正文"

## 定时发布

sau <platform> upload-video --account <name> --file <path> --title "标题" --desc "描述" --schedule "YYYY-MM-DD HH:MM"

## 平台特有参数

B站: --tid 必填 (249=科技/教程)
抖音: --thumbnail, --product-link, --product-title 可选
Kingsway: 纯API, 首次 sau kingsway setup --account <name> --api-key sk-xxx

## 上传结果反馈

成功: YES <Platform> video 发布成功 + 状态 + 消息 + 链接
失败: NO <Platform> video 发布失败 + 状态 + 消息 + 当前页面

## 各平台详细文档

- 抖音: douyin-upload/SKILL.md + references/
- 快手: kuaishou-upload/SKILL.md + references/
- 小红书: xiaohongshu-upload/SKILL.md + references/
- B站: bilibili-upload/SKILL.md + references/
- Kingsway: kingsway-upload/SKILL.md + references/