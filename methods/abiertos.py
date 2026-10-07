import sympy as sp
import pandas as pd
from methods.cerrados import parse_function

def newton_raphson(func_str, x0, tol=0.0001, max_iter=50):
    f, expr = parse_function(func_str)
    
    # Derivación simbólica automática con SymPy
    x_sym = sp.Symbol('x')
    df_expr = sp.diff(expr, x_sym)
    df = sp.lambdify(x_sym, df_expr, modules=["numpy", "math"])
    
    iterations = []
    x_curr = float(x0)
    
    for i in range(1, max_iter + 1):
        fx = f(x_curr)
        dfx = df(x_curr)
        
        if dfx == 0:
            raise ValueError(f"La derivada f'(x) se hizo cero en la iteración {i}. El método no puede continuar.")
            
        x_next = x_curr - (fx / dfx)
        
        error = abs((x_next - x_curr) / x_next) * 100 if x_next != 0 else 0.0
        
        iterations.append({
            "Iteración": i,
            "x_i": round(x_curr, 6),
            "f(x_i)": round(fx, 8),
            "f'(x_i)": round(dfx, 8),
            "x_{i+1}": round(x_next, 6),
            "Error (%)": round(error, 6)
        })
        
        if abs(fx) < tol or error < (tol * 100):
            break
            
        x_curr = x_next
        
    df_results = pd.DataFrame(iterations)
    return x_next, f(x_next), error, len(iterations), df_results

def secante(func_str, x0, x1, tol=0.0001, max_iter=50):
    f, _ = parse_function(func_str)
    
    iterations = []
    
    for i in range(1, max_iter + 1):
        fx0 = f(x0)
        fx1 = f(x1)
        
        if (fx1 - fx0) == 0:
            raise ValueError("División por cero en la fórmula de la secante (f(x1) - f(x0) = 0).")
            
        x2 = x1 - (fx1 * (x1 - x0)) / (fx1 - fx0)
        fx2 = f(x2)
        
        error = abs((x2 - x1) / x2) * 100 if x2 != 0 else 0.0
        
        iterations.append({
            "Iteración": i,
            "x_{i-1}": round(x0, 6),
            "x_i": round(x1, 6),
            "x_{i+1}": round(x2, 6),
            "f(x_{i+1})": round(fx2, 8),
            "Error (%)": round(error, 6)
        })
        
        if abs(fx2) < tol or error < (tol * 100):
            break
            
        x0 = x1
        x1 = x2
        
    df_results = pd.DataFrame(iterations)
    return x2, fx2, error, len(iterations), df_results

def punto_fijo(gx_str, x0, tol=0.0001, max_iter=50):
    g, _ = parse_function(gx_str)
    
    iterations = []
    x_curr = float(x0)
    
    for i in range(1, max_iter + 1):
        x_next = g(x_curr)
        
        error = abs((x_next - x_curr) / x_next) * 100 if x_next != 0 else 0.0
        
        iterations.append({
            "Iteración": i,
            "x_i": round(x_curr, 6),
            "g(x_i)": round(x_next, 6),
            "Error (%)": round(error, 6)
        })
        
        if error < (tol * 100):
            break
            
        x_curr = x_next
        
    df_results = pd.DataFrame(iterations)
    return x_next, x_next, error, len(iterations), df_results