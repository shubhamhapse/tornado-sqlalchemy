from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
import json
import config

engine = create_engine(config.engine_url,echo=False)
students=None
lecture=None
stu_lec=None


def create_tables():
    """Create tables using meta class"""
    meta = MetaData()
    global students,lecture,stu_lec
    students = Table(
        'students', meta, 
        Column('student_id', Integer, primary_key = True), 
        Column('name', String), 
        Column('lastname', String), 
    )

    lecture = Table(
        'lecture', meta, 
        Column('lecture_id', Integer, primary_key = True), 
        Column('class_name', String), 
        Column('subject', String), 
    )
    stu_lec= Table(
        'student_lecture', meta,  
        Column('student_id', String), 
        Column('lecture_id', String), 
    )
    # create all tables at once
    meta.create_all(engine)

def insert_student(_name,_lastname):
    """Insert student row into the table"""
    ins = students.insert().values(name = _name,lastname = _lastname)
    conn= engine.connect()
    conn.execute(ins)

def insert_lecture(_class,_subject):
    """insert lecture info into table"""
    ins = lecture.insert().values(class_name = _class,subject = _subject)
    conn= engine.connect()
    conn.execute(ins)

def assign_student_to_lecture(_student_id,_lecture_id):
    ins = stu_lec.insert().values(student_id = _student_id , lecture_id = _lecture_id)
    conn= engine.connect()
    conn.execute(ins)


def change_student_name(_student_id,_new_name):
    ins = students.update().where(students.c.id == _student_id).values(name = _new_name)
    conn = engine.connect()
    conn.execute(ins)


def get_lecture(_id):
    """Get lecture info which has given id"""
    lecture_list=[]
    ins=lecture.select().where(lecture.c.id == _id)
    conn= engine.connect()
    result=conn.execute(ins)
    for row in result:
        lecture_dict={}
        lecture_dict['lecture_id']=row['lecture_id']
        lecture_dict['class_name']=row['class_name']
        lecture_dict['subject']=row['subject']
        lecture_list.append(lecture_dict)
    return json.dumps(lecture_list)

def get_attendance():
    """returns Students attending lectures map"""
    students_in_class =[]
    ins=stu_lec.select()
    conn= engine.connect()
    result=conn.execute(ins)
    for row in result:
        dict ={}
        dict['student_id']=row['student_id']
        dict['lecture_id']=row['lecture_id']
        students_in_class.append(dict)
    return json.dumps(students_in_class)

def list_students():
    """Returns JSON array contains list of students"""
    student_list=[]
    ins=students.select()
    conn= engine.connect()
    result=conn.execute(ins)
    for row in result:
        student_dict={}
        student_dict['name']=row['name']
        student_dict['lastname']=row['lastname']
        student_dict['student_id']=row['student_id']
        student_list.append(student_dict)
    return json.dumps(student_list)


def list_lectures():
    """Returns JSON array contains list of Lectures"""
    lecture_list=[]
    ins=lecture.select()
    conn= engine.connect()
    result=conn.execute(ins)
    for row in result:
        lecture_dict={}
        lecture_dict['lecture_id']=row['lecture_id']
        lecture_dict['class_name']=row['class_name']
        lecture_dict['subject']=row['subject']
        lecture_list.append(lecture_dict)
    return json.dumps(lecture_list)


create_tables()
