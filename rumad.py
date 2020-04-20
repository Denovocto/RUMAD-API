import paramiko
import datetime as dt
import time as tm
import re


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', line)


class Course:
    def __init__(self, name=str(), section=str(), credits=int(), classroom=str(), time=dt.datetime(), professor=str()):
        self.CLASS = {
            "section": section,
            "credits": credits,
            "classroom": classroom,
            "time": time,
            "professor": professor,
        }


class Student:
    def __init__(self, studentNum=int(), pn=int(), bday=dt.datetime(1, 1, 1), soc=int()):
        self.student_number = studentNum
        self.pin = pn
        self.birthdate = bday
        self.ss = soc
        self.courses = dict()

    def addCourse(self, name, course=Course()):
        self.courses.update({name: course})


class Rum:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host = "rumad.uprm.edu"
        self.user = "estudiante"
        self.passwd = str()

    def connect(self):
        self.ssh.connect(self.host, username=self.user, password=self.passwd, look_for_keys=False)
        print('Connected to %s.' % self.host)
        self.channel = self.ssh.invoke_shell()

    def send(self, b_string):
        self.channel.send(b_string)

    def recieve(self):
        channel_data = str()
        for i in range(10):
            if self.channel.recv_ready():
                channel_data += str(self.channel.recv(9999), 'ascii', 'ignore')
        return channel_data

    def close(self):
        self.ssh.close()

    def get_me_to(self, page):
        pages = {
                 "Hacer Matricula": [2],
                 "Informacion": [5],
                 "Curriculo": [5, 2],
                 "Ver Matricula": [5, 4],
                 "Ver Secciones": [5, 6],
        }
        for i in pages[page]:
            self.send(str(i))
        if page == "Curriculo" or page == "Ver Matricula":
            self.login()

    def addStudentCred(self, studentNum, pn, bday, soc):
        self.student = Student(studentNum, pn, bday, soc)

    def addStudent(self, student):
        self.student = student

    def findStudentCourses(self):
        # FIXME: professor pattern is wrong for some cases that don't have a ','
        # NOTE: Maybe natural language processing?
        name_patern = re.compile(r"([A-Z]{4} \d{4})")
        section_pattern = re.compile(r"\b\d{3}[#]?(?!\d)(?!\))")
        classroom_patern = re.compile(r"(?:[A-Z]{2}\d{3})|(?:[BFQ]{1}\s(?:[ABCDE]{1}|\d{1,3}))")
        professor_pattern = re.compile(r"(?:[A-Z]+\s[A-Z]+[,]\s[A-Z]+)|(?:[A-Z]+[,]\s[A-Z]+\s[A-Z]+)|(?:[A-Z]+[,]\s[A-Z]+)")
        period_pattern = re.compile(r"(MJ\s+\d{1,2}:\d{2}-\s?\d{1,2}:\d{2}(?:am|pm)?)|(LWV\s+\d{1,2}:\d{2}-\s?\d{1,2}:\d{2}(?:am|pm)?)")

        self.get_me_to('Ver Matricula')
        tm.sleep(13)
        text = self.recieve()
        text = escape_ansi(text)

        name_matches = name_patern.findall(text)
        section_matches = section_pattern.findall(text)
        classroom_matches = classroom_patern.findall(text)
        professor_matches = professor_pattern.findall(text)
        period_matches = period_pattern.findall(text)
        # for i in range(len(name_matches)):
        #     print('course: ', name_matches[i])
        #     credits = input('Enter credits: ')
        #     print(i in classroom_matches)
        #     classroom_index = input("Enter index of course's classroom: ")
        #     print(i in period_matches)
        #     period_index = input("Enter index of course's hour: ")
        #     period = date_matches[date_index].strip(' ')
        #     professor = input("Enter the name of the professor: ")
            # self.student.addCourse(name_matches[i], section_matches[i], credits, classroom_matches[classroom_index], )
        print('courses: ', name_matches)
        print('sections: ', section_matches[0:len(name_matches)])
        print('found professors: ', professor_matches)
        print('classrooms: ', classroom_matches)
        print('hours: ', period_matches)
        # print('classrooms: ', classroom_matches)

        # course = Course()
        # self.student.addCourse()

    def login(self):
        self.send(str(self.student.student_number))
        self.send(str(self.student.pin))
        self.send(str(self.student.ss))
        self.send(self.student.birthdate.strftime("%m%d%Y"))
