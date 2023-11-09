# coding:utf-8

import sys

# https://ankiuser.net/

try:
    # 翻译目标=翻译结果
    query = sys.argv[1]
except IndexError:
    query = ''


def save(src_and_dst):
    with open('data/anki.txt', 'a') as file:
        file.write(src_and_dst.replace('=', '|') + '\n')


if 'ANKI-' in query:
    query = query[5:]
    save(query)

sys.stdout.write(query)
