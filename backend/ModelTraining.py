import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import joblib
import os
import re # clean_text fonksiyonu için gerekli olabilir, DataCleaning.py'deki gibi

print("Model eğitim süreci başlatılıyor...")

# 1. Veriyi yükle
# DataCleaning.py'den gelen temizlenmiş veriyi kullanıyoruz.
# Bu script'i 'backend' klasöründen çalıştırdığınızı varsayarak yolu 'dataset/...' olarak belirtiyoruz.
try:
    df_drugs = pd.read_csv("dataset/cleaned_drug_data.csv")
    print("Veri 'cleaned_drug_data.csv' dosyasından başarıyla yüklendi.")
except FileNotFoundError:
    print("Hata: 'dataset/cleaned_drug_data.csv' dosyası bulunamadı.")
    print("Lütfen DataCleaning.py'yi çalıştırdığınızdan ve dosyanın 'backend/dataset/' dizininde olduğundan emin olun.")
    exit() # Dosya bulunamazsa programı sonlandır

# Veri setinizde 'side_effects' sütununda birden fazla yan etki virgülle ayrılmışsa,
# her girdinin ilk yan etkisini modelin hedefi olarak alıyoruz.
# Eğer 'side_effects' sütunu boşsa veya string değilse 'bilinmeyen' olarak ayarla.
df_drugs['primary_side_effect'] = df_drugs['side_effects'].apply(
    lambda x: x.split(',')[0].strip().lower() if isinstance(x, str) and x.strip() else 'bilinmeyen'
)

# Eğer veri setinde 'medical_condition' sütunu yoksa veya boşsa, 'drug_name' kullanmayı düşünebiliriz.
# Bu örnekte 'medical_condition' sütununu giriş (X), 'primary_side_effect' sütununu hedef (y) olarak alıyoruz.
# Giriş verilerinin string olduğundan emin olalım ve NaN değerleri boş string ile dolduralım.
X = df_drugs['medical_condition'].fillna('').astype(str)
y = df_drugs['primary_side_effect']

# Eğer sadece tek bir sınıf varsa stratify kullanılamaz, bu durumu kontrol edelim.
if len(y.unique()) < 2:
    print("Yeterli sayıda benzersiz hedef sınıfı bulunamadı (en az 2 sınıf gerekli). Model eğitimi yapılamıyor.")
    print(f"Bulunan benzersiz hedef sınıfları: {y.unique()}")
    exit()


# 2. Veriyi Eğitim ve Test Setlerine Ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Eğitim seti boyutu: {len(X_train)}")
print(f"Test seti boyutu: {len(X_test)}")

# 3. TF-IDF Vektörleştirme
# max_features parametresi, en sık geçen kelimelerin belirli bir sayısıyla sınırlama getirir.
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)
print("TF-IDF vektörleştirme tamamlandı.")

# 4. Logistic Regression Modeli Eğitimi
# max_iter: Optimizasyon algoritmasının yakınsaması için maksimum iterasyon sayısı.
# solver: Optimizasyon algoritması. 'liblinear' küçük veri setleri için iyi bir seçenektir.
model = LogisticRegression(max_iter=1000, solver='liblinear', random_state=42)
model.fit(X_train_tfidf, y_train)
print("Logistic Regression modeli başarıyla eğitildi.")

# 5. Model Değerlendirme
y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
# 'weighted' ortalama, her sınıfın örnek sayısına göre ağırlıklandırma yapar.
# zero_division=0, bölme sıfıra yol açtığında uyarı yerine 0 döndürür (küçük sınıflar için faydalı).
precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)

print("\nModel Değerlendirme Metrikleri:")
print(f"Doğruluk (Accuracy): {accuracy:.2f}")
print(f"Kesinlik (Precision): {precision:.2f}")
print(f"Duyarlılık (Recall): {recall:.2f}")

# 6. Modeli ve Vektörleştiriciyi .pkl formatında kaydetme
model_dir = "model"
model_path = os.path.join(model_dir, "side_effect_prediction_model.pkl")
vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")

# 'model' klasörünün var olduğundan emin olun, yoksa oluşturun.
os.makedirs(model_dir, exist_ok=True)

joblib.dump(model, model_path)
joblib.dump(tfidf_vectorizer, vectorizer_path)

print(f"\nModel şuraya kaydedildi: {model_path}")
print(f"TF-IDF Vektörleştirici şuraya kaydedildi: {vectorizer_path}")
print("Model eğitim süreci tamamlandı.")