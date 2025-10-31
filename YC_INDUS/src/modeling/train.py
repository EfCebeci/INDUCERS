import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
import pickle

# Kök dizini bul
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_PATH = BASE_DIR / "data/processed/diziler.jsonl"
MODEL_PATH = BASE_DIR / "models/simple_bigram_model.pkl"

def train_bigram_model(jsonl_path):
    """
    Basit bir Bigram (n=2) dil modeli eğitir.
    Model, P(işaret_B | işaret_A) olasılığını hesaplar.
    Modelimiz: { "işaret_A": Counter({"işaret_B": 10, "işaret_C": 5}) }
    """
    print(f"Bigram modeli eğitimi başlatıldı. Kaynak: {jsonl_path}")
    if not jsonl_path.exists():
        print(f"HATA: İşlenmiş veri dosyası bulunamadı: {jsonl_path}", file=sys.stderr)
        sys.exit(1)
        
    # defaultdict, bir anahtar olmadığında otomatik olarak Counter() oluşturur
    model = defaultdict(Counter)
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            rec = json.loads(line)
            dizi = rec.get("dizi", [])
            
            # Dizideki her (işaret_A, işaret_B) çiftini say
            for w1, w2 in zip(dizi, dizi[1:]):
                model[w1].update([w2])
                
    print(f"Model eğitimi tamamlandı. {len(model)} işaret için olasılıklar hesaplandı.")
    return model

def save_model(model, model_path):
    print(f"Model şuraya kaydediliyor: {model_path}")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # modeli pickle formatında kaydet
    with open(model_path, 'wb') as f:
        pickle.dump(dict(model), f) # defaultdict'u normal dict'e çevirerek kaydet
    print("Model başarıyla kaydedildi.")

def main():
    model = train_bigram_model(PROCESSED_PATH)
    save_model(model, MODEL_PATH)

if __name__ == "__main__":
    main()
