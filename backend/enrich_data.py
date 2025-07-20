import pandas as pd
import random

# Girdi dosyasının yolu
input_csv = "backend/dataset/cleaned_drugs_side_effects.csv"  # senin orijinal csv dosyan

# Çıktı dosyasının adı
output_csv = "backend/dataset/final_expanded_drug_dataset.csv"

# Yaş grupları ve cinsiyet listesi
age_groups = ['18-25', '26-35', '36-50', '51-65', '65+']
genders = ['Male', 'Female']

# Yan etkileri temizleyen yardımcı fonksiyon
def clean_side_effects(effects):
    if pd.isna(effects):
        return []
    effects = effects.replace(';', ',').replace('(', '').replace(')', '')
    effects_list = [e.strip().lower() for e in effects.split(',') if len(e.strip()) > 2]
    return list(set(effects_list))  # benzersiz liste

# Alternatif ilaçları düzgün ayıklayan fonksiyon
def extract_alternatives(text):
    if pd.isna(text):
        return []
    # 'https' içeren satırları at, sadece ilaç isimlerini al
    alternatives = [line.split(':')[0].strip() for line in text.split('\n') if 'https://' not in line]
    return [a for a in alternatives if len(a) > 2]

# Veri setini oku
df = pd.read_csv(input_csv)

# Yapay veri üret
synthetic_data = []

for _, row in df.iterrows():
    drug = row['drug_name']
    side_effects_all = clean_side_effects(row['side_effects'])
    if not side_effects_all:
        continue  # boşsa geç

    alternatives_list = extract_alternatives(row['related_drugs'])

    for age in age_groups:
        for gender in genders:
            specific_effects = random.sample(side_effects_all, k=min(3, len(side_effects_all)))
            synthetic_data.append({
                "drug_name": drug,
                "medical_condition": row['medical_condition'],
                "age_group": age,
                "gender": gender,
                "specific_side_effects": ", ".join(specific_effects),
                "all_side_effects": ", ".join(side_effects_all),
                "alternative_drugs": ", ".join(alternatives_list)
            })

# Yeni DataFrame ve CSV'ye yaz
df_synthetic = pd.DataFrame(synthetic_data)
df_synthetic.to_csv(output_csv, index=False)

print(f"✅ Veri seti oluşturuldu: {output_csv}")
