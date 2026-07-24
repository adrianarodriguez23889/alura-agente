# 🤖 Alura Agente - Asistente Corporativo de IA

¡Bienvenido al repositorio del **Alura Agente**! Este proyecto es una solución de inteligencia artificial corporativa diseñada para actuar como una base de conocimiento centralizada y conversacional para colaboradores.

---

## 📌 Descripción del Proyecto

El agente permite a los miembros del equipo realizar preguntas en lenguaje natural y obtener respuestas inmediatas extraídas de documentación interna (políticas corporativas en PDF y datos de inventario en CSV), sin necesidad de revisar los archivos manualmente.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python
- **Procesamiento de Documentos:** PyPDF, Pandas
- **Framework de IA:** LangChain / Google Gemini
- **Deploy:** Oracle Cloud Infrastructure (OCI) Compute

---

## 📁 Estrategia de Curaduría y Gobernanza de Datos

Para garantizar la calidad de las respuestas del agente (*evitando información desactualizada o duplicada*), los documentos se organizaron bajo la siguiente estructura corporativa en el directorio `/data`:

| Documento | Categoría / Dominio | Formato | Ámbito de Aplicación |
| :--- | :--- | :--- | :--- |
| `Politicas_Tienda.pdf` | Operacional / Atención al Cliente | PDF | Tiempos de envío, devoluciones y garantías. |
| `productos_inventario.csv` | Comercial / Inventario | CSV | Precios, stock disponible y especificaciones de catálogo. |

### 🛠️ Ingesta e Integración
- **Modo Actual:** Carga local estructurada (Local Directory Upload) desde el directorio `/data`.
- **Acceso:** Acceso de lectura global para todos los colaboradores de la organización.