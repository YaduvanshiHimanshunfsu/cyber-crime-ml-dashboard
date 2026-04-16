# 🚨 Cyber Crime Intelligence System (Pro Max Edition)

## 📌 Overview
The **Cyber Crime Intelligence System** is an advanced, self-learning ecosystem designed to track, analyze, and predict digital crime trends across India. Powered by automated Machine Learning pipelines and a Google-Grounded Gemini AI Engine, this dashboard serves as a comprehensive portal for cyber threat intelligence, comparative state analysis, and digital law provisions.

Created by **Himanshu Yadav** | *B.Tech-M.Tech CSE (Cybersecurity) @ National Forensic Science University (NFSU)*.

## ✨ Advanced Features & Methodologies

### 1. 🧠 Self-Learning ML Prediction (XGBoost + GridSearch)
The system transcends static modeling. Behind the scenes, the training pipeline utilizes `GridSearchCV` to automatically build thousands of permutations across `XGBoost` and `RandomForest` architectures. It scientifically selects the champion hyperparameter configuration through Negative Mean Squared Error (MSE) testing, ensuring predictions scale accurately as new datasets are introduced.

### 2. 🤖 Google-Grounded Multi-Modal AI (Gemini 2.5)
The platform integrates the Google GenAI SDK. Instead of relying purely on historical data cutoffs, the AI Engine natively hooks into the internet via Google Search tools. 
- Discovers live shifts in motives and trends based on recent internet data.
- Built-in diagnostic failovers catch 429 Rate Limits and 503 Server Drops smoothly, keeping the dashboard crash-free.

### 3. 🎨 Premium Dynamic Visualization
Rebuilt from the ground up featuring:
- **Plotly Dark Mode Ecosystem.**
- Smooth `spline` visual tracking, translucent markers, floating tooltips, and interactive heatmap choropleths.
- Embedded CSS animations utilizing Streamlit-Lottie engines.

### 4. ⚖️ Extensive "Cyber Laws & Agencies" Knowledge Base
Provides a fully mapped out, offline legal encyclopedia:
- **BNS, IPC, IT Act** categorizations based on active specific cybercrimes.
- In-depth Government Nodal Agency directories (CERT-In, I4C).
- Dynamic data correlations mapping States to their exact literacy indexes, helplines, and enforcement capabilities.

## 🛠 Technology Stack
- **Dashboard UI:** `Streamlit`, `plotly-express`, `streamlit-lottie`
- **Machine Learning Core:** `scikit-learn`, `xgboost`, `pandas`, `numpy`
- **API & Intelligence:** `FastAPI`, `uvicorn`, `google-genai` (Gemini)

## 🚀 Quick Start Guide
1. **Clone & Setup Environment:**
   ```bash
   python -m venv ai_env
   .\ai_env\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Key:**
   Ensure you export or set your Gemini API key inside your `.env` space:
   ```bash
   set GEMINI_API_KEY="your_actual_key_here"
   ```
4. **Boot Up Services:**
   - *Backend API (Terminal 1):*
     ```bash
     uvicorn app.api:app --reload
     ```
   - *Frontend Dashboard (Terminal 2):*
     ```bash
     python -m streamlit run app/dashboard.py
     ```

## 🔮 Future Scope
- Seamless PostgreSQL integration for real-world automated police reporting hooks.
- Deploying into an AWS / GCP Dockerized environment.
- Implementing deeper NLP analytics on individual unstructured cyber FIR reports.