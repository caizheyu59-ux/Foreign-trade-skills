# 外贸客户列表示例

## 使用说明

1. 将此文件复制到您的工作区并重命名为 `foreign-trade-customers.md`
2. 根据您的实际客户信息修改下面的示例
3. 系统会自动读取此文件并识别需要激活的客户

---

## 客户列表

### 示例条目 1：新客户（2天未回复 - 活跃状态）

- Sophie Dubois - Paris Tech Vision - France
  - 询盘产品: Digital Signage
  - 最后回复时间: 2026-03-18
  - 联系方式: Email
  - 联系ID: sophie@paristech.fr
  - 未回复天数: 2
  - 跟进次数: 0
  - 状态: 活跃
  - 备注: 需要30套数字标牌，已发样品视频

### 示例条目 2：待激活客户（5天未回复）

- John Smith - ABC Trading Co. - USA
  - 询盘产品: LED Display Screens
  - 最后回复时间: 2026-03-15
  - 联系方式: WhatsApp
  - 联系ID: +1 555 123 4567
  - 未回复天数: 5
  - 跟进次数: 0
  - 状态: 待激活
  - 备注: 询盘100台LED屏幕，等待报价反馈

### 示例条目 3：需要催促（10天未回复）

- Maria Garcia - EuroTech Solutions - Spain
  - 询盘产品: Video Conference System
  - 最后回复时间: 2026-03-10
  - 联系方式: Email
  - 联系ID: maria@eurotech.es
  - 未回复天数: 10
  - 跟进次数: 1
  - 状态: 待激活
  - 备注: 需要20套会议系统，已发报价

### 示例条目 4：最后机会（15天未回复）

- Ahmed Hassan - Middle East Digital - UAE
  - 询盘产品: Interactive Whiteboard
  - 最后回复时间: 2026-03-05
  - 联系方式: WhatsApp
  - 联系ID: +971 50 123 4567
  - 未回复天数: 15
  - 跟进次数: 2
  - 状态: 待激活
  - 备注: 需要50块互动白板，对价格敏感

### 示例条目 5：大型项目（12天未回复）

- Raj Patel - Mumbai Electronics - India
  - 询盘产品: LED Video Wall
  - 最后回复时间: 2026-03-08
  - 联系方式: WhatsApp
  - 联系ID: +91 98 765 4321
  - 未回复天数: 12
  - 跟进次数: 1
  - 状态: 待激活
  - 备注: 需要200平米LED视频墙，大型项目

### 示例条目 6：已关闭客户（超过15天）

- David Chen - Singapore Tech Pte Ltd - Singapore
  - 询盘产品: Transparent OLED
  - 最后回复时间: 2026-02-28
  - 联系方式: Email
  - 联系ID: david@sgtech.sg
  - 未回复天数: 20
  - 跟进次数: 3
  - 状态: 已关闭
  - 备注: 跟进3次无回复，已关闭

---

## 字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| 客户姓名 | 客户的名字 | John Smith |
| 公司名称 | 客户所在公司 | ABC Trading Co. |
| 国家 | 客户所在国家 | USA |
| 询盘产品 | 客户咨询的产品 | LED Display Screens |
| 最后回复时间 | 上次联系的日期 | 2026-03-15 |
| 联系方式 | WhatsApp/Email/Feishu | WhatsApp |
| 联系ID | 电话号码或邮箱 | +1 555 123 4567 |
| 未回复天数 | 距离今天的天数 | 5 |
| 跟进次数 | 已跟进次数 | 1 |
| 状态 | 活跃/待激活/已关闭 | 待激活 |
| 备注 | 重要信息 | 询盘100台LED屏幕 |

---

## 规则说明

1. **状态自动更新** - 系统每天自动计算未回复天数
2. **自动标记** - 超过15天未回复自动标记为"已关闭"
3. **跟进限制** - 同一客户最多跟进3次
4. **每日上限** - 每天最多发送5条激活消息

---

## 提示

- 定期更新"最后回复时间"字段
- 记录每次跟进的结果在"备注"中
- 重要客户可以标记为高优先级
- 已成交客户可以标记为"已完成"
