import datetime
import random
import sys
import time
import os

import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz
from playsound import playsound

# описываем название ассистента, команды, какие слова игнорировать
opts = {
    "alias": ('маруся'),
    "tbr": ('скажи', 'покажи', 'давай', 'я', 'хочу'),
    "cmds": {
        "playtime": ('поиграем', 'играть', 'тренировать слух', 'потренируем слух', 'играть', 'поиграть'),
        "stop_game": ('стоп', 'хватит', 'закончи игру', 'прекрати', 'закончить игру')

    }
}


# функции
def speak(text):
    speak_engine = pyttsx3.init()
    print(text)
    speak_engine.say(text)
    speak_engine.runAndWait()
    speak_engine.stop()


# будет вызывать каждый раз, когда будет записана фраза
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        # если обращение начинается с имени помощника, то вырезаем лишние слова
        if voice.startswith(opts["alias"]):
            # обращаются к Кеше
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


# занимается нечетким поиском команд (сравнивает со всеми возможными фразами из cmds
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            # оставляем в результате самую подходящую комнаду
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


# преобразовывает комнаду в какое-то действие
def execute_cmd(cmd):
    if cmd == 'playtime':
        # начать игру
        speak("Хорошо, запускаю игру\n" +
              "Я буду воспроизводить ноты, а ты будешь их угадывать.\n" +
              "Для ответа назови номер")
        game_process()

    elif cmd == 'stop_game':
        sys.exit()
    else:
        print('Команда не распознана, повторите!')


notes = {'ля': "A.wav", 'си': "B.wav", 'си♭': "Bb.wav", 'до': "a3.wav", 'ре': "D.wav", 'ми': "E.wav",
         'фа': "F.wav",
         'соль': "G.wav"}


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def game_process():
    # количество заданных вопросов
    questions_count = 0
    # количество правильных ответов
    right_answers_count = 0
    speak('Перед началом прослушай ноты')
    for key, value in notes.items():
        speak('Нота ' + str(key))
        playsound(value)

    while True:
        # +1 вопрос
        questions_count = questions_count + 1
        # выбираем 4 рандомных звука
        note = random.sample(notes.items(), 4)
        all_4_notes = {}
        for i in range(len(note)):
            all_4_notes[note[i][0]] = note[i][1]
        # рандомно выбираем звук для озвучивания
        chosen_note, path = random.choice(list(all_4_notes.items()))
        # перемешиваем список
        keys = list(all_4_notes.keys())
        random.shuffle(keys)

        # выводим варианты ответа
        speak('Назовите ответ')
        for i in range(len(all_4_notes)):
            print(str(i + 1) + ") " + keys[i] + "\n")
        # проигрываем звук
        playsound(path, block=False)
        # находим индекс выбранного звука для сравнения ответа
        index = [idx for idx, key in enumerate(keys) if key == chosen_note]

        # ответ игрока
        answer = input().rstrip()
        if is_integer(answer):
            # если ответ верен
            if int(answer) - 1 == index[0]:
                speak('Правильно!')
                right_answers_count = right_answers_count + 1
                # если ответ  не верен
            else:
                speak('Неправильно!')
                speak('Это была нота ' + str(chosen_note))

        # если ввдено слово
        else:
            if answer == 'стоп':
                speak('Игра закончена')
                speak('Вы ответили правильно на ' + str(right_answers_count) + ' из ' + str(
                    questions_count) + ' вопросов')
                os._exit(0)
            else:
                speak('Команда не ясна')


r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    # оду секунду слушает фон, чтобы потом не путать шум с речью
    r.adjust_for_ambient_noise(source)

speak("Привет")
now = datetime.datetime.now()
if 6 <= now.hour < 12:
    speak("Какое прекрасное утро!")
elif 12 <= now.hour < 18:
    speak("Какой прекрасный день!")
elif 18 <= now.hour < 23:
    speak("какой прекрасный вечер!")
else:
    speak("Какая прекрасная ночь")
speak("Что ты хочешь?")

stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)
