# UNIVERSIDAD TÉCNICA PARTICULAR DE LOJA

---

# UNIVERSIDAD TÉCNICA PARTICULAR DE LOJA

<img src="https://drive.google.com/uc?id=1X5UmWVlUX9XmckJgFLmv6mTTX81GEr0c" width="300">

## FACULTAD DE INGENIERÍAS Y ARQUITECTURA
### MAESTRÍA EN INTELIGENCIA ARTIFICIAL APLICADA

---

🌍 Clasificador de Cobertura y Análisis de Cambio

Aplicación web desarrollada con **Streamlit** para visualizar, clasificar y analizar los cambios de cobertura del suelo en el cantón Montúfar, Carchi (Ecuador), utilizando imágenes satelitales de la misión **Landsat** y algoritmos de aprendizaje automático.

---

## 🏫 Proyecto académico

**Universidad Técnica Particular de Loja (UTPL)**  
**Facultad de Ingenierías y Arquitectura**  
**Maestría en Inteligencia Artificial Aplicada**

- **Autor**: Freddy Hernán Villota González  
- **Docente**: M.Sc. Alexandra Cristina González Eras  
- **Fecha**: 16 de mayo de 2025

---

## 🧠 Funcionalidades principales

✅ Clasificación de imágenes satelitales con **Random Forest**  
✅ Visualización de mapas clasificados (años: 1996, 2017 y 2024)  
✅ Matriz de transición entre dos fechas  
✅ Mapa binario de cambios clave:

- 🌳 Bosque → 🌾 Cultivo  
- 🌾 Cultivo → 🏠 Urbano

---

## 🛠️ Tecnologías usadas

- [Streamlit](https://streamlit.io/)
- [Google Earth Engine (GEE)](https://earthengine.google.com/)
- [geemap](https://geemap.org/)
- [folium](https://python-visualization.github.io/folium/)
- [pandas](https://pandas.pydata.org/)
- [seaborn](https://seaborn.pydata.org/)
- [matplotlib](https://matplotlib.org/)

---

## 📁 Estructura del proyecto

# miaa-final-project
Proyecto sobre clasificación multitemporal
miaa-final-project/
├── app.py # Aplicación principal Streamlit
├── README.md # Este archivo
├── requirements.txt # Dependencias del proyecto
├── data/
│ ├── labels1996.geojson
│ ├── labels2017.geojson
│ └── labels2024.geojson
├── images/
│ └── utpl.png # Logo institucional


---

## 🚀 Ejecución rápida (Colab + ngrok)

```python
# 1. Instalar dependencias
!pip install streamlit geemap streamlit-folium seaborn pyngrok

# 2. Ejecutar app
!streamlit run /ruta/a/tu/app.py &

# 3. Generar link público
from pyngrok import ngrok
public_url = ngrok.connect(port=8501)
public_url

🖼️ Paleta de clasificación
Clase	    Emoji	     Color	          Hex
Agua	     💧	    Azul	          #1f78b4
Bosque	     🌳	    Verde oscuro	  #006400
Zona urbana	 🏠	    Magenta	      #e7298a
Cultivo	     🌾	    Verde claro   	  #7fc97f
Suelo	     🌿	    Marrón	          #8c510a

📊 ¿Qué representa la matriz de cambio?
La matriz muestra el número de píxeles que cambian de clase entre dos años seleccionados. Cada celda indica cuántos píxeles pasaron de una clase a otra. Esto permite identificar dinámicas clave como expansión agrícola, deforestación o crecimiento urbano.

🧭 Mapa de Cambios Clave
El mapa final resalta los cambios más importantes:

🟩 Verde: Bosque → Cultivo

🟣 Magenta: Cultivo → Urbano

⚫ Negro: Sin cambio relevante

📄 Licencia
Proyecto educativo sin fines de lucro. Todos los derechos reservados © Freddy Hernán Villota González, 2025.

### 📬 Contacto

Freddy Hernán Villota González
[freddyvillota@gmail.com](mailto:freddyvillota@gmail.com)

