import tkinter as tk
from tkinter import messagebox, scrolledtext
import math

# Function to evaluate the given equation
def f(x, equation_str):
    try:
        return eval(equation_str, {"x": x, "math": math})
    except Exception as e:
        messagebox.showerror("Error", f"Invalid equation: {e}")
        return None

# Bisection Method following the PDF formula
def bisection_method(equation_str, xl, xu, tol, max_iter, stop_error):
    f_xl = f(xl, equation_str)
    f_xu = f(xu, equation_str)

    # Check if xl and xu bracket the root
    if f_xl * f_xu >= 0:
        messagebox.showerror("Error", "Invalid interval: f(xl) and f(xu) must have opposite signs.")
        return None

    results = "Iter  |    xl    |    xu    |    xr    |  f(xl)  |  f(xr)  |  Approx Error (%)\n"
    results += "-" * 85 + "\n"

    xr_prev = xl  # Initial value
    for i in range(1, max_iter + 1):
        xr = (xl + xu) / 2  # Compute midpoint using the correct formula
        f_xr = f(xr, equation_str)

        if f_xr is None:
            return None  # Error in function evaluation

        # Compute approximate relative error
        if i > 1:
            approx_error = abs((xr - xr_prev) / xr) * 100
        else:
            approx_error = float('inf')  # First iteration has no error

        results += f"{i:<5} | {xl:<7.5f} | {xu:<7.5f} | {xr:<7.5f} | {f_xl:<7.5f} | {f_xr:<7.5f} | {approx_error:.5f}%\n"

        # Stop solving if approximate error is less than or equal to the user-defined stop error
        if approx_error <= stop_error:
            results += f"\nRoot found: {xr:.5f} (after {i} iterations)\n"
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, results)
            return xr

        # Update the interval
        if f_xl * f_xr < 0:
            xu = xr  # Root is in lower half
        else:
            xl = xr  # Root is in upper half
            f_xl = f_xr  # Update f_xl for next iteration

        xr_prev = xr  # Store previous xr for error calculation

    results += "\nMethod did not converge within the maximum iterations.\n"
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, results)
    return None

# Function to get user input and call Bisection Method
def solve():
    try:
        equation_str = equation_entry.get()
        xl = float(xl_entry.get())
        xu = float(xu_entry.get())
        tol = float(tol_entry.get()) / 100  # Convert percentage to decimal
        max_iter = int(iter_entry.get())
        stop_error = float(stop_error_entry.get())  # User-defined stop error

        if equation_str.strip() == "":
            messagebox.showerror("Error", "Please enter a valid equation.")
            return

        bisection_method(equation_str, xl, xu, tol, max_iter, stop_error)
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric inputs.")

# GUI Setup
root = tk.Tk()
root.title("Bisection Method Solver")
root.geometry("750x650")

# Labels and Entry Fields
tk.Label(root, text="Enter equation in terms of x (e.g., x**3 - 4*x - 9):").pack(pady=5)
equation_entry = tk.Entry(root, width=40)
equation_entry.pack()

tk.Label(root, text="Lower bound (xl):").pack(pady=5)
xl_entry = tk.Entry(root)
xl_entry.pack()

tk.Label(root, text="Upper bound (xu):").pack(pady=5)
xu_entry = tk.Entry(root)
xu_entry.pack()

tk.Label(root, text="Tolerance (%):").pack(pady=5)
tol_entry = tk.Entry(root)
tol_entry.pack()

tk.Label(root, text="Maximum iterations:").pack(pady=5)
iter_entry = tk.Entry(root)
iter_entry.pack()

tk.Label(root, text="Stop at Approx. Error (%):").pack(pady=5)
stop_error_entry = tk.Entry(root)
stop_error_entry.pack()

# Solve Button
solve_button = tk.Button(root, text="Solve", command=solve)
solve_button.pack(pady=10)

# Output Display
output_text = scrolledtext.ScrolledText(root, width=90, height=20)
output_text.pack(pady=10)

# Run GUI
root.mainloop()
