print("App is starting...")
from flask_cors import CORS
from flask import Flask, render_template, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from flask import send_file
import ssl
import socket
import pickle
from urllib.parse import urlparse
from Levenshtein import distance
import whois
from datetime import datetime

app = Flask(__name__)
CORS(app)

trusted_domains = [
    "google.com", "facebook.com", "amazon.com",
    "paypal.com", "instagram.com", "microsoft.com"
]

# 🔥 NEW: Brand + keyword lists
brand_keywords = [
    "google", "facebook", "amazon", "paypal",
    "github", "microsoft", "instagram"
]

suspicious_words = [
    "login", "secure", "verify", "account", "update", "bank"
]

def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation = w.creation_date

        # Sometimes returns list
        if isinstance(creation, list):
            creation = creation[0]

        age_days = (datetime.now() - creation).days
        return age_days

    except:
        return -1

def check_ssl(domain):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)  # avoid hanging
            s.connect((domain, 443))
            return True
    except:
        return False

# Load saved model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    reasons = []
    risk = 0
    url = request.form['url']

    # -------------------------
    # Extract domain
    # -------------------------
    domain = get_domain(url)

    brand_flag = False

    # -------------------------
    # Domain Age Check 🌍
    # -------------------------
    age = get_domain_age(domain)
    print("Domain:", domain, "| Age:", age)

    # -------------------------
    # SSL Check 🔐
    # -------------------------
    ssl_valid = check_ssl(domain)
    ssl_flag = not ssl_valid

    # -------------------------
    # ML prediction
    # -------------------------
    vec = vectorizer.transform([url])
    prob = model.predict_proba(vec)[0][1]
    confidence = int(max(prob, 1 - prob) * 100)

    # -------------------------
    # Typo detection
    # -------------------------
    typo_flag = False
    for legit in trusted_domains:
        if distance(domain, legit) <= 2 and domain != legit:
            typo_flag = True
            break

    # -------------------------
    # Brand detection
    # -------------------------
    for brand in brand_keywords:
        if brand in domain:
            for word in suspicious_words:
                if word in domain:
                    brand_flag = True
                    break
            if brand_flag:
                break

    # -------------------------
    # Final decision
    # -------------------------
    # Collect ALL reasons + risk
    # -------------------------

    if typo_flag:
        reasons.append("Fake version of trusted domain detected")
        risk += 40

    if brand_flag:
        reasons.append("Contains brand name with suspicious keywords")
        risk += 25

    if ssl_flag:
        reasons.append("No SSL certificate (HTTP)")
        risk += 15

    if age > 0 and age < 30:
        reasons.append("Domain is very new")
        risk += 10

    if prob > 0.6:
        reasons.append("ML model detected phishing pattern")
        risk += 30

    elif prob > 0.3:
        reasons.append("ML model detected suspicious pattern")
        risk += 15
    
    risk = min(risk, 100)


    # -------------------------
    # Final decision
    # -------------------------

    if typo_flag:
        result = "🚨 Phishing Website"

    elif risk >= 50:
        result = "⚠️ High Risk Website"

    elif risk >= 25:
        result = "⚠️ Suspicious Website"

    else:
        result = "✅ Legitimate Website"


    return render_template("index.html",
                       prediction=result,
                       reasons=reasons,
                       risk=risk,
                       confidence=confidence)

@app.route('/download_report')
def download_report():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate("report.pdf")
    styles = getSampleStyleSheet()

    content = []

    # 🔥 Get data from query params
    url = request.args.get("url", "")
    result = request.args.get("result", "")
    risk = request.args.get("risk", "")
    confidence = request.args.get("confidence", "")
    reasons = request.args.getlist("reasons")

    # Title
    content.append(Paragraph("Phishing Detection Report", styles['Title']))
    content.append(Spacer(1, 10))

    # Details
    content.append(Paragraph(f"URL: {url}", styles['Normal']))
    content.append(Paragraph(f"Result: {result}", styles['Normal']))
    content.append(Paragraph(f"Risk Score: {risk}%", styles['Normal']))
    content.append(Paragraph(f"Confidence: {confidence}%", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Reasons:", styles['Heading2']))

    for r in reasons:
        content.append(Paragraph(f"- {r}", styles['Normal']))

    doc.build(content)

    return send_file("report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
