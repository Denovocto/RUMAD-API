from rumad import Rum
import datetime as dt

snum = int(input('student number: '))
pin = int(input('pin: '))
bday = dt.datetime(1, 1, 1)  # year, month, day
ss = int(input('SS: '))


conection = Rum()
conection.connect()
conection.addStudentCred(snum, pin, bday, ss)
conection.findStudentCourses()
# conection.get_me_to('Ver Matricula')
# tm.sleep(13)
# first_page = conection.recieve('Finalizar')
# print(first_page)
conection.close()
