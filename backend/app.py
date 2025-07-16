import pandas as pd
import joblib # Modeli yüklemek için kullanılacak
import re # DataCleaning'deki temizleme fonksiyonu için
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Tüm kökenlerden gelen isteklere izin ver (geliştirme aşaması için)

# Veriyi cleaned_drug_data.csv dosyasından yükle
# CSV dosyanızın backend klasöründeki 'dataset' alt klasöründe olduğunu varsayıyorum.
try:
    df_drugs = pd.read_csv("backend/dataset/cleaned_drug_data.csv")
    # Eğer yan etkiler listelenmiş virgülle ayrılmış bir string olarak geliyorsa
    # ve DataCleaning.py'deki clean_text fonksiyonunu burada da kullanmak isterseniz:
    def clean_text(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^\\w\\s,]', '', text)
        return text
    # df_drugs['side_effects'] = df_drugs['side_effects'].apply(clean_text)
    print("Veri 'cleaned_drug_data.csv' dosyasından başarıyla yüklendi.")
    print(df_drugs.head()) # Yüklenen verinin ilk birkaç satırını kontrol etmek için
except FileNotFoundError:
    print("Hata: 'cleaned_drug_data.csv' dosyası bulunamadı. Lütfen yolu kontrol edin veya DataCleaning.py'yi çalıştırarak dosyayı oluşturun.")
    # Dosya bulunamazsa boş bir DataFrame ile devam edin veya uygulamayı sonlandırın
    df_drugs = pd.DataFrame(columns=['drug_name', 'medical_condition', 'side_effects', 'rating'])
except Exception as e:
    print(f"Veri yüklenirken bir hata oluştu: {e}")
    df_drugs = pd.DataFrame(columns=['drug_name', 'medical_condition', 'side_effects', 'rating'])

# TODO: Burada yapay zeka modelinizi yüklemelisiniz.
# Örneğin: model = joblib.load('path/to/your/trained_model.pkl')
# Şimdilik model olmadığı için basit bir tahmin ve öneri mantığı kullanacağız.
# Gerçek projede burada bir sınıflandırma/regresyon modeli ve öneri sistemi olacak.

# Örnek tahmin ve öneri fonksiyonları güncellenecek
def predict_side_effect_mock(drug_name, age, gender):
    # Gerçek modelinizi burada kullanacaksınız
    # Şimdilik yüklediğimiz df_drugs'tan veri çekmeye çalışalım
    drug_info = df_drugs[df_drugs['drug_name'].str.lower() == drug_name.lower()]
    if not drug_info.empty:
        # Örnek olarak ilk yan etkiyi döndürelim, modelinizden gerçek tahmin gelecek
        side_effects_str = drug_info['side_effects'].iloc[0]
        if side_effects_str:
            return side_effects_str.split(',')[0].strip().capitalize()
    return 'Belirlenemeyen yan etki (Model eğitiminden sonra gerçek tahmin gelecek)'

def get_all_side_effects_for_drug_mock(drug_name):
    drug_info = df_drugs[df_drugs['drug_name'].str.lower() == drug_name.lower()]
    if not drug_info.empty:
        side_effects_str = drug_info['side_effects'].iloc[0]
        return [effect.strip().capitalize() for effect in side_effects_str.split(',')] if side_effects_str else []
    return []

def get_similar_drugs_mock(predicted_side_effect_profile):
    # Bu fonksiyon benzer yan etki profiline sahip ilaçları döndürür.
    # Gerçekte bu, yan etki vektörlerinin veya metin benzerliğinin karşılaştırılmasıyla olur.
    # Şimdilik basit bir anahtar kelime eşleştirmesi yapalım
    if 'uyuşukluk' in predicted_side_effect_profile.lower():
        # Uyuşukluk içeren ilaçları getir ama istenen ilaç hariç
        return df_drugs[df_drugs['side_effects'].str.contains('uyuşukluk', case=False, na=False)]['drug_name'].drop_duplicates().tolist()
    elif 'mide' in predicted_side_effect_profile.lower():
        # Mide ile ilgili yan etkileri içeren ilaçları getir
        return df_drugs[df_drugs['side_effects'].str.contains('mide', case=False, na=False)]['drug_name'].drop_duplicates().tolist()
    return ['Alternatif ilaç bulunamadı']


@app.route('/predict_side_effect', methods=['POST'])
def predict_side_effect():
    data = request.get_json()
    drug_name = data.get('drugName')
    age = data.get('age')
    gender = data.get('gender')
    # disease = data.get('disease') # README'de belirtilen hastalık bilgisi de burada kullanılabilir.

    if not drug_name or not age or not gender:
        return jsonify({'error': 'İlaç adı, yaş ve cinsiyet alanları zorunludur.'}), 400

    # TODO: Gerçek modelinizi kullanarak tahmin yapın
    # predicted_side_effect = model.predict(drug_name, age, gender, disease)

    # TODO: Veritabanından veya temizlenmiş DataFrame'den tüm yan etkileri çekin
    # all_side_effects = get_all_side_effects_from_db(drug_name)

    # TODO: Benzer ilaçları bulan öneri sisteminizi kullanın
    # similar_drugs = recommendation_system.find_similar_drugs(predicted_side_effect_profile)

    # Şimdilik örnek fonksiyonları kullanıyoruz
    predicted_side_effect_result = predict_side_effect_mock(drug_name, age, gender)
    all_side_effects_result = get_all_side_effects_for_drug_mock(drug_name)
    similar_drugs_result = get_similar_drugs_mock(predicted_side_effect_result)


    return jsonify({
        'predicted_side_effect': predicted_side_effect_result,
        'all_side_effects': all_side_effects_result,
        'similar_drugs': similar_drugs_result
    })

if __name__ == '__main__':
    # Flask uygulamasını çalıştırma (debug modu geliştirme için uygundur)
    app.run(debug=True, port=5000)