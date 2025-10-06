# ♊ Multi-Agent Code Explainer & Optimizer


An **AI-driven multi-step workflow** that automatically **explains** or **optimizes** code using **LangGraph** and **Gemini (Google Generative AI)**.  
This project demonstrates how **multi-agent systems** can dynamically route tasks — first analyzing user intent, then executing the appropriate agent to deliver results.

---

## ✨ Features
- 🧠 **Intent Detection:** Determines if the user wants *explain* or *optimize* for any code snippet.
- 💬 **Code Explanation Agent:** Provides clear, line-by-line explanations.
- ⚙️ **Optimization Agent:** Refactors code for efficiency, readability, and best practices.
- 🔁 **Conditional Workflow:** Built with **LangGraph** for modular multi-step AI processing.
- 🌐 **Streamlit UI:** Interactive front-end for running and visualizing results.

---

## 🧠 Tech Stack
| Component | Purpose |
|------------|----------|
| **Python** | Core programming language |
| **LangGraph** | Multi-agent workflow graph |
| **LangChain** | LLM prompt handling |
| **Gemini (Google Generative AI)** | Code explanation and optimization |
| **Streamlit** | Web-based user interface |
| **dotenv** | Securely load environment variables |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/multi-agent-code-explainer-optimizer.git
cd multi-agent-code-explainer-optimizer

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate


### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Setup Environment Variable
Copy `.env.example` to `.env` and add your Gemini API key:
GOOGLE_API_KEY=your_google_gemini_api_key_here

### 5️⃣ Run the App
streamlit run app.py
