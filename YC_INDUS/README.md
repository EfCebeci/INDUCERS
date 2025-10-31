# $PROJE_ADI

Bu proje, Iravatham Mahadevan'ın 1977 tarihli korpusunu kullanarak İndus yazıtları üzerinde
veri işleme ve sıralı dil modelleri (sequential language models) geliştirmeyi amaçlamaktadır.

## Proje Yapısı

- \`data/\`: Veri dosyaları
  - \`raw\`: Orijinal, dokunulmamış transkripsiyon metinleri.
  - \`interim\`: Veri işleme için ara dosyalar (örn: \`allograph_map.json\`).
  - \`processed\`: Modellerin okuyacağı temizlenmiş, işlenmiş veri (\`diziler.jsonl\`).
- \`src/\`: Tüm Python kaynak kodları.
  - \`data_processing\`: Ham veriyi işleyen script'ler (\`normalize.py\`).
  - \`analysis\`: İşlenmiş veri üzerinde istatistiksel analiz yapan script'ler (\`stats.py\`).
  - \`modeling\`: Dil modellerini eğiten ve değerlendiren script'ler (\`train.py\`).
- \`notebooks/\`: Keşifsel veri analizi (EDA) için Jupyter Notebook'lar.
- \`models/\`: Eğitilmiş ve serileştirilmiş model dosyaları (örn: \`.pkl\`, \`.json\`).
- \`reports/\`: Analiz sonuçları, görseller ve raporlar.
