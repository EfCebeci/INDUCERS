# src/analysis/stats.py
# (INDUCERS SPRINT v9.0 - "Süper-Ekmek" (.csv) Kaydedici)
# Bu script, "Zengin Analiz" (v8.0) yapar VE "enine sonuna Pandas"ı (v9.0) kaydeder.

import pandas as pd
from conllu import parse_incr
import sys
import os
from collections import Counter

# --- SPRINT KONFİGÜRASYONU (v9.0) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'TamilTB.v0.1.utf8.conll')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# YENİ HEDEF (v9.0): "SÜPER-EKMEK" (Sizin "eşleştirme" yapacağınız dosya)
SUPER_BREAD_PATH = os.path.join(REPORTS_DIR, '00_INDUCERS_Super_Bread.csv')
# --- SPRINT KONFİGÜRASYONU BİTTİ ---

def load_rich_corpus_from_conll(filepath):
    """
    INDUCERS Makine 2 (v9.0): 
    "Yeni Süper-Ekmek"i (.conll) "zengin" (rich) bir Pandas DataFrame'e dönüştürür.
    """
    print(f"[Makine 2.1] 'Zengin Ekmek' ({filepath}) yükleniyor...")
    
    try:
        data_file = open(filepath, "r", encoding="utf-8")
    except Exception as e:
        print(f"[Makine 2.1] HATA: {e}")
        sys.exit(1)

    print("[Makine 2.1] 'Zengin Ekmek' (.conll) 'Pandas' (DataFrame) haline getiriliyor...")
    parsed_data = []
    
    for sentence_index, tokenlist in enumerate(parse_incr(data_file)):
        sentence_id = tokenlist.metadata.get('sent_id', f's{sentence_index+1}')
        for token in tokenlist:
            # "Zengin Ekmek" (v7.0) verisi:
            row = {
                'sentence_id': sentence_id,
                'token_id': token['id'],
                'form': token['form'],     # "Harf" (Sütun 1)
                'lemma': token['lemma'],   # "Yanındaki" (Sütun 2)
                'upos': token['upos'],     # "Yanındaki" (Sütun 3)
                'deprel': token['deprel'], # "Yanındaki" (Sütun 4)
                'head': token['head'],     # "Yanındaki" (Sütun 5)
            }
            parsed_data.append(row)
    
    data_file.close()
    
    df = pd.DataFrame(parsed_data)
    print(f"[Makine 2.1] BAŞARILI! {len(df)} 'zengin' sembol/token yüklendi.")
    return df

def analyze_and_save_structure(df, reports_dir):
    """
    KANIT (v8.0): "Özet Raporları" (Aggregate) üretir.
    """
    print(f"[Makine 2.1] 'Zengin Ekmek' (Pandas) Yapısal Analizi başlatılıyor...")
        
    os.makedirs(reports_dir, exist_ok=True)
    
    # --- KANIT 1: "Gramer" Frekansı (UPOS) ---
    print("[Makine 2.1] KANIT 1: 'Gramer' (UPOS) frekansı hesaplanıyor...")
    upos_counts = df['upos'].value_counts()
    upos_path = os.path.join(reports_dir, '01_upos_frequency.csv')
    upos_counts.to_csv(upos_path, header=['frequency'])

    # --- KANIT 2: "Kök" (Lemma) Frekansı ---
    print("[Makine 2.1] KANIT 2: 'Kök' (Lemma) frekansı hesaplanıyor...")
    lemma_counts = df['lemma'].value_counts()
    lemma_path = os.path.join(reports_dir, '02_lemma_frequency.csv')
    lemma_counts.to_csv(lemma_path, header=['frequency'])

    # --- KANIT 3: "Bağlantı Türü" (DEPREL) Frekansı ---
    print("[Makine 2.1] KANIT 3: 'Bağlantı Türü' (DEPREL) frekansı hesaplanıyor...")
    deprel_counts = df['deprel'].value_counts()
    deprel_path = os.path.join(reports_dir, '03_deprel_frequency.csv')
    deprel_counts.to_csv(deprel_path, header=['frequency'])

    print("[Makine 2.1] Tüm 'Özet Rapor' analizleri başarıyla tamamlandı.")

def main():
    print("--- INDUCERS SPRINT v9.0 (Süper-Ekmek Makinesi) BAŞLATILDI ---")
    
    # 1. "Ekmek"i (.conll) yükle ve "Zengin Pandas"a (DataFrame) çevir
    df = load_rich_corpus_from_conll(RAW_DATA_PATH)
    
    # 2. (YENİ GÖREV v9.0) "SÜPER-EKMEĞİ" (O 'enine sonuna Pandas'ı) KAYDET
    # "Eşleştirme" (Matching) yapmak için bu dosyayı kullanacaksınız.
    print(f"[Makine 2.1] 'Süper-Ekmek' (Zengin CSV) kaydediliyor: {SUPER_BREAD_PATH}")
    df.to_csv(SUPER_BREAD_PATH, index=False, encoding='utf-8')
    print("  -> 'Süper-Ekmek' kaydedildi. (Eşleştirme için bu dosyayı açın)")
    
    # 3. (Eski Görev v8.0) "Özet Raporları" (Aggregate) üret
    analyze_and_save_structure(df, REPORTS_DIR)
    
    print("\n--- BISH BASH BOSH! (v9.0) ---")
    print(f"KANITLAR (Özet Raporlar) VE 'SÜPER-EKMEK' (Zengin CSV) 'reports/' klasöründe üretildi.")
    print(f"\nEŞLEŞTİRME İÇİN: '{SUPER_BREAD_PATH}' dosyasını açın.")

if __name__ == "__main__":
    main()