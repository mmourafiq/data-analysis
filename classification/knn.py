import math
import random


class Item(object):
    """
    Describe an item
    
    @type id: string
    @param id: the id of the elemet
    
    @type value: float
    @param value: the value of the item
    
    @type coords: list
    @param coords: a list representing the parameters that locates the item   
    """

    def __init__(self, id, coords, value=None):
        self.id = id
        self.coords = coords
        self.value = value


class KNN(object):
    @staticmethod
    def euclidean(v1, v2):
        d = 0.0
        for i in range(len(v1)):
            d += (v1[i] - v2[i]) ** 2
        return math.sqrt(d)

    @staticmethod
    def all_distances(data, item):
        distancelist = []
        for i in range(len(data)):
            item2 = data[i]
            distancelist.append((KNN.euclidean(item.coords, item2.coords), i))
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
    def knn_estimate(data, item, k=3):
        # Get sorted distances
        all_dist = KNN.all_distances(data, item)
        avg = 0.0
        # Take the average of the top k results
        for i in range(k):
            idx = all_dist[i][1]
            avg += data[idx].value
        avg = avg / k
        return avg

    @staticmethod
    def weighted_knn(data, item, k=5, weight_f="gaussian"):
        if weight_f == "subtract_weight":
            weightf = KNN.subtract_weight
        elif weight_f == "inverse_weight":
            weightf = KNN.inverse_weight
        elif weight_f == "gaussian":
            weightf = KNN.gaussian
        # Get distances
        all_dist = KNN.all_distances(data, item)
        avg = 0.0
        totalweight = 0.0
        # Get weighted average
        for i in range(k):
            dist = all_dist[i][0]
            idx = all_dist[i][1]
            weight = weightf(dist)
            avg += weight * int(data[idx].value)
            totalweight += weight
        avg = avg / totalweight
        return avg

    @staticmethod
    def prob_guess(data, item, low, high, k=5, weightf=gaussian):
        all_dist = KNN.all_distances(data, item)
        nweight = 0.0
        tweight = 0.0
        for i in range(k):
            dist = all_dist[i][0]
            idx = all_dist[i][1]
            weight = weightf(dist)
            v = data[idx].value
            # Is this point in the range?
            if v >= low and v <= high:
                nweight += weight
            tweight += weight
        if tweight == 0: return 0
        # The probability is the weights in the range
        # divided by all the weights
        return nweight / tweight

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
            error += (item.value - guess) ** 2
        return error / len(testset)

    @staticmethod
    def cross_validate(algf, data, trials=100, test=0.05):
        error = 0.0
        for i in range(trials):
            trainset, testset = KNN.divide_data(data, test)
            error += KNN.test_algorithm(algf, trainset, testset)
        return error / trials

    @staticmethod
    def rescale(data, scale):
        scaleddata = []
        for item in data:
            scaled_coords = [scale[i] * item.coords[i] for i in range(len(scale))]
            scaled_item = Item(id=item.id, value=item.value, coords=scaled_coords)
            scaleddata.append(scaled_item)
        return scaleddata

    @staticmethod
    def cost_function(algf, data):
        """
        this function should be used all along with an optimization function to determine the perfect scale
        notably one could use the annealing algorithm or the genetic algorithm
        """

        def costf(scale):
            sdata = KNN.rescale(data, scale)
            return KNN.cross_validate(algf, sdata, trials=10)

        return costf

    @staticmethod
    def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
        # Initialize the values randomly
        vec = [float(random.randint(domain[i][0], domain[i][1]))
               for i in range(len(domain))]

        while T > 0.1:
            # Choose one of the indices
            i = random.randint(0, len(domain) - 1)

            # Choose a direction to change it
            dir = random.randint(-step, step)

            # Create a new list with one of the values changed
            vecb = vec[:]
            vecb[i] += dir
            if vecb[i] < domain[i][0]:
                vecb[i] = domain[i][0]
            elif vecb[i] > domain[i][1]:
                vecb[i] = domain[i][1]

            # Calculate the current cost and the new cost
            ea = costf(vec)
            eb = costf(vecb)
            p = pow(math.e, (-eb - ea) / T)

            # Is it better, or does it make the probability
            # cutoff?
            if (eb < ea or random.random() < p):
                vec = vecb

            # Decrease the temperature
            T = T * cool
        return vec
