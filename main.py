"""Studi Kasus 3 - Career and competition in industrial era with GIS.
Kasus: memilih lokasi pabrik/gudang baru di sekitar Palembang dengan analisis spasial:
weighted overlay (jarak ke pelabuhan, jalan tol, tenaga kerja) + jarak ke kompetitor.
Data sintetis dengan koordinat lat/lon; fungsi haversine menggantikan GIS library.
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

def haversine(lat1, lon1, lat2, lon2):
    p = np.pi / 180
    a = np.sin((lat2-lat1)*p/2)**2 + np.cos(lat1*p)*np.cos(lat2*p)*np.sin((lon2-lon1)*p/2)**2
    return 12742 * np.arcsin(np.sqrt(a))                          # km

lat, lon = np.meshgrid(np.linspace(-3.15, -2.85, 40), np.linspace(104.55, 104.95, 40))
grid = pd.DataFrame({"lat": lat.ravel(), "lon": lon.ravel()})

port = (-2.99, 104.77)                                            # titik acuan pelabuhan (ilustrasi)
toll = (-3.05, 104.70)                                            # akses jalan tol (ilustrasi)
labor = pd.DataFrame({"lat": rng.uniform(-3.1, -2.9, 8), "lon": rng.uniform(104.6, 104.9, 8),
                      "pekerja": rng.integers(5, 30, 8) * 1000})
rivals = pd.DataFrame({"lat": rng.uniform(-3.1, -2.9, 5), "lon": rng.uniform(104.6, 104.9, 5)})

grid["d_port"] = haversine(grid.lat, grid.lon, *port)
grid["d_toll"] = haversine(grid.lat, grid.lon, *toll)
grid["labor"] = sum(r.pekerja / (1 + haversine(grid.lat, grid.lon, r.lat, r.lon)) for r in labor.itertuples())
grid["d_rival"] = np.min([haversine(grid.lat, grid.lon, r.lat, r.lon) for r in rivals.itertuples()], axis=0)

norm = lambda s: (s - s.min()) / (s.max() - s.min())
grid["skor"] = (0.30 * (1 - norm(grid.d_port)) + 0.25 * (1 - norm(grid.d_toll))
                + 0.25 * norm(grid.labor) + 0.20 * norm(grid.d_rival))   # jauh dari kompetitor = bagus

best = grid.nlargest(5, "skor")
print("Top 5 lokasi kandidat:")
print(best[["lat", "lon", "d_port", "d_toll", "d_rival", "skor"]].round(3).to_string(index=False))

fig, ax = plt.subplots(figsize=(7, 6))
sc = ax.scatter(grid.lon, grid.lat, c=grid.skor, cmap="viridis", s=18)
ax.scatter(rivals.lon, rivals.lat, marker="X", c="red", s=90, label="Kompetitor")
ax.scatter(port[1], port[0], marker="*", c="orange", s=180, label="Pelabuhan")
ax.scatter(best.lon.iloc[0], best.lat.iloc[0], marker="o", fc="none", ec="white", s=220, lw=2, label="Lokasi terbaik")
plt.colorbar(sc, label="Skor kesesuaian"); ax.legend(); ax.set_title("Weighted overlay: kesesuaian lokasi industri")
fig.tight_layout(); fig.savefig("outputs/case3_gis.png", dpi=150)
print("Gambar tersimpan: outputs/case3_gis.png")
