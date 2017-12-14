#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Lecture module of Lectures Serzor.
    Contain class Lecture.

    Author: Holy Chen
    Create Time: 2017-12-14
    Last Update Time: 2017-12-14
    License: GPL v3
"""

import datetime


_TIME_FORMAT = r'%Y/%m/%d %H:%M:%S' # Year(4)/Month(2)/Day(2) Hour(2):Minute(2):Second(2)

STATUS = {
    "waiting": 0,
    "fullfilled": 1,
    "seizable": 2,
    "gotten": 3
}

_STATUS_TO_STR = {
    0: 'waiting',
    1: 'fullfilled',
    2: 'seizable',
    3: 'gotten'
}

class Lecture:
    """Lecture struct"""


    def __init__(self, chair_id, teacher, title, term, total_tickets, left_tickets,
                 seize_begin_time, lecture_begin_time, classroom, status=0, ctl=''):
        """A Lecture object represents a lecture in the system.

        Arguments:
            chair_id {tuple} -- (lecture id, value)
            teacher {str} -- teacher to give the lecture
            title {str} -- title of the lecture
            term {str} -- school term
            total_tickets {str|int} -- total number of tickets
            left_tickets {str|int} -- left number of tickets
            seize_begin_time {str} -- begin time to seize the lecture,
                                      which format should consists of TIME_FORMAT
            lecture_begin_time {str} -- begin time of the lecture,
                                        which format should consists of TIME_FORMAT
            classroom {str} -- classroom where the lecture is held
            status {int} -- status of the lecture, use dict STATUS to assign
            ctl {str} -- ctl value
        """
        self.chair_id = chair_id
        self.teacher = teacher
        self.title = title
        self.term = term
        self.total_tickets = \
            int(total_tickets.strip()) if isinstance(total_tickets, str) else total_tickets
        self.left_tickets = \
            int(left_tickets.strip()) if isinstance(left_tickets, str) else left_tickets
        self.seize_begin_time = datetime.datetime.strptime(
            seize_begin_time.strip(), _TIME_FORMAT)
        self.lecture_begin_time = datetime.datetime.strptime(
            lecture_begin_time.strip(), _TIME_FORMAT)
        self.classroom = classroom
        self.status = status
        self.ctl = ctl

    def __str__(self):
        return ("Id - Order - ctl:  {!s} - {!s} - {!s}\n" +
                "Teacher:           {!s}\n" +
                "Title:             {!s}\n" +
                "Term:              {!s}\n" +
                "Total Tickets:     {:d}\n" +
                "Left Tickes:       {:d}\n" +
                "Seize Begins at:   {:s}\n" +
                "Lecture Begins at: {:s}\n" +
                "Where:             {:s}\n" +
                "Status:            {:s}\n").format(
                    self.chair_id[0], self.chair_id[1], self.ctl,
                    self.teacher,
                    self.title,
                    self.term,
                    self.total_tickets,
                    self.left_tickets,
                    self.seize_begin_time.strftime(_TIME_FORMAT),
                    self.lecture_begin_time.strftime(_TIME_FORMAT),
                    self.classroom,
                    _STATUS_TO_STR[self.status]
                )

    def __repr__(self):
        return self.__str__()

__all__ = ['STATUS', 'Lecture']
