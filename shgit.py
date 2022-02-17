#! /usr/bin/env python
# -*- coding:utf8 -*-

import time
from git import Repo

# project_path = '/Users/lcy/Documents/mobile-android'
project_path = '/Users/lcy/Documents/code/CodeUtils'
author = 'boredream'

repo = Repo(project_path)
git = repo.git


def has_commit_today():
    # 判断自己今天是否已提交
    log = git.log('-1', '--author=' + author)
    date_str = log.split('\n')[2]\
        .replace('Date:', '')\
        .replace('+0800', '')\
        .strip()
    date = time.strptime(date_str)
    now = time.localtime()
    return time.strftime('%Y %m %d', date) == time.strftime('%Y %m %d', now)


def get_un_commit_files():
    # 罗列所有未提交文件
    diff = git.diff_files()
    lines = diff.split('\n')
    if len(lines) == 0:
        print("内容都提交完了")
        return

    lines = list(map(lambda x: x.split('\t')[-1], lines))
    return lines


def add_and_commit(files, comment):
    # add and commit
    for file in files:
        git.add(file)
    git.commit('-m', 'feat: ' + comment)


if __name__ == '__main__':
    # 先判断今天是否已经提交过了
    if has_commit_today():
        print('今日已提交')
    else:
        files = get_un_commit_files()
        # 每次修改一个文件
        files = files[0:1]
        add_and_commit(files, "优化代码")
