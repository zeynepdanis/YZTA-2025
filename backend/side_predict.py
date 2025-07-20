import pandas as pd
import re
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.sparse import hstack

# 1. VERİYİ YÜKLE
df = pd.read_csv("backend/dataset/final_expanded_drug_dataset.csv")  # Kendi dosya yolunu yaz

# 2. GEREKLİ SÜTUNLAR ve TEMİZLİK
df = df[['drug_name', 'specific_side_effects', 'age_group', 'gender']].copy()
df.dropna(inplace=True)

# 3. SIK GÖRÜLEN YAN ETKİLERİ SEÇ (en az 10 tekrar eden)
side_effect_counts = df['specific_side_effects'].value_counts()
valid_effects = side_effect_counts[side_effect_counts >= 10].index
df = df[df['specific_side_effects'].isin(valid_effects)].copy()

# 4. GİRDİLERİ BİRLEŞTİR (metin olarak)
X_raw = df[['drug_name', 'age_group', 'gender']].astype(str)
X_combined = X_raw['drug_name'] + ' ' + X_raw['age_group'] + ' ' + X_raw['gender']

# 5. TF-IDF VEKTÖRLEŞTİRME
vectorizer = TfidfVectorizer(max_features=1000)
X_vec = vectorizer.fit_transform(X_combined)

# 6. ETİKET ENCODING (YAN ETKİLER)
le = LabelEncoder()
y = le.fit_transform(df['specific_side_effects'])

# 7. TRAIN-TEST BÖLÜŞÜMÜ
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

# 8. MODEL EĞİTİMİ
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 9. BAŞARI DEĞERLENDİRME
accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.2%}")

# 10. MODELİ VE ARAÇLARI KAYDET
joblib.dump(model, "backend/model/specific_side_effect_predictor.pkl")
joblib.dump(vectorizer, "backend/model/tfidf_vectorizer_side_effect.pkl")
joblib.dump(le, "backend/model/specific_side_effect_label_encoder.pkl")
