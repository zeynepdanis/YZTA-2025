import pandas as pd
import re

# CSV dosyasını yükle
df = pd.read_csv("backend/dataset/drugs_side_effects_drugs_com.csv")

# Gerekli sütunları seç
columns_to_keep = ['drug_name', 'medical_condition', 'side_effects', 'rating']
df_clean = df[columns_to_keep].copy()

# Eksik verileri temizle
df_clean.dropna(inplace=True)

# Yan etkileri temizle: Küçük harfe çevir, özel karakterleri temizle
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s,]', '', text)  # Noktalama işaretlerini sil (virgül hariç)
    return text

df_clean['side_effects'] = df_clean['side_effects'].apply(clean_text)

# Aynı ilaca ait verileri gruplayarak birleştir
df_grouped = df_clean.groupby('drug_name').agg({
    'side_effects': lambda x: ', '.join(set(x)),         # tekrar eden yan etkileri birleştir
    'medical_condition': lambda x: x.mode()[0],          # en sık görülen hastalığı seç
    'rating': 'mean'                                     # puanların ortalamasını al
}).reset_index()

# Temizlenmiş veriyi incele
print(df_grouped.head())

# (İsteğe bağlı) Temiz veriyi kaydet
df_grouped.to_csv("backend/dataset/cleaned_drug_data.csv", index=False)
