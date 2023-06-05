# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import logging
from collections import defaultdict
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
import numpy as np
from collections import defaultdict

TOKEN = '5895436877:AAGZ47lMgPFuM0wi0j4m-K0I9AMeomUHW40'


def get_cut(graph, r):
    G = dict()
    for i in graph.keys():
        G[i] = graph[i].copy()
    while len(G) != 2:

        n = len(G)

        np.random.seed(r)

        # print(G, d)

        a = np.random.choice(list(G.keys()), 1)[0]

        # print('a= ', a)

        b = np.random.choice(G[a], 1)[0]
        # print('b= ',b)

        k = max(G.keys())

        while b in G[a]:
            G[a].remove(b)

        while a in G[b]:
            G[b].remove(a)

        G[k + 1] = G[a] + G[b]
        for i in G[a]:
            G[i].remove(a)
            G[i].append(k + 1)
        for i in G[b]:
            G[i].remove(b)
            G[i].append(k + 1)

        G.pop(a)
        G.pop(b)
        # print(G)
    return len(G[list(G.keys())[0]])

def min_cut(G):
    answer = np.inf
    n = len(G)
    for i in range(int(n**2*np.log(n))):
        cur_cut = get_cut(G, i)
        if cur_cut < answer:
            answer = cur_cut
        #print(curCut, answer)
    return answer

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

class reg():
    def __init__(self):
        self.v = 0
        self.p = 0
        self.c = defaultdict(list)
        self.k = 0
        self.mc = -1
a = reg()

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if a.mc != -1:
        a.v = 0
        a.p = 0
        a.c = defaultdict(list)
        a.k = 0
        a.mc = -1
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    await message.reply(f"Здравствуйте, {user_full_name}!")
    await bot.send_message(user_id, f"Введите количество вершин!")


    #v = message
    #user_id = message.from_user.id
    #await message.reply(f"Вершина, {v.text}!")



@dp.message_handler(lambda x: len(x.text.split())==1)
async def get_v(message):
    user_id = message.from_user.id
    #await bot.send_message(user_id, f"Количество вершин! {len(message.text)}")
    if a.v == 0:
        a.v = int(message.text)
        await bot.send_message(user_id, f"Введите количество ребер!")
    else:
        a.p = int(message.text)
        await bot.send_message(user_id, f"Введите ребро (вершины через пробел)")
    #await bot.send_message(user_id, f"Количество вершин! {a.v}")



@dp.message_handler(lambda x: len(x.text.split())==2)
async def get_c(message):
    user_id = message.from_user.id
    #await bot.send_message(user_id, f"Количестsdfво вершин! {a.k, a.p, a.c}")

    t = [int(i) for i in message.text.split()]
    #await bot.send_message(user_id, f"Количестsdfво вершин! {t, len(t), t[1]}")
    if a.k < a.p-1:
        a.c[t[0]].append(t[1])
        a.c[t[1]].append(t[0])
        await bot.send_message(user_id, f"Введите ребро (вершины через пробел)")
        a.k += 1
    else:
        a.c[t[0]].append(t[1])
        a.c[t[1]].append(t[0])
        min_cut(a.c)
        a.mc=min_cut(a.c)
        await bot.send_message(user_id, f"Полученный минимальный разрез {a.mc}")
        await bot.send_message(user_id, "Для повторного подсчета используйте /start")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
