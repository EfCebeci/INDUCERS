import json
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MAP_PATH = BASE_DIR / "data/interim/allograph_map.json"
RAW_DIR = BASE_DIR / "data/raw/"
PROCESSED_PATH = BASE_DIR / "data/processed/diziler.jsonl"

def haritayi_yukle(map_path):
    print(f"Allograf haritası yükleniyor: {map_path}")
    try:
        with open(map_path, 'r', encoding='utf-8') as f:
            allograph_map = json.load(f)
        allograph_map.pop("comment", None)
        print(f"Başarıyla yüklendi. {len(allograph_map)} kural bulundu.")
        return allograph_map
    except FileNotFoundError:
        print(f"HATA: Allograf haritası bulunamadı: {map_path}", file=sys.stderr)
        sys.exit(1)

def ham_kulliyati_yukle(raw_dir):
    print(f"Ham transkripsiyonlar yükleniyor: {raw_dir}")
    raw_corpus = []
    files = list(raw_dir.glob("*.txt"))
    if not files:
        print(f"UYARI: '{raw_dir}' içinde hiç '.txt' dosyası bulunamadı.", file=sys.stderr)
        return [], []
        
    file_names = []
    for file_path in files:
        file_names.append(file_path.name)
        with open(file_path, 'r', encoding='utf-8') as f:
            line = f.read().strip()
            if line:
                signs = line.split(' ')
                raw_corpus.append(signs)
                
    print(f"Toplam {len(raw_corpus)} adet ham yazıt yüklendi.")
    return raw_corpus, file_names

def kulliyati_normallestir(raw_corpus, allograph_map):
    print("Külliyat normalleştiriliyor...")
    normalized_corpus = []
    normalized_vocabulary = set()
    
    for raw_inscription in raw_corpus:
        normalized_inscription = []
        for raw_sign in raw_inscription:
            normalized_sign = allograph_map.get(raw_sign, raw_sign)
            normalized_inscription.append(normalized_sign)
            normalized_vocabulary.add(normalized_sign)
            
        normalized_corpus.append(normalized_inscription)
        
    print(f"Normalleştirme tamamlandı. {len(normalized_vocabulary)} benzersiz ana işaret bulundu.")
    return normalized_corpus, sorted(list(normalized_vocabulary))

def sonuclari_kaydet(processed_path, normalized_corpus, file_names):
    print(f"İşlenmiş diziler şuraya kaydediliyor: {processed_path}")
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(processed_path, 'w', encoding='utf-8') as f:
        for i, inscription in enumerate(normalized_corpus):
            line_data = {"dizi": inscription, "kaynak_dosya": file_names[i]}
            json.dump(line_data, f)
            f.write('\n')
    print("Kaydetme işlemi tamamlandı.")

def main():
    print("--- Metin Normalleştirme Script'i Başlatıldı ---")
    allograph_map = haritayi_yukle(MAP_PATH)
    raw_corpus, file_names = ham_kulliyati_yukle(RAW_DIR)
    if not raw_corpus:
        print("İşlenecek veri yok. Çıkılıyor.")
        return
    normalized_corpus, _ = kulliyati_normallestir(raw_corpus, allograph_map)
    sonuclari_kaydet(PROCESSED_PATH, normalized_corpus, file_names)
    print("--- Tüm İşlemler Başarıyla Tamamlandı ---")

if __name__ == "__main__":
    main()
