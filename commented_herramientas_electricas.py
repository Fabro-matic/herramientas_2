from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import os, sys

def resource_path(relative_path):
    try:
        base_path = os.path.join(os.path.dirname(sys.argv[0]), '..', 'Resources')
        return os.path.join(base_path, relative_path)
    except Exception:
        return os.path.abspath(relative_path)

#print(resource_path('color_after_name.db'))
class Herramientas:
    #db_name = resource_path('don't_use_color_after_name.db')
    db_name = 'herramientas_electricas.db'


    def __init__(self, window):
        self.wind =  window
        self.wind.title('HERRAMIENTAS')

              

        #Creating a Frame Container (FRAME)
        frame = LabelFrame(self.wind, text = 'REGISTRAR NUEVA HERRAMIENTA')
        frame.grid(row = 0, column = 0, columnspan = 2, pady = 10)

        #Definning a bold font tied to the root
        self.bold_font = tkFont.Font(root = self.wind, family = "Helvetica", size = 12, weight = "bold")
        self.emoji_font = tkFont.Font(root = self.wind, family = "Segoe UI Emoji", size = 12)


        #Nombre Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row = 1, column = 1)

        
        #Marca Input
        Label(frame, text = 'Marca: ').grid(row = 3, column = 0)
        self.marca = Entry(frame)
        self.marca.grid(row = 3, column = 1)

        #Modelo Input
        Label(frame, text = 'Modelo: ').grid(row = 4, column = 0)
        self.modelo = Entry(frame)
        self.modelo.grid(row = 4, column = 1)

        #N° de serie input
        Label(frame, text = 'N° de Serie: ').grid(row = 5, column = 0)
        self.ndeserie = Entry(frame)
        self.ndeserie.grid(row = 5, column = 1)
        
        #Fecha de Compra
        Label(frame, text = 'Fecha de Compra: ').grid(row = 6, column = 0)
        self.fechadecompra = Entry(frame)
        self.fechadecompra.grid(row = 6, column = 1)

        #Ubicación
        Label(frame, text = 'Ubicación: ').grid(row = 7, column = 0)
        self.ubicación = Entry(frame)
        self.ubicación.grid(row = 7, column = 1)

        #Botón Agregar Herramienta
        ttk.Button(frame, text = 'AGREGAR NUEVA HERRAMIENTA', command = self.agregar_herramientas_electricas).grid(row = 8, columnspan = 2, sticky = W + E)

        #Output Messages
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 9, column = 0, columnspan = 2, sticky = W + E)


        #Tabla de Herramientas con Scrollbar
        
        #Frame contenedor para tabla + scrollbar
        tabla_frame = Frame(self.wind)
        tabla_frame.grid(row = 11, column = 0, columnspan = 2, sticky = W + E)

       

        #Asegurar que el contenedor princpal permita la expansión
        self.wind.grid_rowconfigure(10, weight = 1)
        self.wind.grid_columnconfigure(0, weight = 1)

        #Configurar expansión del frame
        tabla_frame.grid_rowconfigure(0, weight = 1)
        tabla_frame.grid_columnconfigure(0, weight = 1)
        
        #Treeview
        self.tree = ttk.Treeview(tabla_frame, height = 40, columns = ("col1", "col2", "col3", "col4", "col5"))
        self.tree.grid(row = 0, column = 0, sticky = "nsew")

        #Scroll vertical
        scroll_y = ttk.Scrollbar(tabla_frame, orient = "vertical", command = self.tree.yview)
        scroll_y.grid(row = 0, column = 1, sticky = "ns")
        self.tree.configure(yscrollcommand = scroll_y.set)

        #Scroll horizontal
        scroll_x = ttk.Scrollbar(tabla_frame, orient = "horizontal", command = self.tree.xview)
        scroll_x.grid(row = 1, column = 0, sticky = "ew")
        self.tree.configure(xscrollcommand = scroll_x.set)


        #Headings
        self.tree.heading('#0', text = 'nombre', anchor = W)
        self.tree.heading('col1', text = 'marca', anchor = W)
        self.tree.heading('col2', text = 'modelo', anchor = W)
        self.tree.heading('col3', text = 'n_de_serie', anchor = W)
        self.tree.heading('col4', text = 'fecha_de_compra', anchor = W)
        self.tree.heading('col5', text = 'ubicación', anchor = W)
        
        #Ajustar ancho de columnas para que no se desborden
        self.tree.column('#0', width = 150, stretch=False)
        self.tree.column('col1', width = 100, stretch=False)
        self.tree.column('col2', width = 120, stretch=False)
        self.tree.column('col3', width = 120, stretch=False)
        self.tree.column('col4', width = 150, stretch=False)
        self.tree.column('col5', width = 120, stretch=False)

        # Evento doble clic en fila
        self.tree.bind("<Double-1>", self.on_double_click)

        #Botones de EDITAR Y BORRAR registros
        botones_frame = Frame(self.wind)
        botones_frame.grid(row=11, column=0, columnspan=2, pady=10, sticky=W+E)

        
        ttk.Button(botones_frame, text='EDITAR', command=self.editar_herramienta_electrica).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(botones_frame, text='BORRAR', command=self.delete_registro).pack(side=LEFT, expand=True, fill=X)
        ttk.Button(botones_frame, text='IMPRIMIR SELECCIÓN', command=self.imprimir_seleccion).pack(side=LEFT, expand=True, fill=X)
        
        # Label para mostrar cantidad total de herramientas
        self.total_label = Label(self.wind, text = 'TOTAL HERRAMIENTAS: 0', font = self.bold_font, fg = "blue")
        self.total_label.grid(row = 12 , column = 0, columnspan = 2, pady = 10, sticky = W+E)

        #Llenar la tabla
        self.get_herramientas_electricas()


#PARA OPERAR CON LA DB
    def run_query(self, query, parameters = ()): #Para ejecutar consultas en la db, obtener parámetros (si los hay)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
            rows = result.fetchall()   # acá lo convertís en lista
        return rows
    
    def get_herramientas_electricas(self):
        #Cleaning table
        records = self.tree.get_children() #Para obterner todos los datos de la tabla
        for element in records:
            self.tree.delete(element) 

        query = 'SELECT * FROM herramientas_electricas ORDER BY nombre collate nocase ASC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 'end', iid=row[0], text = row [1], values = (row[2], row[3], row[4], row[5], row[6]))
        
        #Actualizar el Label con la cantidad total
        total = len(db_rows)
        self.total_label.config(text = "Total de herramientas: " + str(total))

    def validation(self):
        return (len(self.nombre.get()) != 0 and len(self.marca.get()) != 0 and len(self.modelo.get()) !=0 and len(self.ndeserie.get()) != 0 and len(self.fechadecompra.get()) != 0 and len(self.ubicación.get()) != 0) 

    def agregar_herramientas_electricas(self):
        if self.validation():
            query = 'INSERT INTO herramientas_electricas VALUES(NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (self.nombre.get(), self.marca.get(), self.modelo.get(), self.ndeserie.get(), self.fechadecompra.get(), self.ubicación.get())
            self.run_query(query, parameters)
            self.message['text'] = '✅¡HERRAMIENTA << {} >> AGREGADA EXITOSAMENTE. 👍'.format(self.nombre.get())
            self.message['fg'] = 'green'
            self.message['font'] = self.bold_font
            self.nombre.delete(0, END)
            self.marca.delete(0, END)
            self.modelo.delete(0, END)
            self.ndeserie.delete(0, END)
            self.fechadecompra.delete(0, END)
            self.ubicación.delete(0, END)

            self.get_herramientas_electricas()

        else:           
            self.message['text'] = 'TENÉS QUE COMPLETAR TODA LA INFO DE ARRIBA PARA AGREGAR. USÁ - - - -  SI NO LA TENÉS ;D'
            self.message['fg'] = 'red'
            self.message['font'] = self.bold_font
            self.get_herramientas_electricas()
        
        #Refrescar tabla y contador
        self.get_herramientas_electricas()


    def delete_registro(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = '❌ PARA BORRAR, SELECCIONE UNA HERREMIENTA ❌'
            self.message['fg'] = 'red'
            self.message['font'] = self.bold_font
            

            
            return            
        self.message['text'] = ''
        selected_item = self.tree.selection()[0]
        nombre = self.tree.item(self.tree.selection())['text']
        
        #Cuadro de confirmación con icono de advertencia
        respuesta = messagebox.askyesno(
            'CONFIRMÁME BORRAR, X FA',
            '¿¿¿QUERÉS BORRAR LA HERRAMIENTA << {} >> DENSERIO MBOLÓ????? 🤣'.format(nombre),
            icon = 'warning',
            )
       
        if respuesta:
            query = 'DELETE FROM herramientas_electricas WHERE id = ?'
            self.run_query(query, (selected_item, ))
            self.message['text'] = '✅ ¡HERRAMIENTA << {} >> BORRADA EXITOSAMENTE 👍'.format(nombre)
            self.message['fg'] = 'green'
            self.message ['font'] = self.bold_font
            self.get_herramientas_electricas()
           
        else:
            self.message['text'] = 'NO SE BORRÓ LA HERRAMIENTA << {} >>'.format(nombre)
            self.message['fg'] = 'blue'
            self.message['font'] = self.bold_font


    def editar_herramienta_electrica(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = '❌ PARA EDITAR, SELECCIONÁ UNA HERREMIENTA. ❌'
            self.message['fg'] = 'red'
            self.message['font'] = self.bold_font
            return
        id_registro = self.tree.selection()[0]       
        nombre = self.tree.item(self.tree.selection())['text']
        marca = self.tree.item(self.tree.selection())['values'][0]
        modelo = self.tree.item(self.tree.selection())['values'][1]
        n_de_serie = self.tree.item(self.tree.selection())['values'][2]
        fecha_de_compra = self.tree.item(self.tree.selection())['values'][3]
        ubicación = self.tree.item(self.tree.selection())['values'][4]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'EDITAR HERRAMIENTA'

        #Nombre
        Label(self.edit_wind, text = 'Nombre:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = nombre), state = 'readonly').grid(row = 0, column = 2)
        #Nuevo Nombre
        Label(self.edit_wind, text = 'Nuevo Nombre:').grid(row =1 , column =1)
        nuevo_nombre = Entry(self.edit_wind)
        nuevo_nombre.grid(row = 1, column = 2)

        #Marca
        Label(self.edit_wind, text = 'Marca:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = marca), state = 'readonly').grid(row = 4, column = 2)
        #Nueva Marca
        Label(self.edit_wind, text = 'Nueva Marca:').grid(row =5 , column =1)
        nueva_marca = Entry(self.edit_wind)
        nueva_marca.grid(row = 5, column = 2)

        #Modelo
        Label(self.edit_wind, text = 'Modelo:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = modelo), state = 'readonly').grid(row = 6, column = 2)
        #Nuevo Modelo
        Label(self.edit_wind, text = 'Nuevo Modelo:').grid(row =7 , column =1)
        nuevo_modelo = Entry(self.edit_wind)
        nuevo_modelo.grid(row = 7, column = 2)

        #N° de serie
        Label(self.edit_wind, text = 'N° de Serie:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = n_de_serie), state = 'readonly').grid(row = 8, column = 2)
        #Nuevo n° de serie
        Label(self.edit_wind, text = 'Nuevo N° de Serie:').grid(row =9 , column =1)
        nuevo_n_de_serie = Entry(self.edit_wind)
        nuevo_n_de_serie.grid(row = 9, column = 2)

        #Fecha de Compra
        Label(self.edit_wind, text = 'Fecha de Compra:').grid(row = 10, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = fecha_de_compra), state = 'readonly').grid(row = 10, column = 2)
        #Nueva Fecha de Compra
        Label(self.edit_wind, text = 'Nueva Fecha de Compra:').grid(row =11 , column =1)
        nueva_fecha_de_compra = Entry(self.edit_wind)
        nueva_fecha_de_compra.grid(row = 11, column = 2)

        #Ubicación
        Label(self.edit_wind, text = 'Ubicación:').grid(row = 12, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = ubicación), state = 'readonly').grid(row = 12, column = 2)
        #Nueva ubicación
        Label(self.edit_wind, text = 'Nueva Ubicación:').grid(row =13 , column =1)
        nueva_ubicación = Entry(self.edit_wind)
        nueva_ubicación.grid(row = 13, column = 2)

        Button(self.edit_wind, text = 'EDITAR', command = lambda: self.editar_registros(nuevo_nombre.get(), nombre, nueva_marca.get(), marca, nuevo_modelo.get(), modelo, nuevo_n_de_serie.get(), n_de_serie, nueva_fecha_de_compra.get(), fecha_de_compra, nueva_ubicación.get(), ubicación, id_registro)).grid(row = 14, column =2, sticky = W)

    def editar_registros(self,nuevo_nombre, nombre, nueva_marca, marca, nuevo_modelo, modelo, nuevo_n_de_serie, n_de_serie, nueva_fecha_de_compra, fecha_de_compra, nueva_ubicación, ubicación, id):
      
        if nuevo_nombre.strip() == "":
            nuevo_nombre = nombre
        if nueva_marca.strip() == "":
            nueva_marca = marca
        if nuevo_modelo.strip() == "":
            nuevo_modelo = modelo
        if nuevo_n_de_serie.strip() == "":
            nuevo_n_de_serie = n_de_serie
        if nueva_fecha_de_compra.strip() == "":
            nueva_fecha_de_compra = fecha_de_compra
        if nueva_ubicación.strip() == "":
            nueva_ubicación = ubicación

        query = 'UPDATE herramientas_electricas SET nombre = ?, marca = ?, modelo = ?, n_de_serie = ?, fecha_de_compra = ?, ubicación = ? WHERE id = ? '
        parameters = (nuevo_nombre, nueva_marca, nuevo_modelo, nuevo_n_de_serie, nueva_fecha_de_compra, nueva_ubicación, id)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = '✅ HERRAMIENTA << {} >> EDITADA CORRECTAMENTE 👍'.format(nombre)
        self.message['fg'] = 'green'
        self.message['font'] = self.bold_font
        self.get_herramientas_electricas()
    
    def on_double_click(self, event):
        self.message['text'] = ''
        if not self.tree.selection():
            return
        id_registro = self.tree.selection()[0]
        item = self.tree.item(id_registro)
        ubicación = item['values'][4]   # columna ubicación
        self.mostrar_por_ubicación(ubicación)

    def mostrar_por_ubicación(self, ubicación):
        self.ubic_win = Toplevel()
        self.ubic_win.title = 'HERRAMIENTAS EN "{}"'.format(ubicación.upper())

        
        Label(self.ubic_win, text = 'HERRAMIENTAS EN "{}"'.format(ubicación.upper()), font = self.bold_font, fg = "blue").grid(row = 0, column = 0, columnspan = 2, pady = 10)
        
        # Label para mostrar cantidad total de herramientas por ubicación
        self.total_label_ubi = Label(self.ubic_win, text = 'TOTAL: 0', font = self.bold_font, fg = "blue")
        self.total_label_ubi.grid(row = 1, column = 0, columnspan = 2, pady = 10, sticky = W+E)
        ttk.Button(self.ubic_win, text="IMPRIMIR TODO", command=lambda: self.imprimir_registros(tree_ubic, "HERRAMIENTAS EN {}".format(ubicación.upper()))).grid(row=3, column=0, pady=10, sticky=W+E)

        tree_ubic = ttk.Treeview(self.ubic_win, height = 10, columns = ("col1", "col2", "col3", "col4", "col5"))
        tree_ubic.grid(row = 2, column = 0, columnspan = 2)

        tree_ubic.heading('#0', text = 'nombre', anchor = CENTER)
        tree_ubic.heading('col1', text = 'marca', anchor = CENTER)
        tree_ubic.heading('col2', text = 'modelo', anchor = CENTER)
        tree_ubic.heading('col3', text = 'n_de_serie', anchor = CENTER)
        tree_ubic.heading('col4', text = 'fecha_de_compra', anchor = CENTER)
        tree_ubic.heading('col5', text = 'ubicación', anchor = CENTER)

        def normalizar_ubicación(ubicación):
            return ubicación.strip().upper()

        query = 'SELECT * FROM herramientas_electricas WHERE UPPER(ubicación) = ? ORDER BY nombre collate nocase ASC'
        db_rows = self.run_query(query, (normalizar_ubicación(ubicación),))
        for row in db_rows:
            tree_ubic.insert('', 'end', iid = row[0], text = row[1], values = (row[2], row[3], row[4], row[5], row[6]))
        total = len(db_rows)
        self.total_label_ubi.config(text = "Total: " + str(total))



    def imprimir_registros(self, tree, titulo):
        registros = tree.get_children()
        if not registros:
            messagebox.showwarning("Imprimir", "SELECCIONE UNO O MÁS HERRAMIENTAS PARA IMPRIMIR.")
            return

        archivo = "herramientas.pdf"
        c = canvas.Canvas(archivo, pagesize=A4)
        width, height = A4

        # Título
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 50, titulo)
        c.setFont("Helvetica", 10)

        # Encabezados
        encabezados = ["Nombre", "Marca", "Modelo", "N° Serie", "Fecha Compra", "Ubicación", "✔"]
        x = [40, 120, 200, 280, 360, 440, 520]  # coordenadas ajustadas para A4
        y_inicio = height - 80

        for i in range(len(encabezados)):
            c.drawString(x[i], y_inicio, encabezados[i])

        # Línea debajo de encabezados
        c.line(30, y_inicio - 5, width - 30, y_inicio - 5)

        # Filas
        y = y_inicio - 20
        for item in registros:
            nombre = tree.item(item, "text")
            valores = self.tree.item(item, "values") if tree == self.tree else tree.item(item, "values")
            fila = [nombre] + list(valores)

            for i in range(len(fila)):
                c.drawString(x[i], y, str(fila[i]))

            # Casilla de verificación
            c.rect(x[6], y - 2, 12, 12)

            # Línea horizontal de la fila
            c.line(30, y - 5, width - 30, y - 5)

            y = y - 20

        # Bordes verticales
        for pos in x:
            c.line(pos - 5, y_inicio + 5, pos - 5, y + 15)

        c.save()

        try:
            if sys.platform.startswith("win"):
                os.startfile(archivo, "print")
            else:
                subprocess.run(["lp", archivo])
            messagebox.showinfo("Imprimir", "✅ Registros enviados a la impresora.")
        except Exception as e:
            messagebox.showerror("Error", "❌ Error al imprimir: {} ❌".format(e))


    def imprimir_seleccion(self):
        seleccion = self.tree.selection()
        if not seleccion:
            self.message['text'] = '❌ PARA IMPRIMIR, SELECCIONE UNA O MÁS HERRAMIENTAS. ❌'
            self.message['fg'] = 'red'
            self.message['font'] = self.bold_font
            return

        temp_tree = ttk.Treeview()
        for item in seleccion:
            nombre = self.tree.item(item, "text")
            valores = self.tree.item(item, "values")
            temp_tree.insert("", "end", text=nombre, values=valores)

        self.imprimir_registros(temp_tree, "HERRAMIENTAS SELECCIONADAS")









if __name__ == '__main__':
    window = Tk()
    application = Herramientas(window)
    window.mainloop()





