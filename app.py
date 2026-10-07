import os

import streamlit as st
import numpy as np
import plotly.graph_objects as go

from pathlib import Path

from methods.cerrados import biseccion, regula_falsi, parse_function
from methods.abiertos import newton_raphson, secante, punto_fijo

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Numerix | Solucionador de Ecuaciones",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGAR CSS
def load_css(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass


load_css("styles.css")


# 3. RUTA BASE Y DOCUMENTACIÓN
BASE_DIR = Path(__file__).resolve().parent


def load_markdown(relative_path):
    """Carga un archivo Markdown desde la carpeta del proyecto."""
    file_path = BASE_DIR / relative_path

    if file_path.is_file():
        return file_path.read_text(encoding="utf-8")

    return f"""
    ⚠️ El archivo `{relative_path}` no se encuentra disponible.
    """


# 4. ESTADO DE NAVEGACIÓN
if "vista" not in st.session_state:
    st.session_state.vista = "solucionador"


def mostrar_documentacion(tipo):
    st.session_state.vista = tipo


def volver_al_solucionador():
    st.session_state.vista = "solucionador"

# 5. SIDEBAR
with st.sidebar:

    # Logo
    logo_path = BASE_DIR / "assets" / "logo.jpeg"

    if logo_path.exists():
        st.image(str(logo_path), width=260)

    st.title("Configuración")

    st.markdown("---")

    # Categoría
    categoria = st.selectbox(
        "Categoría",
        [
            "Métodos Cerrados",
            "Métodos Abiertos",
            "Polinomios / Otros"
        ]
    )

    # Método
    if categoria == "Métodos Cerrados":

        metodo = st.selectbox(
            "Método",
            [
                "Bisección",
                "Regula Falsi"
            ]
        )

    elif categoria == "Métodos Abiertos":

        metodo = st.selectbox(
            "Método",
            [
                "Newton-Raphson",
                "Secante",
                "Punto Fijo"
            ]
        )

    else:

        metodo = st.selectbox(
            "Método",
            [
                "Müller",
                "Bairstow"
            ]
        )

    st.markdown("---")

    # Función
    st.subheader("Ecuación y parámetros")

    if metodo == "Punto Fijo":

        func_input = st.text_input(
            "Función despejada g(x)",
            value="(x + 2)**(1/3)"
        )

        st.caption(
            "Escribe g(x) tal que x = g(x). "
            "Ejemplo: `(x + 2)**(1/3)`"
        )

    else:

        func_input = st.text_input(
            "Función f(x)",
            value="x**3 - x - 2"
        )

        st.caption(
            "Ejemplo: `x**3 - x - 2` o `exp(x) - 3*x`"
        )

    # Parámetros
    col_a, col_b = st.columns(2)

    with col_a:

        if metodo in ["Bisección", "Regula Falsi"]:

            param_a = st.number_input(
                "Límite a",
                value=1.0
            )

        elif metodo == "Secante":

            param_a = st.number_input(
                "Punto x₀",
                value=1.0
            )

        else:

            param_a = st.number_input(
                "Punto Inicial x₀",
                value=1.0
            )

    with col_b:

        if metodo in ["Bisección", "Regula Falsi"]:

            param_b = st.number_input(
                "Límite b",
                value=2.0
            )

        elif metodo == "Secante":

            param_b = st.number_input(
                "Punto x₁",
                value=2.0
            )

        else:

            param_b = None

    # Tolerancia e iteraciones
    col_tol, col_iter = st.columns(2)

    with col_tol:

        tol = st.number_input(
            "Tolerancia",
            value=0.0001,
            format="%.5f"
        )

    with col_iter:

        max_iter = st.number_input(
            "Máx. iteraciones",
            value=50,
            step=1
        )

    st.markdown("")

    calcular = st.button(
        "⚡ Calcular",
        width='stretch',
        type="primary"
    )


# 6. VISTA DE DOCUMENTACIÓN
if st.session_state.vista in [
    "manual_usuario",
    "manual_tecnico"
]:

    # Encabezado
    col_title, col_back = st.columns([5, 1])

    with col_title:

        st.markdown(
            '<h1 class="gradient-title">Centro de Documentación</h1>',
            unsafe_allow_html=True
        )

    with col_back:

        st.button(
            "← Volver",
            width='stretch',
            on_click=volver_al_solucionador
        )

    st.markdown("---")

    # Selección del documento
    if st.session_state.vista == "manual_usuario":

        st.markdown(
            '<div class="doc-header">'
            '<span class="doc-icon">📘</span>'
            '<div>'
            '<div class="doc-title">Manual de Usuario</div>'
            '<div class="doc-subtitle">'
            'Guía para utilizar Numerix'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        content = load_markdown(
            "docs/MANUAL_USUARIO.md"
        )

    else:

        st.markdown(
            '<div class="doc-header">'
            '<span class="doc-icon">🛠️</span>'
            '<div>'
            '<div class="doc-title">Manual Técnico</div>'
            '<div class="doc-subtitle">'
            'Arquitectura y funcionamiento de Numerix'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        content = load_markdown(
            "docs/MANUAL_TECNICO.md"
        )

    st.markdown("")

    # Contenido
    st.markdown(
        '<div class="documentation-container">',
        unsafe_allow_html=True
    )

    st.markdown(content)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.stop()

# 7. ENCABEZADO PRINCIPAL DEL SOLUCIONADOR
header_col, docs_col = st.columns([7, 3])

with header_col:

    st.markdown(
        '<h1 class="gradient-title">Numerix</h1>',
        unsafe_allow_html=True
    )

    st.write(
        "Solucionador numérico de ecuaciones no lineales"
    )

with docs_col:

    st.markdown(
        '<div class="documentation-links">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="documentation-label">DOCUMENTACIÓN</div>',
        unsafe_allow_html=True
    )

    doc_col1, doc_col2 = st.columns(2)

    with doc_col1:

        if st.button(
            "📘 Usuario",
            width='stretch'
        ):
            mostrar_documentacion("manual_usuario")
            st.rerun()

    with doc_col2:

        if st.button(
            "🛠️ Técnico",
            width='stretch'
        ):
            mostrar_documentacion("manual_tecnico")
            st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


st.markdown("---")


# 8. INFORMACIÓN DEL MÉTODO
st.markdown(
    f"""
    <div class="method-banner">
        <div>
            <span class="method-label">MÉTODO SELECCIONADO</span>
            <div class="method-name">{metodo}</div>
        </div>
        <div class="method-category">
            {categoria}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")


# 9. EJECUCIÓN DEL MÉTODO
# Si no se ha presionado calcular, mostrar pantalla inicial.
if not calcular:

    st.markdown(
        """
        <div class="welcome-card">
            <div class="welcome-icon">⚡</div>
            <h2>Listo para resolver</h2>
            <p>
                Configura la función, selecciona los parámetros
                y presiona <strong>Calcular</strong> para iniciar
                el análisis numérico.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# 10. CÁLCULO
try:

    if metodo == "Bisección":

        raiz, fxr, err_rel, iters, df_iter = biseccion(
            func_input,
            param_a,
            param_b,
            tol,
            max_iter
        )

    elif metodo == "Regula Falsi":

        raiz, fxr, err_rel, iters, df_iter = regula_falsi(
            func_input,
            param_a,
            param_b,
            tol,
            max_iter
        )

    elif metodo == "Newton-Raphson":

        raiz, fxr, err_rel, iters, df_iter = newton_raphson(
            func_input,
            param_a,
            tol,
            max_iter
        )

    elif metodo == "Secante":

        raiz, fxr, err_rel, iters, df_iter = secante(
            func_input,
            param_a,
            param_b,
            tol,
            max_iter
        )

    elif metodo == "Punto Fijo":

        raiz, fxr, err_rel, iters, df_iter = punto_fijo(
            func_input,
            param_a,
            tol,
            max_iter
        )

    else:

        st.info(
            "Este método estará disponible en las siguientes "
            "entregas del módulo."
        )

        st.stop()


    # 11. KPIs
    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Raíz encontrada
                </div>
                <div class="metric-value">
                    {raiz:.6f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Valor f(xr)
                </div>
                <div class="metric-value">
                    {fxr:.2e}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Error relativo
                </div>
                <div class="metric-value">
                    {err_rel:.4f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Iteraciones
                </div>
                <div class="metric-value">
                    {iters}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # 12. TABS
    tab_grafica, tab_tabla, tab_teoria = st.tabs(
        [
            "📊 Gráfica Interactiva",
            "📋 Tabla de Iteraciones",
            "📖 Fundamento Teórico"
        ]
    )


    # 13. GRÁFICA
    with tab_grafica:

        st.subheader(
            "Comportamiento de la función y convergencia"
        )

        f_eval, _ = parse_function(func_input)

        x_min = (
            param_a - 1
            if param_b is None
            else min(param_a, param_b) - 1
        )

        x_max = (
            param_a + 1
            if param_b is None
            else max(param_a, param_b) + 1
        )

        x_vals = np.linspace(
            x_min,
            x_max,
            400
        )

        y_vals = f_eval(x_vals)

        fig = go.Figure()

        if metodo == "Punto Fijo":

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines",
                    name="g(x)",
                    line=dict(
                        color="#00D4FF",
                        width=3
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=x_vals,
                    mode="lines",
                    name="y = x",
                    line=dict(
                        color="gray",
                        dash="dash"
                    )
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=[raiz],
                    y=[raiz],
                    mode="markers",
                    name="Punto Fijo",
                    marker=dict(
                        color="#FF2A6D",
                        size=12,
                        symbol="star"
                    )
                )
            )

        else:

            fig.add_trace(
                go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode="lines",
                    name="f(x)",
                    line=dict(
                        color="#00D4FF",
                        width=3
                    )
                )
            )

            fig.add_hline(
                y=0,
                line_dash="dash",
                line_color="gray",
                opacity=0.7
            )

            fig.add_trace(
                go.Scatter(
                    x=[raiz],
                    y=[fxr],
                    mode="markers",
                    name="Raíz xr",
                    marker=dict(
                        color="#FF2A6D",
                        size=12,
                        symbol="star"
                    )
                )
            )

        fig.update_layout(
            template="plotly_dark",
            height=450,
            margin=dict(
                l=20,
                r=20,
                t=30,
                b=20
            ),
            xaxis_title="x",
            yaxis_title="y",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            width='stretch'
        )


    # 14. TABLA
    with tab_tabla:

        st.subheader(
            "Registro paso a paso"
        )

        st.dataframe(
            df_iter,
            width='stretch',
            height=350
        )

        st.download_button(
            label="📥 Descargar iteraciones en CSV",
            data=df_iter.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=(
                f"iteraciones_"
                f"{metodo.lower().replace(' ', '_')}.csv"
            ),
            mime="text/csv",
        )

    # 15. FUNDAMENTO TEÓRICO
    with tab_teoria:

        st.subheader(
            f"Ecuaciones y principios: {metodo}"
        )

        if metodo == "Bisección":

            st.markdown(
                """
                El **Método de Bisección** divide el intervalo
                a la mitad consecutivamente.
                """
            )

            st.latex(
                r"x_r = \frac{a+b}{2}"
            )

        elif metodo == "Regula Falsi":

            st.markdown(
                """
                El **Método de Regula Falsi** aproxima la raíz
                utilizando una recta que une los puntos extremos
                del intervalo.
                """
            )

            st.latex(r"x_r =b -\frac{f(b)(a-b)}{f(a)-f(b)}")

        elif metodo == "Newton-Raphson":

            st.markdown(
                """
                El **Método de Newton-Raphson** utiliza la
                recta tangente de la función en cada iteración.
                """
            )

            st.latex(r"x_{i+1} =x_i - \frac{f(x_i)}{f'(x_i)}")
        elif metodo == "Secante":

            st.markdown(
                """
                El **Método de la Secante** aproxima la derivada
                utilizando diferencias finitas y dos puntos
                iniciales.
                """
            )

            st.latex(r"x_{i+1} =x_i -\frac{f(x_i)(x_i-x_{i-1})}{f(x_i)-f(x_{i-1})}")

        elif metodo == "Punto Fijo":

            st.markdown(
                """
                El **Método de Punto Fijo** reescribe
                f(x) = 0 en la forma x = g(x) y realiza
                aproximaciones sucesivas.
                """
            )

            st.latex(
                r"x_{i+1}=g(x_i)"
            )


# 16. MANEJO DE ERRORES
except Exception as e:

    st.error(
        f"⚠️ **Atención:** {str(e)}"
    )