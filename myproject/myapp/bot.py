
import telebot
import psycopg2
from psycopg2 import Error
import requests
import traceback

bot = telebot.TeleBot('6067492832:AAHQS3M04prSw6gOmyaGnV6qJineUw6JZ0s')

code_to_smile = {
"Clear": "Ясно \U00002600",
"Clouds": "Облачно \U00002601",
"Rain": "Дождь \U00002614",
"Drizzle": "Дождь \U00002614",
"Thunderstorm": "Гроза \U000026A1",
"Snow": "Снег \U0001F328",
"Mist": "Туман \U0001F32B"
}


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.from_user.id,"Напиши команду" )

@bot.message_handler(commands = ["weather"])
def weather_command(message):
    bot.send_message(message.from_user.id,"Введите название города" )
    bot.register_next_step_handler(message, get_weather)
@bot.message_handler(commands = ["plan"])
def plan_command(message):
    bot.send_message(message.from_user.id,"Напиши свой план мне, а я его сохраню!" )
    return (message,bot.register_next_step_handler(message, write_plan))
    

@bot.message_handler(commands = ["delplan"])
def delplan_command(message):

    try:
        conn = psycopg2.connect(user="postgres",
                                  password="weravboga",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")
        
        
        curs = conn.cursor()
        
    # выполняем SQL запрос
        
        curs.execute("""DELETE FROM myapp_plan""")
        conn.commit()
        bot.send_message(message.from_user.id,f"План успешно удален")
    except Exception as ex:
        err = str(traceback.format_exc())[-3000:-1]        
        bot.send_message(message.from_user.id,f'{err}' )
    finally:
        if conn:
            curs.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

    


def write_plan(message):
    name=message.from_user.full_name
    username = message.from_user.username if message.from_user.username else None
    global  plan
    plan= message.text
    print(plan)
    bot.send_message(message.from_user.id,f"{plan} ")
    try:
        conn = psycopg2.connect(user="postgres",
                                  password="weravboga",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="postgres")

        
        curs = conn.cursor()

       # формируем SQL запрос на вставку данных
        insert_query = f"""
            INSERT INTO myapp_plan (username, tools)
            VALUES ( '{username}','{plan}' );
            """

    # выполняем SQL запрос
        curs.execute(insert_query)
        conn.commit()
        curs.execute(f""" SELECT tools  FROM myapp_plan WHERE  username like '{username}' """)
        bot.send_message(message.from_user.id,f"Результат:,{curs.fetchall()} ")
    except Exception as ex:
        err = str(traceback.format_exc())[-3000:-1]        
        bot.send_message(message.from_user.id,f'{err}' )
    finally:
        if conn:
            curs.close()
            conn.close()
            print("Соединение с PostgreSQL закрыто")

def get_weather(message):
    city = message.text
    try:
        response = requests.get(
f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=325ce0c15d03ab86280856e221b9bb19"
)
        data = response.json()
        cur_temp = data["main"]["temp"]
        feel = data["main"]["feels_like"]
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
	        wd = code_to_smile[weather_description]
        else:
            wd = "Не понимаю какая там погода, посмотри в окошко :)"
        

        bot.send_message(message.from_user.id, f'В городе: {city} сейчас {cur_temp}  {wd}, ощущается как {feel}\n'
                        f'' )
        bot.send_message(message.from_user.id,"Введите название города" )
        bot.register_next_step_handler(message, get_weather)
    except Exception:
        bot.send_message(message.from_user.id,"Такого города нет") 
        bot.send_message(message.from_user.id,"Введите название города" )
        bot.register_next_step_handler(message, get_weather)
bot.polling(none_stop=True, interval=0)
