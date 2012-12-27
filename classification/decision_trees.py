"""
Created on Nov 01, 2012

@author: Mourad Mourafiq
"""

from math import log

log2 = lambda x: log(x) / log(2)


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

    def __init__(self, id, coords, value=None):
        self.id = id
        self.coords = coords
        self.value = value


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
            for i in data:
                results_count[i[-1]] += 1
        return results_count

    @staticmethod
    def divide_data(data, column, value):
        """
        Divides a set of rows on a specific column.
        """
        # a function that decides if the row goes to the first or the second group (true or false)
        spliter = None
        if isinstance(value, int) or isinstance(value, float):
            spliter = lambda item: item.coords[column] >= value
        else:
            spliter = lambda item: item.coords[column] == value
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
        nbr_coords = len(data[0].coords)
        for coord_ind in xrange(nbr_coords):
            #get unique values of the current column
            coord_values = {}
            for item in data:
                coord_values[item.coords[coord_ind]] = 1
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
        observation_value = observation.coords[tree.col]
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
