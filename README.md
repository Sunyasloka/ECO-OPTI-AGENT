# ECO-OPTI-AGENT

# EcoOptiAgent – Multi-Agent AI for Carbon Optimization in Businesses 🌱

🚀 Overview
EcoOptiAgent is a multi-agent AI-based system that helps businesses measure, understand, and reduce their carbon footprint across domains like electricity, transport, and infrastructure. It combines a Flask backend with a React.js frontend to deliver intelligent, personalized emission-reduction suggestions.

---

💡 Key Features

1. Multi-agent architecture: Electricity, Transport, Infrastructure, and more
2. Central decision agent combines domain suggestions and user preferences
3. CO₂ emissions estimation by category (tons/year)
4. Suggests alternative plans based on user constraints
5. Clean frontend built with React.js (HTML/CSS/JS)
6. Form-based input and dynamic results display

---

 🛠️ Tech Stack

| Layer      | Technology                 |
|------------|----------------------------|
| Frontend   | React.js, HTML, CSS, JavaScript |
| Backend    | Python, Flask, LangGraph, Gemini API |
| Versioning | Git, GitHub                 |

---

## 📁 Project Structure

EcoOptiAgent/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── decision_agent.py
│   │   ├── electricity_agent.py
│   │   ├── fuel_agent.py
│   │   ├── greeninfra_agent.py
│   │   ├── optimizer_agent.py
│   │   ├── router_agent.py
│   │   └── transport_agent.py
│   ├── prompts/
│   ├── main.py
│   ├── utils.py
│   └── requirement.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── FullLogo_NoBuffer.jpg
│   └── Titillium_Web.zip
├── list_models.py
├── README.md
├── .gitignore
└── .env





