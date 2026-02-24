# HealthCockpit 🛡️ v1.2.5

A comprehensive, private health dashboard to track vitals, laboratory results, nutrition, medication, and lifestyle habits.

## Key Features

- **📊 Dashboard:** High-level overview of weight, hydration, steps, mood, and **real-time weight loss statistics**.
- **📉 Analytics & Graphs:** Visual trends for weight, blood pressure, and steps (integrated in Dashboard and PDF).
- **⚖️ Body Composition:** Detailed weight tracking (Fat%, BMI, Muscle Mass, etc.) and smart weight loss projection.
- **🍎 Nutrition:** Detailed macro-logging (P/C/F) and calorie tracking with PDF export.
- **📄 PDF Export:** Professional health reports with integrated graphs and meal macros.
- **💾 Full Data Export:** Comprehensive JSON export including all tracked metrics and profile data.
- **🌙 Dark Mode:** Premium high-contrast interface.

## Changelog

### v1.2.5 (Februar 2026)
- **NEW:** **Full JSON Export:** Every data point (Water, Sleep, Mood, Meds, Profile, etc.) is now included in the export.
- **FIX:** Corrected Mood and Energy sliders to use a proper 1-10 scale with clear labels.
- **FIX:** Enhanced database migration resilience for existing installations.

### v1.2.0 (Februar 2026)
- **NEW:** Integrated graphs (Weight, BP, Steps) into the PDF report.
- **NEW:** Meal macros included in the PDF export.
- **NEW:** **Advanced Weight Tracker:** Track total lost, remaining to lose, and estimated goal date (with countdown in days).
- **NEW:** Smart Calculation: Projections prioritize the last 30 days for a realistic "current" trend.
- **NEW:** Target weight setting in the Profile.
- **IMPROVED:** Dashboard overview with color-coded weight progress alert.

### v1.1.0 (Februar 2026)
- **NEW:** Expanded weight metrics (Körperfett, BMI, Muskelmasse, Grundumsatz, etc.).
- **NEW:** Universal Edit system - Modify any entry (Labs, Vitals, Food, etc.) after saving.
- **NEW:** Master Data Management - Edit or delete predefined Blood Markers and Medication types.
- **UI:** New icons and layout improvements.

## Quick Start

1. **Clone & Run:**
   ```bash
   git clone https://github.com/fachinformatiker/healthcockpit.git
   cd healthcockpit
   docker compose up -d --build
   ```
2. **Access:** Open `http://localhost:8130` in your browser.

*Created for privacy-focused health management by fachinformatiker.*

<img width="1256" height="859" alt="Dashboard" src="https://github.com/user-attachments/assets/2fe12835-f1fc-4a09-aab0-d776b09d256c" />

<img width="1253" height="859" alt="Analytics" src="https://github.com/user-attachments/assets/43cd7dbf-a3fa-48e5-ac83-054095a5d5d4" />
