from tkinter import Tk, Label, Button, messagebox
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import webbrowser
from datetime import datetime 
from Data import Data
from Alumno import Alumno
from Notas import Notas
from Calculo import Calculo
from Reporte import Reporte
from Services import Services
import base64
import io
import urllib
from PIL import ImageTk, Image 



class MyProgram:
    def __init__(self, master):
        self._database = Data()
        self._materias = self._database.consultar('MATERIA')
        self._estudiantes = self._database.consultar('ESTUDIANTE')
        self._carrera = self._database.consultar('CARRERA')
        self._provincia = self._database.consultar('PROVINCIA')
        self._imgfile='profileIcon.png'
        self._master = master
        master.title("Sistema de Estudiantes")
        self.menubar = Menu(master)
        self.router_tree_view = ttk.Treeview(self._master)
        #menu 1
        self.estudiantesmenu = Menu(self.menubar, tearoff=0)
        self.estudiantesmenu.add_command(label="Consultar", command=lambda:self.consultar("ESTUDIANTE"))
        self.estudiantesmenu.add_command(label="Modificar", command=lambda:self.estudianteControl())
        self.menubar.add_cascade(label="Estudiantes", menu=self.estudiantesmenu)
        #menu 2
        self.materiasmenu = Menu(self.menubar, tearoff=0)
        self.materiasmenu.add_command(label="Consultar", command=lambda:self.consultar("MATERIA"))
        self.materiasmenu.add_command(label="Modificar", command=lambda:self.materiaControl())
        self.menubar.add_cascade(label="Materias", menu=self.materiasmenu)
        #menu 3
        self.calificacionesmenu = Menu(self.menubar, tearoff=0)
        self.calificacionesmenu.add_command(label="Consultar", command=lambda:self.consultar("CALIFICACIONES"))
        self.calificacionesmenu.add_command(label="Modificar", command=lambda:self.calificacionControl())
        self.menubar.add_cascade(label="Calificaciones", menu=self.calificacionesmenu)
        #menu 4
        self.reportesmenu = Menu(self.menubar, tearoff=0)
        self.reportesmenu.add_command(label="Reporte html", command=lambda:self.reporteControl())
        self.reportesmenu.add_command(label="Reporte mapa", command=lambda:self.reporteControlM())
        self.reportesmenu.add_command(label="Reporte grafico", command=lambda:self.reporteControlG())
        self.menubar.add_cascade(label="Reportes", menu=self.reportesmenu)

        master.config(menu=self.menubar)
        master.geometry("400x300")
    #end _init

    def reporteControl(self):
        idEstudiante =StringVar()
        filewin = Toplevel(self._master) 

        Label(filewin,text = "Estudiante").place(x=10, y=30)
        CbBoxEstudiante = ttk.Combobox(filewin, state='readonly', textvariable=idEstudiante, values=self.get_dataCombo('ESTUDIANTE')).place(x=100,y=30)
        botonReportee=Button(filewin, text = "Reporte html", width= 14, command= lambda:self.reporteH(idEstudiante.get())).place(x=100, y=80)

        filewin.geometry("250x200")
        filewin.mainloop()
    #end method

    def reporteControlM(self):
        idMateria =StringVar()
        idProvincia =StringVar()
        idLitereal = StringVar()
        filewin = Toplevel(self._master)

        Label(filewin,text = "Materia").place(x=10, y=30)
        Label(filewin,text = "Provincia").place(x=10, y=60)
        Label(filewin, text="Literal").place(x=10,y=90)
        CbBoxEstudiante = ttk.Combobox(filewin, state='readonly', textvariable=idMateria, values=self.get_dataCombo('MATERIA')).place(x=100,y=30)
        CbBoxProvincia = ttk.Combobox(filewin, state='readonly', textvariable=idProvincia, values=self.get_dataCombo('PROVINCIA')).place(x=100,y=60)
        CbBoxLiteral = ttk.Combobox(filewin,state='readonly', textvariable=idLitereal, values=['A','B','C','D','F','TODOS']).place(x=100,y=90)
        botonReporte=Button(filewin, text = "Reporte mapa", width= 14, command= lambda:self.reportM([idMateria.get(),idProvincia.get(),idLitereal.get()])).place(x=100, y=130)

        filewin.geometry("250x200")
        filewin.mainloop()
    #end method

    def reporteControlG(self):
        filewin = Toplevel(self._master)
        
        idprovinciaBarra = StringVar()
        idprovinciaComp1 = StringVar()
        idprovinciaComp2 = StringVar()
        
        
        ttk.Combobox(filewin, state='readonly', textvariable=idprovinciaBarra, values=self.get_dataCombo('PROVINCIA')).place(x=170,y=71)
        ttk.Combobox(filewin, state='readonly', textvariable=idprovinciaComp1, values=self.get_dataCombo('PROVINCIA')).place(x=10,y=190)
        ttk.Combobox(filewin, state='readonly', textvariable=idprovinciaComp2, values=self.get_dataCombo('PROVINCIA')).place(x=230,y=190)
        
        
        Label(filewin,text = "Notas por literales").place(x=10, y=30)
        Label(filewin,text = "Literal por provincia").place(x=10, y=70)
        Label(filewin,text = "Estudiantes por carrera").place(x=10, y=110)
        Label(filewin,text = "Comparativo por provincia").place(x=10, y=150)
        photoLabel = Label(filewin)
        photoLabel.place(x=10, y=230)
        
        def setPhotoLabel(imagen):
            img = ImageTk.PhotoImage(Image.open(imagen))
            photoLabel.config(image=img)
            photoLabel.photo = img
        
        # Label(filewin, text="Literal").place(x=10,y=90)
        # CbBoxEstudiante = ttk.Combobox(filewin, state='readonly', textvariable=idMateria, values=self.get_dataCombo('MATERIA')).place(x=100,y=30)
        # CbBoxProvincia = ttk.Combobox(filewin, state='readonly', textvariable=idProvincia, values=self.get_dataCombo('PROVINCIA')).place(x=100,y=60)
        # CbBoxLiteral = ttk.Combobox(filewin,state='readonly', textvariable=idLitereal, values=['A','B','C','D','F','TODOS']).place(x=100,y=90)
        botonReporteL=Button(filewin, text = "Generar", width= 14, command= lambda:self.reportG1(setPhotoLabel)).place(x=170, y=30)
        botonReporteP=Button(filewin, text = "Generar", width= 10, command= lambda:self.reportG2(idprovinciaBarra.get(), setPhotoLabel)).place(x=330, y=67)
        botonReporteP3d=Button(filewin, text = "Generar en 3D", width= 10, command= lambda:self.reportG5(idprovinciaBarra.get(), setPhotoLabel)).place(x=420, y=67)
        botonReporteC=Button(filewin, text = "Generar", width= 14, command= lambda:self.reportG3(setPhotoLabel)).place(x=170, y=110)
        botonReporteComp =Button(filewin, text = "Generar", width= 10, command= lambda:self.reportG4(idprovinciaComp1.get(),idprovinciaComp2.get(),setPhotoLabel)).place(x=440, y=186)
        
        
        
        

        filewin.geometry("600x550")
        filewin.mainloop()
    #end method

    def materiaControl(self, id=0):
        codigo = StringVar()
        nombre = StringVar()
        filewin = Toplevel(self._master) 
        Label(filewin,text = "Codigo").place(x=10, y=30)
        Label(filewin,text = "Nombre").place(x=10, y=60)
        
        TxtBoxCodigo=Entry(filewin, width=20, textvariable=codigo).place(x=100,y=30)
        TxtBoxNombre=Entry(filewin, width=20, textvariable=nombre).place(x=100,y=60)
        
        botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:self.insert_materia([codigo.get(), nombre.get()])).place(x=10, y=120)
        # botonModificar=Button(filewin, text = "Modificar", width= 14).place(x=120, y=120)
        # botonBorrar=Button(filewin, text = "Borrar", width= 14,command=lambda:self.greet()).place(x=60, y=160)
        if id!=0:
            data = self._database.consultarById("MATERIA","CODIGO",id)
            print(data[0])
            codigo.set(data[0])
            nombre.set(data[1])
        #end condition 
        filewin.geometry("250x200")
        filewin.mainloop()
    #end method

    def estudianteControl(self, id=0):
        mat = StringVar()
        cedula = StringVar()
        nom = StringVar()
        apellido = StringVar()
        self._imgfile="profileIcon.png"
        sex = StringVar()
        idcarrera = StringVar()
        idprovincia = StringVar()
        filewin = Toplevel(self._master)
        Label(filewin,text = "Cecula").place(x=10, y=30)
        Label(filewin,text = "Nombre").place(x=10, y=60)
        Label(filewin,text = "Apellido").place(x=10, y=90)
        Label(filewin,text = "Sexo").place(x=10, y=120)
        Label(filewin,text = "Matricula").place(x=10, y=150)
        Label(filewin,text = "Carrera").place(x=10, y=180)
        Label(filewin,text = "Provincia").place(x=10, y=210)
        
        canvas = Canvas(filewin, width = 300, height = 300).place(x=310, y=60)    
        img = ImageTk.PhotoImage(Image.open(self._imgfile))
        photoLabel = Label(filewin, image = img)
        photoLabel.place(x=320, y=60)
        TxtBoxCedula=Entry(filewin, width=20, textvariable=cedula).place(x=100,y=30)
        TxtBoxNombre=Entry(filewin, width=20, textvariable=nom).place(x=100,y=60)
        TxtBoxApellido=Entry(filewin, width=20, textvariable=apellido).place(x=100,y=90)
        TxtBoxSexo=Entry(filewin, width=20, textvariable=sex).place(x=100,y=120)
        TxtBoxMatricula=Entry(filewin, width=20, textvariable=mat).place(x=100,y=150)
        CbBoxCarrera = ttk.Combobox(filewin, state='readonly', textvariable=idcarrera, values=self.get_dataCombo('CARRERA')).place(x=100,y=180)
        CbBoxProvincia = ttk.Combobox(filewin, state='readonly', textvariable=idprovincia, values=self.get_dataCombo('PROVINCIA')).place(x=100,y=210)
        
        botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:self.insert_estudiante([mat.get(),nom.get(),apellido.get(),cedula.get(),self._imgfile,sex.get(),idprovincia.get(),idcarrera.get()])).place(x=10, y=240)
        botonConsultar=Button(filewin, text = "Consultar", width= 10, command= lambda:self.estudianteDesdeApi(cedula.get(), [nom,apellido, sex], photoLabel)).place(x=300, y=30)
        #botonModificar=Button(filewin, text = "Modificar", width= 14,).place(x=120, y=120)
        #botonBorrar=Button(filewin, text = "Borrar", width= 14, command= lambda:self.greet()).place(x=60, y=160)
        if id!=0:
            data = self._database.consultarById("ESTUDIANTE","ID_ESTUDIANTE",id)
            print(data[0])
            mat.set(data[1])
            nom.set(data[2])
            apellido.set(data[3])
            cedula.set(data[4])
            self._imgfile=data[5]
            raw_data = urllib.request.urlopen(self._imgfile).read()
            img = Image.open(io.BytesIO(raw_data))
            photo =  ImageTk.PhotoImage(img)
            photoLabel.config(image=photo)
            photoLabel.photo = photo
            sex.set(data[6])
            idprovincia.set(data[7])
            idcarrera.set(data[8])
        #end condition 
        filewin.geometry("450x280")
        filewin.mainloop()
    #end method

    def calificacionControl(self, id=0):
        idEstudiante = StringVar()
        idMateria = StringVar()
        practica1 = StringVar()
        practica2 = StringVar()
        foro1 = StringVar()
        foro2 = StringVar()
        primerParcial = StringVar()
        segundoParcial = StringVar()
        examenFinal = StringVar()
        filewin = Toplevel(self._master)
        Label(filewin,text = "Estudiante").place(x=10, y=10)
        Label(filewin,text = "Materia").place(x=260, y=10)
        Label(filewin,text = "Practica1").place(x=10, y=30)
        Label(filewin,text = "Practica2").place(x=10, y=50)
        Label(filewin,text = "Foro1").place(x=260, y=30)
        Label(filewin,text = "Foro2").place(x=260, y=50)
        Label(filewin,text = "Primer Parcial").place(x=10, y=70)
        Label(filewin,text = "Segundo Parcial").place(x=10, y=90)
        Label(filewin,text = "Examen Final").place(x=260, y=70)

        # TxtBoxEstudiante=Entry(filewin, width=20, textvariable=idEstudiante).place(x=100,y=10)
        CbBoxEstudiante = ttk.Combobox(filewin, state='readonly', textvariable=idEstudiante, values=self.get_dataCombo('ESTUDIANTE')).place(x=100,y=10)
        CbBoxMateria = ttk.Combobox(filewin, state='readonly', textvariable=idMateria, values=self.get_dataCombo('MATERIA')).place(x=350,y=10)
        # TxtBoxMateria1=Entry(filewin, width=20, textvariable=idMateria).place(x=350,y=10)
        TxtBoxPractica1=Entry(filewin, width=20, textvariable=practica1).place(x=100,y=30)
        TxtBoxPractica2=Entry(filewin, width=20, textvariable=practica2).place(x=100,y=50)
        TxtBoxForo1=Entry(filewin, width=20, textvariable=foro1).place(x=350,y=30)
        TxtBoxForo2=Entry(filewin, width=20, textvariable=foro2).place(x=350,y=50)
        TxtBoxPrimerParcial=Entry(filewin, width=20, textvariable=primerParcial).place(x=100,y=70)
        TxtBoxSegundoParcial=Entry(filewin, width=20, textvariable=segundoParcial).place(x=100,y=90)
        TxtBoxExamenfinal=Entry(filewin, width=20, textvariable=examenFinal).place(x=350,y=70)
        
        botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:self.insert_calificaciones(id if(id!=0) else 0,[idEstudiante.get(),idMateria.get()],[practica1.get(),practica2.get(),foro1.get(),foro2.get(),primerParcial.get(),segundoParcial.get(),examenFinal.get()])).place(x=100, y=120)
        # botonModificar=Button(filewin, text = "Modificar", width= 14,).place(x=260, y=120)
        # botonBorrar=Button(filewin, text = "Borrar", width= 14,command= lambda:self.greet()).place(x=180, y=160)
        if id!=0:
            data = self._database.consultarById("CALIFICACIONES","ID_CALIFICACION",id)
            print(data)
            idEstudiante.set(data[1])
            idMateria.set(data[2])
            practica1.set(data[3])
            practica2.set(data[4])
            foro1.set(data[5])
            foro2.set(data[6])
            primerParcial.set(data[7])
            segundoParcial.set(data[8])
            examenFinal.set(data[9])
        #end condition 
        filewin.geometry("500x200")
        filewin.mainloop()  
    #end method

    def consultar(self, tabla):
        print(tabla)
        filewin = Toplevel(self._master)
        frame_router = Frame(filewin)
        frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
        infoTabla = self._database.infotabla(tabla)
        buscartabla=[]
        for campo in infoTabla:
            buscartabla.append(campo[1])
        #end for
        dataTable = self._database.consultar(tabla) 
        # print(dataTable[0][0])
        columns = buscartabla
        self.router_tree_view = Treeview(frame_router, columns=columns, show="headings")
        self.router_tree_view.bind("<Double-1>", self.itemEvent)
        self.router_tree_view.column(buscartabla[0], width=100)
        for col in columns[0:]:
            self.router_tree_view.column(col, width=120)
            self.router_tree_view.heading(col, text=col)
        #end for
        print(dataTable)
        if type(dataTable) is list:
            i=0
            for data in dataTable:
                self.router_tree_view.insert(parent='',index='end', iid=self.dinamyFill(tabla, data)[0], values = self.dinamyFill(tabla, data))
                i=i+1
        #end for
        self.router_tree_view.pack(side="left", fill="y")
        scrollbar = Scrollbar(frame_router, orient='vertical')
        scrollbar.configure(command=self.router_tree_view.yview)
        scrollbar.pack(side="right", fill="y")
        self.router_tree_view.config(yscrollcommand=scrollbar.set)
        botonEliminar=Button(filewin, text = "Eliminar", width= 14, command= lambda:self.tableItemDelete(tabla,filewin)).place(x=20, y=250)
        botonEditar=Button(filewin, text = "Editar", width= 14, command=lambda:self.tableItemEdit(tabla, filewin)).place(x=150, y=250)
        filewin.geometry(self.set_dimension(tabla))
        filewin.mainloop()
    #end method

    def dinamyFill(self, tabla, data):
        if tabla =="ESTUDIANTE":
            return (data[0], data[1], data[2], data[3],data[4],data[5],data[6],data[7],data[8])
        elif tabla=="MATERIA":
            return (data[0], data[1])
        elif tabla=="CALIFICACIONES":
            return (data[0], data[1], data[2], data[3],data[4],data[5],data[6],data[7],data[8],data[9])
    #end method

    def set_dimension(self, tabla):
        dimension ="700x300"
        if tabla=="MATERIA":
            dimension="400x300"
        elif tabla=="CALIFICACIONES":
            dimension="800x300"
        return dimension
    #end method

    def itemEvent(self):
        item = self.router_tree_view.selection()#[0] # now you got the item on that tree
        print("you clicked on id", item[0])
    #end method

    def tableItemDelete(self, tabla, f):
        item = self.router_tree_view.selection()#[0] # now you got the item on that tree
        if len(item)>0:
            print("you clicked on id", item[0])
            if tabla == "ESTUDIANTE":
                data = self._database.delete(item[0], tabla, 'ID_ESTUDIANTE')
                messagebox.showinfo(title='Informacion', message=data)
                f.destroy()
            elif tabla == 'MATERIA':
                data = self._database.delete(item[0], tabla, 'CODIGO')
                messagebox.showinfo(title='Informacion', message=data)
                f.destroy()
            else:
                data = self._database.delete(item[0], tabla, 'ID_CALIFICACION')
                messagebox.showinfo(title='Informacion', message=data)
                f.destroy()
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione algo')
    #end method

    def tableItemEdit(self, tabla, f):
        item = self.router_tree_view.selection()#[0] # now you got the item on that tree
        if len(item)>0:
            print("you clicked on id", item[0])
            if tabla == "ESTUDIANTE":
                f.destroy()
                self.estudianteControl(item[0])
                #print(self._database.delete(item[0], tabla, 'ID_ESTUDIANTE'))
            elif tabla == 'MATERIA':
                f.destroy()
                self.materiaControl(item[0])
                # print(self._database.delete(item[0], tabla, 'CODIGO'))
            else:
                f.destroy()
                self.calificacionControl(item[0])
                # print(self._database.delete(item[0], tabla, 'ID_CALIFICACION'))
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione algo')
    #end method

    def insert_estudiante(self,values):
        dic = {'data':values,'notas':[0,0,0,0,0,0,0]}
        alumno = Alumno(dic)
        print('data antes', dic['data'])
        if alumno.is_valid():
            data = self._database.insert([(dic['data'][0],dic['data'][0],dic['data'][1],dic['data'][2],dic['data'][3],dic['data'][4],dic['data'][5],dic['data'][6],dic['data'][7])],'ESTUDIANTE',9)
            messagebox.showinfo(title='Informacion', message=data)
            self._estudiantes = self._database.consultar('ESTUDIANTE')
        else:
            messagebox.showinfo(title='Informacion', message='Datos no validos')
    #end method

    def insert_materia(self, values):
        if values[0]!="" and values[0]!="":
            data = self._database.insert([(values[0], values[1])], 'MATERIA',2)
            messagebox.showinfo(title='Informacion', message=data)
            self._materias = self._database.consultar('MATERIA')
        else:
            messagebox.showinfo(title='Informacion', message='Datos no validos')
    #end method

    def insert_calificaciones(self,editing, info, values):
        # dic = {'data':['','',''],'notas':values}
        ncalif = self._database.calificacionByEstudiante(info[0])
        print(len(ncalif))
        nota = Notas(values)
        print(info)
        print(values)
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        id = str(timestamp)
        if nota.is_valid() and info[0]!="" and info[1]!='' and len(ncalif)<4:
            data = self._database.insert([(editing if(editing!=0) else id[11:17],info[0],info[1],values[0],values[1],values[2],values[3],values[4],values[5],values[6])], "CALIFICACIONES",10)
            messagebox.showinfo(title='Informacion', message=data)
        else:  
            messagebox.showinfo(title='Informacion', message='Ya tiene 3 materias.' if(len(ncalif)==3) else 'Datos no validos')
    #end method
    
    def estudianteDesdeApi(self, cedula, inputsFields, photoLabel):        
        if(cedula != ""):
            respuestaServicio = Services(cedula).get_datos()
            #manejo de service fail
            print('aqui', respuestaServicio)
            if respuestaServicio['ok']!=False:
                if "Cedula" in respuestaServicio:
                    print(respuestaServicio)
                    inputsFields[0].set(respuestaServicio['Nombres'])
                    inputsFields[1].set(f"{respuestaServicio['Apellido1']} {respuestaServicio['Apellido2']}")
                    inputsFields[2].set(respuestaServicio['IdSexo'])
                    print(respuestaServicio["foto"])
                    self._imgfile = respuestaServicio["foto"]
                    raw_data = urllib.request.urlopen(self._imgfile).read()
                    img = Image.open(io.BytesIO(raw_data))
                    photo =  ImageTk.PhotoImage(img)
                    photoLabel.config(image=photo)
                    photoLabel.photo = photo
                    print(photo)
                    #image = ImageTk.PhotoImage(im)
                # else:
                #     messagebox.showinfo(title='Informacion', message='Cedula no encontrada') 
            else:
                messagebox.showinfo(title='Informacion', message='Ha ocurrido un error, intente otra cedula.') 
        else:
            messagebox.showinfo(title='Informacion', message='Cedula no valida.')
    #end method 

    def greet(self):
        messagebox.showinfo(title='Informacion', message='Greetings!')
    #end methhod

    def get_dataCombo(self, tabla):
        data=[]
        values = self._estudiantes
        if tabla=='MATERIA':
            values = self._materias
        elif tabla=='CARRERA':
            values = self._carrera
        elif tabla=='PROVINCIA':
            values= self._provincia
        i=0
        for v in values:
            data.append(v[1]if(tabla=='PROVINCIA' or tabla=='CARRERA')else v[0])
            i=i+1
        return data
    #end method

    def reporteH(self, m):
        print(m)
        report = Reporte(m)
        report.get_report()
    #end method

    def reportM(self, values):
        #0 materi 1 provincia 2 literal
        if values[0]!="" and values[1]!="" and values[2]!="":
            report = Reporte('20202020')
            report.get_reportM(values)
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione los campos.')
    #end method

    def reportG3(self,setPhotoLabel):
        values = self._database.estudianteByCarrera()
        # values=[(1, 'Ingeniería de software'), (2, 'Ingeniería industrial')]
        value=[]
        legend=[]
        for i in values:
            value.append(i[0])
            legend.append(i[1])
        report = Reporte('20202020')
        # values=['tipo',[0,2,4],['juan','pedro'],'title','colum','values']
        data=['pastel',value,legend,'Estudiantes por carreras']
        report.get_reportG(data)
        setPhotoLabel("pastel.png")
    #end method

    def reportG1(self, setPhotoLabel):
        n = self._database.consultar('CALIFICACIONES')
        letras ={'A':0,'B':0,'C':0,'D':0,'F':0}
        for i in n:
            nota = Notas([i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
            cal = Calculo(nota)
            for f in letras:
                if f==cal.get_literal():
                    letras[f]=letras[f]+1
        print(letras)
        report = Reporte('20202020')
        # values=['tipo',[0,2,4],['juan','pedro'],'title','colum','values']
        value=[i for i in letras]
        legend=[letras[i] for i in letras]
        data=['barra',value,legend,'Notas por literal','Literal','Cantidad']
        report.get_reportG(data)
        setPhotoLabel("barra.png")
        
    #end method
    
    def reportG5(self, idProvincia,setPhotoLabel):
        if(idProvincia):
            n = self._database.literalesByProvincia()
            graphData = self.filterLiteralsByProvince(idProvincia, n)
            report = Reporte('20202020')
            data=['barra3D',graphData[0],graphData[1],f'Notas en {idProvincia}','Literal','Cantidad']
            report.get_reportG(data)
            setPhotoLabel("barra3D.png")
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione una provincia')
        
        
     #end method

    def reportG2(self, idProvincia,setPhotoLabel):
        if(idProvincia):
            n = self._database.literalesByProvincia()
            graphData = self.filterLiteralsByProvince(idProvincia, n)
            report = Reporte('20202020')
            data=['barra',graphData[0],graphData[1],f'Notas en {idProvincia}','Literal','Cantidad']
            report.get_reportG(data)
            setPhotoLabel("barra.png")
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione una provincia')
        
        
     #end method
    def filterLiteralsByProvince(self, idProvincia, grade):
         letras = {'A':0,'B':0,'C':0,'D':0,'F':0}
         for i in grade:
             if(i[10] == idProvincia):
                 nota = Notas([i[3],i[4],i[5],i[6],i[7],i[8],i[9]])
                 cal = Calculo(nota)
                 for f in letras:
                     if f==cal.get_literal():
                         letras[f]=letras[f]+1
         value=[i for i in letras]
         legend=[letras[i] for i in letras]
         return [value,legend]
     
    def reportG4(self, idProvincia1,idProvincia2,setPhotoLabel):
        if(idProvincia1 and idProvincia2):
            values = self._database.literalesByProvincia()
            graphData1 = self.filterLiteralsByProvince(idProvincia1,values)
            graphData2 = self.filterLiteralsByProvince(idProvincia2,values)
            provincias = [idProvincia1,idProvincia2]
            report = Reporte('20202020')
            data=['Comparativo',graphData1,graphData2,'Grafico Comparativo', provincias]
            report.get_reportG(data)
            setPhotoLabel("Comparativo.png")
        else:
            messagebox.showinfo(title='Informacion', message='Seleccione las provincias')
        
        
     #end method

#end class

root = Tk()
my_gui = MyProgram(root)
root.mainloop()