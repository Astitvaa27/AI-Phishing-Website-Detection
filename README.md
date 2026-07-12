# 🛡️ AI Phishing Website Detection

An AI-powered web application that detects whether a website is **legitimate or phishing** using Machine Learning. Users can enter a URL and receive an instant prediction along with additional security information and a downloadable PDF report.

---

## 📌 Features

- 🔍 Detects phishing websites using Machine Learning
- 🌐 Analyzes URL-based security features
- 📄 Generates a downloadable PDF security report
- 📊 Displays prediction confidence
- ⚡ Fast and responsive Flask web application
- 🎨 Simple and user-friendly interface

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-CORS

### Machine Learning
- Scikit-learn
- Pickle

### Frontend
- HTML
- CSS
- JavaScript

### Report Generation
- ReportLab

---

## 📂 Project Structure

```
AI-Phishing-Website-Detection/
│
├── app.py
├── main.py
├── model.pkl
├── vectorizer.pkl
├── final_dataset.csv
├── verified_online.csv
├── top-1m.csv
│
├── templates/
│   └── index.html
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YourUsername/AI-Phishing-Website-Detection.git
```

Navigate to the project folder

```bash
cd AI-Phishing-Website-Detection
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000
```

---

## 📈 Workflow

1. User enters a website URL.
2. The application extracts security-related URL features.
3. The trained Machine Learning model predicts whether the URL is phishing or legitimate.
4. The prediction and security details are displayed.
5. A PDF report can be generated and downloaded.

---

## 📸 Screenshots

Add screenshots of your application here.

### Home Page

```
/screenshots/home.png
```

### Prediction Result

```
/screenshots/result.png
```

---

## 📚 Dataset

The model was trained using phishing and legitimate website datasets containing URL-based features.

---

## 🎯 Future Improvements

- Real-time WHOIS analysis
- SSL certificate validation
- VirusTotal API integration
- Domain reputation scoring
- Browser extension support
- Deep Learning-based detection
- User authentication and history

---

## 👨‍💻 Author

**Astitva Arun Mhatre**

- GitHub: https://github.com/Astitvaa27
- LinkedIn: https://www.linkedin.com/in/astitva-mhatre/

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
