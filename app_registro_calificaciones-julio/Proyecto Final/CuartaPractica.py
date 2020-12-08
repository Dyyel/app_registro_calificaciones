# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 13:09:36 2020

@author: Daniel Hernández 2019-0683


"""

import sqlite3
from tkinter import *
from tkinter.ttk import Treeview
import webbrowser
from datetime import date

cConnect = sqlite3.connect("ESTUDIO")
CursorSql = cConnect.cursor()

sentencia = "CREATE TABLE IF NOT EXISTS ESTUDIANTE (ID_ESTUDIANTE INTEGER PRIMARY KEY AUTOINCREMENT, MATRICULA INT NOT NULL, NOMBRE VARCHAR(15), SEXO NCHAR(1))"
CursorSql.execute(sentencia)

sentencia = "CREATE TABLE IF NOT EXISTS MATERIA (CODIGO VARCHAR(6), NOMBRE_MATERIA VARCHAR(15))"
CursorSql.execute(sentencia)

sentencia = '''CREATE TABLE IF NOT EXISTS CALIFICACIONES (ID_CALIFICACION INTEGER PRIMARY KEY AUTOINCREMENT, ID_ESTUDIANTE INTEGER, 
ID_MATERIA VARCHAR(6), PRACTICA1 INT, PRACTICA2 INT, FORO1 INT, FORO2 INT, PRIMER_PARCIAL INT, SEGUNDO_PARCIAL INT, EXAMEN_FINAL INT,
FOREIGN KEY(ID_ESTUDIANTE) REFERENCES ESTUDIANTE(ID_ESTUDIANTE),
FOREIGN KEY(ID_MATERIA) REFERENCES MATERIA(CODIGO))'''
CursorSql.execute(sentencia)

def limit(n):
  texto=''
  for i in range(0,n):
    texto=texto=texto+'?,' if(i<(n-1)) else texto+'?'
  return texto
#end method

def insertar(varios, buscartabla, n):
  if exist(varios[0][0], buscartabla):
    update(varios, buscartabla)
  else:
    try:
      query=f"INSERT INTO {buscartabla} VALUES ({limit(n)})"
      CursorSql.executemany(query, varios)
      cConnect.commit()
      print('insertado')
    except:
      print('Error')
  #end condition
#end method    
def update(varios, tabla):
  sql = ''
  if tabla =="ESTUDIANTE":
    sql=f'''UPDATE {tabla}
              SET MATRICULA = {varios[0][0]} ,
                  NOMBRE = '{varios[0][2]}' 
              WHERE ID_ESTUDIANTE = {varios[0][0]}'''
  elif tabla=="MATERIA":
    sql=f'''UPDATE {tabla}
              SET  NOMBRE_MATERIA = '{varios[0][1]}'
              WHERE CODIGO = "{varios[0][0]}"'''
  elif tabla=="CALIFICACIONES":
    sql=f'''UPDATE {tabla}
              SET CODIGO = {varios[0][0]} ,
                  NOMBRE_MATERIA = {varios[0][1]} 
              WHERE CODIGO = {varios[0][0]}'''
  # try:
  print(sql)
  CursorSql.execute(sql)
  cConnect.commit()
  # print("editado")
  # except:
  # print("error")
#end method
def consultar(buscartabla):
  name= buscartabla
  # fetch(buscartabla)
  filewin = Toplevel(root)
  frame_router = Frame(filewin)
  frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
  buscarColumnas="""PRAGMA table_info({});""".format(buscartabla)
  infoTabla=CursorSql.execute(buscarColumnas)

  buscartabla=[]
  for campo in infoTabla:
    buscartabla.append(campo[1])
  #end for
  query= f"select * from '{name}'"
  dataTable = CursorSql.execute(query).fetchall()
  # print(dataTable[0][0])
  columns = buscartabla
  router_tree_view = Treeview(frame_router, columns=columns, show="headings")
  router_tree_view.column(buscartabla[0], width=100)
  for col in columns[0:]:
    router_tree_view.column(col, width=120)
    router_tree_view.heading(col, text=col)
  #end for
  if type(dataTable) is list:
    for data in dataTable:
      i=0
      router_tree_view.insert('', i, values = dinamyFill(name, data))
      i=i+1
  #end for
  router_tree_view.pack(side="left", fill="y")
  scrollbar = Scrollbar(frame_router, orient='vertical')
  scrollbar.configure(command=router_tree_view.yview)
  scrollbar.pack(side="right", fill="y")
  router_tree_view.config(yscrollcommand=scrollbar.set)
  filewin.geometry("400x300")
  filewin.mainloop()
#end method   

def editarMateria():
  codigo = StringVar()
  nombre = StringVar()
  filewin = Toplevel(root)
  Label(filewin,text = "Codigo").place(x=10, y=30)
  Label(filewin,text = "Nombre").place(x=10, y=60)
  
  TxtBoxCodigo=Entry(filewin, width=20, textvariable=codigo).place(x=100,y=30)
  TxtBoxNombre=Entry(filewin, width=20, textvariable=nombre).place(x=100,y=60)
  
  botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:insertarM(codigo.get(),nombre.get())).place(x=10, y=120)
  botonModificar=Button(filewin, text = "Modificar", width= 14).place(x=120, y=120)
  botonBorrar=Button(filewin, text = "Borrar", width= 14,command=lambda:delete(codigo.get(),'MATERIA','CODIGO')).place(x=60, y=160)

  filewin.geometry("250x200")
  filewin.mainloop()
#end method
def editarEstudiante():
  mat = StringVar()
  nom = StringVar()
  sex = StringVar()
  filewin = Toplevel(root)
  Label(filewin,text = "Matricula").place(x=10, y=30)
  Label(filewin,text = "Nombre").place(x=10, y=60)
  Label(filewin,text = "Sexo").place(x=10, y=90)
  
  TxtBoxMatricula=Entry(filewin, width=20, textvariable=mat).place(x=100,y=30)
  TxtBoxNombre=Entry(filewin, width=20, textvariable=nom).place(x=100,y=60)
  TxtBoxSexo=Entry(filewin, width=20, textvariable=sex).place(x=100,y=90)
  
  botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:insertarE(mat.get(),nom.get(),sex.get())).place(x=10, y=120)
  botonModificar=Button(filewin, text = "Modificar", width= 14,).place(x=120, y=120)
  botonBorrar=Button(filewin, text = "Borrar", width= 14, command= lambda:delete(mat.get(),'ESTUDIANTE','ID_ESTUDIANTE')).place(x=60, y=160)

  filewin.geometry("250x200")
  filewin.mainloop()
#end method   

def editarCalificacion():
      idEstudiante = StringVar()
      idMateria = StringVar()
      practica1 = StringVar()
      practica2 = StringVar()
      foro1 = StringVar()
      foro2 = StringVar()
      primerParcial = StringVar()
      segundoParcial = StringVar()
      examenFinal = StringVar()
      filewin = Toplevel(root)
      Label(filewin,text = "Estudiante").place(x=10, y=10)
      Label(filewin,text = "Materia").place(x=260, y=10)
      Label(filewin,text = "Practica1").place(x=10, y=30)
      Label(filewin,text = "Practica2").place(x=10, y=50)
      Label(filewin,text = "Foro1").place(x=260, y=30)
      Label(filewin,text = "Foro2").place(x=260, y=50)
      Label(filewin,text = "Primer Parcial").place(x=10, y=70)
      Label(filewin,text = "Segundo Parcial").place(x=10, y=90)
      Label(filewin,text = "Examen Final").place(x=260, y=70)
      
      
      TxtBoxEstudiante=Entry(filewin, width=20, textvariable=idEstudiante).place(x=100,y=10)
      TxtBoxMateria1=Entry(filewin, width=20, textvariable=idMateria).place(x=350,y=10)
      TxtBoxPractica1=Entry(filewin, width=20, textvariable=practica1).place(x=100,y=30)
      TxtBoxPractica2=Entry(filewin, width=20, textvariable=practica2).place(x=100,y=50)
      TxtBoxForo1=Entry(filewin, width=20, textvariable=foro1).place(x=350,y=30)
      TxtBoxForo2=Entry(filewin, width=20, textvariable=foro2).place(x=350,y=50)
      TxtBoxPrimerParcial=Entry(filewin, width=20, textvariable=primerParcial).place(x=100,y=70)
      TxtBoxSegundoParcial=Entry(filewin, width=20, textvariable=segundoParcial).place(x=100,y=90)
      TxtBoxExamenfinal=Entry(filewin, width=20, textvariable=examenFinal).place(x=350,y=70)
      
      botonInsertar=Button(filewin, text = "Insertar", width= 14, command= lambda:insertarC(idEstudiante.get(),idMateria.get(),practica1.get(), practica2.get(), foro1.get(), foro2.get(), primerParcial.get(), segundoParcial.get(), examenFinal.get())).place(x=100, y=120)
      botonModificar=Button(filewin, text = "Modificar", width= 14,).place(x=260, y=120)
      botonBorrar=Button(filewin, text = "Borrar", width= 14,command= lambda:deleteC(idEstudiante.get())).place(x=180, y=160)


      filewin.geometry("480x200")
      filewin.mainloop()
      
#end method

def insertarC(idEstudiante, idMateria, practica1, practica2, foro1, foro2, primerParcial, segundoParcial, examenFinal):
  if(validarCalificacion(idEstudiante, idMateria, practica1, practica2, foro1, foro2, primerParcial, segundoParcial, examenFinal)):
    insertar([(idEstudiante,idEstudiante, idMateria, practica1, practica2, foro1, foro2, primerParcial, segundoParcial, examenFinal)],'CALIFICACIONES',10)
  else:
    print('No valido')
#end method

def deleteC(ma):
    if ma!="":
        delete(ma,'CALIFICACIONES','ID_CALIFICACION ')
    else:
        print('No valido')
#end method

def validarCalificacion(idEstudiante, idMateria, practica1, practica2, foro1, foro2, primerParcial, segundoParcial, examenFinal):
  valido=True
  if idEstudiante=='':
    valido=False
  if idMateria=='':
    valido=False
  if practica1==''or int(practica1) < 0 or int(practica1) > 100:
    valido=False
  if practica2=='' or int(practica2) < 0 or int(practica2) > 100:
    valido=False
  if foro1=='' or int(foro1) < 0 or int(foro1) > 100:
    valido=False
  if foro2=='' or int(foro2) < 0 or int(foro2) > 100:
    valido=False
  if primerParcial=='' or int(primerParcial) < 0 or int(primerParcial) > 100:
    valido=False
  if segundoParcial=='' or int(segundoParcial) < 0 or int(segundoParcial) > 100:
    valido=False
  if examenFinal=='' or int(examenFinal) < 0 or int(examenFinal) > 100:
    valido=False
  return valido
#end method
def validarEstudiante(mat, nom, sex):
  valido=True
  if mat=='' or len(mat)!=8:
    valido=False
  if nom=='':
    valido=False
  if sex=='':
    valido=False
  return valido
#end method
def insertarE(mat, nom, sex):
  if(validarEstudiante(mat,nom,sex)):
    insertar([(mat,mat,nom,sex)],'ESTUDIANTE',4)
  else:
    print('No valido')
#end method
def insertarM(codigo, nombre):
  if nombre!="" and codigo!="":
    insertar([(codigo, nombre)], 'MATERIA',2)
  else:
    print('No valido')
#end method
def fetch(query):
  CursorSql.execute("SELECT * FROM ({})".format(query)) 
  rows = CursorSql.fetchall()
  return rows
#end method
def dinamyFill(tabla, data):
  if tabla =="ESTUDIANTE":
    return (data[0], data[1], data[2], data[3])
  elif tabla=="MATERIA":
    return (data[0], data[1])
  elif tabla=="CALIFICACIONES":
    return (data[0], data[1], data[2], data[3],data[4],data[5],data[6],data[7],data[8],data[9])
#end method
def delete(_id, tabla, field):
  if id!="":
    # try:
    query=f"DELETE FROM {tabla} WHERE {field}={_id}" if(tabla!='MATERIA') else f"DELETE FROM {tabla} WHERE {field}='{_id}'"
    print(query)
    CursorSql.execute(query)
    cConnect.commit()
    print('eliminado')
    # except:
    #   print('Error')
  else:
    print('No valido')
#end method
# def delete(_id, buscartabla, field):
#   try:
#     query=f"DELETE FROM {buscartabla} WHERE {field} = {_id}" if(buscartabla=='MATERIA') else f"DELETE FROM {buscartabla} WHERE {field} = '{_id}'"
#     print(query)
#     CursorSql.execute(query)
#     cConnect.commit()
#     print('eliminado')
#   except:
#     print('Error')
#end method
def exist(value, tabla):
  if tabla =="ESTUDIANTE":
    query= f"select * from '{tabla}' where ID_ESTUDIANTE={value}"
    dataTable = CursorSql.execute(query).fetchone()
    return True if(type(dataTable) is tuple) else False
  elif tabla=="MATERIA":
    query= f"select * from '{tabla}' where CODIGO='{value}'"
    dataTable = CursorSql.execute(query).fetchone()
    return True if(type(dataTable) is tuple) else False
  elif tabla=="CALIFICACIONES":
    query= f"select * from '{tabla}' where ID_CALIFICACION={value}"
    dataTable = CursorSql.execute(query).fetchone()
    return True if(type(dataTable) is tuple) else False
#end method
def generateHtmlReport(nombre, matricula, materias):
    
    def getHtmlLiteral(literal, color):
        return f'''<td rowspan = 5 style="text-align:center; font-size:200px; color:{color};">{literal}</td>'''
    
    def generarHtmlLiteral(literal):
        htmlLiteral = getHtmlLiteral("A","#0070c0")
        if(literal == "B"):
            htmlLiteral = getHtmlLiteral("B","#00b050")
        if(literal == "C"):
            htmlLiteral = getHtmlLiteral("C","#ffc000")
        if(literal == "D"):
            htmlLiteral = getHtmlLiteral("D","#fa62ef")
        if(literal == "F"):
            htmlLiteral = getHtmlLiteral("F","#ff0000")
        return htmlLiteral;
    
    def generateDate():
        today = date.today()
        return today.strftime("%m/%d/%Y")
    
    def calcular_promedio(nota1, nota2, nota3 = 0, nota4 = 0, notfinal = True):
        return (float((nota1+nota2)/2) if notfinal else float((nota1+nota2+nota3+nota4)/4))
    
    def getLiteral(promedio):
        literal = "A"
        if(promedio<60):
            literal = "F"
        elif(promedio<70):
            literal = "D"
        elif(promedio<80):
            literal = "C"
        elif(promedio<90):
            literal = "B"
        return literal
        
        
    def generateCalificationsRow(materia, calificaciones, matricula = "", nombre = ""):
        promedioPractica = calcular_promedio(calificaciones[0],calificaciones[1])
        promedioForo = calcular_promedio(calificaciones[2],calificaciones[3])
        promedioParcial = calcular_promedio(calificaciones[4],calificaciones[5])
        promedioFinal = calcular_promedio(calificaciones[6],promedioParcial,promedioForo,promedioPractica,False)
        htmlLiteral = generarHtmlLiteral(getLiteral(promedioFinal))
        return f'''<tr>
        <td style="text-align:center; font-size:25px;"><b>{matricula}</b></td>
        <td style="text-align:center; font-size:25px;"><b>{nombre}</b></td>
        <td style="text-align:center; font-size:25px;"><b>{materia}</b></td>
        <td style="text-align:center; font-size:20px;">Practica1 {calificaciones[0]}</td>
        <td style="text-align:center; font-size:20px;">Practica2 {calificaciones[1]}</td>
        {htmlLiteral}
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Foro1 {calificaciones[2]}</td>
        <td style="text-align:center; font-size:20px;">Foro2 {calificaciones[3]}</td>
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">P. Parcial {calificaciones[4]}</td>
        <td style="text-align:center; font-size:20px;">S. Parcial {calificaciones[5]}</td>
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Promedio {calificaciones[6]}</td>
        <td style="text-align:center; font-size:20px;"></td> 
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Promedio {promedioFinal}</td>
        <td style="text-align:center; font-size:20px;"></td> 
      </tr>'''
    
    actualDate = generateDate()
    calificacion = ""
    for materia in materias:
        calificacion = calificacion + generateCalificationsRow(materia['materia'],materia['calificaciones'],matricula,nombre)
        matricula = ""
        nombre = ""
        
    
    mensaje = f'''
    <html>
    <head></head>
    <body>
    
    <center>
    <h2>Sistema de Estudiantes</h2>
    </center>
    <div style="overflow: hidden;">
    <p style="float: left;
    width:33.33333%;
    text-align:left;"></p>
    <p style="float: left;
    width:33.33333%;
    text-align:center; font-size:25px;">Listado de Calificaciones de un Estudiante</p>
    <p style="float: left;
    width:33.33333%;
    text-align:right; font-size:25px;">Fecha: {actualDate}</p>
    </div>
    
    <table style="width:100%">
      <tr>
        <th><div style="color: #0070c0; font-size:30px; font-family: Calibri">Matrícula</div></th>
        <th><div style="color: #0070c0; font-size:30px; font-family: Calibri">Nombre</h3></th>
        <th><div style="color: #0070c0; font-size:30px; font-family: Calibri">Materia</div></th>
        <th colspan="2"><div style="color:#0070c0 ; font-size:30px; font-family: Calibri">Calificaciones</div></th>
        <th><div style="color:#0070c0; font-size:30px;font-family: Calibri">Literal</div></th>
      </tr>
      {calificacion}
      
    </table>
    </body>
    </html>
    
    '''
    file = open("Calificaciones.html","w")
    
    file.write(mensaje)
    
    file.close()
    
    webbrowser.open_new_tab('Calificaciones.html')
def getReportData(matricula):
    nombre  = ""
    calificaciones = []
    try:
        dataTable = CursorSql.execute(f"select nombre from ESTUDIANTE where MATRICULA ={matricula}").fetchall()
        if(len(dataTable) != 0):
            nombre = dataTable[0][0]
            dataTable = CursorSql.execute(f"select PRACTICA1,PRACTICA2,FORO1,FORO2,PRIMER_PARCIAL,SEGUNDO_PARCIAL,EXAMEN_FINAL,MATERIA.NOMBRE_MATERIA from CALIFICACIONES JOIN MATERIA ON MATERIA.CODIGO = CALIFICACIONES.ID_MATERIA where ID_ESTUDIANTE ={matricula}").fetchall()
            if(len(dataTable) != 0):
                for data in dataTable:
                    data = list(data)
                    materia = data.pop()
                    print(data)
                    calificaciones.append({"materia":materia,"calificaciones":data})
                generateHtmlReport(nombre,matricula,calificaciones)
        cConnect.commit()
    except:
        print("Error al generar Reporte")
    
root = Tk()


'''Menu Bar'''
menubar = Menu(root)
Label(root,text = "Crear Reporte", justify='center').pack()
Label(root,text = "Estudiante", justify='center').pack()
entry1 = Entry(root, justify='center')
entry1.pack()
newButton = Button(root,text=str('Crear Reporte'),justify='center', command = lambda: getReportData(entry1.get()))
newButton.pack()

Estudiantesmenu = Menu(menubar, tearoff=0)
Estudiantesmenu.add_command(label="Consultar", command=lambda:consultar("ESTUDIANTE"))
Estudiantesmenu.add_command(label="Modificar", command=lambda:editarEstudiante())
menubar.add_cascade(label="Estudiantes", menu=Estudiantesmenu)



Materiasmenu = Menu(menubar, tearoff=0)
Materiasmenu.add_command(label="Consultar", command=lambda:consultar("MATERIA"))
Materiasmenu.add_command(label="Modificar", command=lambda:editarMateria())
menubar.add_cascade(label="Materias", menu=Materiasmenu)

Calificacionesmenu = Menu(menubar, tearoff=0)
Calificacionesmenu.add_command(label="Consultar", command=lambda:consultar("CALIFICACIONES"))
Calificacionesmenu.add_command(label="Modificar", command=lambda:editarCalificacion())
menubar.add_cascade(label="Calificaciones", menu=Calificacionesmenu)

root.config(menu=menubar)
root.geometry("400x300")
root.title("Sistema de Estudiantes")
root.mainloop()





# webbrowser.open_new_tab('Calificaciones.html')
