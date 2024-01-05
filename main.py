from data.RDB import RDB
import os
import openpyxl
import requests
import telebot
import time
from telebot import types
from datetime import datetime, timedelta

FLASH = "6469267374:AAGpqOURKiovrWksfOoDwE57bqNC1Eh1h48"
CURRENT_BOT = FLASH
bot = telebot.TeleBot(CURRENT_BOT)

cwd = os.getcwd()
print(cwd)

current_outer_time = datetime.now().strftime('%d.%m.%Y %H:%M')
# time_to_arrive = (datetime.now() + timedelta(hours=2)).strftime('%d.%m.%Y %H:%M')
print(f"Бот запущен в", current_outer_time)
organization = ""
bs_name = ""
address = ""
coordinates = ""
order_type = ""
job_type = ""
job_description = ""
ustk_job_description = ""
job_description_list = []
ustk_job_description_list = []
workers_list = []
job_list = ["АВР", "ДГУ", "ППР", "ТО", "Работы по заданию", "Оптимизация"]
ustk_job_list = ["АВР", "ДГУ", "ППР", "ТО", "Работы по заданию", "Оптимизация"]
worker = ""
partner1 = ""
partner2 = ""
crwo = ""
request = ""
mult_bs_list = []
multi_coordinates_list = []
multi_address_list = []
file_PATH = ""
workers_PATH = ""
PO = "ПОДРЯДЧИК"
MM = "МИР"


def add_preffix(bs_name):
    preffix = (4-len(bs_name))*"0"
    bs_name = "CR" + preffix + bs_name
    if not bs_name in RDB:
        bs_name = bs_name.replace("CR", "SE")
    return bs_name


#выводит список команд
@bot.message_handler(commands=["cmdlist"])
def add_worker(message):
    bot.send_message(message.chat.id, "/addworker-добавить нового сотрудника\n/addjd-добавить новое описание работ ММ\n"
                                      "/addjdu-добавить новое описание работ ЮСТК\n"
                                      "/addjd-добавить новое описание работ\n"
                                      "/jdfile- выгрузить файл с описаниями работ инженерам Миранда-Медиа\n"
                                      "/jdufile- выгрузить файл с описаниями работ ЮСТК\n"
                                      "/del_worker -удалить указанного сотрудника\n"
                                      "/del_jd -удалить задание ММ\n"
                                      "/del_jd_u -удалить  задание ЮСТК\n"
                                      "/printwl -показать список сотрудников\n"
                                      "/wfile -выгрузить  список сотрудников\n"
                                      "/allfiles -выгрузить   все списки файлами\n"
                                      "/destroy_it_all -удалить все базы данных, стереть код, запустить протокол самоуничтожения.")

    ######выгрузить  все списки  в виде файлов  ######
@bot.message_handler(commands=["allfiles"])
def all_files(message):
    bot.send_document(message.chat.id, open(rf"data/workers/workers.txt", 'rb'))
    bot.send_document(message.chat.id, open(rf"data/jd/job_description.txt", 'rb'))
    bot.send_document(message.chat.id, open(rf"data/jd/ustk_job_description.txt", 'rb'))

    #выводит список сотрудников в виде документа
@bot.message_handler(commands=["wfile"])
def wfile(message):
    bot.send_document(message.chat.id, open(rf"data/workers/workers.txt", 'rb'))

    ####### выгрузить список заданий для  миранды


@bot.message_handler(commands=["jdfile"])
def jdfile(message):
    bot.send_document(message.chat.id, open(rf"data/jd/job_description.txt", 'rb'))

@bot.message_handler(commands=["jdufile"])
def jdufile(message):
    bot.send_document(message.chat.id, open(rf"data/jd/ustk_job_description.txt", 'rb'))


#выводит список работников
@bot.message_handler(commands=["printwl"])
def printwl(message):
    with open(f"data/workers/workers.txt","r",encoding="utf-8") as file:
        c = 0
        s = ""
        for worker in sorted(file):
            c += 1
            number = str(c)
            s = s+number+"."+worker+"\n"
        bot.send_message(message.chat.id, s)

# УНИЧТОЖИТЬ ВСЁ
@bot.message_handler(commands=["destroy_it_all"])
def destroy_it_all(message):
    enemy_time = datetime.now().strftime("%d_%m")
    with open(f"enemies/{enemy_time}.txt", "a") as file:
        file.write(f"{message.from_user.first_name} {message.from_user.last_name}\n")
    bot.send_message(message.chat.id, f"Внимание всем! среди нас крыса! И ее имя {message.from_user.last_name} {message.from_user.first_name}")
    time.sleep(2)
    bot.send_message(message.chat.id, "🖕")

#добавить сотрудника
@bot.message_handler(commands=["addworker"])
def add_worker(message):
    bot.send_message(message.chat.id, "Введи Фамилию сотрудника")
    bot.register_next_step_handler(message, add_new_worker)


def add_new_worker(message):
    if len(message.text.split()) > 1:
        for name in range(len(message.text.split())):
            worker = message.text.split()[name]
            with open(f"data/workers/workers.txt", "a",encoding="utf-8") as file:
                file.write(worker.capitalize() + "\n")
                bot.send_message(message.chat.id, f"Сотрудник {worker.capitalize()} добавлен")
    else:
        worker = message.text
        with open(f"data/workers/workers.txt", "a",encoding="utf-8") as file:
            file.write(worker.capitalize() + "\n")
            bot.send_message(message.chat.id, f"Сотрудник {worker.capitalize()} добавлен")

#добавить задание
@bot.message_handler(commands=["addjd"])
def add_worker(message):
    bot.send_message(message.chat.id, "Введи описание работ")
    bot.register_next_step_handler(message, add_job_description)


def add_job_description(message):
    if len(message.text.split()) > 1:
        for job in range(len(message.text.split("/*"))):
            job_descr = message.text.split("/*")[job].strip()
            with open(f"data/jd/job_description.txt", "a", encoding="utf-8") as file:
                file.write(job_descr + "\n")
                bot.send_message(message.chat.id, f"Описание '{job_descr[:15]}...' добавлено")
    else:
        job_descr = message.text
        with open(f"data/jd/job_description.txt", "a") as file:
            file.write(job_descr.capitalize() + "\n")
            bot.send_message(message.chat.id, f"Описание '{job_descr[:15]}...' добавлено")

#Добавить задание ЮСТК
@bot.message_handler(commands=["addjdu"])
def add_worker(message):
    bot.send_message(message.chat.id, "Введи описание работ")
    bot.register_next_step_handler(message, add_ustk_job_description)


def add_ustk_job_description(message):
    if len(message.text.split()) > 1:
        for job in range(len(message.text.split("/*"))):
            job_descr = message.text.split("/*")[job].strip()
            with open(f"data/jd/ustk_job_description.txt", "a",encoding="utf-8") as file:
                file.write(job_descr + "\n")
                bot.send_message(message.chat.id, f"Описание '{job_descr[:15]}...' добавлено")
    else:
        job_descr = message.text
        with open(f"data/jd/ustk_job_description.txt", "a",encoding="utf-8") as file:
            file.write(job_descr.capitalize() + "\n")
            bot.send_message(message.chat.id, f"Описание '{job_descr[:15]}...' добавлено")

#Удалить работника
@bot.message_handler(commands=["del_worker"])
def add_worker(message):
    bot.send_message(message.chat.id, "Введи фамилию удаляемого: ")
    bot.register_next_step_handler(message, del_worker)

def del_worker(message):
    with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
        a = []
        for worker in file:
            a.append(worker.rstrip("\n"))
        if message.text.strip().capitalize() not in a:
            bot.send_message(message.chat.id,
                             "Такого работника и в помине нет,похоже что данные введены 'через жопу', чтобы попробовать еще раз- запустите комманду /del_worker снова.")
            bot.send_message(message.chat.id, "🤷🏻‍♂️")
        else:
            a.remove(message.text.strip().capitalize())
            print(a)
            with open(f"data/workers/workers.txt", "w",encoding="utf-8") as file:
                for worker in a:
                    file.write(worker + "\n")
                bot.send_message(message.chat.id, f"Работник {message.text.strip().capitalize()} был удален")

#удалить задание
@bot.message_handler(commands=["del_jd"])
def add_worker(message):
    bot.send_message(message.chat.id, "Введите задание, которое нужно удалить (скопируйте из чата предварительно..)")
    bot.register_next_step_handler(message, del_jd)


def del_jd(message):
    with open(f"data/jd/job_description.txt", "r",encoding="utf-8") as file:
        a = []
        for job in file:
            a.append(job.rstrip("\n"))
        if message.text.strip() not in a:
            bot.send_message(message.chat.id,
                             "Такого описания задания  в списке нет,похоже что данные введены 'через жопу', чтобы попробовать еще раз- запустите комманду /del_jd снова.")
            bot.send_message(message.chat.id, "🤷🏻‍♂️")
        else:
            a.remove(message.text.strip())
            print(a)
            with open(f"data/jd/job_description.txt", "w",encoding="utf-8") as file:
                for job in a:
                    file.write(job + "\n")
                bot.send_message(message.chat.id, f"Описание задания '{message.text.strip()[:15]}' было удалено")

#удалить задание ЮСТК
@bot.message_handler(commands=["del_jd_u"])
def add_worker(message):
    bot.send_message(message.chat.id,
                     "Введите описание задания подрядчику, которое нужно удалить (скопируйте из чата предварительно..)")
    bot.register_next_step_handler(message, del_jd_u)


def del_jd_u(message):
    with open(f"data/jd/ustk_job_description.txt", "r",encoding="utf-8") as file:
        a = []
        for job in file:
            a.append(job.rstrip("\n"))
        if message.text.strip() not in a:
            bot.send_message(message.chat.id,
                             "Такого описания задания  в списке нет,похоже что данные введены 'через жопу', чтобы попробовать еще раз- запустите комманду /del_jd снова.")
            bot.send_message(message.chat.id, "🤷🏻‍♂️")
        else:
            a.remove(message.text.strip())
            print(a)
            with open(f"data/jd/ustk_job_description.txt", "w",encoding="utf-8") as file:
                for job in a:
                    file.write(job + "\n")
                bot.send_message(message.chat.id,
                                 f"Описание задания для подрядчика.'{message.text.strip()[:15]}' было удалено")


#Код основной
#################################################################
@bot.message_handler()
def start(message):
    global bs_name
    global multi_bs_list
    global multi_coordinates_list
    global multi_address_list


#обработка множественного ввода БС, введенных через пробел
#формирование шестизначного названия БС и распределение между DR,LR,UH и UZ

    if len(message.text.split()) > 1:
        multi_bs_list = []
        multi_address_list = []
        multi_coordinates_list = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        miranda_button = types.KeyboardButton(f"{MM}")
        ustk_button = types.KeyboardButton(f"{PO}")
        markup.add(miranda_button, ustk_button)
        for bs in message.text.upper().split():
            bs_name = bs
            if not bs_name in RDB:
                bs_name = add_preffix(bs_name)
            multi_bs_list.append(bs_name)
            multi_coordinates_list.append(RDB[bs_name]["coordinates"])
            multi_address_list.append(RDB[bs_name]["address"])
        bot.send_message(message.chat.id, "Выбери организацию", reply_markup=markup)
        bot.register_next_step_handler(message, multi_process_miranda)

    else:
        bs_name = message.text.upper()
        if not bs_name in RDB:
            bs_name = add_preffix(bs_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        miranda_button = types.KeyboardButton(f"{MM}")
        ustk_button = types.KeyboardButton(f"{PO}")
        markup.add(miranda_button, ustk_button)
        bot.send_message(message.chat.id, "Выбери организацию", reply_markup=markup)
        bot.register_next_step_handler(message, process_miranda)
def multi_process_miranda(message):
    global job_list
    if message.text == f"{MM}":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for job in job_list:
            markup.add(job)
        bot.send_message(message.chat.id, "Выбери тип работ", reply_markup=markup)
        bot.register_next_step_handler(message, multi_process_job_list)
    elif message.text == f"{PO}":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for job in ustk_job_list:
            markup.add(job)
        bot.send_message(message.chat.id, "Выбери тип задач подрядчику", reply_markup=markup)
        bot.register_next_step_handler(message, multi_process_ustk_job_list)

def multi_process_ustk_job_list(message):
    ustk_job_description_list = []
    with open(f"data/jd/ustk_job_description.txt", "r",encoding="utf-8") as file:
        for jd in file:
            ustk_job_description_list.append(jd.rstrip("\n"))
    global ustk_job_type
    global ustk_job_description
    if message.text in job_list:
        ustk_job_type = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        own_jd = types.KeyboardButton("Свой текст задания")
        markup.add(own_jd)
        for job_des in sorted(ustk_job_description_list):
            markup.add(job_des)
        bot.send_message(message.chat.id, "Выбери описание работ", reply_markup=markup)
        bot.register_next_step_handler(message, multi_get_ustk_job_description)

def multi_get_ustk_job_description(message):
    global job_description_list
    global job_description
    if message.text == "Свой текст задания":
        bot.send_message(message.chat.id,"Введи текст задания :   ")
        bot.register_next_step_handler(message, make_own_multi_jdu)
    else:

        job_description = message.text
        bot.send_message(message.chat.id, "Введи номер CRWO :")
        bot.register_next_step_handler(message, multi_get_ustk_crwo)

def make_own_multi_jdu(message):
    global job_description
    job_description = message.text
    bot.send_message(message.chat.id, "Введи номер CRWO :")
    bot.register_next_step_handler(message, multi_get_ustk_crwo)

def multi_get_ustk_crwo(message):

    global crwo
    global multi_bs_list
    global multi_coordinates_list
    global multi_address_list

    current_log_time = datetime.now().strftime('%d.%m.%Y')
    crwo = message.text
    print("CRWO000000", crwo)
    global job_type
    crwo_delta = 0
    print("multi_bs_list=",multi_bs_list)
    for i in range(len(multi_bs_list)):
        bs_name = multi_bs_list[i]
        coordinates = multi_coordinates_list[i]
        address = multi_address_list[i]
        current_time = (datetime.now() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
        time_to_arrive = ((datetime.now() + timedelta(hours=2))+timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
        bot.send_message(message.chat.id, f"CRWO00000{str(int(crwo) + crwo_delta)} / {bs_name}\n"
                                          f"Адрес: {address}\n"
                                          f"Координаты: {coordinates}\n"
                                          f"Тип работ: {ustk_job_type}\n"
                                          f"Описание работ: {job_description}\n"
                                          f"Дата/время выдачи задания: {current_time}\n"
                                          f"Время прибытия: {time_to_arrive}\n"
                                          f"Подрядная организация :{PO}:\n"
                                          f"Ответственный ММ : {message.from_user.last_name}\n"
                         )
        crwo_delta += 1
        with open(f"data/logs/{current_log_time}.txt", "a") as file:
            file.write(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")
        print(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")

def multi_process_job_list(message):
    global job_description_list
    global job_type
    job_description_list = []
    with open(f"data/jd/job_description.txt", "r",encoding="utf-8") as file:
        for jd in file:
            job_description_list.append(jd.rstrip("\n"))
    if message.text in job_list:
        job_type = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        own_jd = types.KeyboardButton("Свой текст задания")
        markup.add(own_jd)
        for job_des in sorted(job_description_list):
            markup.add(job_des)
        bot.send_message(message.chat.id, "Выбери описание работ", reply_markup=markup)
        # bot.register_next_step_handler(message,get_job_description)
        # job_description = message.text
        print("задача ", message.text)
        bot.register_next_step_handler(message, multi_choose_worker)

def multi_choose_worker(message):
    global job_description_list
    global job_description
    if message.text == "Свой текст задания":
        if message.text == "Свой текст задания":
            bot.send_message(message.chat.id, "Введи текст задания :   ")
            bot.register_next_step_handler(message, make_own_multi)

    elif message.text in job_description_list:
        workers_list = []
        with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
            for employee in file:
                workers_list.append(employee.rstrip("\n"))

        global job_description
        job_description = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        worker_counter = 1
        for worker in sorted(workers_list):
            j = types.KeyboardButton(worker)
            markup.add(j)
            worker_counter += 1
        bot.send_message(message.chat.id, "Выбери инженера", reply_markup=markup)
        bot.register_next_step_handler(message, multi_get_partner)

def make_own_multi(message):
    global job_description
    job_description = message.text
    workers_list = []
    with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
        for employee in file:
            workers_list.append(employee.rstrip("\n"))
    job_description = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker_counter = 1
    for worker in sorted(workers_list):
        j = types.KeyboardButton(worker)
        markup.add(j)
        worker_counter += 1
    bot.send_message(message.chat.id, "Выбери инженера", reply_markup=markup)
    bot.register_next_step_handler(message, multi_get_partner)

def multi_get_partner(message):
    workers_list = []
    with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
        for employee in file:
            workers_list.append(employee.rstrip("\n"))

    global partner1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker_counter = 1
    for worker in sorted(workers_list):
        j = types.KeyboardButton(worker)
        markup.add(j)
        worker_counter += 1
    bot.send_message(message.chat.id, "Первый инженер выбран, теперь выбери второго", reply_markup=markup)
    partner1 = message.text
    bot.register_next_step_handler(message, multi_get_another_partner)
    print(partner1)

def multi_get_another_partner(message):
    bot.send_message(message.chat.id,
                     "Отлично, команда готова! ")
    global partner2
    partner2 = message.text
    print(partner2)
    bot.send_message(message.chat.id, "Введи номер CRWO")
    bot.register_next_step_handler(message, multi_input_crwo)

def multi_input_crwo(message):
    global crwo
    global multi_bs_list
    global multi_coordinates_list
    global multi_address_list
    global job_type
    global crwo_delta
    print("multibslist",multi_bs_list)

    current_log_time = datetime.now().strftime('%d.%m.%Y')
    crwo = message.text
    print("CRWO000000", crwo)
    crwo_delta = 0

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    single_wo = types.KeyboardButton("Единой заявкой")
    multi_wo = types.KeyboardButton("Раздельными заявками")
    markup.add(single_wo, multi_wo)
    bot.send_message(message.chat.id, "Выбери стиль подачи", reply_markup=markup)
    bot.register_next_step_handler(message, multi_choose_style)

def multi_choose_style(message):
    crwo_delta = 0
    global crwo
    global multi_bs_list
    print("multibslist=",multi_bs_list)
    current_log_time = datetime.now().strftime('%d.%m.%Y')

    if message.text == "Раздельными заявками":
        for i in range(len(multi_bs_list)):
            bs_name = multi_bs_list[i]
            coordinates = multi_coordinates_list[i]
            address = multi_address_list[i]
            current_time = (datetime.now() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
            time_to_arrive = ((datetime.now() + timedelta(hours=2)) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
            bot.send_message(message.chat.id, f"CRWO00000{str(int(crwo) + crwo_delta)} / {bs_name}\n"
                                              f"Адрес: {address}\n"
                                              f"Координаты: {coordinates}\n"
                                              f"Тип работ: {job_type}\n"
                                              f"Описание работ: {job_description}\n"
                                              f"Дата/время выдачи задания: {current_time}\n"
                                              f"Время прибытия: {time_to_arrive}\n"
                                              f"Ответственный ММ : {partner1},{partner2}")
            crwo_delta += 1

        with open(f"data/logs/{current_log_time}.txt", "a") as file:
            file.write(
                f"{message.from_user.last_name} создавал заявку на БС {','.join(multi_bs_list)} в {datetime.now().strftime('%H:%M')}\n")
        print(
            f"{message.from_user.last_name} создавал заявку на БС {','.join(multi_bs_list)} в {datetime.now().strftime('%H:%M')}, информация занесена в {current_log_time}.txt")

    elif message.text == "Единой заявкой":
        bs_name = ", ".join(multi_bs_list)
        # coordinates = ",".join(multi_coordinates_list)
        # address = multi_address_list[i]
        current_time = (datetime.now() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
        time_to_arrive = ((datetime.now() + timedelta(hours=2)) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
        bot.send_message(message.chat.id, f"CRWO00000{str(int(crwo) + crwo_delta)} / {bs_name}\n"
        # f"Адрес: {address}\n"
        # f"Координаты: {coordinates}\n"
                                          f"Тип работ: {job_type}\n"
                                          f"Описание работ: {job_description}\n"
                                          f"Дата/время выдачи задания: {current_time}\n"
                                          f"Время прибытия: {time_to_arrive}\n"
                                          f"Ответственный ММ : {partner1},{partner2}")

        with open(f"data/logs/{current_log_time}.txt", "a") as file:
            file.write(
                f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")
        print(
            f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}, информация занесена в {current_log_time}.txt")


def process_miranda(message):
    global job_list
    if message.text == f"{MM}":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for job in job_list:
            markup.add(job)
        bot.send_message(message.chat.id, "Выбери тип работ", reply_markup=markup)
        bot.register_next_step_handler(message, process_job_list)
    elif message.text == f"{PO}":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # back = types.KeyboardButton("<НАЗАД")
        # markup.add(back)
        for job in ustk_job_list:
            markup.add(job)
        bot.send_message(message.chat.id, "Выбери тип задач подрядчику", reply_markup=markup)
        bot.register_next_step_handler(message, process_ustk_job_list)

def process_job_list(message):
    global job_description_list
    global job_type
    job_description_list = []
    with open(f"data/jd/job_description.txt", "r",encoding="utf-8") as file:
        for jd in file:
            job_description_list.append(jd.rstrip("\n"))

    if message.text in job_list:
        job_type = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        own_jd = types.KeyboardButton("Свой текст задания")
        markup.add(own_jd)
        for job_des in sorted(job_description_list):
            markup.add(job_des)
        bot.send_message(message.chat.id, "Выбери описание работ", reply_markup=markup)
        # bot.register_next_step_handler(message,get_job_description)
        # job_description = message.text
        print("задача ", message.text)
        bot.register_next_step_handler(message, choose_worker)


def choose_worker(message):
    global job_description_list
    global job_description
    if message.text == "Свой текст задания":
        bot.send_message(message.chat.id, "Введи текст задания :   ")
        bot.register_next_step_handler(message, make_own)

    elif message.text in job_description_list:
        workers_list = []
        with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
            for employee in file:
                workers_list.append(employee.rstrip("\n"))
        job_description = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        worker_counter = 1
        for worker in sorted(workers_list):
            j = types.KeyboardButton(worker)
            markup.add(j)
            worker_counter += 1
        bot.send_message(message.chat.id, "Выбери инженера", reply_markup=markup)
        bot.register_next_step_handler(message, get_partner)

def make_own(message):
    global job_description
    job_description = message.text
    workers_list = []
    with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
        for employee in file:
            workers_list.append(employee.rstrip("\n"))
    job_description = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker_counter = 1
    for worker in sorted(workers_list):
        j = types.KeyboardButton(worker)
        markup.add(j)
        worker_counter += 1
    bot.send_message(message.chat.id, "Выбери инженера", reply_markup=markup)
    bot.register_next_step_handler(message, get_partner)


def get_partner(message):
    workers_list = []
    with open(f"data/workers/workers.txt", "r",encoding="utf-8") as file:
        for employee in file:
            workers_list.append(employee.rstrip("\n"))

    global partner1
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    worker_counter = 1
    for worker in sorted(workers_list):
        j = types.KeyboardButton(worker)
        markup.add(j)
        worker_counter += 1
    bot.send_message(message.chat.id, "Первый инженер выбран, теперь выбери второго", reply_markup=markup)
    partner1 = message.text
    bot.register_next_step_handler(message, get_another_partner)
    print(partner1)


def process_ustk_job_list(message):
    ustk_job_description_list = []
    with open(f"data/jd/ustk_job_description.txt", "r",encoding="utf-8") as file:
        for jd in file:
            ustk_job_description_list.append(jd.rstrip("\n"))
    global ustk_job_type
    global ustk_job_description
    if message.text in job_list:
        ustk_job_type = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        own_jd = types.KeyboardButton("Свой текст задания")
        markup.add(own_jd)
        for job_des in sorted(ustk_job_description_list):
            markup.add(job_des)
        bot.send_message(message.chat.id, "Выбери описание работ", reply_markup=markup)
        bot.register_next_step_handler(message, get_ustk_job_description)


def get_ustk_job_description(message):
    global job_description_list
    global job_description
    # if message.text in job_description_list:
    if message.text == "Свой текст задания":
        bot.send_message(message.chat.id, "Введи текст задания :   ")
        bot.register_next_step_handler(message, make_own_jdu)
    else:
        job_description = message.text
        print("point 1", message.text)
        bot.send_message(message.chat.id, "Введи номер CRWO :")
        bot.register_next_step_handler(message, get_ustk_crwo)

def make_own_jdu(message):
    global job_description
    job_description = message.text
    bot.send_message(message.chat.id, "Введи номер CRWO :")
    bot.register_next_step_handler(message, get_ustk_crwo)



def get_ustk_crwo(message):
    global crwo
    current_log_time = datetime.now().strftime('%d.%m.%Y')
    crwo = message.text
    # bot.send_message(message.chat.id, f"CRWO000000{crwo}")
    print("CRWO000000", crwo)
    global job_type
    current_time = (datetime.now() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
    time_to_arrive = ((datetime.now() + timedelta(hours=2)) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
    bot.send_message(message.chat.id, f"CRWO00000{crwo} / {bs_name}\n"
                                      f"Адрес: {RDB[bs_name]['address']}\n"
                                      f"Координаты:{RDB[bs_name]['coordinates']}\n"
                                      f"Тип работ: {ustk_job_type}\n"
                                      f"Описание работ: {job_description}\n"
                                      f"Дата/время выдачи задания: {current_time}\n"
                                      f"Время прибытия: {time_to_arrive}\n"
                                      f"Подрядная организация :{PO}\n"
                                      f"Ответственный ММ : {message.from_user.last_name}\n"
                     )
    with open(f"data/logs/{current_log_time}.txt", "a") as file:
        file.write(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")
    print(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")




def get_another_partner(message):
    bot.send_message(message.chat.id,
                     "Отлично, команда готова! ")
    global partner2
    partner2 = message.text
    print(partner2)
    bot.send_message(message.chat.id, "Введи номер  CRWO и заявка сформируется самостоятельно.")
    bot.register_next_step_handler(message, input_crwo)


def input_crwo(message):
    current_log_time = datetime.now().strftime('%d.%m.%Y')
    global crwo
    crwo = message.text
    bot.send_message(message.chat.id, f"CRWO000000{crwo}")
    print("CRWO000000", crwo)
    global job_type
    current_time = (datetime.now() + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
    time_to_arrive = ((datetime.now() + timedelta(hours=2)) + timedelta(hours=3)).strftime('%d.%m.%Y %H:%M')
    bot.send_message(message.chat.id, f"CRWO00000{crwo} / {bs_name}\n"
                                      f"Адрес: {RDB[bs_name]['address']}\n"
                                      f"Координаты: {RDB[bs_name]['coordinates']}\n"
                                      f"Тип работ: {job_type}\n"
                                      f"Описание работ: {job_description}\n"
                                      f"Дата/время выдачи задания: {current_time}\n"
                                      f"Дата/время прибытия: {time_to_arrive}\n"
                                      f"Ответственный ММ : {partner1},{partner2}"
                     )

    with open(f"data/logs/{current_log_time}.txt", "a") as file:
        file.write(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")
    print(f"{message.from_user.last_name} создавал заявку на БС {bs_name} в {datetime.now().strftime('%H:%M')}\n")




try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    # bot.polling(none_stop=True)
except Exception as ex:
    print(ex)
    time.sleep(15)
# bot.infinity_polling
