# -*- coding: utf-8 -*-
"""
Created on Jan 11, 2013

@author: Mourad Mourafiq

About: This is an attempt to solve the Quora challenge Feed Optimizer.
"""
import itertools
import copy
import math
from random import choice, random

BRUTE_FORCE = 1
ANNEALING_SIMULATED = 2


class Story(object):
    """
    Story object 
    
    @type _cpt: int
    @param _cpt: counts the number of instance created.
    
    @type _height: int
    @param _height: The stroy's height.
        
    @type _time: int
    @param _time: The time of publication.
    
    @type _id: int
    @param _id: The story's id.
    
    @type _score: int
    @param _score: The story's score.
    
    @type _height: int
    @param _height: The stroy's height.   
    
    @type _proportioned_score: float
    @param _proportioned_score: The stroy's _score proportioned to height.    
    """
    __cpt = 0

    def __init__(self, time=-1, score=-1, height=-1):
        self._id = Story.__cpt
        self._time = time
        self._score = score
        self._height = height
        self._proportioned_score = float(score) / height
        Story.__cpt += 1

    def __repr__(self):
        return "id: %s, time: %s" % (self._id, self._time)

    def __gt__(self, story):
        if (self._proportioned_score > story._proportioned_score):
            return True
        if (self._proportioned_score < story._proportioned_score):
            return False
        if (self._id < story._id):
            return True
        return False

    def _better_score(self, story):
        if (self._score > story._score):
            return True
        if (self._score < story._score):
            return False
        if (self._id < story._id):
            return True
        return False


class Solution(object):
    """
    Potential solution for the upcoming reload
    
    @type _stories: list
    @param _stories: The list of potential items.

    @type _len_stories : int
    @param _len_stories: The length of the list of stories.    
    
    @type _score: int
    @param _score: The current solution's score.
    
    @type _height: int
    @param _height: The current solution's height.    
    """

    def __init__(self):
        self._stories = []
        self._len_stories = 0
        self._score = 0
        self._height = 0

    def __repr__(self):
        return "%s %s %s" % (
            self._score, self._len_stories, ' '.join(sorted([str(story._id) for story in self._stories])))

    def __gt__(self, solution):
        # check who's score is better
        if self._score > solution._score:
            return True
        if self._score < solution._score:
            return False
        # same score; check who has less stories
        if self._len_stories < solution._len_stories:
            return True
        if self._len_stories > solution._len_stories:
            return False
        #same score, same number of stories; check who has smaller lexicographically
        if sorted([story._id for story in self._stories]) <= sorted([story._id for story in solution._stories]):
            return True
        else:
            return False

    @classmethod
    def clone(cls, solution):
        clone_solution = cls()
        clone_solution._stories = copy.copy(solution._stories)
        clone_solution._len_stories = solution._len_stories
        clone_solution._score = solution._score
        clone_solution._height = solution._height
        return clone_solution

    def add(self, story):
        """
        add story to the solution
        """
        self._stories.append(story)
        self._score += story._score
        self._height += story._height
        self._len_stories += 1

    def remove(self, story):
        """
        remove story from the solution
        """
        self._stories.remove(story)
        self._score -= story._score
        self._height -= story._height
        self._len_stories -= 1


class Optimizer(object):
    """
    Keep track of stories that can potentially make a solution.
    The stories should be sorted by time of publication.
    
    @type _stories: list
    @param stories: The list of stories that can potentially make a solution.
    
    @type _len_stories : int
    @param _len_stories: The length of the list of stories.
    
    @type __height: int 
    @param window: The height of the browser.  
    
    @type __window: int 
    @param window: The window of recent stories.   
    
    @type _best_story: Stroy
    @param _best_story: The  best story so far.   
    """
    __height = 0
    __window = 0

    def __init__(self, window, height):
        self._stories = []
        self._len_stories = 0
        Optimizer.__window = window
        Optimizer.__height = height
        self._best_story = Story()

    def _purge_old_stories(self, current_time):
        """
        remove old stories form the current list of stories
        """
        # check if the oldest stories can still be part of the solution
        to_be_removed = []
        for old_story in self._stories:
            if (current_time - old_story._time) <= Optimizer.__window:
                break
            else:
                to_be_removed.append(old_story)
        for old_story in to_be_removed:
            self._stories.remove(old_story)
            self._len_stories -= 1

    def _brute_force(self):
        """
        check all possibilities:
            1) best solution for combination of 2 stories (if it exists).
            2) best solution for combination of 3 stories (if it exists).
            .
            .
            l-1) best solution for combination of l-1 stories (if it exists).
            
            l : being the length of the current stories.
        """
        best_solution = Solution()
        best_solution.add(self._best_story)
        for i in xrange(2, self._len_stories + 1):
            for tuple_stories in itertools.combinations(self._stories, i):
                if self.addable(tuple_stories):
                    current_solution = Solution()
                    for story in tuple_stories:
                        current_solution.add(story)
                    if current_solution > best_solution:
                        best_solution = current_solution
        return best_solution

    def _annealing_simulated(self, T=1000.0, cool=0.35):
        """
        perform the annealing simulated algorithm:
            1) start with a random solution.
            2) move to a neighbour solution. 
                (favors better solutions, and accepts worst solutions with a certain probabilities
                 to avoid local minimum until the temperature is totally down)
        """
        # order stories based on their proportioned score
        ordered_stories = sorted(self._stories, reverse=True)
        # produce a random solution
        current_solution, stories_in_current = self.random_solution(ordered_stories, self._len_stories)
        best_solution = Solution.clone(current_solution)
        while (T > 0.1):
            temp_solution = Solution.clone(current_solution)
            stories_in_temp = copy.copy(stories_in_current)
            stories_at_true = [i for i in xrange(self._len_stories) if stories_in_temp[i]]
            #check if there is still stories
            if len(stories_at_true) == self._len_stories:
                break
                #choose a story and remove it
            if stories_at_true:
                indice = choice(stories_at_true)
                stories_in_temp[indice] = False
                temp_solution.remove(ordered_stories[indice])
            else:
                indice = -1
            #add any number of other stories available
            for i in xrange(indice + 1, self._len_stories):
                if stories_in_temp[i]:
                    continue
                story = ordered_stories[i]
                if self.addable((story,), temp_solution):
                    stories_in_temp[i] = True
                    temp_solution.add(story)
                elif temp_solution._height == self.__height:
                    break
            #compare temp and current solutions
            if temp_solution > current_solution:
                current_solution = temp_solution
                stories_in_current = stories_in_temp
                #also since temp is better than current, compare it to best
                if current_solution > best_solution:
                    best_solution = Solution.clone(current_solution)
            #current solution is better than temp
            #the algorithm states that we can still give it a try depending on a probability
            else:
                #since temp solution score is < current solution score
                #this probability will be near one at the beginning where T is high 
                #but will get lower and lower as T cool down 
                #hence will accept less and less bad solution
                p = pow(math.e, float(temp_solution._score - current_solution._score) / T)
                if p > random():
                    current_solution = temp_solution
                    stories_in_current = stories_in_temp
                    #decrease the temperature
            T = T * cool
        return best_solution

    def add(self, story):
        # check if the story's height is within the browser's height
        if story._height <= Optimizer.__height:
            self._stories.append(story)
            self._len_stories += 1
            if (story > self._best_story):
                self._best_story = story

    def produce_solution(self, current_time, solution=BRUTE_FORCE):
        self._purge_old_stories(current_time)
        if solution == BRUTE_FORCE:
            return self._brute_force()
        elif solution == ANNEALING_SIMULATED:
            return self._annealing_simulated()

    @classmethod
    def addable(cls, tuple_stories, solution=Solution()):
        total_height = solution._height
        for story in tuple_stories:
            total_height += story._height
        if total_height <= cls.__height:
            return True
        return False

    @classmethod
    def random_solution(cls, list_stories, length_stories):
        """
        produce a random solution
        """
        stories_in = [False] * length_stories
        solution = Solution()
        for i in xrange(length_stories):
            story = list_stories[i]
            if cls.addable((story,), solution):
                solution.add(story)
                stories_in[i] = True
            elif solution._height == cls.__height:
                break
        return solution, stories_in


N, W, H = [int(x) for x in raw_input().split()]
p = Optimizer(W, H)
while (N):
    command = raw_input().split()
    if command[0] == "S":  # story
        t, s, h = [int(x) for x in command[1:]]
        p.add(Story(t, s, h))
    elif command[0] == "R":  # Reload
        tr = int(command[1])
        print p.produce_solution(tr, solution=ANNEALING_SIMULATED)
    N -= 1  