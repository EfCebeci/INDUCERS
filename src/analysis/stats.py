import pandas as pd
from conllu import parse_incr
import sys
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'TamilTB.v0.1.utf8.conll')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

RICH_DATAFRAME_PATH = os.path.join(REPORTS_DIR, '00_INDUCERS_Rich_Dataframe.csv')

def load_rich_corpus_from_conll(filepath):

    print(f"[Makine 2.1] ({filepath}) yükleniyor...")
    
    try:
        data_file = open(filepath, "r", encoding="utf-8")
    except Exception as e:
        print(f"[Makine 2.1] HATA: {e}")
        sys.exit(1)

    print("[Makine 2.1] (.conll) 'Pandas' (DataFrame) haline getiriliyor...")
    parsed_data = []
    
    for sentence_index, tokenlist in enumerate(parse_incr(data_file)):
        sentence_id = tokenlist.metadata.get('sent_id', f's{sentence_index+1}')
        for token in tokenlist:
            
            row = {
                'sentence_id': sentence_id,
                'token_id': token['id'],
                'form': token['form'],     
                'lemma': token['lemma'],   
                'upos': token['upos'],     
                'deprel': token['deprel'], 
                'head': token['head'],     
            }
            parsed_data.append(row)
    
    data_file.close()
    
    df = pd.DataFrame(parsed_data)
    print(f"[Makine 2.1] BAŞARILI! {len(df)} 'zengin' sembol/token yüklendi.")
    return df

def analyze_and_save_structure(df, reports_dir):
    print(f"[Makine 2.1] Yapısal Analiz başlatılıyor...")
        
    os.makedirs(reports_dir, exist_ok=True)
    
    
    print("[Makine 2.1] KANIT 1: 'Gramer' (UPOS) frekansı hesaplanıyor...")
    upos_counts = df['upos'].value_counts()
    upos_path = os.path.join(reports_dir, '01_upos_frequency.csv')
    upos_counts.to_csv(upos_path, header=['frequency'])

    
    print("[Makine 2.1] KANIT 2: 'Kök' (Lemma) frekansı hesaplanıyor...")
    lemma_counts = df['lemma'].value_counts()
    lemma_path = os.path.join(reports_dir, '02_lemma_frequency.csv')
    lemma_counts.to_csv(lemma_path, header=['frequency'])

    
    print("[Makine 2.1] KANIT 3: 'Bağlantı Türü' (DEPREL) frekansı hesaplanıyor...")
    deprel_counts = df['deprel'].value_counts()
    deprel_path = os.path.join(reports_dir, '03_deprel_frequency.csv')
    deprel_counts.to_csv(deprel_path, header=['frequency'])

    print("[Makine 2.1] Tüm 'Özet Rapor' analizleri başarıyla tamamlandı.")

def main():
    print("--- INDUCERS SPRINT BAŞLATILDI ---")
    
    
    df = load_rich_corpus_from_conll(RAW_DATA_PATH)
    
    print(f"[Makine 2.1] kaydediliyor: {RICH_DATAFRAME_PATH}")
    df.to_csv(RICH_DATAFRAME_PATH, index=False, encoding='utf-8')
    print("Kaydedildi. (Eşleştirme için bu dosyayı açın)")
    
    
    analyze_and_save_structure(df, REPORTS_DIR)
    
    print("\n--- BISH BASH BOSH! ---")
    print(f"KANITLAR (Özet Raporlar) reports/' klasöründe üretildi.")
    print(f"\nEŞLEŞTİRME İÇİN: '{RICH_DATAFRAME_PATH}' dosyasını açın.")

if __name__ == "__main__":
    main()