import sympy as sp
import pandas as pd

def parse_function(func_str):
    """Convierte un string a una función ejecutable de SymPy en x."""
    x = sp.Symbol('x')
    # Reemplazos amigables para sintaxis común de Math/Python
    func_str = func_str.replace("^", "**")
    expr = sp.sympify(func_str)
    f = sp.lambdify(x, expr, modules=["numpy", "math"])
    return f, expr

def biseccion(func_str, a, b, tol=0.0001, max_iter=50):
    f, _ = parse_function(func_str)
    
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        raise ValueError("El intervalo [a, b] no contiene un cambio de signo (f(a) * f(b) >= 0).")
    
    iterations = []
    xr_prev = None
    
    for i in range(1, max_iter + 1):
        xr = (a + b) / 2.0
        fxr = f(xr)
        
        # Cálculo del error relativo aproximado
        if xr_prev is not None and xr != 0:
            error = abs((xr - xr_prev) / xr) * 100
        else:
            error = 100.0 if i == 1 else 0.0
            
        iterations.append({
            "Iteración": i,
            "a": round(a, 6),
            "b": round(b, 6),
            "x_r": round(xr, 6),
            "f(x_r)": round(fxr, 8),
            "Error (%)": round(error, 6)
        })
        
        if abs(fxr) < tol or error < (tol * 100):
            break
            
        # Actualización de intervalo
        if f(a) * fxr < 0:
            b = xr
        else:
            a = xr
            
        xr_prev = xr
        
    df_results = pd.DataFrame(iterations)
    return xr, fxr, error, len(iterations), df_results

def regula_falsi(func_str, a, b, tol=0.0001, max_iter=50):
    f, _ = parse_function(func_str)
    
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        raise ValueError("El intervalo [a, b] no contiene un cambio de signo.")
        
    iterations = []
    xr_prev = None
    
    for i in range(1, max_iter + 1):
        fa = f(a)
        fb = f(b)
        xr = b - (fb * (a - b)) / (fa - fb)
        fxr = f(xr)
        
        if xr_prev is not None and xr != 0:
            error = abs((xr - xr_prev) / xr) * 100
        else:
            error = 100.0 if i == 1 else 0.0
            
        iterations.append({
            "Iteración": i,
            "a": round(a, 6),
            "b": round(b, 6),
            "x_r": round(xr, 6),
            "f(x_r)": round(fxr, 8),
            "Error (%)": round(error, 6)
        })
        
        if abs(fxr) < tol or error < (tol * 100):
            break
            
        if fa * fxr < 0:
            b = xr
        else:
            a = xr
            
        xr_prev = xr
        
    df_results = pd.DataFrame(iterations)
    return xr, fxr, error, len(iterations), df_results