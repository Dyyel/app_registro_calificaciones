import webbrowser
from datetime import date
from Data import Data
from Calculo import Calculo
from Notas import Notas

class Reporte:
    def __init__(self, matricula):
        self._database = Data()
        self._estudiante = self._database.consultarById('ESTUDIANTE','ID_ESTUDIANTE',matricula)
        self._calificaiones = self._database.calificacionByEstudiante(matricula)
        self._date = date.today()
    #end method

    def get_Date(self):
        today = self._date.today()
        return today.strftime("%m/%d/%Y")
    #end methd

    def literalhtml(self, literal):
        htmlLiteral = self.html_literalColor("A","#0070c0")
        if(literal == "B"):
            htmlLiteral = self.html_literalColor("B","#00b050")
        if(literal == "C"):
            htmlLiteral = self.html_literalColor("C","#ffc000")
        if(literal == "D"):
            htmlLiteral = self.html_literalColor("D","#fa62ef")
        if(literal == "F"):
            htmlLiteral = self.html_literalColor("F","#ff0000")
        return htmlLiteral
    #end method

    def html_literalColor(self, literal, color):
        return f'''<td rowspan = 5 style="text-align:center; font-size:200px; color:{color};">{literal}</td>'''
    #end method

    def generateCalificationsRow(self, n):
        nota= Notas([n[3],n[4],n[5],n[6],n[7],n[8],n[9]])
        calc = Calculo(nota) 
        materia = self._database.consultarById('MATERIA', 'CODIGO', n[2])
        # promedioPractica = calcular_promedio(calificaciones[0],calificaciones[1])
        # promedioForo = calcular_promedio(calificaciones[2],calificaciones[3])
        # promedioParcial = calcular_promedio(calificaciones[4],calificaciones[5])
        # promedioFinal = calcular_promedio(calificaciones[6],promedioParcial,promedioForo,promedioPractica,False)
        htmlLiteral = self.literalhtml(calc.get_literal())
        return f'''<tr>
        <td style="text-align:center; font-size:25px;"><b>{self._estudiante[1]}</b></td>
        <td style="text-align:center; font-size:25px;"><b>{self._estudiante[2]}</b></td>
        <td style="text-align:center; font-size:25px;"><b>{materia[0]}</b></td>
        <td style="text-align:center; font-size:20px;">Practica1 {nota.get_ppractica()}</td>
        <td style="text-align:center; font-size:20px;">Practica2 {nota.get_spractica()}</td>
        {htmlLiteral}
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Foro1 {nota.get_pforo()}</td>
        <td style="text-align:center; font-size:20px;">Foro2 {nota.get_sforo()}</td>
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">P. Parcial {nota.get_pparcial()}</td>
        <td style="text-align:center; font-size:20px;">S. Parcial {nota.get_sparcial()}</td>
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Ex. Final {nota.get_final()}</td>
        <td style="text-align:center; font-size:20px;"></td> 
      </tr>
      <tr>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;"></td>
        <td style="text-align:center; font-size:20px;">Promedio {calc.get_pr_final()}</td>
        <td style="text-align:center; font-size:20px;"></td> 
      </tr>'''
    #end method

    def get_report(self):
        actualDate = self.get_Date()
        calificacion = ""
        for cal in self._calificaiones:
            calificacion = calificacion + self.generateCalificationsRow(cal)
        #end for
        
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
    #end method

#end class