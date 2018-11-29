#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Main module of Lectures Serzor.
    Author: Holy Chen
    Create Time: 2017-12-13
    Last Update Time: 2017-12-28
    License: GPL v3
"""

import urllib.request
import urllib.parse
import http.cookiejar
import datetime
import time
import sys

from bs4 import BeautifulSoup
from colorama import Fore

import model.lecture as lecture

_REQUEST_NAME = {
    'view_state': '__VIEWSTATE',
    'view_state_generator': '__VIEWSTATEGENERATOR',
    'event_validation': '__EVENTVALIDATION',
    'event_target': '__EVENTTARGET',
    'event_argument': '__EVENTARGUMENT',
    'sumbit': 'sumbit',
}

_DEFAULT_HEAD = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/70.0.3538.77 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
}

_PAGE_NAME = {
    'default': r'Default.aspx',
    'login': r'Default.aspx',
    'lectures': r'admin_bookChair.aspx',
}

_COOKIE_FILE = 'cookie.txt'

_SERVER_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

_LOG_TIME_FORMAT = '[%Y-%m-%d %H:%M:%S] '

class LecturesSeizor:
    """Auto seize lectures held by School of Information and Engineering.

    The class encapsulate serveral method to login the system and select lecture.
    """

    def __init__(self, url_base, username, password, encoding='gb2312', cookie_file=_COOKIE_FILE):
        """Assign initial arguments

        Arguments:
            url_base {str} -- Management System of Information and Engineering, Xiamen University.
                            For example, http://example.xmu.edu.cn/
            username {str} -- Your student Id to log that system.
            password {str} -- Password w.r.t the username.
            encoding {str} -- encoding of the website, gb2312 default.
            cookie_file {str} -- cookie file, 'cookie.txt' default
        """
        self.url_base = url_base
        if not url_base.endswith('/'):
            self.url_base += '/'
        self.encoding = encoding
        self.username = username
        self.password = password
        self.cookie_file = cookie_file
        self.opener = self._get_opener()

        self.lectures = []

        self.view_state = ''
        self.view_state_generator = ''
        self.event_validation = ''
        self.num_of_gotten = 0
        self.num_of_seizable = 0
        self.num_of_not_begin = 0
        self.time_diff = datetime.timedelta(0)
        self.last_log_time = datetime.datetime(1970, 1, 1, 0, 0)

    def _get_opener(self, head=None):
        self.cookie = http.cookiejar.MozillaCookieJar(self.cookie_file)
        try:
            self.cookie.load(self.cookie_file)
        except FileNotFoundError:
            self.cookie.save()
        except:
            print(Fore.RED + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
                  'Unexpected error: ', sys.exc_info()[0])
            raise
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        head = head if head is not None else _DEFAULT_HEAD
        header = [(k, v) for k, v in head.items()]
        opener.addheaders = header
        return opener

    @staticmethod
    def _get_value(input_element):
        return '' if input_element is None else input_element['value']

    def _login(self):
        login_data = ''

        login_url = self.url_base
        with self.opener.open(urllib.request.Request(login_url)) as response:

            self._time_match(response.getheader('Date'))

            soup = BeautifulSoup(response.read(), "lxml", from_encoding=self.encoding)
            request_data = {id_name: self._get_value(soup.find('input', attrs={'id': id_name})) \
                for _, id_name in _REQUEST_NAME.items()}
            self.view_state = self._get_value(soup.find(
                'input', attrs={'id': _REQUEST_NAME['view_state']}))
            self.view_state_generator = self._get_value(soup.find(
                'input', attrs={'id': _REQUEST_NAME['view_state_generator']}))
            self.event_validation = self._get_value(soup.find(
                'input', attrs={'id': _REQUEST_NAME['event_validation']}))
            request_data['userName'] = self.username
            request_data['passWord'] = self.password
            request_data['userType'] = 1

            login_data = urllib.parse.urlencode(request_data)

            self.cookie.save(self.cookie_file)

        login_url = self.url_base + _PAGE_NAME['login']

        try:
            with self.opener.open(urllib.request.Request(
                login_url, login_data.encode(self.encoding), method='POST')) as response:
                self.cookie.save()
            last_log_time = datetime.datetime.now()
        except Exception as Exception:
            raise Exception

    def _list_lecturs(self):

        lectures_url = self.url_base + _PAGE_NAME['lectures']

        with self.opener.open(urllib.request.Request(lectures_url)) as response:
            self._parse_lecture_list(response.read())

    def _parse_lecture_list(self, doc):
        self.num_of_gotten = 0
        self.num_of_seizable = 0
        self.num_of_not_begin = 0

        soup = BeautifulSoup(doc, "lxml", from_encoding=self.encoding)
        lectures = []
        all_td = soup.find_all('td')
        if len(all_td) >= 10: # there're some lectures now
            all_td = all_td[4:]
            base = 0
            while base < len(all_td):
                a_lecture_td = all_td[base : base + 20]
                lecture_para = [(a_lecture_td[1].contents[0]['id'].strip(),
                                 a_lecture_td[1].contents[0]['value'].strip()),
                                a_lecture_td[3].string.strip(),
                                a_lecture_td[5].string.strip(),
                                a_lecture_td[7].string.strip(),
                                a_lecture_td[9].string.strip(),
                                a_lecture_td[11].string.strip(),
                                a_lecture_td[13].string.strip(),
                                a_lecture_td[15].string.strip(),
                                a_lecture_td[17].string.strip()]
                status_string = a_lecture_td[18].string \
                    if a_lecture_td[18].string is not None \
                    else a_lecture_td[18].contents[0]['value']
                if status_string.find('时间还没到') != -1:
                    lecture_para.append(lecture.STATUS['waiting'])
                    self.num_of_not_begin += 1
                elif status_string.find('总人数已满') != -1:
                    lecture_para.append(lecture.STATUS['fullfilled'])
                elif status_string.find('预约该讲座') != -1:
                    lecture_para.append(lecture.STATUS['seizable'])
                    # submit input, have ctl
                    lecture_para.append(a_lecture_td[18].contents[0]['name'].strip())
                    self.num_of_seizable += 1
                elif status_string.find('取消预约') != -1:
                    lecture_para.append(lecture.STATUS['gotten'])
                    lecture_para.append(a_lecture_td[18].contents[0]['name'].strip())
                    self.num_of_gotten += 1
                    base += 1
                elif status_string.find('时间已截止') != -1:
                    lecture_para.append(lecture.STATUS['fullfilled'])
                base += 20
                lectures.append(lecture.Lecture(*lecture_para))

        self.lectures = lectures

        self.view_state = self._get_value(soup.find(
            'input', attrs={'id': _REQUEST_NAME['view_state']}))
        self.view_state_generator = self._get_value(soup.find(
            'input', attrs={'id': _REQUEST_NAME['view_state_generator']}))
        self.event_validation = self._get_value(soup.find(
            'input', attrs={'id': _REQUEST_NAME['event_validation']}))

    def _seize_one(self, chair_id=None):
        seize_url = self.url_base + _PAGE_NAME['lectures']
        if self.num_of_seizable > 0:

            request_data = {lec.chair_id[0]: lec.chair_id[1] for lec in self.lectures}

            for lec in self.lectures:
                if lec.status == lecture.STATUS['seizable'] and \
                        (chair_id is None or lec.chair_id == chair_id):
                    request_data[_REQUEST_NAME['view_state']] = self.view_state
                    request_data[_REQUEST_NAME['view_state_generator']] = self.view_state_generator
                    request_data[_REQUEST_NAME['event_validation']] = self.event_validation
                    request_data[lec.ctl] = '预约该讲座'

                    data = urllib.parse.urlencode(request_data)

                    seize_this_url = seize_url
                    old_num_of_gotten = self.num_of_gotten
                    with self.opener.open(urllib.request.Request(
                        seize_this_url, data=data.encode(self.encoding), method="POST")):
                        pass
                    self._list_lecturs()
                    if self.num_of_gotten > old_num_of_gotten:
                        print(Fore.GREEN + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
                              "Seize lecture SUCCESS!\nId: {}\nName: {}".format(
                                  lec.chair_id, lec.title))
                    else:
                        print(Fore.YELLOW + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
                              "Seize lecture FAILED!\nId: {}\nName: {}".format(
                                  lec.chair_id, lec.title))
                    break
        else:
            print(Fore.WHITE + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
                  "No seizable lecture.")

    def _time_match(self, server_time):
        self.time_diff = (datetime.datetime.strptime(server_time, _SERVER_TIME_FORMAT) \
                                                     - datetime.datetime.utcnow())
        print(Fore.WHITE + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
              "Time Synchronization, server " + str(self.time_diff) + " faster.")

    def _wait(self):
        min_delta = datetime.timedelta(hours=1)
        if self.num_of_not_begin > 0:
            for lec in self.lectures:
                if lec.status == lecture.STATUS['waiting']:
                    min_delta = min(min_delta, lec.seize_begin_time - datetime.datetime.now())

        min_delta += self.time_diff - datetime.timedelta(seconds=5)
        if min_delta < datetime.timedelta(seconds=5):
            min_delta = min(min_delta, datetime.timedelta(seconds=2))
        elif min_delta < datetime.timedelta(seconds=10):
            min_delta = datetime.timedelta(seconds=5)

        print(Fore.CYAN + 'wait for ' + str(min_delta) + '.')
        time.sleep(min_delta.total_seconds())

    def start(self):
        """Start auto seize.

        If there are some lecture seizable, then seize them immediately, else wait for
        at most two hours and refresh.
        """
        while True:    
            try:
                if datetime.datetime.now() - self.last_log_time > datetime.timedelta(minutes=5):
                    self._login()
                self._list_lecturs()
                print(Fore.WHITE + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) + "Lectures:")
                print('\n'.join(str(lec) for lec in self.lectures))
                if self.num_of_seizable > 0:
                    self._seize_one()
                    time.sleep(datetime.timedelta(seconds=2).total_seconds())
                else:
                    print(Fore.CYAN + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) +
                          'No lecture seizable, ', end='')
                    self._wait()
            except Exception as exception:
                print(Fore.RED + datetime.datetime.now().strftime(_LOG_TIME_FORMAT) + "Fatal error: " + 
                              str(exception))
