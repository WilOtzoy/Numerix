import streamlit as st
import numpy as np
import plotly.graph_objects as go
from methods.cerrados import biseccion, regula_falsi, parse_function
from methods.abiertos import newton_raphson, secante, punto_fijo

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Numerix | Solucionador de Ecuaciones",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CARGAR ESTILOS CSS EXTERNOS
def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

try:
    load_css("styles.css")
except FileNotFoundError:
    pass

# 3. SIDEBAR: PANEL DE CONFIGURACIÓN
with st.sidebar:
    st.image("assets/logo.jpeg", width=300)
    st.title("Configuración")
    st.caption("Los cambios se recalculan automáticamente al presionar Enter o cambiar un parámetro.")
    st.markdown("---")
    
    categoria = st.selectbox(
        "Categoría del Método",
        ["Métodos Cerrados", "Métodos Abiertos", "Polinomios / Otros"]
    )
    
    if categoria == "Métodos Cerrados":
        metodo = st.selectbox("Método Específico", ["Bisección", "posicion falsa"])
    elif categoria == "Métodos Abiertos":
        metodo = st.selectbox("Método Específico", ["Newton-Raphson", "Secante", "Punto Fijo"])
    else:
        metodo = st.selectbox("Método Específico", ["Müller", "Bairstow"])
        
    st.markdown("---")
    st.subheader("Ecuación y Parámetros")
    
    # Entradas dinámicas según el método
    if metodo == "Punto Fijo":
        func_input = st.text_input("Función despejada g(x)", value="(x + 2)**(1/3)")
        st.caption("Escribe $g(x)$ tal que $x = g(x)$. Ejemplo: `(x + 2)**(1/3)`")
    else:
        func_input = st.text_input("Función f(x)", value="x**3 - x - 2")
        st.caption("Ejemplo: `x**3 - x - 2` o `exp(x) - 3*x`")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if metodo in ["Bisección", "posicion falsa"]:
            param_a = st.number_input("Límite a", value=1.0)
        elif metodo == "Secante":
            param_a = st.number_input("Punto x₀", value=1.0)
        else: # Newton-Raphson, Punto Fijo
            param_a = st.number_input("Punto Inicial x₀", value=1.0)
            
    with col_b:
        if metodo in ["Bisección", "posicion falsa"]:
            param_b = st.number_input("Límite b", value=2.0)
        elif metodo == "Secante":
            param_b = st.number_input("Punto x₁", value=2.0)
        else:
            param_b = None
        
    col_tol, col_iter = st.columns(2)
    with col_tol:
        tol = st.number_input("Tolerancia", value=0.0001, format="%.5f")
    with col_iter:
        max_iter = st.number_input("Max Iteraciones", value=50, step=1)

    st.button("Calcular", width="stretch", type="secondary")

# 4. ÁREA PRINCIPAL
st.markdown('<h1 class="gradient-title">Numerix</h1>', unsafe_allow_html=True)
st.write(f"Solucionador numérico de ecuaciones no lineales — **Método seleccionado: {metodo}**")
st.markdown("---")

# 5. EJECUCIÓN DIRECTA (REACTIVA)
try:
    if metodo == "Bisección":
        raiz, fxr, err_rel, iters, df_iter = biseccion(func_input, param_a, param_b, tol, max_iter)
    elif metodo == "posicion falsa":
        raiz, fxr, err_rel, iters, df_iter = regula_falsi(func_input, param_a, param_b, tol, max_iter)
    elif metodo == "Newton-Raphson":
        raiz, fxr, err_rel, iters, df_iter = newton_raphson(func_input, param_a, tol, max_iter)
    elif metodo == "Secante":
        raiz, fxr, err_rel, iters, df_iter = secante(func_input, param_a, param_b, tol, max_iter)
    elif metodo == "Punto Fijo":
        raiz, fxr, err_rel, iters, df_iter = punto_fijo(func_input, param_a, tol, max_iter)
    else:
        st.info("Este método estará disponible en las siguientes entregas del módulo.")
        st.stop()

    # 5.1 METRIC CARDS (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Raíz Encontrada (x_r)</div><div class="metric-value">{raiz:.6f}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Valor Eval.</div><div class="metric-value">{fxr:.2e}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Error Relativo (%)</div><div class="metric-value">{err_rel:.4f}%</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Iteraciones</div><div class="metric-value">{iters}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5.2 PESTAÑAS INTERACTIVAS
    tab_grafica, tab_tabla, tab_teoria = st.tabs(["📊 Gráfica Interactiva", "📋 Tabla de Iteraciones", "📖 Fundamento Teórico"])

    with tab_grafica:
        st.subheader("Comportamiento de la Función y Convergencia")
        
        f_eval, _ = parse_function(func_input)
        
        # Rango dinámico para la gráfica según los parámetros disponibles
        x_min = (param_a - 1) if param_b is None else (min(param_a, param_b) - 1)
        x_max = (param_a + 1) if param_b is None else (max(param_a, param_b) + 1)
        
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = f_eval(x_vals)
        
        fig = go.Figure()
        
        if metodo == "Punto Fijo":
            # Para punto fijo dibujamos g(x) y la recta y = x
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='g(x)', line=dict(color='#00D4FF', width=3)))
            fig.add_trace(go.Scatter(x=x_vals, y=x_vals, mode='lines', name='y = x', line=dict(color='gray', dash='dash')))
            fig.add_trace(go.Scatter(x=[raiz], y=[raiz], mode='markers', name='Punto Fijo', marker=dict(color='#FF2A6D', size=12, symbol='star')))
        else:
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='f(x)', line=dict(color='#00D4FF', width=3)))
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.7)
            fig.add_trace(go.Scatter(x=[raiz], y=[fxr], mode='markers', name='Raíz x_r', marker=dict(color='#FF2A6D', size=12, symbol='star')))

        fig.update_layout(
            template="plotly_dark",
            height=450,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis_title="x",
            yaxis_title="y",
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, width="stretch")

    with tab_tabla:
        st.subheader("Registro Paso a Paso")
        st.dataframe(df_iter, width="stretch", height=350)
        
        st.download_button(
            label="📥 Descargar Iteraciones en CSV",
            data=df_iter.to_csv(index=False).encode('utf-8'),
            file_name=f'iteraciones_{metodo.lower()}.csv',
            mime='text/csv',
        )

    with tab_teoria:
        st.subheader(f"Ecuaciones y Principios: {metodo}")
        
        if metodo == "Bisección":
            st.markdown("El **Método de Bisección** divide el intervalo a la mitad consecutivamente.")
            st.latex(r"x_r = \frac{a + b}{2}")
        elif metodo == "posicion falsa":
            st.markdown("El **Método de posicion falsa** aproxima la raíz usando una recta secante entre $a$ y $b$.")
            st.latex(r"x_r = b - \frac{f(b)(a - b)}{f(a) - f(b)}")
        elif metodo == "Newton-Raphson":
            st.markdown("El **Método de Newton-Raphson** utiliza la tangente de la función en cada iteración.")
            st.latex(r"x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}")
        elif metodo == "Secante":
            st.markdown("El **Método de la Secante** aproxima la derivada mediante diferencias finitas con dos puntos iniciales.")
            st.latex(r"x_{i+1} = x_i - \frac{f(x_i)(x_i - x_{i-1})}{f(x_i) - f(x_{i-1})}")
        elif metodo == "Punto Fijo":
            st.markdown("El **Método de Punto Fijo** reescribe $f(x) = 0$ en la forma $x = g(x)$ iterando sucesivamente.")
            st.latex(r"x_{i+1} = g(x_i)")

except Exception as e:
    st.error(f"⚠️ **Atención:** {str(e)}")