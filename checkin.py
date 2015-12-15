# -*- coding=utf-8

from hashlib import md5
from datetime import datetime,date
import os
import atexit

folder_path = os.path.dirname(os.path.realpath(__file__))

class Student:
    def __init__(self, name, stu_id, phone, level):
        self.name = name
        self.stu_id = stu_id
        self.phone = phone
        self.level = level
        self.time = ""

def save_checkin(course, stus):
    fptr = open(folder_path + "/" + str(date.today()), "w", encoding="utf-8")
    fptr.write("簽到記錄：\n")
    normal_count = 0
    for stu in stus:
        if stu.level == course:
            fptr.write(stu.name + "\t\t" + stu.time + "\t\t本日社員\n")
        elif stu.level == "normal":
            normal_count += 1
            fptr.write(stu.name + "\t\t" + stu.time + "\t\t一般社員\n")
        elif stu.level == "staff":
            fptr.write(stu.name + "\t\t" + stu.time + "\t\t工作人員\n")
        else:
            fptr.write(stu.name + "\t\t" + stu.time + "\t\t補課社員\n")
    
    fptr.write("==========================\n")
    fptr.write("一般社員：" + str(normal_count) + "\n")
    fptr.close()
    return True

def get_absence(course_stulist , checked, stu_list):
    result = []
    absences = list(set(course_stulist).difference(set(checked)))
    fptr = open(folder_path + "/" + str(date.today()), "a", encoding="utf-8")
    fptr.write("==========================\n")
    fptr.write("未到社員：\n")
    for absence_stu in absences:
        stu = [stu_ for stu_ in stu_list if stu_.stu_id in absence_stu][0]
        fptr.write(stu.name + "\t\t" + stu.phone + "\n")    
        result.append(stu.name)
    fptr.close()
    return result

def init_Student():
    result = list()
    fptr = open(folder_path + "/stu_list", encoding="utf-8")
    
    student_file = fptr.read().split("\n")
    for student in student_file:
        if student.strip():
            student = student.split(",")
            name = student[0]
            stu_id = student[1]
            phone = student[2]
            level = student[3]
            result.append(Student(name, stu_id, phone, level))
    fptr.close()
    return result
def exit_shell():
    save_checkin(course, checked)
    course_stulist = [stu.stu_id for stu in stu_list if stu.level == course]
    absence = get_absence(course_stulist, checked_stuid, stu_list)
    print("=================================")
    print("未到社員：", len(absence), "人")
    print("\n".join(absence))

atexit.register(exit_shell)
stu_list = init_Student()

print("台科大程式設計研究社 社課簽到系統")
print("=================================")
print("使用說明")
print("這是一套能幫忙進行社課簽到的系統")
print("校內同學請刷學生證")
print("校友與校外學生請輸入電話或學號")
print("輸入0則程式結束")
print("=================================")
print("社課代碼")
print("scratch")

course = ""
while True:
    course = input("請輸入課程代碼： ").strip()
    if course not in ["scratch"]:
        print("輸入錯誤，查無此課程代碼。")
    else:
        break

checked = []
checked_stuid = []
normal_count = 0
logger = open(folder_path + '/signin.log', 'a', encoding="utf-8")
while True:
    stu_id = input("簽到： ").strip().lower()
    logger.write("%s\t%s\n" % (stu_id, datetime.now()))
    if(stu_id == "0"):
        break;

    stu_id_md5 = md5()
    stu_id_md5.update(stu_id.encode("utf8"))
    stu_id_md5 = stu_id_md5.hexdigest()
    
    for stu in stu_list:
        if stu.stu_id == stu_id_md5:
            flag = True
            break
        else:
            flag = False
    
    if flag:
        stu.time = str(datetime.now())
        checked.append(stu)
        checked_stuid.append(stu.stu_id)

        print("姓名：",stu.name)
        print("時間：",datetime.now())
        print("身分：",stu.level)
        
        if stu.level == "normal":
            normal_count += 1
            print("一般社員：", normal_count)
        
        print("簽到成功！")
    else:
        print("查無此人！")

    print("=================================")