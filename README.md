# CompanionCare 陪诊守护 🏥

**子女视角的陪诊服务平台**

> 你在1000公里外，妈妈在老家生病了。陪诊守护，让子女安心。

CompanionCare 是一款专为异地子女设计的陪诊服务平台。不是卖跑腿服务，是卖"让子女安心"——以数据驱动的精准匹配、风控保障、和长期健康档案，构建陪诊服务的壁垒。

## ✨ 核心特点

### 💡 情感定位
- **不是陪诊平台，是子女的"安心代理"**
- 目标用户：异地子女（付款者）× 老年患者（使用者）
- 核心卖点：让子女安心，不只是帮老人看病

### 🎯 数据驱动匹配
- 老人健康档案（病史 + 常去医院 + 过敏药物）
- 陪诊师能力画像（擅长科室 + 好评率 + 响应速度）
- 医院实战攻略（各医院陪诊技巧自动积累）

### 🛡️ 风控保障（行业标配）
- 陪诊服务免责协议（白纸黑字写清服务范围）
- 职业责任险（每次陪诊自动投保）
- 陪诊师实名认证 + 健康证核验

### 🔄 复购提醒（核心壁垒）
- AI 自动计算下次复查时间
- 系统主动推送复诊提醒给子女
- 陪诊师长期绑定，复购无需重新匹配

## 📊 产品数据

| 维度 | 数据 |
|------|------|
| 市场规模 | 1000亿+，35%年增速 |
| 进入门槛 | 极低（无需医疗资质，<1万启动） |
| 差异化定位 | "情感陪伴"无人占 |
| 评分 | **8.5/10，MVP可行** |

## 🚀 快速开始

### 环境要求
- Python 3.8+
- DeepSeek API Key（或其他兼容LLM）

### 安装

```bash
# 克隆仓库
git clone https://github.com/jonhnsonzz/companion-care.git
cd companion-care

# 安装依赖
pip install -r requirements.txt

# 配置
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY

# 运行
python app.py
```

浏览器打开 [http://localhost:5000](http://localhost:5000)

## 🏗️ 项目结构

```
companion-care/
├── app.py                 # Flask 主应用
├── prompts.py             # AI 提示词（匹配逻辑、复诊提醒）
├── requirements.txt       # Python 依赖
├── .env.example           # 环境变量模板
├── templates/
│   ├── index.html        # 首页（子女端）
│   ├── companion.html    # 陪诊师端
│   └── dashboard.html     # 管理端
└── data/
    └── sample_data.json   # 示例数据
```

## 💰 商业模式

| 模式 | 说明 |
|------|------|
| 平台抽佣 | 每单抽15-20%，陪诊师结算 |
| 会员制（季卡/年卡） | 慢病患者专属，覆盖全年陪诊需求 |
| 增值服务 | 肿瘤专科陪诊（800-2000元/单） |

## 📈 演进路线

```
MVP (0-6月)
  → 验证付费意愿（成都三甲医院附近5名陪诊师）
  → 目标：月流水4万，净利润5500元

成长期 (6-18月)
  → 接入养老机构会员（To B）
  → 积累300-500个老人健康档案

规模期 (18-36月)
  → 申请政府养老项目（To G采购）
  → 接入家庭医生数据系统

生态期 (3年+)
  → 健康保险精准推荐（数据变现）
  → 成为空巢老人健康数据基础设施
```

## 🔐 风控体系

| 防护 | 内容 |
|------|------|
| 法律文本 | 陪诊服务协议（服务范围+免责条款） |
| 保险 | 每次陪诊自动投保职业责任险 |
| 认证 | 陪诊师实名+健康证双重核验 |
| 追溯 | 全程定位打卡，子女可实时查看 |

## 🤖 AI 驱动场景

1. **智能匹配**：根据老人病史 + 医院 + 科室，匹配最擅长该领域的陪诊师
2. **复诊提醒**：AI 自动计算下次复查时间，系统主动推送提醒给子女
3. **服务辅助**：陪诊师接单后自动收到该医院的实战技巧（来自历史服务积累）
4. **健康档案**：每次服务后更新老人档案，画像越来越精准

## 🌐 部署

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Railway / Render / 任意云服务器
设置环境变量 `DEEPSEEK_API_KEY`，直接部署即可。

## 📄 开源协议

MIT License

---

**让1000公里外的子女，也能安心。**

---

## 📱 演示页面

陪诊守护的在线演示页（静态landing page）在独立仓库：
👉 **[pei-ban-shouhu](https://github.com/jonhnsonzz/pei-ban-shouhu)** — [在线演示](https://jonhnsonzz.github.io/pei-ban-shouhu/)

- **companion-care** — Flask 后端应用（需部署运行）
- **pei-ban-shouhu** — 静态演示页面（GitHub Pages 直接访问）
