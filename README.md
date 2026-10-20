# Studi Kasus 3: Career and Competition in Industrial Era with GIS

## Deskripsi
Pemilihan lokasi pabrik/gudang di sekitar Palembang dengan weighted overlay: jarak ke pelabuhan (30%), tol (25%), tenaga kerja (25%), dan jarak dari kompetitor (20%), memakai jarak haversine. Bobot dan koordinat pelabuhan, tol, serta kompetitor adalah asumsi ilustrasi; validasi dengan pakar atau AHP. Pengembangan: GeoPandas, OpenStreetMap, data kawasan industri resmi.

## Cara menjalankan
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
Grafik tersimpan di folder `outputs/`.

## Catatan
Data pada proyek ini sintetis atau bawaan library agar bisa dijalankan tanpa dataset eksternal. Kesimpulan substantif perlu divalidasi dengan data nyata.
