#!/usr/bin/env python3
"""
Completa la base CNH_2024.xlsx con coordenadas WGS84 (lat, lon).

Estrategia:
1.  Descarga un GeoJSON ya geolocalizado (≈ 2020) y lo cruza por CODCNH
2.  Para los centros aún sin coordenadas, geocodifica con Nominatim (OSM)
3.  Guarda CSV y GeoJSON listos para D3.js
"""

import io, json, time, requests, sys, re
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter   # respeta pausas

# -------- 1) Cargar CNH 2024 --------------------------------------------------
CNH_XLSX = "CNH_2024.xlsx"
print(f"🔄 Leyendo {CNH_XLSX} …")
cnh = pd.read_excel(CNH_XLSX, dtype={"CODCNH": int})
cnh["CODCNH"] = cnh["CODCNH"].astype(int)

# -------- 2) Descargar GeoJSON de hospitales ya geolocalizados ----------------
GEOJSON_URL = ("https://gist.githubusercontent.com/"
               "brunosan/c1308568e1f488b0c4a7fd7045a48462/raw/"
               "hospitales.geojson")

print("🔄 Descargando GeoJSON con coordenadas existentes …")
gj_bytes = requests.get(GEOJSON_URL, timeout=30).content
geojson   = json.loads(gj_bytes.decode("utf-8"))

# ✅ NORMALIZAR SIN record_path
coords_df = (
    pd.json_normalize(geojson["features"])      # <-- sin record_path
      .loc[:, ["properties.CODCNH",
               "properties.Latitude",
               "properties.Longitude"]]
      .rename(columns={
          "properties.CODCNH": "CODCNH",
          "properties.Latitude": "lat",
          "properties.Longitude": "lon"
      })
)

coords_df["CODCNH"] = coords_df["CODCNH"].astype(int)


# -------- 3) Fusionar ----------------------------------------------------------
print("🔄 Haciendo merge por CODCNH …")
cnh = cnh.merge(coords_df, on="CODCNH", how="left")

# -------- 4) Geocodificar faltantes -------------------------------------------
faltan = cnh["lat"].isna()
print(f"ℹ️  Faltan geocodificar {faltan.sum()} hospitales.")

geolocator = Nominatim(user_agent="cnh_mapper_2025")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1, max_retries=2)

def build_address(row):
    # Direccion completa sin NaN
    bits = [row.get(col, "") for col in
            ["Dirección", "Municipio", "Provincia", "CCAA"]]
    return ", ".join([b for b in bits if pd.notna(b)]) + ", España"

for idx, row in cnh.loc[faltan].iterrows():
    address = build_address(row)
    try:
        loc = geocode(address)
        if loc:
            cnh.at[idx, "lat"] = loc.latitude
            cnh.at[idx, "lon"] = loc.longitude
            print(f"✓ {row['Nombre Centro'][:40]:40s}  ->  {loc.latitude:.5f}, {loc.longitude:.5f}")
        else:
            print(f"⚠️  No se encontró: {address}")
    except Exception as e:
        print(f"⚠️  Error geocodificando '{address}': {e}")

# -------- 5) Exportar ----------------------------------------------------------
OUT_CSV   = "CNH_2024_geocoded.csv"
OUT_GEOJS = "CNH_2024_geocoded.geojson"

print(f"💾 Guardando {OUT_CSV} …")
cnh.to_csv(OUT_CSV, index=False)

print(f"💾 Guardando {OUT_GEOJS} …")
df_ok = cnh.dropna(subset=["lat", "lon"]).copy()

gdf = gpd.GeoDataFrame(
    df_ok,
    geometry=gpd.points_from_xy(df_ok.lon, df_ok.lat),
    crs="EPSG:4326"
)
gdf.to_file(OUT_GEOJS, driver="GeoJSON")

# (opcional) lista de hospitales sin coordenadas
sin_coords_csv = "CNH_2024_sin_coords.csv"
cnh[cnh["lat"].isna()].to_csv(sin_coords_csv, index=False)
print(f"✅ Completado. GeoJSON listo y {cnh['lat'].isna().sum()} sin geolocalizar (ver {sin_coords_csv})")


# -----------------  OPTIONAL: emparejar por nombre con RapidFuzz --------------
# Si tuvieras CNH sin CODCNH o quisieras afinar más:
#
# from unidecode import unidecode
# from rapidfuzz import process, fuzz
#
# def normalize(txt):
#     txt = unidecode(str(txt)).upper()
#     return re.sub(r"[^A-Z0-9 ]+", " ", txt).strip()
#
# coords_df["name_norm"] = coords_df["NOMBRE"].apply(normalize)
# cnh["name_norm"]       = cnh["Nombre Centro"].apply(normalize)
#
# for idx, row in cnh.loc[cnh["lat"].isna()].iterrows():
#     cand, score, _ = process.extractOne(
#         row["name_norm"], coords_df["name_norm"], scorer=fuzz.WRatio
#     )
#     if score >= 90:
#         match_row = coords_df.loc[coords_df["name_norm"] == cand].iloc[0]
#         cnh.at[idx, ["lat", "lon"]] = match_row[["lat", "lon"]].values
# -----------------------------------------------------------------------------
