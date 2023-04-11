# coding:utf-8
import json

import browser_cookie3
from sfa_user import user_id_name_map

dict = browser_cookie3.chrome(domain_name='shinho.net.cn')

cookie = ''
for item in dict:
    cookie += (item.name + "=" + item.value + ";")

import ssl
import urllib.request
import os
import sys
import collections
from lxml import etree

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

ssl._create_default_https_context = ssl._create_unverified_context


# 获取集合中第一个信息
def get_first(info_list):
    if len(info_list) > 0:
        return info_list[0]
    return None


# 递归获取节点下，所有匹配的标签
def get_all_sub(root, tag):
    all_sub_list = []
    queue = collections.deque()
    queue.append(root)
    while len(queue) > 0:
        element = queue.pop()
        if tag == element.tag:
            all_sub_list.append(element)
        else:
            queue.extend(element.xpath('*'))
    return all_sub_list


# confluence里的表格，转为jira需要的信息
def excel_to_jira_info(page_id):
    url = 'http://confluence.shinho.net.cn/pages/viewpage.action?pageId=%s' % page_id
    post_req = urllib.request.Request(url=url, headers={'Cookie': cookie})
    post_res_data = urllib.request.urlopen(post_req)
    content = post_res_data.read().decode('utf-8')

    html = etree.HTML(content)
    table = html.xpath('//*[@id="main-content"]/div[1]/table/tbody')[0]

    cur_story = ''
    story_subtask_map = {}
    for row in table.xpath('tr'):
        tds = row.xpath('td')
        len_tds = len(tds)
        if len_tds < 3:
            continue

        if len_tds == 5:
            # 故事
            story = get_first(tds[0].xpath('div/p/span/@data-jira-key'))
            if story and story != cur_story:
                cur_story = story

        # 子任务
        sub_task = tds[len_tds-3].xpath('string()')
        if not sub_task:
            continue
        sub_task = ''.join(sub_task)

        # 工作量
        point = get_first(tds[len_tds-2].xpath('text()'))
        if not point:
            point = '0'

        # 用户
        user_element_list = get_all_sub(tds[len_tds-1], 'a')
        for element in user_element_list:
            # 每个用户单独一个任务
            user = element.xpath("@data-username")[0]

            jira = {
                'name': sub_task,
                'point': point,
                'user': user,
            }

            if cur_story not in story_subtask_map:
                story_subtask_map[cur_story] = [jira]
            else:
                story_subtask_map[cur_story].append(jira)
    return story_subtask_map


def get_exist_sub_task_names(jira_id):
    url = 'http://jira.shinho.net.cn/rest/api/2/issue/%s' % jira_id
    request = urllib.request.Request(url, headers={
        'Cookie': cookie
    })
    content = urllib.request.urlopen(request).read().decode('utf-8')
    tasks = json.loads(content)['fields']['subtasks']
    names = []
    for task in tasks:
        names.append(task['fields']['summary'])
    return names


def create_issue(story, sub_task):
    project_id = '10301'  # SFA1
    issue_type = '10003'  # 子任务
    issue = {
        "fields": {
            "parent": {
                "key": story,
            },
            "project": {
                "id": project_id
            },
            "summary": sub_task['name'],
            "issuetype": {
                "id": issue_type
            },
            "assignee": {
                "name": sub_task['user']  # 指派人工号
            },
            "reporter": {
                "name": "18010089"  # 报告人工号
            },
            "priority": {
                "id": "3"
            },
            # "customfield_10607": start_date,  # 预计开始时间 2020-12-21
            # "customfield_10609": end_date,  # 预计结束时间 2020-12-21
            "customfield_10006": float(sub_task['point']),  # story point 1.0

        }
    }
    url = 'http://jira.shinho.net.cn/rest/api/2/issue'
    data_json = json.dumps(issue).encode(encoding='utf-8')
    post_req = urllib.request.Request(url=url,
                                      method='POST',
                                      data=data_json,
                                      headers={
                                          'content-type': 'application/json',
                                          'Cookie': cookie
                                      })
    post_res_data = urllib.request.urlopen(post_req)
    content = post_res_data.read().decode('utf-8')
    print("success create = " + sub_task['name'] + " ... response = " + content)


def update_issue_point(jira_id, story_point):
    # 先获取已有分数
    url = 'http://jira.shinho.net.cn/rest/api/2/issue/%s' % jira_id
    request = urllib.request.Request(url, headers={
        'Cookie': cookie
    })
    content = urllib.request.urlopen(request).read().decode('utf-8')
    point = json.loads(content)['fields']['customfield_10006']
    if not point:
        point = 0

    # 累加分数，只有新任务的分数会统计过来
    point += story_point
    issue = {
        "fields": {
            "customfield_10006": point,  # story point 1.0

        }
    }
    data_json = json.dumps(issue).encode(encoding='utf-8')
    post_req = urllib.request.Request(url=url,
                                      method='PUT',
                                      data=data_json,
                                      headers={
                                          'content-type': 'application/json',
                                          'Cookie': cookie
                                      })
    post_res_data = urllib.request.urlopen(post_req)
    content = post_res_data.read().decode('utf-8')
    print("success edit = " + jira_id + " ... response = " + content)


def main():
    confluence_page_id = sys.argv[1]
    # confluence_page_id = '92517447' # test
    user_points = {}
    story_subtask_map = excel_to_jira_info(confluence_page_id)
    for story, sub_task_list in story_subtask_map.items():
        # 先查询jira已有任务，防止重复添加
        exist_sub_task_names = get_exist_sub_task_names(story)

        # 子任务总分
        total_points = 0

        for sub_task in sub_task_list:
            name = sub_task['name']
            user = user_id_name_map[sub_task['user']]
            point = int(sub_task['point'])
            if user not in user_points:
                user_points[user] = point
            else:
                user_points[user] += point

            if name in exist_sub_task_names:
                print("has already create = " + name)
                continue

            try:
                create_issue(story, sub_task)
                total_points += point
            except Exception as e:
                print('[error] %s\n%s\n\n' % (name, str(e)))

        # 更新总分
        if total_points > 0:
            update_issue_point(story, total_points)
    print(user_points)


if __name__ == '__main__':
    main()

