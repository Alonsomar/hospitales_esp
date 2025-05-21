**➡️ Prueba el mapa en directo:**
[https://alonsomar.github.io/hospitales\_esp/map/map.html](https://alonsomar.github.io/hospitales_esp/map/map.html)

[![Vista previa del mapa](https://raw.githubusercontent.com/Alonsomar/hospitales_esp/refs/heads/main/screenshots/captura_camas_hab.png)](https://alonsomar.github.io/hospitales_esp/map/map.html)

---

# Hospidata – Mapa interactivo de hospitales y camas en España

Hospidata es una visualización interactiva que muestra, provincia a provincia, cuántos hospitales existen, cuántas camas ofrecen y quién las gestiona.
El usuario puede …

* **Conmutar** entre hospitales públicos+privados o solo públicos.
* Elegir la **cloropleta**:

  * Ninguna (relleno uniforme)
  * Nº de hospitales
  * Nº de camas
  * Camas por 1000 habitantes
* Hacer *zoom/pan* libre sobre el mapa y explorar tooltips detallados.


---

## Datos y fuentes

| Conjunto                        | Descripción                                  | Fuente                | Año  |
| ------------------------------- | -------------------------------------------- | --------------------- | ---- |
| Catálogo Nacional de Hospitales | Datos maestros de centros, tipología y camas | Ministerio de Sanidad | 2024 |
| Padrón continuo                 | Población por provincia                      | INE                   | 2024 |
| Geocodificación                 | Lat/Lon vía GeoJSON previo + Nominatim/OSM   | Elaboración propia    | 2025 |

---

## Cómo funciona

| Paso                          | Acción                                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1. Limpieza y geocodificación | `main.py` combina un GeoJSON existente con CNH 2024; lo que falta se geocodifica (Nominatim).    |
| 2. Exportación                | Se generan `CNH_2024_geocoded.csv` (`lat`, `lon`) y la tabla de población.                               |
| 3. Visualización              | `map/map.html` carga todo con **D3 v7** y **TopoJSON** directo desde CDNs. No requiere servidor backend. |
| 4. Hosting                    | Publicado en **GitHub Pages** (`/map/`), por lo que basta con abrir la URL para verlo.                   |

---

## Desarrollo local

```bash
git clone https://github.com/Alonsomar/hospitales_esp.git
cd hospitales_esp

# Lanzar un servidor estático (p.ej. con Python 3.11)
python -m http.server 8000
# Visita http://localhost:8000/map/map.html
```

---

## Personalizar

* **Paleta de colores:** edita las variables CSS en `:root` (`map.html`).
* **Filtrado avanzado:** ajusta la línea

  ```js
  hospitals.filter(h => h.dep !== 20) // Excluye privados
  ```

  para añadir/excluir otros códigos (`dep === 21`, `4`, …).
* **Nuevas métricas:** añade otro `<input type="radio">` y extiende
  `updateChoro(metric)` para mapear el nuevo campo.

---


## Créditos y licencias de los datos

| Dataset / recurso                              | Fuente                                                                                           | Tipo de licencia                                                                               | Requisito de atribución                                                    |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Catálogo Nacional de Hospitales (CNH 2024)** | Ministerio de Sanidad, España                                                                    | Reutilización de la información del sector público (Ley 37/2007) – equivalente a **CC-BY 4.0** | Citar origen y fecha de última actualización. ([Ministerio de Sanidad][1]) |
| **Población por provincia** (Padrón continuo)  | Instituto Nacional de Estadística (INE)                                                          | Datos abiertos del INE – **CC-BY 4.0**                                                         | Citar “INE, padrón a 1-ene-2024”. ([INE][2])                               |
| **Topología provincias**                       | Highcharts Maps *es-all.topo.json* (derivada de Natural Earth)                                   | Natural Earth → **Dominio público**; empaquetado Highcharts bajo licencia MIT                  | Mencionar Natural Earth + Highsoft. ([Highcharts Blog \| Highcharts][3])   |
| Id. alternativos (fallback)                    | • *deldersveld/topojson* (MIT) ([GitHub][4])  <br>• *martgnz/es-atlas* (CC-BY 4.0) ([GitHub][5]) | Respetar la licencia especificada en los repos.                                                | Mantener encabezados de licencia en archivos si se redistribuyen.          |
| **Geocodificación**                            | Nominatim – OpenStreetMap                                                                        | **ODbL 1.0**                                                                                   | Añadir “© OpenStreetMap contributors”. ([OpenStreetMap Wiki][6])           |
| **Bibliotecas**                                | D3.js, TopoJSON, Highcharts mapdata (solo ficheros)                                              | MIT / ISC                                                                                      | Conservar aviso MIT/ISC en código fuente.                                  |

> **Nota sobre Natural Earth:** Los datos base de “Admin 0/1” que usa Highcharts son dominio público. El proyecto Highcharts distribuye las conversiones TopoJSON con cabecera MIT; ambas licencias permiten uso comercial y modificación.

### Cómo citar el mapa

> Alonso Valdés. *Hospidata: Mapa interactivo de hospitales y camas en España (edición 2025)*.
> Datos: Ministerio de Sanidad (CNH 2024), INE (Padrón 2024), Natural Earth, OpenStreetMap.
> Disponible en: [https://alonsomar.github.io/hospitales\_esp/map/map.html](https://alonsomar.github.io/hospitales_esp/map/map.html)

---



[1]: https://www.sanidad.gob.es/ciudadanos/prestaciones/centrosServiciosSNS/hospitales/home.htm?utm_source=chatgpt.com "Catálogo Nacional de Hospitales - Ministerio de Sanidad"
[2]: https://www.ine.es/jaxiT3/Tabla.htm?t=2852&utm_source=chatgpt.com "Población por provincias y sexo.(2852) - INE"
[3]: https://highcharts.com/docs/maps/map-collection?utm_source=chatgpt.com "Map Collection | Highcharts"
[4]: https://github.com/topojson/world-atlas?utm_source=chatgpt.com "topojson/world-atlas: Pre-built TopoJSON from Natural Earth. - GitHub"
[5]: https://github.com/martgnz/es-atlas?utm_source=chatgpt.com "martgnz/es-atlas: Pre-built TopoJSON from the Spanish ... - GitHub"
[6]: https://wiki.osm.org/wiki/Nominatim?utm_source=chatgpt.com "Nominatim - OpenStreetMap Wiki"
