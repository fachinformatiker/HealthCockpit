# HealthCockpit 🛡️

A comprehensive, private health dashboard to track vitals, laboratory results, nutrition, medication, and lifestyle habits.

## Key Features

- **📊 Dashboard:** High-level overview of weight, hydration, steps, and mood.
- **🩸 Lab Markers:** Track blood values with visual range indicators (Low/Normal/High).
- **💓 Vital Signs:** Monitor blood pressure and pulse.
- **💊 Medication:** Track treatment with custom dose units (Tablets, Drops, etc.) and quick-select buttons.
- **😴 Lifestyle:** Log sleep quality, water intake, and daily steps.
- **🍎 Nutrition:** Detailed macro-logging (P/C/F) and calorie tracking.
- **📅 Day View:** Full exhaustive summary of every single entry for any specific day.
- **🌙 Dark Mode:** Premium high-contrast interface.
- **📄 PDF Export:** Professional, chronological health reports.

## Tech Stack

- **Backend:** Python (Flask), SQLAlchemy
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, Chart.js
- **Container:** Docker & Docker Compose (V2)

## Quick Start

1. **Clone & Run:**
   ```bash
   git clone https://github.com/fachinformatiker/healthcockpit.git
   cd healthcockpit
   docker compose up -d
   ```
2. **Access:** `http://localhost:8130` or `http://IP_OF_DOCKER_SERVER:8130`

*Created for privacy-focused health management.*
