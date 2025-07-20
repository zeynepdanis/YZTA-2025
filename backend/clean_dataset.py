import pandas as pd

# Girdi ve çıktı dosyaları
input_file = "backend/dataset/drugs_side_effects_drugs_com.csv"
output_file = "backend/dataset/cleaned_drugs_side_effects.csv"

# Veriyi oku
df = pd.read_csv(input_file)

# 1. Sütun isimlerini düzelt
df.columns = df.columns.str.strip()

# 2. Tamamen boş satırları kaldır
df.dropna(how='all', inplace=True)

# 3. Kritik alanlar boşsa sil
df.dropna(subset=['drug_name', 'side_effects'], inplace=True)

# 4. Tekrarlayan ilaç + endikasyon kombinasyonlarını sil
df.drop_duplicates(subset=['drug_name', 'medical_condition'], inplace=True)

# 5. Yan etkileri normalize et
def normalize_side_effects(effects):
    if pd.isna(effects):
        return ""
    cleaned = effects.replace(';', ',').replace('(', '').replace(')', '').lower()
    return cleaned

df['side_effects'] = df['side_effects'].apply(normalize_side_effects)

# 6. Sayısal sütunları float'a çevir
numeric_cols = ['rating', 'no_of_reviews']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 7. Metin sütunlarını kırp (gereksiz boşlukları kaldır)
text_cols = ['drug_name', 'generic_name', 'brand_names', 'medical_condition']
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 8. Kaydet
df.to_csv(output_file, index=False)
print(f"✅ Veri temizlendi ve kaydedildi: {output_file}")
