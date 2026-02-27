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

*Created for privacy-focused health management by Patrick Szalewicz.*


<img width="1227" height="859" alt="Dashboard" src="https://github.com/user-attachments/assets/e15936b5-6ccc-4569-9a37-62a303c68c6d" />

<img width="1225" height="856" alt="Analytics" src="https://github.com/user-attachments/assets/be927a0b-f793-4074-90cf-8b95ff0bff01" />

<img width="1221" height="852" alt="Daily view" src="https://github.com/user-attachments/assets/32abcc1b-274a-4ac6-bbdb-e49e55d3c2b4" />
