from datetime import datetime

dias_de_la_semana = ["Lunes", "Martes", "Miercoles","Jueves", "Viernes", "Sábado", "Domingo"]

hoy = datetime.now()
dia = hoy.weekday()
print(dias_de_la_semana[dia])