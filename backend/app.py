import pandas as pd
import joblib
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

# 🔧 Flask kurulumu
app = Flask(__name__)
CORS(app)

# ✅ Yaş aralığını belirle
def get_age_group(age):
    try:
        age = int(age)
        if age <= 17:
            return "0-17"
        elif age <= 25:
            return "18-25"
        elif age <= 35:
            return "26-35"
        elif age <= 50:
            return "36-50"
        elif age <= 65:
            return "51-65"
        else:
            return "65+"
    except:
        return "unknown"

# ✅ Veri dosyasını yükle (tüm yan etkileri göstermek için)
try:
    df_drugs = pd.read_csv("backend/dataset/final_expanded_drug_dataset.csv")
except Exception as e:
    print(f"CSV yükleme hatası: {e}")
    df_drugs = pd.DataFrame(columns=['drug_name', 'specific_side_effects', 'all_side_effects'])

# ✅ Model bileşenlerini yükle
try:
    model = joblib.load("backend/model/specific_side_effect_predictor.pkl")
    vectorizer = joblib.load("backend/model/tfidf_vectorizer_side_effect.pkl")
    label_encoder = joblib.load("backend/model/specific_side_effect_label_encoder.pkl")
    print("✅ Model bileşenleri yüklendi.")
except Exception as e:
    print("❌ Model bileşenleri yüklenemedi:", e)
    model, vectorizer, label_encoder = None, None, None

# ✅ Ana tahmin fonksiyonu
def predict_side_effect_real(drug_name, age, gender):
    if None in (model, vectorizer, label_encoder):
        return "Model yüklenemedi."

    age_group = get_age_group(age)
    input_text = f"{drug_name} {age_group} {gender}"
    try:
        input_vector = vectorizer.transform([input_text])
        prediction = model.predict(input_vector)
        return label_encoder.inverse_transform(prediction)[0]
    except Exception as e:
        return f"Tahmin hatası: {str(e)}"

# ✅ İlgili ilacın tüm yan etkilerini veriden getir
def get_all_side_effects_for_drug(drug_name):
    match = df_drugs[df_drugs['drug_name'].str.lower() == drug_name.lower()]
    if not match.empty:
        raw = match['all_side_effects'].iloc[0]
        return [x.strip().capitalize() for x in raw.split(',')] if pd.notna(raw) else []
    return []

# ✅ Basit benzer ilaç önerisi (aynı yan etkiye sahip olanlardan)
def get_similar_drugs(predicted_effect):
    if not isinstance(predicted_effect, str):
        return []
    result = df_drugs[df_drugs['specific_side_effects'].str.contains(predicted_effect, case=False, na=False)]
    return result['drug_name'].drop_duplicates().tolist()

# ✅ API endpoint
@app.route('/predict_side_effect', methods=['POST'])
def predict_side_effect():
    data = request.get_json()
    drug_name = data.get('drugName')
    age = data.get('age')
    gender = data.get('gender')

    if not all([drug_name, age, gender]):
        return jsonify({'error': 'İlaç adı, yaş ve cinsiyet zorunludur.'}), 400

    predicted = predict_side_effect_real(drug_name, age, gender)
    all_effects = get_all_side_effects_for_drug(drug_name)
    similar_drugs = get_similar_drugs(predicted)

    return jsonify({
        'predicted_side_effect': predicted,
        'all_side_effects': all_effects,
        'similar_drugs': similar_drugs
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
