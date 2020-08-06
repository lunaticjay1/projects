import numpy as np
class classRoom:
    def __init__(self, building=None, room=None, cap=None):
        if building is not None and room is not None and cap is not None:
            self.bno = building
            self.roomno = room
            self.capacity = cap
        else:
            self.bno = 0
            self.roomno = 0
            self.capacity = 0


class Dept:
    def __init__(self, dept_name=None, building=None, budget=None):
        if dept_name is not None and building is not None and budget is not None:
            self.dep_name = dept_name
            self.bno = building
            self.budget = budget
        else:
            self.dept_name = "Default"
            self.bno = 0
            self.budget = 0


class course:
    def __init__(self, course_id=None, title=None, dept_name=None, credits=None):
        if course_id is not None and title is not None and dept_name is not None and credits is not None:
            self.course_id = course_id
            self.title = title
            self.dept_name = dept_name
            self.credits = credits
        else:
            self.course_id = 0
            self.title = "Default"
            self.dept_name = "Default"
            self.credits = 0


class instructor:
    def __init__(self, i_id=None, iname=None, dept_name=None, salary=None):
        if i_id is not None and iname is not None and dept_name is not None and salary is not None:
            self.i_id = i_id
            self.iname = iname
            self.dept_name = dept_name
            self.salary = salary
        else:
            self.i_id = 0
            self.iname = "Default"
            self.dept_name = "Default"
            self.salary = 0


class section:
    def __init__(self, course_id, sec_id, semester, year, building, room_number, time_slot_id):
        self.course_id = course_id
        self.sec_id = sec_id
        self.semester = semester
        self.year = year
        self.building = building
        self.rno = room_number
        self.tsi = time_slot_id


class teaches:
    def __init__(self, i_id, course_id, sec_id, semester, year):
        self.i_id = i_id
        self.course_id = course_id
        self.sec_id = sec_id
        self.semester = semester
        self.year = year


class student:
    def __init__(self, s_id, sname, dept_name, tot_cred):
        self.s_id = s_id
        self.sname = sname
        self.dept_name = dept_name
        self.tot_cred = tot_cred


class takes:
    def __init__(self, s_id, course_id, sec_id, semester, year, grade):
        self.s_id = s_id
        self.course_id = course_id
        self.sec_id = sec_id
        self.semester = semester
        self.year = year
        self.grade = grade


class dataBase:
    def __init__(self):
        self.courses = np.array([])
        self.takes = np.array([])
        self.teaches = np.array([])
        self.students = np.array([])
        self.instructors = np.array([])
        self.sec_taken = {}
        self.sec_teach = {}
        self.sec_count = {}
        self.course_taught = []
        self.students_dict = {}
        self.teachers = {}

    def addCourse(self, course):
        self.courses = np.append(self.courses, course)

    def addTakes(self, take):
        self.takes = np.append(self.takes, take)
        if take.year in self.sec_count.keys():
            if take.semester in self.sec_count[take.year].keys():
                if take.sec_id in self.sec_count[take.year][take.semester].keys():
                    self.sec_count[take.year][take.semester][take.sec_id] += 1
                else:
                    self.sec_count[take.year][take.semester][take.sec_id] = 1
            else:
                self.sec_count[take.year][take.semester] = {}
                self.sec_count[take.year][take.semester][take.sec_id] = 1
        else:
            self.sec_count[take.year] = {}
            self.sec_count[take.year][take.semester] = {}
            self.sec_count[take.year][take.semester][take.sec_id] = 1
        if take.sec_id in self.sec_taken.keys():
            self.sec_taken[take.sec_id].append(take.s_id)
        else:
            self.sec_taken[take.sec_id] = [take.s_id]

    def addteaches(self, teach):
        self.teaches = np.append(self.teaches, teach)
        self.sec_teach[teach.i_id] = teach.sec_id

    def addStudents(self, st):
        self.students = np.append(self.students, st)
        self.students_dict[st.s_id] = st.sname

    def addInstructor(self, inst):
        self.instructors = np.append(self.instructors, inst)
        self.teachers[inst.i_id] = inst.iname

    def addSection(self, sec):
        self.course_taught.append(sec.course_id)

    def func1(self, creds):
        ret = []
        for i in self.courses:
            if i.dept_name == "EE" or i.dept_name == "CS":
                if i.credits == creds:
                    ret.append(i.title)

        return ret

    def func2(self, inst_name):
        for i in self.instructors:
            if i.iname == inst_name:
                iid = i.i_id
                if iid in self.sec_teach.keys():
                    t = self.sec_teach[iid]
                    return self.sec_taken[t]
                else:
                    return []
        return []

    def func3(self):
        m = -1
        for i in self.instructors:
            if i.salary >= m:
                m = i.salary
        return m

    def func4(self):
        m = -1
        m_list = []
        for i in self.instructors:
            if i.salary > m:
                m = i.salary
                m_list = [i.iname]
            elif i.salary == m:
                m_list.append(i.iname)
        return m_list

    def func5(self, year, semester):
        try:
            return self.sec_count[year][semester]
        except:
            return 0

    def func6(self, year, semester):
        vals = self.sec_count[year][semester].values()
        vals = list(vals)
        vals = np.array(vals)
        return np.max(vals)

    def func7(self, year, semester):
        m = -1
        max_list = []
        for i in self.sec_count[year][semester]:
            if self.sec_count[year][semester][i] >= m:
                m = self.sec_count[year][semester][i]
                max_list.append(i)
        return max_list

    def func8(self):
        for i in self.instructors:
            i.salary *= 1.1

    def func9(self):
        for i in range(len(self.courses)):
            if self.courses[i].course_id not in self.course_taught:
                self.courses = np.delete(self.courses, i)

    def func10(self, thresh, salary):
        for i in self.students:
            if i.tot_cred >= thresh:
                t = instructor(0, i.sname, i.dept_name, salary)
                self.instructors = np.append(self.instructors, t)
                self.teachers[t.i_id] = t.iname

    def printCourses(self):
        for i in self.courses:
            print(i.title)


D = dataBase()
c = course(1, "DBMS", "CS", 3)
D.addCourse(c)
c = course(2, "EEE", "EE", 3)
D.addCourse(c)
c = course(3, "ALGO", "CS", 6)
D.addCourse(c)
c = course(4, "DLD", "CS", 6)
D.addCourse(c)
i = instructor(1, "JAI", "CS", 200001)
D.addInstructor(i)
i = instructor(2, "CHARAN", "CS", 200000)
D.addInstructor(i)
i = instructor(3, "SOMEONE", "EE", 200001)
D.addInstructor(i)
i = instructor(4, "SOMEBODY", "EE", 200000)
D.addInstructor(i)
s = student(1, "char", "CS", 99)
D.addStudents(s)
s = student(2, "Jai", "CS", 110)
D.addStudents(s)
s = student(3, "P", "EE", 95)
D.addStudents(s)
sec = section(1, 1, "FALL", 2019, "cse", 1, 4)
D.addSection(sec)
sec = section(2, 2, "SPRING", 2019, "eee", 1, 3)
D.addSection(sec)
sec = section(3, 3, "FALL", 2018, "cse", 2, 3)
D.addSection(sec)
t = takes(1, 1, 1, "FALL", 2019, 9)
D.addTakes(t)
t = takes(1, 3, 3, "FALL", 2018, 10)
D.addTakes(t)
t = takes(2, 1, 1, "FALL", 2019, 10)
D.addTakes(t)
t = takes(2, 3, 3, "FALL", 2018, 9)
D.addTakes(t)
t = takes(3, 4, 4, "FALL", 2019, 8)
D.addTakes(t)
t = takes(3, 1, 1, "FALL", 2019, 8)
D.addTakes(t)
t = takes(3, 2, 2, "SPRING", 2019, 9)
D.addTakes(t)
te = teaches(1, 1, 1, "FALL", 2019)
D.addteaches(te)
te = teaches(1, 3, 3, "FALL", 2018)
D.addteaches(te)
te = teaches(2, 3, 3, "FALL", 2018)
D.addteaches(te)
te = teaches(3, 2, 2, "SPRING", 2019)
D.addteaches(te)
print(D.func1(3))  # corresponds to subjects with credits > 3
print(D.func2("JAI"))  # corresponding to students whom JAI teaches
print(D.func3())  # corresponds to Highest salary
print(D.func4())  # List of instructors with Highest salary
print(D.func5(2019, "FALL"))  # enrollment of each section that was offered in a certain semester
print(D.func6(2019, "FALL"))  # maximum enrollment, across all sections, in a certain semester
print(D.func7(2019, "FALL"))  # sections that had the maximum enrollment in a certain semester
D.func8()  # Increment of salary
print(D.func3())  # Check if salary is increased, outputs the maximum one that should be increased
D.printCourses()  # courses before deleting
D.func9()  # deleting not-required courses
print("-----------After deleting-------------")
D.printCourses()  # Courses after deleting
D.func10(100, 300000)  # Making a student Instructor if the requirement is met
print(D.func4())  # Above instructor is inserted with max salary, so he should print (checking)