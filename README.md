# HealthCockpit 🛡️ v1.1.0

A comprehensive, private health dashboard to track vitals, laboratory results, nutrition, medication, and lifestyle habits.

## Key Features

- **📊 Dashboard:** High-level overview of weight, hydration, steps, and mood.
- **🩸 Lab Markers:** Track blood values with visual range indicators (Low/Normal/High).
- **💓 Vital Signs:** Monitor blood pressure and pulse.
- **⚖️ Body Composition:** Detailed weight tracking including Fat%, BMI, Muscle Mass, Protein, BMR, Visceral Fat, and Bone Mass.
- **💊 Medication:** Track treatment with custom dose units (Tablets, Drops, etc.) and quick-select buttons.
- **😴 Lifestyle:** Log sleep quality, water intake, and daily steps.
- **🍎 Nutrition:** Detailed macro-logging (P/C/F) and calorie tracking.
- **📅 Day View:** Full exhaustive summary of every single entry for any specific day.
- **✏️ Universal Edit:** Ability to edit or delete any recorded entry across all categories.
- **🌙 Dark Mode:** Premium high-contrast interface.
- **📄 PDF Export:** Professional, chronological health reports.

## Changelog

### v1.1.0 (Februar 2026)
- **NEW:** Expanded weight metrics (Körperfett, BMI, Muskelmasse, Grundumsatz, etc.).
- **NEW:** Time tracking for weight entries (allows multiple weigh-ins per day).
- **NEW:** Universal Edit system - Modify any entry (Labs, Vitals, Food, etc.) after saving.
- **NEW:** Master Data Management - Edit or delete predefined Blood Markers and Medication types.
- **IMPROVED:** Timezone synchronization between Docker host and container.
- **UI:** New icons and layout improvements for the weight history and daily summary.

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
   docker compose up -d --build
   ```
2. **Access:** `http://localhost:8130` or `http://IP_OF_DOCKER_SERVER:8130`

*Created for privacy-focused health management.*

<img width="1256" height="859" alt="Dashboard" src="https://github.com/user-attachments/assets/2fe12835-f1fc-4a09-aab0-d776b09d256c" />

<img width="1253" height="859" alt="Analytics" src="https://github.com/user-attachments/assets/43cd7dbf-a3fa-48e5-ac83-054095a5d5d4" />
