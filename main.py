import sqlite3
import vk_api
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType


def wr(mess):
    vk.method('messages.send', {'user_id': event.user_id, 'message': mess, 'random_id':get_random_id()})

def get_acc(id):
    if id != 'secret':
        uid = c.execute("SELECT userid FROM lastusers WHERE lastuserid={}".format(str(id))).fetchone()
        print(uid[0])
        acc = c.execute("SELECT log, cash, lvl FROM users WHERE userid={}".format(str(uid[0]))).fetchone()
        print(acc)

        wr('Данные об акке:\nЛогин:\t{}\nДеньги:\t{}\nУровень:\t{}'.format(acc[0],str(acc[1]),str(acc[2])))
    else:
        id = event.user_id
        uid = c.execute("SELECT userid FROM lastusers WHERE lastuserid={}".format(str(id))).fetchone()
        acc = c.execute("SELECT log, cash, lvl FROM users WHERE userid={}".format(str(uid[0]))).fetchone()

        return acc[0]

def safe_acc(id, log, passw, uid):
    if chek_acc(log):
        c.execute("INSERT INTO users VALUES (?,?,?,?,?);",(id,log,passw,1,1))

        c.execute("INSERT OR REPLACE into lastusers VALUES (?,?);",(uid,id))
    else:
        1/0

def chek_acc(log):
    for i in list_users:
        if log in i:
            return False
    return True

def change_pass(log, pas):
    c.execute("UPDATE users SET pass='{}' WHERE log='{}'".format(pas,log))

def change_cash(log, x):

    c.execute("UPDATE users SET cash={} WHERE log='{}'".format(x, log))

def change_lvl(log, x):
    c.execute("UPDATE users SET lvl={} WHERE log='{}'".format(x, log))


vk = vk_api.VkApi(token='29bc1b3f813fb92406c0baf67a5017561005257ec6538fa97ad32bd3850be7fd1a249f87c6f269248f586')

# Работа с сообщениями
longpoll = VkLongPoll(vk)

f=0
list = ['справка', '1','2','3','4','5']
# Основной цикл
for event in longpoll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня( то есть бота)
        if event.to_me:

            conn = sqlite3.connect('customer.db')
            c = conn.cursor()
            print(c.execute("SELECT * FROM users").fetchall())
            list_users = c.execute("SELECT * FROM users").fetchall()
            N = 0
            for i in list_users:
                 N += 1

            # Сообщение от пользователя
            request = event.text

            # Каменная логика ответа
            if request.lower() not in list and f==0:
                wr('Для помощи напишите "Справка"')

            elif event.text.lower() == "справка" and f == 0:
                wr('Для создания акка напиши 1, для смены пароля 2, для установки уровня 3, денег - 4,'
                   ' получить данные -5')

            elif request=='1' and f==0:
                wr("Введите логин")
                f = 1

            elif request and f==1:
                if chek_acc(event.text):
                    log = event.text
                    wr("Введите пароль")
                    f = 10
                else:
                    wr("Логин занят")
                    f = 0

            elif request and f == 10:
                wr("Акк создан")
                safe_acc(N, log, event.text, event.user_id)
                f = 0

            elif request=='2':
                wr("меняй")
                f=2

            elif request and f==2:
                change_pass(get_acc('secret'),request)
                wr("успешно поменял")
                f=0

            elif request=='3' and f==0:
                wr('укажи ник')
                f=3

            elif request and f==3:
                log = request
                wr('пиши какой лвл')
                f=30


            elif request and f==30:
                try:
                    change_lvl(log, int(request))
                    wr('все')
                except:
                    wr("Введено не число")
                f=0
            elif request=='4' and f==0:
                wr('укажи ник')
                f=4

            elif request and f==4:
                wr('сколько маней')
                f=40
                log = request


            elif request and f==40:
                print(request)
                try:
                    request = int(request)
                except:
                    wr('Вы не ввели число')
                    continue
                change_cash(log, int(request))
                wr('деньги на аккаунте')
                f = 0

            elif request=='5' and f==0:
                get_acc(event.user_id)

            conn.commit()
            conn.close()

