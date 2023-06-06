
from collections import defaultdict
import numpy as np
from aiogram import Bot, Dispatcher, executor, types

TOKEN = '5895436877:AAGZ47lMgPFuM0wi0j4m-K0I9AMeomUHW40'

def get_cut(graph, r):
    G = dict()
    for i in graph.keys():
        G[i] = graph[i].copy()
    while len(G) != 2:

        n = len(G)

        np.random.seed(r)

        a = np.random.choice(list(G.keys()), 1)[0]

        b = np.random.choice(G[a], 1)[0]

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


def min_cut(G, k):
    answer = np.inf
    l = len(G)
    if l< k:
        return 0
    for i in range(int(l**2*np.log(l))):
        curCut = get_cut(G, i)
        if curCut < answer:
            answer = curCut

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


@dp.message_handler(lambda x: len(x.text.split())==1)
async def get_v(message):
    user_id = message.from_user.id

    if a.v == 0:
        a.v = int(message.text)
        await bot.send_message(user_id, f"Введите количество ребер!")
    else:
        a.p = int(message.text)
        await bot.send_message(user_id, f"Введите ребро (вершины через пробел)")


@dp.message_handler(lambda x: len(x.text.split())==2)
async def get_c(message):
    user_id = message.from_user.id
    t = [int(i) for i in message.text.split()]

    if a.k < a.p-1:
        a.c[t[0]].append(t[1])
        a.c[t[1]].append(t[0])
        await bot.send_message(user_id, f"Введите ребро (вершины через пробел)")
        a.k += 1
    else:
        a.c[t[0]].append(t[1])
        a.c[t[1]].append(t[0])

        a.mc=min_cut(a.c, a.v)
        await bot.send_message(user_id, f"Полученный минимальный разрез {a.mc}")
        await bot.send_message(user_id, "Для повторного подсчета используйте /start")


if __name__ == '__main__':
    executor.start_polling(dp)


