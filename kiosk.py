# -*- coding: euc-kr -*-    # �ѱ� ����� ���� 5��
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from select import select
import time
import threading

room = {101 : 0, 102 : 0, 103 : 0, 104 : 0}     # �� ��ȣ : �ð�
standby = []    # �����
d_standby = {}  # {����ȣ : �й�}
cnt = 0     # ��ⳡ�� �ο�
lock = []   # lock�ɸ� ��
use_room = {101 : 0, 102 : 0, 103 : 0, 104 :0}     # ��� ���� �� �й��� �й� �Է�
escape_room = {101 : 0, 102 : 0, 103 : 0, 104 : 0}  # �ڸ���� �� ��ȣ : �ð�


############################## ȸ������ ############################## ########################################################################################################################

def addd():     # ȸ�� �߰�
    student = {}
    clsnum = input("�й� �Է� : ")
    while len(clsnum) != 10:
        print("10�ڸ��� �Է����ּ���.(��� : 0)")
        clsnum = input("�й� �Է� : ")
        if clsnum == '0':
            management()

    phone = input("�޴��ȣ �Է� : ")
    while len(phone) != 11:
        print("11�ڸ��� �Է����ּ���.(��� : 0)")
        phone = input("�޴��ȣ �Է� : ")
        if phone == '0':
            management()

    student[clsnum] = phone
    f_a = open("C:/Users/ASUS/source/repos/m_l.txt", 'a', encoding = 'UTF-8-SIG')   # �޸��� �̾��
    student = str(student)
    f_a.write(student)
    f_a.write('\n')     # �޸��� �� �� ���
    f_a.close()
    print(f"{student[2:12]}ȸ���� �߰��Ǿ����ϴ�.")
    management()
    

def delll():    # ȸ�� ����
    del_cnt = 0
    with open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8') as f:
        lines = f.readlines()
    clsnum = str(input("�й� �Է� : "))
    while len(clsnum) != 10:
        print("10�ڸ��� �Է����ּ���.(��� : 0)")
        clsnum = input("�й� �Է� : ")
        if clsnum == '0':
            management()
    for i in lines :
        del_cnt += 1
        if clsnum == i[2:12] :
            with open("C:/Users/ASUS/source/repos/m_l.txt", "w", encoding = 'UTF8') as fw:
                for line in lines:
                    if line.strip("\n") != i[:-1] : # �� ���� ����[:-1]
                        fw.write(line)
            print(f"{i[2:12]}ȸ���� �����Ǿ����ϴ�.")
            management()
        if del_cnt == len(lines) :
            print("�й��� Ȯ���ϼ���")
            delll()
    management()


def management():   # main ȸ������
    print("ȸ�� ���� ������")
    print("1 : �߰�\n2 : ����\n3 : ���\n0 : ����")
    select = int(input("-> "))
    if select == 1:
        addd()
    elif select == 2:
        delll()
    elif select == 3:   # ���
        f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
        lines = f_r.readlines()
        print("ȸ���� : ", len(lines)-1)     # ȸ�� ��
        for i in lines[1:] :    # ȸ�� ���
            print(i)
        management()
    elif select == 0:
        main()
    else:
        management()


############################## login ���� �Լ� ############################## ########################################################################################################################

def login(select, timer):   # �α���(�Խ�)
    global room
    global use_room
    log_cnt = 0
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    log_num = str(input("�й� �Է� : "))
    while len(log_num) != 10:
        print("10�ڸ��� �Է����ּ���.(��� : 0)")
        log_num = input("�й� �Է� : ")
        if log_num == '0':
            main()
    if [k for k, v in use_room.items() if v == log_num]:    # ��� ���� �й����� Ȯ��
        print("��� ���� ���� �ֽ��ϴ�.")
        main()
    else:
        for i in lines :
            log_cnt += 1
            if log_num == i[2:12] :
                pw = str(input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : "))
                while len(pw) != 4:
                    print("4�ڸ��� �Է����ּ���.(��� : 0)")
                    pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : ")
                    if pw == '0':
                        main()
                if pw == i[23:27]:
                    use_room[select] = log_num
                    timer -= 1
                    print(f"{select}�� ���� {timer}�� ���Ƚ��ϴ�.")
                    return 1
                    main()
                else :
                    print("�Է��� ������ �ùٸ��� �ʽ��ϴ�.")
                    login(select, timer)
            if log_cnt == len(lines) :
                print("�й��� Ȯ���ϼ���")
                login(select, timer)

    main()

def logout(select):   # �α׾ƿ�(���)
    global room
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    for i in lines :
        if use_room[select] == i[2:12] :
            pw = str(input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : "))
            while len(pw) != 4:
                print("4�ڸ��� �Է����ּ���.(��� : 0)")
                pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                return 0
            else :
                print("�Է��� ������ �ùٸ��� �ʽ��ϴ�.")
                logout(select)


def w_login():   # �α���(�����)
    global room
    global use_room
    global cnt
    global standby
    global d_standby

    log_cnt = 0
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    log_num = str(input("�й� �Է� : "))
    while len(log_num) != 10:
        print("10�ڸ��� �Է����ּ���.(��� : 0)")
        log_num = input("�й� �Է� : ")
        if log_num == '0':
            main()
    rest = len(standby) - cnt
    for j in range(rest):
        j += 1
        if d_standby[cnt+j] == log_num:
            print("�̹� ��� ���Դϴ�.")
            main()
    if [k for k, v in use_room.items() if v == log_num]:    # ��� ���� �й����� Ȯ��
        print("��� ���� ���� �ֽ��ϴ�.")
        main()
    else:
        for i in lines :
            log_cnt += 1
            if log_num == i[2:12] :
                pw = str(input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : "))
                while len(pw) != 4:
                    print("4�ڸ��� �Է����ּ���.(��� : 0)")
                    pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�) : ")
                    if pw == '0':
                        main()
                if pw == i[23:27]:
                    return i[2:12]  # �й� ��ȯ
                else :
                    print("�Է��� ������ �ùٸ��� �ʽ��ϴ�.")
                    w_login()
            if log_cnt == len(lines) :
                print("�й��� Ȯ���ϼ���")
                w_login()
                

def enter_login(select):  # ��й�ȣ�� �Է� (����� ����)
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�)(��� : 0)\n-> ")
    if pw == '0':
        main()
    for i in lines:
        if d_standby[cnt] == i[2:12]:
            while len(pw) != 4:
                print("4�ڸ��� �Է����ּ���.(��� : 0)")
                pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�)(��� : 0)\n-> ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                use_room[select] = i[2:12]
            else:
                print("�Է��� ������ �ùٸ��� �ʽ��ϴ�.")
                enter_login(select)


def extend_login(select):
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�)(��� : 0)\n-> ")
    print("��")
    if pw == '0':
        main()
    for i in lines:
        print("��")
        if use_room[select] == i[2:12]:
            print("��")
            while len(pw) != 4:
                print("4�ڸ��� �Է����ּ���.(��� : 0)")
                pw = input("��й�ȣ �Է�(�޴���ȭ �� ��ȣ 4�ڸ�)(��� : 0)\n-> ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                    print("��")
                    return 1
            else:
                    print("�Է��� ������ �ùٸ��� �ʽ��ϴ�.")
                    extend_login(select)
        

############################## Ű����ũ ############################## ########################################################################################################################

def rent():     # �뿩
   global room
   global lock
   print(room)
   select = int(input("���� ������\n�� ��ȣ : "))
   if select == 0:      
      main()
   elif(select in room):      
       if room[select] > 0:
         print("��� ���� ���Դϴ�.")
         rent()
       elif(select in lock):
           print(f"{select}�� ���� ���� ���� ���Դϴ�. (����� �� : {len(standby) - cnt})")
            # ����� ����
           enter_login(select)
           timer = int(input("���� �󸶳� �����ðڽ��ϱ�?\nminute : "))
           timer += 1
           t = threading.Thread(target=thrd_timer, args=(select, timer))  # ��Ƽ������
           t.daemon = True
           t.start()
           main()
       else:
         timer = int(input("���� �󸶳� �����ðڽ��ϱ�?\nminute : "))
         timer += 1
         # login() �Լ� �߰�
         success = login(select, timer)
         if success == 1:
            t = threading.Thread(target=thrd_timer, args=(select, timer))  # ��Ƽ������
            t.daemon = True
         main()
   else:      
      print("���� ���Դϴ�.")
      rent()
   return room


def thrd_timer(select, timer):      # ��Ƽ ������ (ī��Ʈ, ��)
    global room
    global cnt
    global standby
    global lock
    room[select] = timer
    while (room[select] != 0):
        room[select] -= 1
        time.sleep(60)
    print("\n", select, "�� �� �̿��� �������ϴ�.")
    use_room[select] = 0    # ��� ���� �� 0���� ����
    if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):  # ���� ����ڰ� �ִٸ� ��
        thrd_lock_timer(select)


def checkout():   # ���
   global room
   global cnt
   global standby
   print(room)
   select = int(input("���� ������\n�� ��ȣ : "))
   if select == 0:      
      main()
   elif(select in room):      
      if room[select] <= 0:
         print("��� �ֽ��ϴ�.")
         checkout()
      else:
         logout(select)
         room[select] = 0
         print("\n", select, "�� ���� �����߽��ϴ�.")
         if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):
            tt = threading.Thread(target=thrd_lock_timer, args=(select,))
            tt.daemon = True
            tt.start()

   else:      
      print("���� ���Դϴ�.")
      checkout()

def thrd_lock_timer(select):    # ��
    global standby
    global cnt
    global lock
    global room
    print("\n", standby[cnt], "�� �����", select, "�� ������ ������.")       
    cnt += 1
    lock.append(select)
    sleep_time = 5     # �� �ð�
    while room[select] <= 0 and sleep_time >= 0:
        sleep_time -= 1
        time.sleep(60)
    if sleep_time <= 0:
        print(f"{select}�� ��� �ð��� �������ϴ�.")
        if cnt < len(standby):
            thrd_lock_timer(select)
    lock.remove(select)
    


def extend():   # ����
   print(room)
   if len(standby) > cnt:
       print("����ڰ� ���� ���� ������ �� �� �����ϴ�")
       main()
   else:
       select = int(input("���� ������\n�� ��ȣ : "))
       if select == 0:
          main()
       elif(select in room):
          if room[select] == 0:
             print("�� ���Դϴ�.")
             extend()
          elif room[select] > 0:
             success = extend_login(select)  # ��й�ȣ �Է�
             if success == 1:
                 add_time = int(input("�󸶳� ���� �Ͻðڽ��ϱ�?\nminute : "))
                 room[select] += add_time
                 print(f"{room[select]}�� ���� {add_time}�� �����߽��ϴ�.")
                 main()
       else:
          print("���� ���Դϴ�.")
          extend()


def wait():     # ���
   global room
   global lock
   if ([k for k, v in room.items() if v == 0]) and (len(lock) == 0):
      print("�� ���� �ֽ��ϴ�.")
      main()
   else:
      waiter = w_login()
      standby.append((len(standby)+1))  # standby[��� ��ȣ] 
      d_standby[standby[-1]] = waiter   # d_standby{��� ��ȣ : �й�}
      print("��� ��ȣ : ", standby[-1])
      main()


def awaiter_lock(select):   # ����� ��
    global stanby
    global cnt
    global lock
    if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):  # ����� 1���̻�, ����� cnt����, ��[] �ȿ� ������� 
        ttt = threading.Thread(target=thrd_lock_timer, args=(select,))
        ttt.daemon = True
        ttt.start()
        main()


def escape():
    global escape_room
    global room
    print(room)
    print(escape_room)
    select = int(input("Ż���� ��(��� : 0)\n->"))
    if select == 0:
        main()
    elif select in escape_room:
        if room[select] <= 0:
            print("�� �� �Դϴ�.")
            main()
        t = threading.Thread(target=thrd_escape, args=(select,))
        t.daemon = True
        t.start()
    else:
        print("���� �� �Դϴ�.")
        escape()
    main()


def thrd_escape(select):
    global escape_room
    global room
    if (escape_room[select] <= 0):
        escape_room[select] += 1
        while (room[select] > 0) and (escape_room[select] > 0):
            escape_room[select] += 1
            time.sleep(60)
    escape_room[select] = 0
        

############################## ���� ############################## ########################################################################################################################
def main():     
   print("���� ������")
   print("1 : �뿩 \n2 : ��� \n3 : ���� \n4 : ��� \n5 : �� ��Ȳ\n6 : �ڸ����\n7 : ȸ������\n0 : ������")   
   select = int(input("-> "))
   if select == 1:
      rent()
      main()
   elif select == 2:
      checkout()
      main()
   elif select == 3:
      extend()
   elif select == 4:
      wait()
   elif select == 5:
       print("���� �ð�", room)
       main()
   elif select == 6:
       escape()
   elif select == 7:
       management()
   elif select == 0:
       exit()
   else:
       main()


main()
