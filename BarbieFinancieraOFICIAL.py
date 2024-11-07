import tkinter as tk
from tkinter import messagebox
import sqlite3

# Variables globales para almacenar los datos
ingreso_mensual = [0]  # Lista que contiene el ingreso mensual ingresado por el usuario
categoria_montos = []  # Lista que contiene las categorías y montos ingresados
mes_seleccionado = [""]  # Lista que contiene el mes seleccionado

def open_mes_window(volver_callback):
    """
    Abre una ventana para seleccionar el mes y guarda el mes seleccionado en la base de datos.

    :param volver_callback: Función de devolución de llamada que se ejecuta después de seleccionar el mes.
    """
    try:
        # Conectar a la base de datos y crear la tabla 'selected_month' si no existe
        conn = sqlite3.connect('barbi_es.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS selected_month (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                month TEXT NOT NULL
            )
        ''')
        conn.commit()

        # Crear la ventana principal
        ventana = tk.Tk()
        ventana.title("Seleccionar Mes")
        ventana.state("zoomed")  # Maximizar la ventana
        ventana.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

        # Crear un marco para centrar los widgets
        frame = tk.Frame(ventana, bg="#FFD1DC")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Lista de meses
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Variable para almacenar el mes seleccionado
        mes_var = tk.StringVar(value=meses[0])

        # Crear un menú desplegable para seleccionar el mes
        font_option_menu = ('Century Gothic', 16)
        option_menu = tk.OptionMenu(frame, mes_var, *meses)
        option_menu.config(font=font_option_menu, width=20)
        option_menu.pack(pady=20)

        # Función para guardar el mes seleccionado en la base de datos
        def guardar_mes():
            mes_seleccionado[0] = mes_var.get()
            cursor.execute('''
                INSERT INTO selected_month (month)
                VALUES (?)
            ''', (mes_seleccionado[0],))
            conn.commit()

        # Botón para guardar el mes seleccionado
        font_button = ('Century Gothic', 16)
        button_guardar = tk.Button(frame, text="Agregar Mes", font=font_button, command=guardar_mes)
        button_guardar.pack(pady=20)

        # Botón para continuar a la siguiente ventana
        boton_volver = tk.Button(frame, text="Continuar", font=font_button, command=lambda: [ventana.destroy(), volver_callback()])
        boton_volver.pack(pady=20)

        frame.pack(expand=True)
        ventana.mainloop()

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

    finally:
        conn.close()

def open_ingreso_window(ingreso_mensual, next_window_callback):
    """
    Abre una ventana para ingresar el monto de ingresos mensuales y guarda el ingreso en la base de datos.

    :param ingreso_mensual: Lista que almacena el ingreso mensual.
    :param next_window_callback: Función de devolución de llamada que se ejecuta después de ingresar el monto.
    """
    try:
        # Conectar a la base de datos y crear la tabla 'monthly_income' si no existe
        conn = sqlite3.connect('barbi_es.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_income (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income REAL NOT NULL,
                month TEXT NOT NULL
            )
        ''')
        conn.commit()

        # Crear la ventana principal
        new_window = tk.Tk()
        new_window.title("Barbie Financiera")
        new_window.state('zoomed')  # Maximizar la ventana
        new_window.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

        # Crear un marco para centrar los widgets
        frame = tk.Frame(new_window, bg="#FFD1DC")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta y campo de entrada para el monto de ingresos
        font_monto = ('Century Gothic', 16)
        label_monto = tk.Label(frame, text="Monto de ingresos totales mensuales:", font=font_monto, bg="#FFD1DC")
        label_monto.pack(pady=5)
        entry_monto = tk.Entry(frame, font=font_monto)
        entry_monto.pack(pady=5)

        # Función para guardar el monto de ingresos en la base de datos
        def guardar_datos():
            try:
                ingreso_mensual[0] = float(entry_monto.get())
                if ingreso_mensual[0] < 0:
                    raise ValueError("El monto no puede ser negativo.")
                cursor.execute('''
                    INSERT INTO monthly_income (income, month)
                    VALUES (?, ?)
                ''', (ingreso_mensual[0], mes_seleccionado[0]))
                conn.commit()
                messagebox.showinfo("Éxito", f"Ingresos totales mensuales guardados: ${ingreso_mensual[0]:.2f}")
                new_window.destroy()
                next_window_callback()
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada no válida: {e}")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error en la base de datos: {e}")

        # Botón para guardar los datos y continuar
        font_button = ('Century Gothic', 12)
        button_guardar = tk.Button(frame, text="Continuar", font=font_button, command=guardar_datos)
        button_guardar.pack(pady=20)
        frame.pack(expand=True)

        # Cerrar la conexión a la base de datos al cerrar la ventana
        def on_closing():
            conn.close()
            new_window.destroy()
        new_window.protocol("WM_DELETE_WINDOW", on_closing)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

def open_categoria_window(categoria_montos, next_window_callback):
    """
    Abre una ventana para ingresar categorías de gastos y guarda los datos en la base de datos.

    :param categoria_montos: Lista que almacena las categorías y montos.
    :param next_window_callback: Función de devolución de llamada que se ejecuta después de ingresar los datos.
    """
    try:
        # Conectar a la base de datos y crear la tabla 'categories' si no existe
        conn = sqlite3.connect('barbi_es.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                amount REAL NOT NULL,
                month TEXT NOT NULL
            )
        ''')
        conn.commit()

        # Crear la ventana principal
        new_window = tk.Tk()
        new_window.title("Barbie Financiera")
        new_window.state('zoomed')  # Maximizar la ventana
        new_window.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

        # Crear un marco para centrar los widgets
        frame = tk.Frame(new_window, bg="#FFD1DC")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta y campo de entrada para la categoría de gasto
        font_label = ('Century Gothic', 16)
        label_categoria = tk.Label(frame, text="Nombre de la categoría:", font=font_label, bg="#FFD1DC")
        label_categoria.pack(pady=5)
        entry_categoria = tk.Entry(frame, font=font_label)
        entry_categoria.pack(pady=5)

        # Etiqueta y campo de entrada para el monto del gasto
        label_monto = tk.Label(frame, text="Monto:", font=font_label, bg="#FFD1DC")
        label_monto.pack(pady=5)
        entry_monto = tk.Entry(frame, font=font_label)
        entry_monto.pack(pady=5)

        # Función para guardar la categoría y monto en la base de datos
        def guardar_datos():
            try:
                categoria = entry_categoria.get()
                monto = float(entry_monto.get())
                if monto < 0:
                    raise ValueError("El monto no puede ser negativo.")
                cursor.execute('''
                    INSERT INTO categories (name, amount, month)
                    VALUES (?, ?, ?)
                ''', (categoria, monto, mes_seleccionado[0]))
                conn.commit()
                categoria_montos.append((categoria, monto))
                messagebox.showinfo("Éxito", f"Categoría '{categoria}' con monto ${monto:.2f} guardada.")
                entry_categoria.delete(0, tk.END)
                entry_monto.delete(0, tk.END)
            except ValueError as e:
                messagebox.showerror("Error", f"Entrada no válida: {e}")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error en la base de datos: {e}")

        # Botón para guardar los datos y continuar
        font_button = ('Century Gothic', 12)
        button_guardar = tk.Button(frame, text="Agregar Categoría", font=font_button, command=guardar_datos)
        button_guardar.pack(pady=20)
        button_continuar = tk.Button(frame, text="Continuar", font=font_button, command=lambda: [conn.close(), new_window.destroy(), next_window_callback()])
        button_continuar.pack(pady=20)
        frame.pack(expand=True)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

def open_opciones_window(next_gastos_callback, next_detalle_callback, next_categoria_callback, next_ingreso_callback, next_mes_callback):
    """
    Abre la ventana de opciones, permitiendo navegar entre diferentes funcionalidades.

    :param next_gastos_callback: Función de devolución de llamada para mostrar el balance.
    :param next_detalle_callback: Función de devolución de llamada para mostrar el detalle de categorías.
    :param next_categoria_callback: Función de devolución de llamada para agregar una nueva categoría.
    :param next_ingreso_callback: Función de devolución de llamada para actualizar los ingresos.
    :param next_mes_callback: Función de devolución de llamada para seleccionar un nuevo mes.
    """
    # Crear la ventana principal
    opciones_window = tk.Tk()
    opciones_window.title("Barbie Financiera")
    opciones_window.geometry("1500x800")
    opciones_window.state("zoomed")  # Maximizar la ventana
    opciones_window.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

    # Crear un marco para centrar los widgets
    frame = tk.Frame(opciones_window, bg="#FFD1DC")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Definir el estilo de fuente para los botones
    font_button = ('Century Gothic', 16)

    # Función para borrar todos los datos de la base de datos
    def borrar_datos():
        if messagebox.askyesno("Confirmación", "¿Seguro que deseas eliminar todos los datos?"):
            try:
                conn = sqlite3.connect('barbi_es.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM monthly_income')
                cursor.execute('DELETE FROM categories')
                cursor.execute('DELETE FROM selected_month')
                conn.commit()
                messagebox.showinfo("Éxito", "Todos los datos han sido eliminados.")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error en la base de datos: {e}")
            finally:
                conn.close()

    # Botones para navegar entre las diferentes funcionalidades
    boton_balance = tk.Button(frame, text="Balance", font=font_button, command=next_gastos_callback)
    boton_balance.pack(pady=20)

    boton_detalle = tk.Button(frame, text="Detalle de Categorías", font=font_button, command=next_detalle_callback)
    boton_detalle.pack(pady=20)

    boton_categoria = tk.Button(frame, text="Agregar Categoría", font=font_button, command=next_categoria_callback)
    boton_categoria.pack(pady=20)

    boton_ingreso = tk.Button(frame, text="Actualizar Ingresos", font=font_button, command=next_ingreso_callback)
    boton_ingreso.pack(pady=20)

    boton_mes = tk.Button(frame, text="Seleccionar Mes", font=font_button, command=next_mes_callback)
    boton_mes.pack(pady=20)

    boton_borrar = tk.Button(frame, text="Borrar Datos Actuales", font=font_button, command=borrar_datos)
    boton_borrar.pack(pady=20)

    boton_cerrar = tk.Button(frame, text="Cerrar Sesión", font=font_button, command=opciones_window.destroy)
    boton_cerrar.pack(pady=20)

    frame.pack(expand=True)

def open_gastos_window(total_gastos, dinero_disponible, volver_callback):
    """
    Abre una ventana para mostrar el total de gastos y el dinero disponible.

    :param total_gastos: Monto total de los gastos.
    :param dinero_disponible: Monto de dinero disponible después de los gastos.
    :param volver_callback: Función de devolución de llamada para volver a la ventana de opciones.
    """
    # Crear la ventana principal
    ventana_gastos = tk.Tk()
    ventana_gastos.title("Barbie Financiera")
    ventana_gastos.state("zoomed")  # Maximizar la ventana
    ventana_gastos.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

    # Crear un marco para centrar los widgets
    frame = tk.Frame(ventana_gastos, bg="#FFD1DC")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Etiquetas para mostrar el total de gastos y el dinero disponible
    font_label = ('Century Gothic', 16)
    label_gastos = tk.Label(frame, text=f"Total de Gastos: ${total_gastos:.2f}", font=font_label, bg="#FFD1DC")
    label_gastos.pack(pady=10)
    label_disponible = tk.Label(frame, text=f"Dinero Disponible: ${dinero_disponible:.2f}", font=font_label, bg="#FFD1DC")
    label_disponible.pack(pady=10)

    # Botón para volver a la ventana de opciones
    font_button = ('Century Gothic', 16)
    boton_volver = tk.Button(frame, text="Volver", font=font_button, command=lambda: [ventana_gastos.destroy(), volver_callback()])
    boton_volver.pack(pady=20)
    frame.pack(expand=True)

def open_detalle_categorias_window(categoria_montos, volver_callback):
    """
    Abre una ventana para mostrar el detalle de las categorías de gastos.

    :param categoria_montos: Lista que contiene las categorías y montos.
    :param volver_callback: Función de devolución de llamada para volver a la ventana de opciones.
    """
    try:
        # Conectar a la base de datos y obtener los detalles de las categorías
        conn = sqlite3.connect('barbi_es.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, amount, month FROM categories
            ORDER BY month
        ''')
        rows = cursor.fetchall()

        # Crear la ventana principal
        ventana_detalle = tk.Tk()
        ventana_detalle.title("Barbie Financiera")
        ventana_detalle.state("zoomed")  # Maximizar la ventana
        ventana_detalle.config(bg="#FFD1DC")  # Establecer el fondo rosita pálido

        # Crear un marco para centrar los widgets
        frame = tk.Frame(ventana_detalle, bg="#FFD1DC")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Etiqueta para el título
        font_label = ('Century Gothic', 16)
        label_titulo = tk.Label(frame, text="Detalle de Categorías", font=font_label, bg="#FFD1DC")
        label_titulo.pack(pady=10)

        # Mostrar los detalles de las categorías
        for row in rows:
            categoria, monto, mes = row
            label_detalle = tk.Label(frame, text=f"{mes} - {categoria}: ${monto:.2f}", font=font_label, bg="#FFD1DC")
            label_detalle.pack(pady=5)

        # Botón para volver a la ventana de opciones
        font_button = ('Century Gothic', 16)
        boton_volver = tk.Button(frame, text="Volver", font=font_button, command=lambda: [ventana_detalle.destroy(), volver_callback()])
        boton_volver.pack(pady=20)
        frame.pack(expand=True)

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error en la base de datos: {e}")

    finally:
        conn.close()

def open_login_window(root, next_window_callback):
    """
    Abre una ventana para el inicio de sesión.

    :param root: Ventana raíz de Tkinter.
    :param next_window_callback: Función de devolución de llamada que se ejecuta después de un inicio de sesión exitoso.
    """
    root.title("Barbie Financiera")
    root.configure(bg="#FFD1DC")
    root.state('zoomed')  # Maximizar la ventana

    # Definir los estilos de las etiquetas y entradas
    label_font = ("Century Gothic", 16, "bold")
    entry_font = ("Century Gothic", 14)
    button_font = ("Century Gothic", 14)

    # Crear un marco para centrar los widgets
    frame = tk.Frame(root, bg="#FFD1DC")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Etiqueta y entrada para el usuario
    label_usuario = tk.Label(frame, text="Usuario:", font=label_font, bg="#FFD1DC")
    label_usuario.pack(pady=10)
    entry_usuario = tk.Entry(frame, font=entry_font)
    entry_usuario.pack(pady=10)

    # Etiqueta y entrada para la contraseña
    label_contrasena = tk.Label(frame, text="Contraseña:", font=label_font, bg="#FFD1DC")
    label_contrasena.pack(pady=10)
    entry_contrasena = tk.Entry(frame, font=entry_font, show="*")
    entry_contrasena.pack(pady=10)

    # Función para manejar el inicio de sesión
    def login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()
        if usuario == "admin" and contrasena == "password":
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
            root.destroy()
            next_window_callback()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Botón para iniciar sesión
    boton_login = tk.Button(frame, text="Iniciar Sesión", font=button_font, command=login)
    boton_login.pack(pady=20)
    frame.pack(expand=True)

# Funciones de devolución de llamada para el flujo de ventanas
def open_mes_window_callback():
    open_mes_window(open_new_window)

def open_new_window():
    open_ingreso_window(ingreso_mensual, open_complete_form_window)

def open_complete_form_window():
    open_categoria_window(categoria_montos, open_opciones_window_callback)

def open_opciones_window_callback():
    open_opciones_window(open_gastos_window_callback, open_detalle_categorias_window_callback, open_complete_form_window, open_new_window, open_mes_window_callback)

def open_gastos_window_callback():
    total_gastos = sum(monto for _, monto in categoria_montos)
    dinero_disponible = ingreso_mensual[0] - total_gastos
    open_gastos_window(total_gastos, dinero_disponible, open_opciones_window_callback)

def open_detalle_categorias_window_callback():
    open_detalle_categorias_window(categoria_montos, open_opciones_window_callback)

# Iniciar la aplicación
root = tk.Tk()
open_login_window(root, open_mes_window_callback)
root.mainloop()
