# CompanionCare — Elderly Hospital Companion Service 🏥

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**A companion service platform designed for adult children living away from their elderly parents.**

> Your mom is sick back home, and you're a thousand kilometers away. CompanionCare gives you peace of mind.

CompanionCare is a Flask-based backend platform purpose-built for adult children who live apart from their aging parents. It is not merely a delivery service for hospital chaperones — it sells **peace of mind**. Powered by data-driven matching, risk control guarantees, and long-term health records, CompanionCare builds a true moat in the elder companionship service market.

---

## 🔍 The Problem

- **1000+ km away** — Adult children cannot take time off to accompany parents to hospital visits.
- **Elderly struggle with hospitals** — Navigating registrations, consultations, payments, and pharmacy queues is overwhelming for seniors.
- **No accountability** — Existing services lack vetting, insurance, and follow-up mechanisms.
- **Emotional burden** — Children feel guilty and anxious, not knowing if their parents received proper care.

CompanionCare bridges this gap by providing a trusted, insured, AI-enhanced companion who acts as the child's **"peace-of-mind proxy."**

---

## ✨ Features

### 🧠 Emotional Positioning
- **Not a companion platform — your child's "peace-of-mind agent"**
- Target users: Remote adult children (payers) × Elderly patients (users)
- Core value proposition: Peace of mind for children, not just hospital help for seniors

### 🎯 AI-Powered Data Matching
- Elderly health profiles (medical history + frequent hospitals + drug allergies)
- Companion skill profiles (specialty departments + ratings + response speed)
- Crowdsourced hospital guides (automatically accumulated tips for each hospital)

### 🛡️ Risk Control & Insurance
- Legally binding companion service agreements (clear scope + disclaimers)
- Professional liability insurance (automatically enrolled per visit)
- Real-name verification + health certificate checks for all companions

### 🔄 Smart Follow-up Reminders
- AI automatically calculates next checkup date based on diagnosis
- Proactive push notifications to the child's device
- Long-term companion binding — no need to re-match for recurring visits

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- DeepSeek API Key (or any compatible LLM API key)

### Installation

```bash
# Clone the repository
git clone https://github.com/jonhnsonzz/companion-care.git
cd companion-care

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and fill in DEEPSEEK_API_KEY

# Run the app
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🏗️ Project Structure

```
companion-care/
├── app.py                 # Flask main application
├── prompts.py             # AI prompts (matching logic, follow-up reminders)
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── templates/
│   ├── index.html        # Landing page (child-facing)
│   ├── companion.html    # Companion-facing dashboard
│   └── dashboard.html     # Admin dashboard
└── data/
    └── sample_data.json   # Sample/seed data
```

---

## 💰 Business Model

| Model | Description |
|-------|-------------|
| Platform Commission | 15–20% per order, settled with the companion |
| Subscription (Quarterly/Annual) | Chronic disease patients — covers all visits for the period |
| Premium Services | Oncology specialist accompaniment (¥800–2000/visit) |

---

## 🤖 AI Features

1. **Smart Matching** — Matches the best companion based on patient history + hospital + department
2. **Follow-up Reminders** — AI calculates next checkup date and pushes reminders to the child
3. **Service Assistance** — Companions receive hospital-specific tips upon accepting a booking
4. **Health Records** — Profiles are updated after each visit, continuously improving accuracy

---

## 📈 Product Metrics

| Dimension | Data |
|-----------|------|
| Market Size | ¥100B+, 35% annual growth |
| Entry Barrier | Very low (no medical license required, <¥10K startup) |
| Differentiation | "Emotional companionship" — an unoccupied niche |
| Viability Score | **8.5/10, MVP feasible** |

---

## 🗺️ Roadmap

```
MVP (0–6 months)
  → Validate willingness to pay (5 companions near Chengdu top hospital)
  → Target: ¥40K monthly revenue, ¥5.5K net profit

Growth (6–18 months)
  → Partner with nursing homes (B2B)
  → Accumulate 300–500 elderly health profiles

Scale (18–36 months)
  → Apply for government elderly-care procurement (B2G)
  → Integrate with family doctor data systems

Ecosystem (3 years+)
  → Precision health insurance recommendations (data monetization)
  → Become the health data infrastructure for empty-nest seniors
```

---

## 🔐 Risk Control System

| Protection | Details |
|------------|---------|
| Legal | Companion service agreement (service scope + liability disclaimers) |
| Insurance | Professional liability insurance auto-enrolled per visit |
| Verification | Real-name + health certificate dual-check for all companions |
| Traceability | GPS check-in throughout the visit — children can monitor in real time |

---

## 🌐 Deployment

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

### Railway / Render / Any Cloud Server
Set the environment variable `DEEPSEEK_API_KEY` and deploy directly.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Peace of mind for children a thousand kilometers away.**

---

## 📱 Demo Page

The static landing page for CompanionCare lives in a separate repository:
👉 **[pei-ban-shouhu](https://github.com/jonhnsonzz/pei-ban-shouhu)** — [Live Demo](https://jonhnsonzz.github.io/pei-ban-shouhu/)

- **companion-care** — Flask backend application (requires deployment)
- **pei-ban-shouhu** — Static landing page (accessible via GitHub Pages)

---

[中文说明](README_CN.md)
