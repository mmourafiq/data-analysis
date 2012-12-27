# -*- coding: utf-8 -*-
"""
Created on Jan 05, 2013

@author: Mourad Mourafiq

About: This is an attempt to solve the Quora challenge Answer classifier.
"""
import numpy
import math
import random
from collections import defaultdict, Counter

log2 = lambda x: math.log(x) / math.log(2)


class Item(object):
    """
    Describe an item
    
    @type id: string
    @param id: the id of the elemet
    
    @type value: string
    @param value: the value of the item
    
    @type coords: list
    @param coords: a list representing the parameters that locates the item   
    """
    __highs = []
    __lows = []

    def __init__(self, id, coords, value=None):
        self.id = id
        self.coords = coords
        self.scaled_coords = coords[:]
        self.value = value
        self.__update_highs()
        self.__update_lows()

    def __update_highs(self):
        if Item.__highs == []:
            Item.__highs = [-9999999.0] * len(self.coords)
        else:
            for i in xrange(len(self.coords)):
                if self.coords[i] > Item.__highs[i]:
                    Item.__highs[i] = self.coords[i]

    def __update_lows(self):
        if Item.__lows == []:
            Item.__lows = [9999999.0] * len(self.coords)
        else:
            for i in xrange(len(self.coords)):
                if self.coords[i] < Item.__lows[i]:
                    Item.__lows[i] = self.coords[i]

    def scale(self, factors=None):
        if factors is None:
            self.scaled_coords = [(self.coords[i] - Item.__lows[i]) / ((Item.__highs[i] - Item.__lows[i]) + 0.0001) for
                                  i in xrange(len(self.coords))]
        else:
            self.scaled_coords = [
                ((self.coords[i] - Item.__lows[i]) / ((Item.__highs[i] - Item.__lows[i]) + 0.0001) * factors[i]) for i
                in xrange(len(self.coords))]


######################################################
##### The approach of the Linear classification ######
###################################################### 
def linear_mean(data, t_value, f_value, mask=None):
    # two categories
    t_coords = []
    f_coords = []
    for item in data:
        if item.value == t_value:
            if mask is None:
                t_coords.append(item.scaled_coords)
            else:
                t_coords.append([item.scaled_coords[i] for i in xrange(len(item.scaled_coords)) if i in mask])
        elif item.value == f_value:
            if mask is None:
                f_coords.append(item.scaled_coords)
            else:
                f_coords.append([item.scaled_coords[i] for i in xrange(len(item.scaled_coords)) if i in mask])
    t_mean = numpy.average(numpy.array(t_coords), 0)
    f_mean = numpy.average(numpy.array(f_coords), 0)
    return t_mean, f_mean


def dot_product_classification(item, means, t_value, f_value, mask=None):
    t_mean, f_mean = means
    if mask is None:
        item_coords = numpy.array(item.scaled_coords)
    else:
        item_coords = numpy.array([item.scaled_coords[i] for i in xrange(len(item.scaled_coords)) if i in mask])
    y = (numpy.dot(f_mean, f_mean) - numpy.dot(t_mean, t_mean)) / 2
    x = (numpy.dot(item_coords, t_mean) - numpy.dot(item_coords, f_mean)) + y
    return t_value if x > 0 else f_value


######################################################
### The approach of the non Linear classification ####
######################################################
def radial_basis(item1, item2, gamma=10):
    diff_item = numpy.array(item1.coords) - numpy.array(item2.coords)
    dist_item = numpy.sqrt(numpy.sum(diff_item))
    return math.e ** (-gamma * dist_item)


def non_linear_classification(item, data, t_value, f_value, offset, gamma=10):
    t_sum = 0
    t_count = 0
    f_sum = 0
    f_count = 0
    for item2 in data:
        if item2.value == t_value:
            t_sum += radial_basis(item2, item, gamma)
            t_count += 1
        elif item2.value == f_value:
            f_sum += radial_basis(item2, item, gamma)
            f_count += 1
    res = (float(t_sum) / t_count - float(f_sum) / f_count) + offset
    return t_value if res > 0 else f_value


def calculate_offset(data, t_value, f_value, gamma=10):
    t_data = []
    f_data = []
    for item in data:
        if item.value == t_value:
            t_data.append(item)
        elif item.value == f_value:
            f_data.append(item)
    t_sum = sum(sum([radial_basis(item1, item2, gamma) for item1 in t_data]) for item2 in t_data)
    f_sum = sum(sum([radial_basis(item1, item2, gamma) for item1 in f_data]) for item2 in f_data)
    return (float(f_sum) / (len(f_data) ** 2)) - (float(t_sum) / (len(t_data) ** 2))


######################################################
######### The approach of the decision trees #########
###################################################### 
class Node(object):
    """
    A node object in a decision tree
    
    @type column: int
    @param column: the column index of the criteria to be tested
    
    @type value: string
    @param value: the value that the column must match to get a true result

    @type results: dict
    @param results: stores a dictionary of results for this branch. This is None for everything
                    except endpoints
    
    @type t_node: Node
    @param t_node: the next nodes in the tree if the result is true
    
    @type f_node: Node
    @param f_node: the next nodes in the tree if the result is false
    """

    def __init__(self, col=-1, value=None, results=None, t_node=None, f_node=None):
        self.col = col
        self.value = value
        self.results = results
        self.t_node = t_node
        self.f_node = f_node

    def draw(self, indent=''):
        # Is this a leaf node?
        if self.results != None:
            print str(self.results)
        else:
            # Print the criteria
            print str(self.col) + ':' + str(self.value) + '? '
            # Print the branches
            print indent + 'T->',
            self.t_node.draw(indent + '  ')
            print indent + 'F->',
            self.f_node.draw(indent + '  ')


class DecisionTree(object):
    """
    A decision tree object
    """

    @staticmethod
    def count_results(data, item=True):
        """
        count the occurrences of each result in the data set
        """
        results_count = defaultdict(int)
        if item:
            for i in data:
                results_count[i.value] += 1
        else:
            results_count = Counter(data)
        return results_count

    @staticmethod
    def divide_data(data, column, value):
        """
        Divides a set of rows on a specific column.
        """
        # a function that decides if the row goes to the first or the second group (true or false)
        spliter = None
        if isinstance(value, int) or isinstance(value, float):
            spliter = lambda item: item.scaled_coords[column] >= value
        else:
            spliter = lambda item: item.scaled_coords[column] == value
        #divide the rows into two sets and return them
        set_true = []
        set_false = []
        for item in data:
            if spliter(item):
                set_true.append(item)
            else:
                set_false.append(item)
        return (set_true, set_false)

    @staticmethod
    def gini_impurity(data, item=True):
        """
        Probability that a randomly placed item will be in the wrong category
        """
        results_count = DecisionTree.count_results(data, item)
        len_data = len(data)
        imp = 0.0
        for k1, v1 in results_count.iteritems():
            p1 = float(v1) / len_data
            for k2, v2 in results_count.iteritems():
                if k1 == k2: continue
                p2 = float(v2) / len_data
                imp += p1 * p2
        return imp

    @staticmethod
    def entropy(data, item=True):
        """
        estimate the disorder in the data set : sum of p(x)log(p(x))
        """
        results_count = DecisionTree.count_results(data, item)
        len_data = len(data)
        ent = 0.0
        for v in results_count.itervalues():
            p = float(v) / len_data
            ent -= p * log2(p)
        return ent

    @staticmethod
    def variance(data):
        """
        calculates the statistical variance for a set of rows
        more preferably to be used with numerical outcomes
        """
        len_data = len(data)
        if len_data == 0: return 0
        score = [float(item.value) for item in data]
        mean = sum(score) / len(score)
        variance = sum([(s - mean) ** 2 for s in score]) / len(score)
        return variance


    @staticmethod
    def build_tree(data, disorder_function="entropy"):
        """
        a recursive function that builds the tree by choosing the best dividing criteria
        disorder_function : 
            for data that contains words and booleans; it is recommended to use entropy or gini_impurity
            for data that contains number; it is recommended to use variance
        """
        if disorder_function == "entropy":
            disorder_estimator = DecisionTree.entropy
        elif disorder_function == "gini_impurity":
            disorder_estimator = DecisionTree.gini_impurity
        elif disorder_function == "variance":
            disorder_estimator = DecisionTree.variance
        len_data = len(data)
        if len_data == 0: return Node()
        current_disorder_level = disorder_estimator(data)
        # track enhancement of disorer's level
        best_enhancement = 0.0
        best_split = None
        best_split_sets = None
        # number columns
        nbr_coords = len(data[0].scaled_coords)
        for coord_ind in xrange(nbr_coords):
            #get unique values of the current column
            coord_values = {}
            for item in data:
                coord_values[item.scaled_coords[coord_ind]] = 1
            for coord_value in coord_values.iterkeys():
                set1, set2 = DecisionTree.divide_data(data, coord_ind, coord_value)
                p1 = float(len(set1)) / len_data
                p2 = (1 - p1)
                enhancement = current_disorder_level - (p1 * disorder_estimator(set1)) - (p2 * disorder_estimator(set2))
                if (enhancement > best_enhancement) and (len(set1) > 0 and len(set2) > 0):
                    best_enhancement = enhancement
                    best_split = (coord_ind, coord_value)
                    best_split_sets = (set1, set2)
        if best_enhancement > 0:
            t_node = DecisionTree.build_tree(best_split_sets[0])
            f_node = DecisionTree.build_tree(best_split_sets[1])
            return Node(col=best_split[0], value=best_split[1],
                        t_node=t_node, f_node=f_node)
        else:
            return Node(results=DecisionTree.count_results(data))

    @staticmethod
    def prune(tree, min_enhancement, disorder_function="entropy"):
        """
        checking pairs of nodes that have a common parent to see if merging 
        them would increase the entropy by less than a specified threshold
        """
        if disorder_function == "entropy":
            disorder_estimator = DecisionTree.entropy
        elif disorder_function == "gini_impurity":
            disorder_estimator = DecisionTree.gini_impurity
        elif disorder_function == "variance":
            disorder_estimator = DecisionTree.variance
        if tree.t_node.results == None:
            DecisionTree.prune(tree.t_node, min_enhancement)
        if tree.f_node.results == None:
            DecisionTree.prune(tree.f_node, min_enhancement)
        # If both the subbranches are now leaves, see if they should merged
        if (tree.t_node.results != None and tree.f_node.results != None):
            # Build a combined dataset
            t_node, f_node = [], []
            for key, value in tree.t_node.results.items():
                t_node += [[key]] * value
            for key, value in tree.f_node.results.items():
                f_node += [[key]] * value
            # Test the enhancement 
            delta = disorder_estimator(t_node + f_node, item=False) - (
            disorder_estimator(t_node, item=False) + disorder_estimator(f_node, item=False) / 2)
            if delta < min_enhancement:
                # Merge the branches
                tree.t_node, tree.f_node = None, None
                tree.results = DecisionTree.count_results(t_node + f_node, item=False)

    @staticmethod
    def classify(observation, tree):
        """
        Classify a new observation given a decision tree
        """
        if tree.results != None:
            return tree.results
        # the observation value for the current criteria column
        observation_value = observation.scaled_coords[tree.col]
        if observation_value == None:
            t_results, f_results = DecisionTree.classify(observation, tree.t_node), DecisionTree.classify(observation,
                                                                                                          tree.f_node)
            t_count = sum(t_results.values())
            f_count = sum(f_results.values())
            t_prob = float(t_count) / (t_count + f_count)
            f_prob = float(f_count) / (t_count + f_count)
            result = {}
            for key, value in t_results.items(): result[key] = value * t_prob
            for key, value in f_results.items(): result[key] = value * f_prob
            return result
        else:
            #with branch to follow
            branch = None
            if (isinstance(observation_value, int) or isinstance(observation_value, float)):
                branch = tree.t_node if (observation_value >= tree.value) else tree.f_node
            else:
                branch = tree.t_node if (observation_value == tree.value) else tree.f_node
            return DecisionTree.classify(observation, branch)


######################################################
######### The approach of the KNN            #########
######################################################
class KNN(object):
    @staticmethod
    def euclidean(v1, v2):
        d = 0.0
        for i in range(len(v1)):
            d += (v1[i] - v2[i]) ** 2
        return math.sqrt(d)

    @staticmethod
    def all_distances(data, item, mask=None):
        len_coords = len(data[0].coords)
        if mask is None:
            mask = [i for i in xrange(len_coords)]
        distancelist = []
        for i in range(len(data)):
            item2 = data[i]
            distancelist.append((KNN.euclidean([item.scaled_coords[x] for x in xrange(len_coords) if x in mask],
                                               [item2.scaled_coords[x] for x in xrange(len_coords) if x in mask]), i))
        distancelist.sort()
        return distancelist

    @staticmethod
    def inverse_weight(dist, num=1.0, const=0.1):
        return num / (dist + const)

    @staticmethod
    def subtract_weight(dist, const=1.0):
        if dist > const:
            return 0
        else:
            return const - dist

    @staticmethod
    def gaussian(dist, sigma=10.0):
        return math.e ** (-dist ** 2 / (2 * sigma ** 2))

    @staticmethod
    def knn_estimate(data, item, k=8, mask=None):
        # Get sorted distances
        all_dist = KNN.all_distances(data, item, mask)
        avg = 0.0
        # Take the average of the top k results
        for i in range(k):
            idx = all_dist[i][1]
            avg += int(data[idx].value)
        # avg=avg/k
        result = "-1"
        if avg > 0:
            result = "+1"
        return result

    @staticmethod
    def weighted_knn(data, item, k=8, weight_f="gaussian", mask=None):
        if weight_f == "subtract_weight":
            weightf = KNN.subtract_weight
        elif weight_f == "inverse_weight":
            weightf = KNN.inverse_weight
        elif weight_f == "gaussian":
            weightf = KNN.gaussian
        # Get distances
        all_dist = KNN.all_distances(data, item, mask)
        avg = 0.0
        totalweight = 0.0
        # Get weighted average
        for i in range(k):
            dist = all_dist[i][0]
            idx = all_dist[i][1]
            weight = weightf(dist)
            avg += weight * int(data[idx].value)
            totalweight += weight
        # avg=avg/totalweight
        result = "-1"
        if avg > 0:
            result = "+1"
        return result

    @staticmethod
    def divide_data(data, test=0.05):
        trainset = []
        testset = []
        for row in data:
            if random.random() < test:
                testset.append(row)
            else:
                trainset.append(row)
        return trainset, testset

    @staticmethod
    def test_algorithm(algf, trainset, testset):
        error = 0.0
        for item in testset:
            guess = algf(trainset, item)
            if item.value != guess:
                error += 1
        return error / len(testset)

    @staticmethod
    def cross_validate(algf, data, trials=100, test=0.05):
        error = 0.0
        for i in range(trials):
            trainset, testset = KNN.divide_data(data, test)
            error += KNN.test_algorithm(algf, trainset, testset)
        return error / trials


######################################################
##### create scores for parameters based on knn ######
######################################################
def create_score_factors_knn(algf, training_data, classify_data, results, k=8):
    len_coords = len(training_data[0].coords)
    corrects = [0] * len_coords
    factors = [0] * len_coords
    for i in xrange(len_coords):
        for obs in classify_data:
            cr = algf(training_data, obs, k, [i])
            if cr == results[obs.id]:
                corrects[i] += 1
    min_corrects = min(corrects)
    max_corrects = max(corrects)
    for i in xrange(len_coords):
        factors[i] = ((corrects[i] - min_corrects) / ((max_corrects - min_corrects) + 0.000001)) * 100
    return factors


###########################################################
## create mask and scores for parameters based on linear ##
###########################################################
def create_score_factors_linear(training_data, classify_data, results):
    len_coords = len(training_data[0].coords)
    corrects = [0] * len_coords
    factors = [0] * len_coords
    scores = [0] * len_coords
    for i in xrange(len_coords):
        means = linear_mean(training_set, "+1", "-1", [i])
        for obs in classify_data:
            if dot_product_classification(obs, means, "+1", "-1", [i]) == results[obs.id]:
                corrects[i] += 1
    scores = [(corrects[i], i) for i in xrange(len_coords)]
    scores.sort()
    mask = [scores[-1][1]]
    current_correct = scores[-1][0]
    for i in xrange(0, len_coords - 1):
        new_mask = mask[:]
        new_mask.append(scores[i][1])
        means = linear_mean(training_set, "+1", "-1", new_mask)
        correct = 0
        for obs in classify_data:
            if dot_product_classification(obs, means, "+1", "-1", new_mask) == results[obs.id]:
                correct += 1
        if correct >= current_correct:
            current_correct = correct
            mask = new_mask[:]
    min_corrects = min(corrects)
    max_corrects = max(corrects)
    for i in xrange(len_coords):
        factors[i] = ((corrects[i] - min_corrects) / ((max_corrects - min_corrects) + 0.000001))
    return mask, factors


###########################################################
#### create mask and scores for parameters based on knn ###
###########################################################
def create_score_factors_linear_knn(training_data, classify_data, results, k=8):
    len_coords = len(training_data[0].coords)
    corrects = [0] * len_coords
    t_corrects = [0] * len_coords
    f_corrects = [0] * len_coords
    factors = [0] * len_coords
    scores = [0] * len_coords
    for i in xrange(len_coords):
        means = linear_mean(training_set, "+1", "-1", [i])
        for obs in classify_data:
            if dot_product_classification(obs, means, "+1", "-1", [i]) == results[obs.id]:
                corrects[i] += 1
                if results[obs.id] == "-1":
                    f_corrects[i] += 1
                else:
                    t_corrects[i] += 1
    print corrects
    print t_corrects
    print f_corrects
    scores = [(corrects[i], i) for i in xrange(len_coords)]
    scores.sort()
    mask = [scores[-1][1]]
    current_correct = scores[-1][0]
    for i in xrange(len_coords - 2, -1, -1):
        new_mask = mask[:]
        new_mask.append(scores[i][1])
        correct = 0
        for obs in classify_data:
            cr = KNN.knn_estimate(training_data, obs, k, mask)
            if cr == results[obs.id]:
                correct += 1
        if correct >= current_correct - 5:
            current_correct = correct
            mask = new_mask[:]
    min_corrects = min(corrects)
    max_corrects = max(corrects)
    for i in xrange(len_coords):
        factors[i] = ((corrects[i] - min_corrects) / ((max_corrects - min_corrects) + 0.000001))
    return mask, factors

######################################################
########### Reading the test and results #############
###################################################### 
r_file = open('test.txt', 'r')
w_file = open('results.txt', 'r')
N, M = [int(x) for x in r_file.readline().strip('\n').split()]
training_set = []
for i in xrange(N):
    current_line = r_file.readline().strip('\n').split()
    id = current_line[0]
    value = current_line[1]
    coords = [float(x.split(':')[1]) for x in current_line[2:]]
    assert len(coords) == M
    # coords=[coords[i] for i in xrange(M) if i in [1, 2, 4, 6, 7, 11, 14, 18]]
    training_set.append(Item(id=id, coords=coords, value=value))
Q = int(r_file.readline().strip('\n'))
classify_set = []
for i in xrange(Q):
    current_line = r_file.readline().strip('\n').split()
    id = current_line[0]
    coords = [float(x.split(':')[1]) for x in current_line[1:]]
    assert len(coords) == M
    # coords=[coords[i] for i in xrange(M) if i in [1, 2, 4, 6, 7, 11, 14, 18]]
    classify_set.append(Item(id=id, coords=coords))
# reading the results
results = {}
for i in xrange(Q):
    current_line = w_file.readline().strip('\n').split()
    results[current_line[0]] = current_line[1]

#mask, factors = create_score_factors_linear_knn(training_set, classify_set, results)
#print mask
#print factors
####linear######
#mask = [1, 2, 4, 6, 7, 11, 14, 18]
#print create_score_factors_linear(training_set, classify_set, results)
##275
#correct = 0
#means = linear_mean(training_set, "+1", "-1", mask)
#for obs in classify_set:    
#    if dot_product_classification(obs, means, "+1", "-1", mask) == results[obs.id]:
#        correct += 1
#print correct 
####linear scaled######
#342
#correct = 0
#for item in training_set:
#    item.scale()
#means = linear_mean(training_set, "+1", "-1")
#for obs in classify_set:
#    obs.scale()    
#    if dot_product_classification(obs, means, "+1", "-1") == results[obs.id]:
#        correct += 1
#print correct

####non linear######
#250
#correct = 0
#offset = calculate_offset(training_set, "+1", "-1", gamma=20)
#for obs in classify_set:    
#    if non_linear_classification(obs, training_set, "+1", "-1", offset, gamma=20) == results[obs.id]:
#        correct += 1
#print correct 

####decision tree######
#367
#d = DecisionTree()
#node = d.build_tree(training_set)
#correct=0
#for obs in classify_set:    
#    cr = d.classify(obs, node)    
#    if cr.keys()[0] == results[obs.id]:
#        correct += 1
#print correct

#####KNN & weighted KNn#######
#best mask I've got so far, with classification result of 82.8% - 83% 
mask = [1, 2, 4, 6, 7, 11, 14, 18]
for item in training_set:
    item.scale()
correct = 0
for obs in classify_set:
    obs.scale()
    cr = KNN.knn_estimate(training_set, obs, k=8, mask=mask)
    if cr == results[obs.id]:
        correct += 1
print correct
correct = 0
for obs in classify_set:
    cr = KNN.weighted_knn(training_set, obs, k=8, mask=mask)
    if cr == results[obs.id]:
        correct += 1
print correct
correct = 0
for obs in classify_set:
    cr = KNN.weighted_knn(training_set, obs, k=8, weight_f="subtract_weight", mask=mask)
    if cr == results[obs.id]:
        correct += 1
print correct
correct = 0
for obs in classify_set:
    cr = KNN.weighted_knn(training_set, obs, k=8, weight_f="inverse_weight", mask=mask)
    if cr == results[obs.id]:
        correct += 1
print correct
