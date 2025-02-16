# Tavily Chatbot - AI-Powered Search Assistant  

## 🔹 Overview  
Tavily Chatbot is an AI-powered chatbot that integrates LangGraph, OpenAI GPT-3.5, and Tavily Search to provide conversational AI responses with real-time search capabilities.  

It is built using Flask (backend), Tailwind CSS + JavaScript (frontend), and follows the MVC architecture for maintainability.  


## 🚀 Features  
✅ **Conversational AI** – Uses OpenAI GPT-3.5 for intelligent responses.  
✅ **Real-Time Search** – Fetches external data using Tavily Search API.  
✅ **Markdown Support** – Displays formatted responses with bullet points, headers, and code blocks.  
✅ **Web UI** – Simple chatbot interface built with Tailwind CSS & JavaScript.  
✅ **Flask Backend** – REST API handles user requests and chatbot logic.  
✅ **Secure API Keys** – Uses `.env` (local) or Google Secret Manager (GCP) for credentials.  

## ⚙️ Local Setup & Installation  

### 🔹 1️⃣ Clone the Repository  
```sh
git clone https://github.com/Seiro10/AI-tavily-chatbot.git
cd Tavily_Chatbot
```

### 🔹 2️⃣ Set Up a Virtual Environment  
```sh
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

### 🔹 3️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 🔹 4️⃣ Set API Keys in `.env` (For Local Testing)  
Create a `.env` file and add:  
```sh
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### 🔹 5️⃣ Run the Flask Application  
```sh
flask --app app run
```
Then open your browser and visit:  
👉 **http://127.0.0.1:5000/**  


## 🚀 Deploying on Google Cloud (GCP)  

### **🔹 1️⃣ Authenticate & Set Up GCP**
First, login and set your project:  
```sh
gcloud auth login
gcloud config set project chatbot-tavily  # Replace with your actual GCP project ID
```
Then enable required services:  
```sh
gcloud services enable compute.googleapis.com artifactregistry.googleapis.com secretmanager.googleapis.com
```


### **🔹 2️⃣ Store API Keys in Google Secret Manager**  
Instead of storing API keys in `.env`, we use **Google Secret Manager**.  
Run the following commands to create and store your API keys securely:  
```sh
echo -n "sk-your-openai-key" | gcloud secrets create OPENAI_API_KEY --data-file=-
echo -n "tvly-your-tavily-key" | gcloud secrets create TAVILY_API_KEY --data-file=-
```
👉 **Verify Secrets Exist:**  
```sh
gcloud secrets list
```

### **🔹 3️⃣ Build & Push Docker Image to Google Artifact Registry**  

#### **📌 3.1 Authenticate Docker with GCP**
```sh
gcloud auth configure-docker europe-west10-docker.pkg.dev
```

#### **📌 3.2 Build the Docker Image Locally**
```sh
docker build --no-cache -t europe-west10-docker.pkg.dev/chatbot-tavily/tavily-repo/tavily-chatbot .
```

#### **📌 3.3 Push the Image to Artifact Registry**
```sh
docker push europe-west10-docker.pkg.dev/chatbot-tavily/tavily-repo/tavily-chatbot
```

👉 **Verify the image exists:**
```sh
gcloud artifacts docker images list europe-west10-docker.pkg.dev/chatbot-tavily/tavily-repo
```


### **🔹 4️⃣ Deploy to Compute Engine**  

#### **📌 4.1 Delete Old VM (If Needed)**
```sh
gcloud compute instances delete chatbot-vm --zone=europe-west10-a --quiet
```

#### **📌 4.2 Deploy New VM with the Container**
```sh
gcloud compute instances create-with-container chatbot-vm \
    --machine-type=e2-medium \
    --zone=europe-west10-a \
    --container-image=europe-west10-docker.pkg.dev/chatbot-tavily/tavily-repo/tavily-chatbot \
    --tags=http-server \
    --service-account=chatbot-sa@chatbot-tavily.iam.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/cloud-platform \
    --container-env="OPENAI_API_KEY=$(gcloud secrets versions access latest --secret=OPENAI_API_KEY),TAVILY_API_KEY=$(gcloud secrets versions access latest --secret=TAVILY_API_KEY)" \
    --restart-on-failure
```

#### **📌 4.3 Allow Traffic on Port 8080**
```sh
gcloud compute firewall-rules create allow-http-8080 \
    --allow tcp:8080 \
    --target-tags=http-server \
    --source-ranges=0.0.0.0/0 \
    --description="Allow external traffic on port 8080"
```

#### **📌 4.4 Get the External IP of Your VM**
```sh
gcloud compute instances list --zones=europe-west10-a
```
✅ **Expected Output:**
```
NAME         ZONE             EXTERNAL_IP      INTERNAL_IP   STATUS
chatbot-vm   europe-west10-a  34.XX.XX.XX      10.XX.XX.XX   RUNNING
```
👉 **Visit** `http://34.XX.XX.XX:8080` in your browser!


## 🚀 Debugging (If Something Goes Wrong)

### **Check Logs in the VM**
```sh
gcloud compute ssh chatbot-vm --zone=europe-west10-a
docker logs $(docker ps -q) --tail=50
```

### **Check If API Keys Are in the Container**
```sh
docker exec -it $(docker ps -q) env | grep API_KEY
```

### **Restart the Container Manually**
```sh
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker run -p 8080:8080 europe-west10-docker.pkg.dev/chatbot-tavily/tavily-repo/tavily-chatbot
```
