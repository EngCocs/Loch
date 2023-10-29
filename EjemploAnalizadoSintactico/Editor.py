import os
from pickle import TRUE
import string
from tkinter import INSERT, Tk, TkVersion, ttk, Frame, PhotoImage
from tkinter import Button, Entry, Label, Menu, Scrollbar, Text
from tkinter import messagebox, filedialog, Toplevel, colorchooser
from tkinter import font, BooleanVar
import tkinter
import tkinter as tk
from subprocess import check_output
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import List, Any
from AnalizadorLexico import *
from AnalizadorSintactico import *
import subprocess




class Ventana(Frame):
    def __init__(self, master):
        super().__init__( master)
        self.master.title('PROYECTO1')
        self.master.geometry('1300x600+380+20')
        self.señal_ajustes = BooleanVar()
        self.info_estado =  BooleanVar()
        self.info_estado.set(False)
        self.señal_ajustes.set(True)
        self.clik_aceptar = False
        self.x = 0
        self.y = 0
        self.n = 12
        self.f = 'Arial'
        self.widgets()
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        # Botón para analizar el código
        self.boton_analizar = Button(self.master, text='Analizar Código', command=self.analizar_codigo)
        self.boton_analizar.grid(column=2, row=1, sticky='nsew')



    
    
    def widgets(self):
        #configuramos el menú superior
        menu = Menu(self.master)
        self.master.config(menu = menu)
        # Configuramos la consola
        self.consola = Text(self.master, state='disabled', width=60, bg='white', fg='green', font=('Courier', 10))
        self.consola.grid(column=2, row=0, sticky='nsew')

    
    
        #pestaña de archivo
        archivo = Menu(menu, tearoff=0)	
        archivo.add_command(label="Nuevo", command = self.nueva_ventana)
        archivo.add_command(label="Abrir", command = self.abrir_archivo)
        archivo.add_command(label="Guardar", command = self.guardar_archivo)
        archivo.add_command(label="Guardar Como", command = self.guardar_archivoComo)
        archivo.add_separator()			
        archivo.add_command(label="Salir", command = self.master.quit)



        #pestaña de ver
        ver = Menu(menu, tearoff=0)
        ver.add_checkbutton(label="Barra de estado", variable = self.info_estado, command = self.barra_de_estado)

        #pestaña de ayuda
        ayuda = Menu(menu, tearoff=0)
        ayuda.add_command(label="Acerca de", command= self.acerca_de)

        #pestaña de analizar
        analizar = Menu(menu, tearoff=0)
       # analizar.add_command(label="analizar el archivo", command = self.analizar) #Agregar esta funcion, command = self.analizar)
       

        #pestaña de reportes
        Reportes = Menu(menu, tearoff=0)
        Reportes.add_command(label="Reporte de Tokens") #Agregar esta funcion, command = self.verreportes
        Reportes.add_command(label="Reporte de Errores")
        Reportes.add_command(label="Árbol de derivación")

     
        #añadimos las pestañas al menú superior 
        menu.add_cascade(label="Archivo", menu=archivo)
        menu.add_cascade(label="Analisis",menu=analizar)
        
        menu.add_cascade(label="reportes", menu=Reportes)
        menu.add_cascade(label="Ver", menu=ver)
        menu.add_cascade(label="Ayuda", menu=ayuda)
        
        #configuramos la entrada de texto
        self.texto = Text(self.master, font= ('Arial', 12), 
            undo= True, background='#34495E', foreground='Aqua', insertbackground = "white") #colores letras, fondo, cursor
        self.texto.grid(column=0, row=0, sticky='nsew')
        self.texto.config(wrap='none')
        ladox = Scrollbar(self.master, orient = 'horizontal', command= self.texto.xview)
        ladox.grid(column=0, row = 1, sticky='ew')
        ladoy = Scrollbar(self.master, orient ='vertical', command = self.texto.yview)
        ladoy.grid(column = 1, row = 0, sticky='ns')
        self.texto.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
        self.barra_estado = Label(self.master, font = ('Segoe UI Symbol', 10))


    #funcion para ver el numero de letras
    def barra_de_estado(self):
        if self.info_estado.get() == True:
            n = len(self.texto.get('1.0','end'))

            self.barra_estado.grid(column=0, row = 2, sticky='ew')
            #self.barra_estado.config(text = f'Numero de letras: {n}' )	

        x = self.barra_estado.after(10, self.barra_de_estado)

        if self.info_estado.get() == False: 			
            self.barra_estado.after_cancel(x)
            self.barra_estado.grid_forget()
        (self.fila, self.col) = self.texto.index(INSERT).split('.')
        self.colum = int(self.col) + 1
        #print(f'Fila: {self.fila} Columna: {str(self.colum)}')
        self.barra_estado.config(text = f'Fila: {self.fila} Columna: {str(self.colum)}' )


    #funcion para abrir un archivo ya listo
    def abrir_archivo(self):
        '''direccion = filedialog.askopenfilename(initialdir ='/', 
            #title='Archivo', filetype=(('txt files', '*.txt*'),('All files', '*.*')))
            title='Archivo', filetype=(('json files', '*.json*'),('All files', '*.*')))

        if direccion != '':		
            archivo = open(direccion, 'r')
            contenido = archivo.read()
            self.texto.delete('1.0', 'end')
            self.texto.insert('1.0', contenido)
            #self.master.title(direccion)
            self.ruta = direccion'''
        
        direccion = filedialog.askopenfilename(filetypes=[("Archivos txt", "*.txt")])
        if direccion:
            with open(direccion, 'r') as file:
                content = file.read()
                self.texto.delete(1.0, tk.END)
                self.texto.insert(tk.END, content)
        self.data = self.texto.get(1.0, tk.END)
        self.ruta = direccion

    #funcion para guardar un archivo como
    def guardar_archivoComo(self):
        try: 
            filename = filedialog.asksaveasfilename(defaultextension='.txt')
            archivo = open(filename, 'w')
            archivo.write(self.texto.get('1.0', 'end'))
            archivo.close()
            messagebox.showinfo('Guardar Archivo','Archivo guardado en: ' + str(filename) )
            self.ruta = filename
        except:
            messagebox.showerror('Guardar Archivo', 'ERROR: Archivo no guardado')
        
    #funcion para guardar una archivo  
    def guardar_archivo(self):
        try:
            archivo = open(self.ruta, 'w')
            archivo.write(self.texto.get('1.0', 'end'))
            archivo.close()
            messagebox.showinfo('Guardar Archivo','Archivo guardado')
        except:
            messagebox.showerror('Guardar Archivo', 'ERROR: Archivo no guardado')
     
    #funcion de documento nuevo (gurada y borra o no guarda y borra)
    def nueva_ventana(self):
        if self.texto.get !=" ":
            valor = messagebox.askyesno('Proyecto1', '¿Desea guardar el archivo?',parent= self.master)
            if valor == True:
                self.guardar_archivoComo()
                self.ruta = ''
                self.texto.delete('1.0', 'end')
            else:
                self.texto.delete('1.0', 'end')
                self.ruta = ''
        else:
            self.texto.delete('1.0', 'end')
            self.ruta = ''
        
    #funcion acerca de
    def acerca_de(self):
        vent_info = Toplevel(self.master)
        vent_info.config( bg='white')
        vent_info.title('Información')
        vent_info.resizable(0,0)
        #vent_info.iconbitmap('icono.ico')
        vent_info.geometry('290x100+200+200')
        Label(vent_info, bg='white', 
            text= 'Curso: Lab. Lenguajes Formales y de Programación \n Nombre: Engel Emilio Coc Raxjal \n Carné: 202200314').pack(expand=True)
        
    def analyze_code(self):
        # Obtén el código del área de texto
        code = self.text_widget.get(1.0, tk.END)
        imprimir_consola = ''
        codigo = self.texto.get('1.0', 'end')
        
        # Llama al analizador léxico
        tokens = instruccion(codigo)
        
        # Llama al analizador sintáctico
        instrucciones = instrucciones_sintactico(tokens)
        
        # Muestra los resultados en la consola
        self.imprimir_en_consola('Tokens:\n' + '\n'.join(str(token) for token in tokens))
        self.imprimir_en_consola('Instrucciones:\n' + '\n'.join(str(instruccion) for instruccion in instrucciones))
        try:
            # Ejecuta el análisis léxico
            instrucciones_lexico = instruccion(code)
            lista_instrucciones = []
            while True:
                instrucciones_lenguaje = instrucciones_sintactico(instrucciones_lexico)
                if instrucciones_lenguaje:
                    lista_instrucciones.append(instrucciones_lenguaje)
                else:
                    break

            #! Ejecutar instrucciones

            for elemento in lista_instrucciones:
                if isinstance(elemento, DeclaracionClaves):
                    continue
                elif isinstance(elemento, Imprimir):
                    imprimir_consola += elemento.ejecutarT()

            print(imprimir_consola)
            for error in lista_errores:
                print(error.operar(None))

                    # Muestra el resultado en la consola de salida
            self.output_console.config(state='normal')
            self.output_console.delete(1.0, tk.END)
            self.output_console.insert(tk.END, imprimir_consola)
            self.output_console.config(state='disabled')
            messagebox.showinfo("Análisis exitoso", "El código se analizó exitosamente.")

        except Exception as e:
            messagebox.showerror(f"Ocurrió un error al analizar el código: {str(e)}")
            print("Ocurrió un error al analizar el código: ", e)



    def run_analysis(self, code):
        # Aquí puedes realizar el análisis del código, por ejemplo, usando subprocess
        try:
            # Ejemplo: Ejecutar un comando de consola y capturar la salida
            result = subprocess.check_output(["python", "-c", code], universal_newlines=True, stderr=subprocess.STDOUT)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e.returncode}\n{e.output}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"

        
    
    def imprimir_en_consola(self, mensaje):
        self.consola.config(state='normal')
        self.consola.insert('end', mensaje + '\n')
        self.consola.config(state='disabled')
        self.consola.yview('end')
        self.consola.config(state='normal')
        self.consola.insert('end', mensaje + '\n')
        self.consola.config(state='disabled')
        self.consola.yview('end')


        


if __name__ == "__main__":
        ventana = Tk()
        app = Ventana(ventana)
        app.imprimir_en_consola('Pana necesito de su ayuda para sacar un 60 :(')  # Esta línea debería estar dentro de la clase Ventana
        app.mainloop()