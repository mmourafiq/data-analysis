# -*- coding: utf-8 -*-
"""
Created on Jan 09, 2013

@author: Mourad Mourafiq

About: This is an attempt to solve the Quora challenge Nearby.
"""
import math
import heapq

THRESHOLD = 0.001
SQUARE_SIDE = 10


class Square(object):
    """
    Square is data structure that represents a part of the plane.
    A square is divided to 4 parts.
    
    @type _origine_x: float
    @param _origine_x: the x coordinate of the origine of this square
    
    @type _origine_y: float
    @param _origine_y: the y coordinate of the origine of this square
    
    @type _curent_distance: int
    @param _curent_distance: current distance from the query coordiantes
     
    @type _tn: int
    @param _tn: numbre of points in this square  
     
    @type _topics: list
    @param _topics: list of topics
    """

    def __init__(self, origine_x, origine_y):
        self._origine_x = origine_x
        self._origine_y = origine_y
        self._current_distance = 0
        self._tn = 0
        self._topics = []

    def __gt__(self, square):
        delta = self._current_distance - square._current_distance
        if delta < 0:
            return True
        if delta > 0:
            return False

    def add(self, topic):
        self._tn += 1
        self._topics.append(topic)

    def set_current_distance(self, origin_x, origin_y):
        self._current_distance = Topic.euclidean_dis(self._origine_x, self._origine_y, origin_x, origin_y)
        for topic in self._topics:
            topic.set_current_distance(origin_x, origin_y)

    def get_topics(self, tn):
        if self._tn >= tn:
            return self._topics[:tn], 0, False
        else:
            return self._topics, tn - self._tn, True


class Topic(object):
    """
    Topic
    
    @type _id: int
    @param _id: the id of the topic
    
    @type _x: float
    @param _x: the x coordinate in the plane
    
    @type _y: float
    @param _y: the y coordinate in the plane
    
    @type _current_distance: float
    @param _current_distance: the current distance from the origin(origin being the query coordiantaes) 
    
    @type _qn: int
    @param _qn: the number of questions associated with this topics
    
    @type _questions: list
    @param _questions: the list of the questions associated with this topic
    """

    def __init__(self, id, x, y):
        self._id = id
        self._x = x
        self._y = y
        self._current_distance = 0
        self._qn = 0
        self._questions = []

    def __gt__(self, topic):
        delta = self._current_distance - topic._current_distance
        if delta < -THRESHOLD:
            return True
        if delta > THRESHOLD:
            return False
        return True if self._id > topic._id else False

    def add(self, question):
        self._qn += 1
        self._questions.append(question)

    def get_questions(self, qn, questions):
        go_on = True
        for question in self._questions:
            if question not in questions:
                questions.append(question)
                qn -= 1
                if qn == 0:
                    go_on = False
                    break
        return sorted(questions, reverse=True), qn, go_on

    def set_current_distance(self, origin_x, origin_y):
        self._current_distance = self.euclidean_dis(self._x, self._y, origin_x, origin_y)

    @staticmethod
    def euclidean_dis(x1, y1, x2, y2):
        return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


class Nearby(object):
    """
    Nearby solver
    
    @type _tn: int
    @param _tn: the number of topics created
    
    @type _topics: dict
    @param _topics: the dictionary of topics created  
    """


    def __init__(self, tn):
        self._tn = tn
        self._topics = {}

    def add_topic(self, topic_id, x, y):
        self._topics[topic_id] = Topic(topic_id, x, y)

    def add_question(self, question, nbr_topics, topics):
        if nbr_topics <= 0:
            return
        for i in xrange(nbr_topics):
            topic_id = int(topics[i])
            self._topics[topic_id].add(question)

    def _process_query_topic(self, nbr_results, list_topics):
        if nbr_results > self._tn:
            nbr_results = self._tn
        return ' '.join([str(list_topics[i]._id) for i in xrange(nbr_results - 1, -1, -1)])

    def _process_query_question(self, nbr_results, list_topics):
        results = []
        go_on = True
        for i in xrange(self._tn - 1, -1, -1):
            results, nbr_results, go_on = list_topics[i].get_questions(nbr_results, results)
            if not go_on:
                break
        return ' '.join([str(x) for x in results])

    def process_query(self, q_type, q_nbr_results, q_x, q_y):
        list_topics = []
        for topic in self._topics.itervalues():
            topic.set_current_distance(q_x, q_y)
            heapq.heappush(list_topics, topic)
        if q_type == "t":
            return self._process_query_topic(q_nbr_results, list_topics)
        if q_type == "q":
            return self._process_query_question(q_nbr_results, list_topics)


class NearbySquare(Nearby):
    """
    Nearby solver using the square data structure
    
    @type _tn: int
    @param _tn: the number of topics created
    
    @type _topics: dict
    @param _topics: the dictionary of topics created
    
    @type _squares: dict
    @param _squares: the dictionary of squares created  
    """


    def __init__(self, tn):
        self._tn = tn
        self._ts = 0
        self._topics = {}
        self._squares = {}

    def add_topic(self, topic_id, x, y):
        topic = Topic(topic_id, x, y)
        self._topics[topic_id] = topic
        # locate which square this topic should go
        left_x = x % 10
        left_y = y % 10
        square_x = (x - left_x) + 5
        square_y = (y - left_y) + 5
        # check if this square exists
        try:
            square = self._squares[(square_x, square_y)]
        except:
            square = Square(square_x, square_y)
            self._squares[(square_x, square_y)] = square
            self._ts += 1
        square.add(topic)

    def _process_query_topic(self, nbr_results, list_squares):
        results = []
        go_on = True
        if nbr_results > self._tn:
            nbr_results = self._tn
        for i in xrange(self._ts - 1, -1, -1):
            temp_results, nbr_results, go_on = list_squares[i].get_topics(nbr_results)
            results += temp_results
            if not go_on:
                break
        results = sorted(results, reverse=True)
        return ' '.join([str(result._id) for result in results])

    def _process_query_question(self, nbr_results, list_squares):
        results = []
        go_on = True
        for i in xrange(self._ts - 1, -1, -1):
            for topic in sorted(list_squares[i]._topics, reverse=True):
                results, nbr_results, go_on = topic.get_questions(nbr_results, results)
                if not go_on:
                    break
            if not go_on:
                break
        return ' '.join([str(x) for x in results])

    def process_query(self, q_type, q_nbr_results, q_x, q_y):
        list_squares = []
        for square in self._squares.itervalues():
            square.set_current_distance(q_x, q_y)
            heapq.heappush(list_squares, square)
        if q_type == "t":
            return self._process_query_topic(q_nbr_results, list_squares)
        if q_type == "q":
            return self._process_query_question(q_nbr_results, list_squares)


T, Q, N = [int(x) for x in raw_input().split()]
nearby = NearbySquare(T)
while (T):  # list of topics
    command = raw_input().split()
    nearby.add_topic(int(command[0]), float(command[1]), float(command[2]))
    T -= 1
while (Q):  # list of questions
    command = raw_input().split()
    nearby.add_question(int(command[0]), int(command[1]), command[2:])
    Q -= 1
while (N):  # process queries
    command = raw_input().split()
    print nearby.process_query(command[0], int(command[1]), float(command[2]), float(command[3]))
    N -= 1    