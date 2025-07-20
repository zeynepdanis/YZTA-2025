import pandas as pd
import joblib  # Modeli yüklemek için kullanılacak
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Tüm kökenlerden gelen isteklere izin ver (geliştirme aşaması için)

# Veri setini yükle
try:
    df_drugs = pd.read_csv("backend/dataset/cleaned_drug_data.csv")

    def clean_text(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^\\w\\s,]', '', text)
        return text

    print("Veri 'cleaned_drug_data.csv' dosyasından başarıyla yüklendi.")
    print(df_drugs.head())
except FileNotFoundError:
    print("Hata: 'cleaned_drug_data.csv' dosyası bulunamadı.")
    df_drugs = pd.DataFrame(columns=['drug_name', 'medical_condition', 'side_effects', 'rating'])
except Exception as e:
    print(f"Veri yüklenirken bir hata oluştu: {e}")
    df_drugs = pd.DataFrame(columns=['drug_name', 'medical_condition', 'side_effects', 'rating'])

# ✅ MODEL ve VECTORIZER YÜKLENİYOR
try:
    model = joblib.load("side_effect_prediction_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    print("Model ve TF-IDF vectorizer başarıyla yüklendi.")
except Exception as e:
    print(f"Model veya vectorizer yüklenemedi: {e}")
    model = None
    vectorizer = None

# ✅ Gerçek tahmin fonksiyonu
def predict_side_effect_real(drug_name, age, gender):
    if model is None or vectorizer is None:
        return "Model yüklenemedi."

    try:
        # Basit metin oluşturma – model eğitimine göre güncellenebilir
        input_text = f"{drug_name} yaş:{age} cinsiyet:{gender}"
        vectorized_input = vectorizer.transform([input_text])
        prediction = model.predict(vectorized_input)
        return prediction[0]
    except Exception as e:
        return f"Tahmin hatası: {str(e)}"

# Diğer örnek fonksiyonlar (dokunulmadı)
def get_all_side_effects_for_drug_mock(drug_name):
    drug_info = df_drugs[df_drugs['drug_name'].str.lower() == drug_name.lower()]
    if not drug_info.empty:
        side_effects_str = drug_info['side_effects'].iloc[0]
        return [effect.strip().capitalize() for effect in side_effects_str.split(',')] if side_effects_str else []
    return []

def get_similar_drugs_mock(predicted_side_effect_profile):
    if 'uyuşukluk' in predicted_side_effect_profile.lower():
        return df_drugs[df_drugs['side_effects'].str.contains('uyuşukluk', case=False, na=False)]['drug_name'].drop_duplicates().tolist()
    elif 'mide' in predicted_side_effect_profile.lower():
        return df_drugs[df_drugs['side_effects'].str.contains('mide', case=False, na=False)]['drug_name'].drop_duplicates().tolist()
    return ['Alternatif ilaç bulunamadı']

# Tahmin API endpoint’i
@app.route('/predict_side_effect', methods=['POST'])
def predict_side_effect():
    data = request.get_json()
    drug_name = data.get('drugName')
    age = data.get('age')
    gender = data.get('gender')

    if not drug_name or not age or not gender:
        return jsonify({'error': 'İlaç adı, yaş ve cinsiyet alanları zorunludur.'}), 400

    # ✅ ARTIK GERÇEK MODEL KULLANILIYOR
    predicted_side_effect_result = predict_side_effect_real(drug_name, age, gender)

    # Diğer mock fonksiyonlar aynı şekilde çalışıyor
    all_side_effects_result = get_all_side_effects_for_drug_mock(drug_name)
    similar_drugs_result = get_similar_drugs_mock(predicted_side_effect_result)

    return jsonify({
        'predicted_side_effect': predicted_side_effect_result,
        'all_side_effects': all_side_effects_result,
        'similar_drugs': similar_drugs_result
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
