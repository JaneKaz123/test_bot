import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from tokenp import token
bot=telebot.TeleBot(token) 

points = 0

incorrect_respose = 'Неправильный ответ'
correct_respose = 'Правильный ответ'

kviz_data = [ 
    {
        "question": "Как называется тип данных для хранения целых чисел в Python?",
        "options": ["int", "float", "str"],
        "correct": "int"
    },
    {
        "question": "Какая функция используется для вывода текста в Python?",
        "options": ["print()", "input()", "def()"],
        "correct": "print()"
    },
    {
        "question": "Каким символом обозначаются комментарии в Python?",
        "options": ["//", "#", "--"],
        "correct": "#"
    },
    {
        "question": "Какой метод используется для добавления элемента в список в Python?",
        "options": ["append()", "insert()", "add()"],
        "correct": "append()"
    }
]



current_question = 0

@bot.message_handler(commands=['start'])
def start(message):
    global points, current_question
    points = 0 
    current_question = 0   
    
    keyboard = InlineKeyboardMarkup() 
    buttonstart = InlineKeyboardButton(text= 'Начать (Start)', callback_data='start_kviz')

    keyboard.add(buttonstart)

    bot.send_message(message.chat.id, 'Привет, это я бот-викторина. Нажмите на кнопку "Начать", чтобы начать викторину!', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:call.data == 'start_kviz')
def start_kviz(call):
    global points, current_question
    points = 0 
    current_question = 0
    ask_question(call.message)

def ask_question(message):
    global current_question
    if current_question < len(kviz_data):
        kviz_question = kviz_data[current_question]['question']
        options = kviz_data[current_question]['options']

        keyboard = InlineKeyboardMarkup()
        for option in options:
            keyboard.add(InlineKeyboardButton(option, callback_data=option))
        
        bot.send_message(message.chat.id, kviz_question, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f'Викторина окончена, у вас {points} правильных ответов из {len(kviz_data)}')
        current_question = 0

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text in [opt for q in kviz_data for opt in q['options']]:
        check_answer(message)


@bot.callback_query_handler(func=lambda call: call.data in [opt for q in kviz_data for opt in q['options']])
def check_answer(call):
    global current_question, points
    correct_answer = kviz_data[current_question]['correct']
    if call.data == correct_answer:
        points += 1
        bot.answer_callback_query(call.id, text=correct_respose)
    else:
        bot.answer_callback_query(call.id, text=incorrect_respose + f'Правильный ответ: {correct_answer}')
    
    current_question += 1
    ask_question(call.message)

bot.polling(non_stop=True)