# ⚡ Numerix

**Calcula. Visualiza. Comprende.**

Numerix es una aplicación desarrollada en **Python** para la resolución y análisis de ecuaciones no lineales mediante diferentes **métodos numéricos**.

El proyecto surge como una propuesta académica para el curso de **Investigación de Operaciones I**, con el objetivo de integrar el cálculo numérico, la programación y la visualización de resultados en una herramienta sencilla e interactiva.

## 🎯 ¿Qué hace Numerix?

La aplicación permite seleccionar un método numérico, ingresar una función y sus parámetros, y obtener:

* La raíz aproximada de la ecuación.
* El valor de la función en la raíz encontrada.
* El error relativo.
* El número de iteraciones realizadas.
* La tabla detallada del proceso iterativo.
* Una representación gráfica de la función.
* La posibilidad de descargar las iteraciones en formato CSV.
* Una explicación básica del fundamento matemático de cada método.

## 🧮 Métodos implementados

Actualmente Numerix trabaja con los siguientes métodos:

### Métodos cerrados

* **Bisección**
* **Regula Falsi**

### Métodos abiertos

* **Newton-Raphson**
* **Secante**
* **Punto Fijo**

Cada método utiliza sus propios parámetros de entrada y criterios de convergencia.

## 🖥️ Tecnologías utilizadas

* **Python**
* **Streamlit** — interfaz de la aplicación.
* **NumPy** — operaciones numéricas.
* **SymPy** — procesamiento simbólico y funciones matemáticas.
* **Pandas** — manejo de tablas de iteraciones.
* **Plotly** — generación de gráficas interactivas.
* **CSS** — personalización de la interfaz.

## 📂 Estructura del proyecto

```text
Numerix/
│
├── app.py
├── styles.css
├── requirements.txt
│
├── assets/
│   └── logo.jpeg
│
├── methods/
│   ├── __init__.py
│   ├── cerrados.py
│   ├── abiertos.py
│   └── polynomial_methods.py
│
└── docs/
    ├── MANUAL_USUARIO.md
    └── MANUAL_TECNICO.md
```

## 🚀 Ejecución local

Clona el repositorio e instala las dependencias:

```bash
git clone URL_DEL_REPOSITORIO
cd Numerix
pip install -r requirements.txt
```

Luego ejecuta la aplicación con:

```bash
streamlit run app.py
```

La aplicación se abrirá en el navegador mediante el servidor local de Streamlit.

## 📚 Documentación

Para obtener información más detallada sobre el funcionamiento de la aplicación, consulta:

* [`MANUAL_USUARIO.md`](docs/MANUAL_USUARIO.md) — guía de uso de Numerix.
* [`MANUAL_TECNICO.md`](docs/MANUAL_TECNICO.md) — descripción técnica, estructura y funcionamiento del proyecto.

## 🔬 Relación con Investigación de Operaciones

Numerix busca servir como herramienta de apoyo para el análisis de problemas matemáticos relacionados con la **Ingeniería y la Investigación de Operaciones**.

El flujo general planteado por el proyecto es:

**Problema real → Modelo matemático → Ecuación → Método numérico → Solución aproximada → Interpretación**

De esta manera, la aplicación no se limita a proporcionar un resultado numérico, sino que permite observar el proceso mediante el cual se obtiene la solución.

## 👥 Proyecto académico

Numerix fue desarrollado como proyecto académico para la **Feria EMI**, integrando conocimientos de programación, métodos numéricos e Investigación de Operaciones.

---

**Numerix — Calcula. Visualiza. Comprende.**
