# **📝 Tavily Chatbot - AI-Powered Search Assistant**  

### **🔹 Overview**  
Tavily Chatbot is an AI-powered chatbot that integrates **LangGraph**, **OpenAI GPT-3.5**, and **Tavily Search** to provide **conversational AI responses with real-time search capabilities**.  

It is built using **Flask (backend)**, **Tailwind CSS + JavaScript (frontend)**, and follows the **MVC architecture** for maintainability.  

---

## **🚀 Features**  
✅ **Conversational AI** – Uses OpenAI GPT-3.5 for intelligent responses.  
✅ **Real-Time Search** – Fetches external data using Tavily Search API.  
✅ **Markdown Support** – Displays formatted responses with bullet points, headers, and code blocks.  
✅ **Web UI** – Simple chatbot interface built with Tailwind CSS & JavaScript.  
✅ **Flask Backend** – REST API handles user requests and chatbot logic.  
✅ **Secure API Keys** – Uses `.env` to store sensitive credentials.  

---

## **📂 Project Structure (MVC Architecture)**
```
TAVILY_CHATBOT/
│── app/                     # Main Flask application
│   ├── controllers/         # Controllers (Handles API requests)
│   │   ├── chat_controller.py 
│   ├── models/              # Models (Chatbot logic)
│   │   ├── chatbot.py        
│   │   ├── tool_node.py     
│   ├── templates/           # Views (Frontend templates)
│   │   ├── base.html     
│   │   ├── index.html    
│   ├── static/              # Static files (CSS, JS)
│   ├── __init__.py          # App initialization
│── main.py                  # Entry point
│── requirements.txt         # Dependencies
│── wsgi.py                  # Production WSGI server
│── .env                     # (Ignored) API keys (Tavily & OpenAI)
│── .gitignore               # Exclude sensitive files from Git
│── README.md                # Project Documentation
```

---

## **⚙️ Setup & Installation**  

### **🔹 1️⃣ Clone the Repository**  
```sh
git clone https://github.com/your-github-username/Tavily_Chatbot.git
cd Tavily_Chatbot
```

### **🔹 2️⃣ Set Up a Virtual Environment**  
```sh
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

### **🔹 3️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **🔹 4️⃣ Set API Keys in `.env`**  
Create a `.env` file and add:  
```ini
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### **🔹 5️⃣ Run the Flask Application**  
```sh
flask --app app run
```
Then open your browser and visit:  
```
http://127.0.0.1:5000/
```
