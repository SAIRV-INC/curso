import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import ee
import geemap
import json


from IPython.display import display, Markdown

# Mostrar el bloque de estilo actualizado
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f8fbff;
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }

        h1, h2, h3 {
            color: #003366;
        }

        label, .stSelectbox label, .stFileUploader label {
            color: #000000 !important;
            font-weight: 500;
        }

        .stSelectbox, .stFileUploader {
            background-color: #e6f0ff !important;
            color: #000000 !important;
            border-radius: 6px;
        }

        .st-emotion-cache-1d3w5wq {
            background-color: #003366 !important;
            color: #ffffff !important;
        }

        .st-emotion-cache-1d3w5wq div {
            color: #ffffff !important;
        }

        .stAlert-success {
            background-color: #d4edda !important;
            color: #000000 !important;
            border-left: 5px solid #28a745 !important;
        }
        
        .st-dv {
            color: black !important;

        .stButton>button {
            background-color: #003366;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #0059b3;
        }
    </style>
    """,
    unsafe_allow_html=True
)



# Inicializar Earth Engine
if not ee.data._credentials:
    ee.Initialize(project="ee-freddyvillota")

# Paleta de colores y nombres
class_palette = ['#1f78b4', '#006400', '#e7298a', '#7fc97f', '#8c510a']
class_names = ['Agua', 'Bosque', 'Urbano', 'Cultivo', 'Suelo']

# ----------------------------
# Encabezado institucional
# ----------------------------
st.image("/content/drive/MyDrive/MIAA/Clases/Herramientas IA/Prácticas/miaa-final-project/images/utpl.png", width=250)
st.markdown("""
## UNIVERSIDAD TÉCNICA PARTICULAR DE LOJA
### FACULTAD DE INGENIERÍAS Y ARQUITECTURA
### MAESTRÍA EN INTELIGENCIA ARTIFICIAL APLICADA

**Autor:** Freddy Hernán Villota González  
**Docente:** M.Sc. Alexandra Cristina González Eras  
**Fecha:** 16 de mayo de 2025
""")

st.title("🌍 Clasificador de Cobertura y Análisis de Cambio")
st.markdown("---")

# Selección de años
st.header("1. Selección de Años")
year1 = st.selectbox("Año anterior:", [1996, 2017, 2024], index=0)
year2 = st.selectbox("Año actual:", [1996, 2017, 2024], index=2)

# Subida de archivos
st.header("2. Cargar archivos de etiquetas (GeoJSON)")
col1, col2 = st.columns(2)
with col1:
    uploaded_labels_1 = st.file_uploader("Etiquetas de entrenamiento (imagen anterior)", type=["geojson"])
with col2:
    uploaded_labels_2 = st.file_uploader("Etiquetas de entrenamiento (imagen actual)", type=["geojson"])

# Sensor y bandas
sensor_info = {
    1996: ("LANDSAT/LT05/C02/T1_L2", ['SR_B1','SR_B2','SR_B3','SR_B4','SR_B5','SR_B7']),
    2017: ("LANDSAT/LC08/C02/T1_L2", ['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7']),
    2024: ("LANDSAT/LC09/C02/T1_L2", ['SR_B2','SR_B3','SR_B4','SR_B5','SR_B6','SR_B7'])
}

roi = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2") \
    .filter(ee.Filter.eq("ADM0_NAME", "Ecuador")) \
    .filter(ee.Filter.eq("ADM1_NAME", "Carchi")) \
    .filter(ee.Filter.eq("ADM2_NAME", "Montufar"))

def mask_clouds(image):
    qa = image.select('QA_PIXEL')
    mask = qa.bitwiseAnd(1 << 3).eq(0) \
             .And(qa.bitwiseAnd(1 << 4).eq(0)) \
             .And(qa.bitwiseAnd(1 << 5).eq(0))
    return image.updateMask(mask).multiply(0.0000275).add(-0.2)

def classify(year, uploaded_geojson):
    col_id, bands = sensor_info[year]
    image = ee.ImageCollection(col_id) \
        .filterBounds(roi) \
        .filterDate(f"{year}-01-01", f"{year}-12-31") \
        .filter(ee.Filter.eq("WRS_PATH", 10)) \
        .filter(ee.Filter.eq("WRS_ROW", 60)) \
        .sort("CLOUD_COVER").first()

    image = mask_clouds(image).select(bands).clip(roi)
    labels_ee = geemap.geojson_to_ee(json.loads(uploaded_geojson.read().decode("utf-8")))

    training = image.sampleRegions(collection=labels_ee, properties=['class'], scale=30)
    classifier = ee.Classifier.smileRandomForest(100).train(training, 'class', bands)
    return image.classify(classifier)

if uploaded_labels_1 and uploaded_labels_2:
    st.success("Etiquetas cargadas correctamente")

    classified1 = classify(year1, uploaded_labels_1)
    classified2 = classify(year2, uploaded_labels_2)

    url1 = classified1.getThumbURL({
        'min': 0, 'max': 4,
        'palette': class_palette,
        'region': roi.geometry(),
        'dimensions': 512
    })

    url2 = classified2.getThumbURL({
        'min': 0, 'max': 4,
        'palette': class_palette,
        'region': roi.geometry(),
        'dimensions': 512
    })

    st.header("3. Clasificaciones por IA")
    st.markdown("""
    Clasificación de uso de suelo desarrollada con el algoritmo de bosques aleatorios (Random Forest) aplicado sobre bandas reflectivas Landsat. 
    Se identifican 5 clases:
    - 🔵 **Azul:** Agua 💧
    - 🌳 **Verde oscuro:** Bosque 🌳
    - 🟣 **Magenta:** Zona urbana 🏠
    - 🟢 **Verde claro:** Cultivo 🌾
    - 🟫 **Marrón:** Suelo descubierto o degradado
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.image(url1, caption=f"Clasificación {year1}")
    with col2:
        st.image(url2, caption=f"Clasificación {year2}")

    st.header("4. Matriz de cambio de cobertura")
    st.markdown("""
    La matriz representa el número de píxeles que transicionaron de una clase de cobertura en el año anterior a otra clase en el año actual. 
    Permite detectar persistencias o transformaciones significativas (por ejemplo: deforestación, urbanización o abandono de cultivos).
    """)
    stack = classified1.rename(f'class_{year1}').addBands(classified2.rename(f'class_{year2}'))
    matrix = pd.DataFrame(0, index=class_names, columns=class_names)
    for i in range(5):
        for j in range(5):
            mask = classified1.eq(i).And(classified2.eq(j))
            count = mask.reduceRegion(ee.Reducer.sum(), roi, 30, maxPixels=1e9).getInfo()
            val = list(count.values())[0] if count else 0
            matrix.iloc[i,j] = int(val)

    fig, ax = plt.subplots(figsize=(7,5))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_title(f"Matriz de cambio {year1} → {year2}")
    ax.set_xlabel(f"Clase en {year2}")
    ax.set_ylabel(f"Clase en {year1}")
    st.pyplot(fig)

    st.header("5. Cambios clave: Bosque → Cultivo, Cultivo → Urbano")
    st.markdown("""
    Visualización de los cambios más relevantes:
    - 🟢 **Verde:** Bosque que fue convertido en cultivos
    - 🟣 **Magenta:** Cultivo que fue reemplazado por zonas urbanas
    - ⚫ **Negro:** Áreas sin estos cambios
    """)

    bosque_cultivo = classified1.eq(1).And(classified2.eq(3))
    cultivo_urbano = classified1.eq(3).And(classified2.eq(2))
    cambio_img = bosque_cultivo.multiply(1).add(cultivo_urbano.multiply(2))

    url_cambio = cambio_img.getThumbURL({
        'min': 0, 'max': 2,
        'palette': ['000000', '00FF00', 'FF00FF'],
        'region': roi.geometry(),
        'dimensions': 512
    })

    st.image(url_cambio, caption="🟩 Bosque→Cultivo | 🟣 Cultivo→Urbano | ⚫ Sin cambio")
    st.success("Dashboard generado exitosamente.")

# Botón para reiniciar
# Botón para recargar la app
st.markdown("""
    <br>
    <form action="/" method="get">
        <button style="
            background-color: #003366;
            color: white;
            padding: 0.5em 1em;
            border: none;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        ">🔄 Volver a ejecutar</button>
    </form>
""", unsafe_allow_html=True)