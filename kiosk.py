# -*- coding: euc-kr -*-    # 한글 사용을 위한 5줄
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from select import select
import time
import threading

room = {101 : 0, 102 : 0, 103 : 0, 104 : 0}     # 방 번호 : 시간
standby = []    # 대기자
d_standby = {}  # {대기번호 : 학번}
cnt = 0     # 대기끝난 인원
lock = []   # lock걸린 방
use_room = {101 : 0, 102 : 0, 103 : 0, 104 :0}     # 사용 중인 방 학번에 학번 입력
escape_room = {101 : 0, 102 : 0, 103 : 0, 104 : 0}  # 자리비움 방 번호 : 시간


############################## 회원관리 ############################## ########################################################################################################################

def addd():     # 회원 추가
    student = {}
    clsnum = input("학번 입력 : ")
    while len(clsnum) != 10:
        print("10자리로 입력해주세요.(취소 : 0)")
        clsnum = input("학번 입력 : ")
        if clsnum == '0':
            management()

    phone = input("휴대번호 입력 : ")
    while len(phone) != 11:
        print("11자리로 입력해주세요.(취소 : 0)")
        phone = input("휴대번호 입력 : ")
        if phone == '0':
            management()

    student[clsnum] = phone
    f_a = open("C:/Users/ASUS/source/repos/m_l.txt", 'a', encoding = 'UTF-8-SIG')   # 메모장 이어쓰기
    student = str(student)
    f_a.write(student)
    f_a.write('\n')     # 메모장 한 줄 띄기
    f_a.close()
    print(f"{student[2:12]}회원이 추가되었습니다.")
    management()
    

def delll():    # 회원 삭제
    del_cnt = 0
    with open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8') as f:
        lines = f.readlines()
    clsnum = str(input("학번 입력 : "))
    while len(clsnum) != 10:
        print("10자리로 입력해주세요.(취소 : 0)")
        clsnum = input("학번 입력 : ")
        if clsnum == '0':
            management()
    for i in lines :
        del_cnt += 1
        if clsnum == i[2:12] :
            with open("C:/Users/ASUS/source/repos/m_l.txt", "w", encoding = 'UTF8') as fw:
                for line in lines:
                    if line.strip("\n") != i[:-1] : # 빈 공간 제거[:-1]
                        fw.write(line)
            print(f"{i[2:12]}회원이 삭제되었습니다.")
            management()
        if del_cnt == len(lines) :
            print("학번을 확인하세요")
            delll()
    management()


def management():   # main 회원관리
    print("회원 관리 페이지")
    print("1 : 추가\n2 : 삭제\n3 : 목록\n0 : 종료")
    select = int(input("-> "))
    if select == 1:
        addd()
    elif select == 2:
        delll()
    elif select == 3:   # 목록
        f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
        lines = f_r.readlines()
        print("회원수 : ", len(lines)-1)     # 회원 수
        for i in lines[1:] :    # 회원 명단
            print(i)
        management()
    elif select == 0:
        main()
    else:
        management()


############################## login 관련 함수 ############################## ########################################################################################################################

def login(select, timer):   # 로그인(입실)
    global room
    global use_room
    log_cnt = 0
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    log_num = str(input("학번 입력 : "))
    while len(log_num) != 10:
        print("10자리로 입력해주세요.(취소 : 0)")
        log_num = input("학번 입력 : ")
        if log_num == '0':
            main()
    if [k for k, v in use_room.items() if v == log_num]:    # 사용 중인 학번인지 확인
        print("사용 중인 방이 있습니다.")
        main()
    else:
        for i in lines :
            log_cnt += 1
            if log_num == i[2:12] :
                pw = str(input("비밀번호 입력(휴대전화 뒷 번호 4자리) : "))
                while len(pw) != 4:
                    print("4자리로 입력해주세요.(취소 : 0)")
                    pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리) : ")
                    if pw == '0':
                        main()
                if pw == i[23:27]:
                    use_room[select] = log_num
                    timer -= 1
                    print(f"{select}번 방을 {timer}분 빌렸습니다.")
                    return 1
                    main()
                else :
                    print("입력한 정보가 올바르지 않습니다.")
                    login(select, timer)
            if log_cnt == len(lines) :
                print("학번을 확인하세요")
                login(select, timer)

    main()

def logout(select):   # 로그아웃(퇴실)
    global room
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    for i in lines :
        if use_room[select] == i[2:12] :
            pw = str(input("비밀번호 입력(휴대전화 뒷 번호 4자리) : "))
            while len(pw) != 4:
                print("4자리로 입력해주세요.(취소 : 0)")
                pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리) : ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                return 0
            else :
                print("입력한 정보가 올바르지 않습니다.")
                logout(select)


def w_login():   # 로그인(대기자)
    global room
    global use_room
    global cnt
    global standby
    global d_standby

    log_cnt = 0
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    log_num = str(input("학번 입력 : "))
    while len(log_num) != 10:
        print("10자리로 입력해주세요.(취소 : 0)")
        log_num = input("학번 입력 : ")
        if log_num == '0':
            main()
    rest = len(standby) - cnt
    for j in range(rest):
        j += 1
        if d_standby[cnt+j] == log_num:
            print("이미 대기 중입니다.")
            main()
    if [k for k, v in use_room.items() if v == log_num]:    # 사용 중인 학번인지 확인
        print("사용 중인 방이 있습니다.")
        main()
    else:
        for i in lines :
            log_cnt += 1
            if log_num == i[2:12] :
                pw = str(input("비밀번호 입력(휴대전화 뒷 번호 4자리) : "))
                while len(pw) != 4:
                    print("4자리로 입력해주세요.(취소 : 0)")
                    pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리) : ")
                    if pw == '0':
                        main()
                if pw == i[23:27]:
                    return i[2:12]  # 학번 반환
                else :
                    print("입력한 정보가 올바르지 않습니다.")
                    w_login()
            if log_cnt == len(lines) :
                print("학번을 확인하세요")
                w_login()
                

def enter_login(select):  # 비밀번호만 입력 (대기자 입장)
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리)(취소 : 0)\n-> ")
    if pw == '0':
        main()
    for i in lines:
        if d_standby[cnt] == i[2:12]:
            while len(pw) != 4:
                print("4자리로 입력해주세요.(취소 : 0)")
                pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리)(취소 : 0)\n-> ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                use_room[select] = i[2:12]
            else:
                print("입력한 정보가 올바르지 않습니다.")
                enter_login(select)


def extend_login(select):
    global use_room
    f_r = open("C:/Users/ASUS/source/repos/m_l.txt", "r", encoding = 'UTF8')
    lines = f_r.readlines()
    pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리)(취소 : 0)\n-> ")
    print("가")
    if pw == '0':
        main()
    for i in lines:
        print("나")
        if use_room[select] == i[2:12]:
            print("다")
            while len(pw) != 4:
                print("4자리로 입력해주세요.(취소 : 0)")
                pw = input("비밀번호 입력(휴대전화 뒷 번호 4자리)(취소 : 0)\n-> ")
                if pw == '0':
                    main()
            if pw == i[23:27]:
                    print("라")
                    return 1
            else:
                    print("입력한 정보가 올바르지 않습니다.")
                    extend_login(select)
        

############################## 키오스크 ############################## ########################################################################################################################

def rent():     # 대여
   global room
   global lock
   print(room)
   select = int(input("방을 고르세요\n방 번호 : "))
   if select == 0:      
      main()
   elif(select in room):      
       if room[select] > 0:
         print("사용 중인 방입니다.")
         rent()
       elif(select in lock):
           print(f"{select}번 방은 예약 중인 방입니다. (대기자 수 : {len(standby) - cnt})")
            # 대기자 입장
           enter_login(select)
           timer = int(input("방을 얼마나 빌리시겠습니까?\nminute : "))
           timer += 1
           t = threading.Thread(target=thrd_timer, args=(select, timer))  # 멀티쓰레드
           t.daemon = True
           t.start()
           main()
       else:
         timer = int(input("방을 얼마나 빌리시겠습니까?\nminute : "))
         timer += 1
         # login() 함수 추가
         success = login(select, timer)
         if success == 1:
            t = threading.Thread(target=thrd_timer, args=(select, timer))  # 멀티쓰레드
            t.daemon = True
         main()
   else:      
      print("없는 방입니다.")
      rent()
   return room


def thrd_timer(select, timer):      # 멀티 쓰레드 (카운트, 락)
    global room
    global cnt
    global standby
    global lock
    room[select] = timer
    while (room[select] != 0):
        room[select] -= 1
        time.sleep(60)
    print("\n", select, "번 방 이용이 끝났습니다.")
    use_room[select] = 0    # 사용 중인 방 0으로 변경
    if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):  # 다음 대기자가 있다면 락
        thrd_lock_timer(select)


def checkout():   # 퇴실
   global room
   global cnt
   global standby
   print(room)
   select = int(input("방을 고르세요\n방 번호 : "))
   if select == 0:      
      main()
   elif(select in room):      
      if room[select] <= 0:
         print("비어 있습니다.")
         checkout()
      else:
         logout(select)
         room[select] = 0
         print("\n", select, "번 방을 종료했습니다.")
         if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):
            tt = threading.Thread(target=thrd_lock_timer, args=(select,))
            tt.daemon = True
            tt.start()

   else:      
      print("없는 방입니다.")
      checkout()

def thrd_lock_timer(select):    # 락
    global standby
    global cnt
    global lock
    global room
    print("\n", standby[cnt], "번 대기자", select, "번 방으로 오세요.")       
    cnt += 1
    lock.append(select)
    sleep_time = 5     # 락 시간
    while room[select] <= 0 and sleep_time >= 0:
        sleep_time -= 1
        time.sleep(60)
    if sleep_time <= 0:
        print(f"{select}방 대기 시간이 끝났습니다.")
        if cnt < len(standby):
            thrd_lock_timer(select)
    lock.remove(select)
    


def extend():   # 연장
   print(room)
   if len(standby) > cnt:
       print("대기자가 있을 때는 연장을 할 수 없습니다")
       main()
   else:
       select = int(input("방을 고르세요\n방 번호 : "))
       if select == 0:
          main()
       elif(select in room):
          if room[select] == 0:
             print("빈 방입니다.")
             extend()
          elif room[select] > 0:
             success = extend_login(select)  # 비밀번호 입력
             if success == 1:
                 add_time = int(input("얼마나 연장 하시겠습니까?\nminute : "))
                 room[select] += add_time
                 print(f"{room[select]}번 방을 {add_time}분 연장했습니다.")
                 main()
       else:
          print("없는 방입니다.")
          extend()


def wait():     # 대기
   global room
   global lock
   if ([k for k, v in room.items() if v == 0]) and (len(lock) == 0):
      print("빈 방이 있습니다.")
      main()
   else:
      waiter = w_login()
      standby.append((len(standby)+1))  # standby[대기 번호] 
      d_standby[standby[-1]] = waiter   # d_standby{대기 번호 : 학번}
      print("대기 번호 : ", standby[-1])
      main()


def awaiter_lock(select):   # 대기자 락
    global stanby
    global cnt
    global lock
    if (len(standby) >= 1) and (len(standby) >= cnt) and (select not in lock):  # 대기자 1명이상, 대기자 cnt이하, 락[] 안에 없어야함 
        ttt = threading.Thread(target=thrd_lock_timer, args=(select,))
        ttt.daemon = True
        ttt.start()
        main()


def escape():
    global escape_room
    global room
    print(room)
    print(escape_room)
    select = int(input("탈주자 방(취소 : 0)\n->"))
    if select == 0:
        main()
    elif select in escape_room:
        if room[select] <= 0:
            print("빈 방 입니다.")
            main()
        t = threading.Thread(target=thrd_escape, args=(select,))
        t.daemon = True
        t.start()
    else:
        print("없는 방 입니다.")
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
        

############################## 메인 ############################## ########################################################################################################################
def main():     
   print("메인 페이지")
   print("1 : 대여 \n2 : 퇴실 \n3 : 연장 \n4 : 대기 \n5 : 방 현황\n6 : 자리비움\n7 : 회원관리\n0 : 나가기")   
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
       print("남은 시간", room)
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
