# Raporlar: Yapısal Desenlerin Deneysel Kanıtı

## 1. Amaç
Bu klasör, analiz motorumuz (`src/analysis/stats.py`) tarafından üretilen `.csv` formatındaki sonuç raporlarını içerir.

Bu raporlar, YC başvurumuzun temelindeki **deneysel kanıtlardır.**

Bu dosyalar, bizim "Hard Tech" hipotezimizi doğrular: Etiketlenmiş dil verisi (Tamil-TTB), basit sembol sıklığının (frekansının) çok ötesinde, **zengin, analiz edilebilir yapısal ve gramatik desenler** içermektedir.

## 2. Rapor Tanımları
Bu dosyaların ne anlama geldiği ve neden önemli oldukları aşağıda açıklanmıştır:

### `00_INDUCERS_Rich_Dataframe.csv`
* **Nedir:** `.conll` dosyalarından elde edilen, işlenmiş ve `pandas` DataFrame olarak yapılandırılmış tam veri setidir. Diğer tüm raporlar bu ana veri setinden türetilir.

### `01_upos_frequency.csv`
* **Nedir:** **UPOS (Universal Part of Speech - Evrensel Kelime Türü)** etiketlerinin frekans sayımıdır.
* **Neden Önemli:** Bu rapor, dili oluşturan temel yapı taşlarını (İsim, Fiil, Sıfat, Zamir vb.) gösterir. Bu, gramer analizinin ilk katmanıdır.

### `02_lemma_frequency.csv`
* **Nedir:** **Lemma** (kelimelerin kök/sözlük hali) frekans sayımıdır.
* **Neden Önemli:** Bu bize, metindeki temel *kavramları* (örn: "kral", "su", "gitmek"), o kelimenin cümle içindeki çekiminden (örn: "gidiyor", "gitti") bağımsız olarak gösterir.

### `03_deprel_frequency.csv` (En Önemli Rapor)
* **Nedir:** **DEPREL (Dependency Relations - Bağımlılık İlişkileri)** frekans sayımıdır.
* **Neden Önemli (Bizim "Hack"imiz Budur):** Bu, dilin derin gramer "mimari planıdır". Bize kelimelerin cümle içindeki *işlevini* ve *ilişkisini* söyler:
    * `nsubj`: Özne (Eylemi *yapan*)
    * `obj`: Nesne (Eylemden *etkilenen*)
    * `iobj`: Dolaylı Tümleç
    * `advmod`: Belirteç (Zarf)
* **Bu veri, bizim sadece sembolleri değil, dilin karmaşık *gramer kurallarını* da sayısallaştırabildiğimizi kanıtlar. Bizim YZ modellerimiz (GNN/Transformer) tam olarak bu yapısal veri üzerine eğitilecektir.**