import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.parse import urlparse
from Levenshtein import distance

# =========================
# STEP 1: LOAD DATA
# =========================
print("Loading datasets...")

# Phishing data
phish = pd.read_csv("verified_online.csv")
phish.columns = phish.columns.str.lower()
phish = phish[['url']]
phish['label'] = 1

# Legit data
legit = pd.read_csv("top-1m.csv", header=None)
legit = legit[[1]]
legit.columns = ['url']
legit['url'] = "https://" + legit['url']
legit['label'] = 0

print("Datasets loaded ✅")

# =========================
# STEP 2: CREATE DYNAMIC TRUSTED LIST 🔥
# =========================
print("Generating trusted domains...")

# Take top 200 popular domains
trusted_domains = legit['url'].str.replace("https://", "").head(200).tolist()

# =========================
# STEP 3: BALANCE DATA
# =========================
print("Balancing dataset...")

phish = phish.sample(n=20000, random_state=42)
legit = legit.sample(n=20000, random_state=42)

data = pd.concat([phish, legit], ignore_index=True)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

print("Final dataset size:", data.shape)

print(data['label'].value_counts())

# =========================
# STEP 4: TRAIN MODEL
# =========================
X = data['url']
y = data['label']

vectorizer = TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(3,6),
    max_features=15000,
    min_df=2
)

X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# =========================
# 🔥 UPDATED MODEL (XGBOOST)
# =========================
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    use_label_encoder=False,
    eval_metric='logloss'
)

model.fit(X_train, y_train)

print("Model trained ✅")
print("Accuracy:", model.score(X_test, y_test))

import pickle

# Save model and vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model & vectorizer saved ✅")

# =========================
# HELPER FUNCTION
# =========================
def get_domain(url):
    return urlparse(url).netloc.replace("www.", "")

# =========================
# STEP 5: REAL-TIME PREDICTION
# =========================
while True:
    url = input("\nEnter URL (or type 'exit'): ")

    if url.lower() == "exit":
        print("Exiting...")
        break

    domain = get_domain(url)

    # ML Prediction
    vec = vectorizer.transform([url])
    prob = model.predict_proba(vec)[0][1]

    # Typo Detection (Dynamic)
    typo_flag = False
    for legit_domain in trusted_domains:
        if distance(domain, legit_domain) <= 2 and domain != legit_domain:
            typo_flag = True
            print(f"⚠️ Possible spoofing of {legit_domain}")
            break

    # Final Decision
    if prob > 0.6:
        result = "⚠️ Phishing Website Detected!"
    if "login" in url or "verify" in url:
        print("⚠️ Contains suspicious keywords")
    elif prob > 0.3:
        result = "⚠️ Suspicious Website (be cautious)"
    else:
        result = "✅ Legitimate Website"