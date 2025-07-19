# 🚴‍♂️ Fitter – FIT File Speed Simulator

**Fitter** is a Streamlit app that reads `.FIT` files from your cycling devices (like Garmin or Wahoo), simulates realistic speed based on elevation gradient, and adjusts timestamps accordingly to reflect more natural cycling behavior on climbs and descents.

---

## 🌟 Features

- 📥 Upload `.FIT` files directly in the browser
- 📍 Parses GPS coordinates and altitude from ride data
- 📈 Calculates distance and elevation gradient between each point
- ⚙️ Applies a simple physics-based speed model (slower uphill, faster downhill)
- 🕒 Generates new timestamps based on adjusted speed
- 📊 Outputs updated ride log with speed and gradient per point
- 📤 Download modified data as CSV (GPX or FIT export coming soon)

---

## 🚀 Getting Started (for local dev)

1. **Clone the repo**

`git clone https://github.com/grahanurdian/fitter.git
cd fitter`

2. **Install dependencies**

`pip install -r requirements.txt`

3. **Run the app**

`streamlit run app.py`

---