#-------------------------------------------------------------------------------
# Name:        Recommendations
# 
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division
import multiprocessing
from math import sqrt
import collections 
from map_reduce import MapReduce

# A dictionary of movie critics and their ratings of a small
# set of movies
def loadMovieLens(path='movielens'):
    # Get movie titles
    movies={}
    for line in open(path+'/u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title
    # Load data
    prefs=collections.defaultdict(dict)
    for line in open(path+'/u.data'):
        (user,movieid,rating,ts)=line.split('\t')        
        prefs[user][movies[movieid]]=float(rating)
    return prefs

critics =  loadMovieLens()

PEARSON_SIMILARITY_CACHE = {}
EUCLIDEAN_SIMILARITY_CACHE = {}
TANIMOTO_SIMILARITY_CACHE = {}

def transform_items(items):
    result=collections.defaultdict(dict)
    for x in items:
        for y in items[x]:            
            # Flip item and person
            result[y][x]=items[x][y]
    return result


def get_commun_items(x, y):
    """
    Returns the commun items between x and y
    """
    return [i for i in x.keys() if i in y.keys()] 
    
    
def hamming_distance(s1, s2):
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))


def euclidean_dis(x, y, commun_items):
    """
    Returns the euclidean distance between x and y for a given list of commun items
    """
    return sqrt(sum([pow(x[i] - y[i], 2) for i in commun_items]))


def euclidean_sim(items, x, y, cache=False):
    """
    Returns the euclidean similarity between x and y.
    """  
    if cache:
        if (x,y) in EUCLIDEAN_SIMILARITY_CACHE:
            return EUCLIDEAN_SIMILARITY_CACHE[(x,y)]
        i_x = items[x]
        i_y = items[y]
        sim =  1 / (1 + euclidean_dis(i_x, i_y, get_commun_items(i_x, i_y)))
        EUCLIDEAN_SIMILARITY_CACHE[(x,y)] = sim
        EUCLIDEAN_SIMILARITY_CACHE[(y,x)] = sim 
        return sim
    i_x = items[x]
    i_y = items[y]
    return 1 / (1 + euclidean_dis(i_x, i_y, get_commun_items(i_x, i_y)))

def pearson_correlation(x, y, commun_items):
    """
    The population correlation coefficient corr(x,y) between x and y with expected
    values m(x) and m(y) and standard deviations std(x) and std(y) is defined as:
        corr(x,y) = cov(x, y) / (std(x) * std(y)) = E((x - m(x))(y - m(y))) / (std(x) * std(y))
    
    Returns the pearson correlation for x and y for a given list of commun items 
    """
    # Find the number of elements
    n=len(commun_items)
    # if they are no ratings in common, return 0
    if n==0: return 0
    # Add up all the preferences
    sumX=sum([x[i] for i in commun_items])
    sumY=sum([y[i] for i in commun_items])
    # Sum up the squares
    sumX2=sum([pow(x[i],2) for i in commun_items])
    sumY2=sum([pow(y[i],2) for i in commun_items])
    # Sum up the products
    prodSum=sum([x[i]*y[i] for i in commun_items])
    # Calculate Pearson score
    num=prodSum-(sumX*sumY/n)
    den=sqrt((sumX2-pow(sumX,2)/n)*(sumY2-pow(sumY,2)/n))
    if den==0: return 0
    r=num/den
    return r


def pearson_sim(items, x, y, cache=False):
    """
    Returns the similarity between x and y based on the pearson correaltion
    """
    if cache:
        if (x,y) in PEARSON_SIMILARITY_CACHE:
            return PEARSON_SIMILARITY_CACHE[(x,y)]
        i_x = items[x]
        i_y = items[y]
        sim = pearson_correlation(i_x, i_y, get_commun_items(i_x, i_y))
        PEARSON_SIMILARITY_CACHE[(x,y)] = sim
        PEARSON_SIMILARITY_CACHE[(y,x)] = sim
        return sim
    i_x = items[x]
    i_y = items[y]
    return pearson_correlation(i_x, i_y, get_commun_items(i_x, i_y))

def tanimoto_score(x, y, commun_items):
    """
    Return the tanimoto score :
        X inter Y / X union Y
    """
    return len(commun_items)/(len(x) + len(y))

def tanimoto_sim(items, x, y, cache=False):
    """
    Returns the similarity between x and y based on the tanimoto score
    """
    if cache:
        if (x,y) in TANIMOTO_SIMILARITY_CACHE:
            return TANIMOTO_SIMILARITY_CACHE[(x,y)]
        i_x = items[x]
        i_y = items[y]
        sim = tanimoto_score(i_x, i_y, get_commun_items(i_x, i_y))
        TANIMOTO_SIMILARITY_CACHE[(x,y)] = sim
        TANIMOTO_SIMILARITY_CACHE[(y,x)] = sim
        return sim
    i_x = items[x]
    i_y = items[y]
    return tanimoto_score(i_x, i_y, get_commun_items(i_x, i_y))

def top_similars_map(data):
    """
    map for top similars
    """
    items, x, i, similarity = data
    l = len(items)
    y_items = items.keys()[i*(int(round(l/4))):(i+1)*(int(round(l/4)))]
    print multiprocessing.current_process().name, 'processing ', x, i
    return [(similarity(items, x, y),y) for y in y_items if y!=x]

def top_similars_reduce(data):
    """
    reduce for top similars
    """
    sim, item = data
    return (sim, item)

def top_similars_mapreduce(items ,x ,n=5 ,similarity=pearson_sim):
    """
    Returns the best matches for x from the items.
    Number of results and similarity function are optional params.
    """
    mapper = MapReduce(top_similars_map, top_similars_reduce)    
    scores = mapper([(items, x, i, similarity) for i in range(4)])    
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[:n]

def top_similars(items ,x ,n=5 ,similarity=pearson_sim):
    """
    Returns the best matches for x from the items.
    Number of results and similarity function are optional params.
    """    
    scores=[(similarity(items, x, y, cache=True),y) for y in items.keys() if y!=x]
    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[:n]


def similar_items(items, n=5, similarity=euclidean_sim, top_similars=top_similars):
    """
    Returns a dictionary of top n similar items for each item
    """
    similar_items_output = collections.defaultdict(dict)
    cpt = 0
    for item in items:
        cpt += 1
        if cpt%100 == 0: print "%d / %d" % (cpt, len(items))
        similars = top_similars(items=items, x=item, n=n, similarity=similarity)    
        similar_items_output[item] = similars  
    return similar_items_output

def get_recommendations_user_filtred_map(data):
    """
    map for the get_recommendations_user_filter function
    """
    items, x, i, similarity = data
    l = len(items)
    y_items = items.keys()[i*(int(round(l/4))):(i+1)*(int(round(l/4)))]    
    print multiprocessing.current_process().name, 'processing ', x, i
    output = []
    for y in y_items:
        if x == y: continue
        sim = similarity(items, x, y, cache=True)
        if sim <= 0: continue
        for item, score in items[y].items():
            if item in items[x] and items[x][item] > 0: continue #ignore items x already interacted with
            output.append((item, (sim, score * sim)))            
    return output

def get_recommendations_user_filtred_reduce(data):
    """
    reduce for the get_recommendations_user_filtred function
    """
    item, scores = data
    ssim = 0
    ssim_x_score = 0
    for sim, sim_x_score in scores:
        ssim += sim
        ssim_x_score += sim_x_score    
    return (item, ssim, ssim_x_score)

def get_recommendations_user_filtred_mapreduce(items, x, n=5, similarity=pearson_sim):
    """
    Returns recommendationx for x from the items, based on items from similar users     
    """
    mapper = MapReduce(get_recommendations_user_filtred_map, get_recommendations_user_filtred_reduce)    
    scores = mapper([(items, x, i, similarity) for i in range(4)]) 
    # Divide each total score by total weighting to get an average
    rankings = [(sim_x_score/sim, item) for (item, sim, sim_x_score) in scores]
    rankings.sort()
    rankings.reverse()
    return rankings[:n]


def get_recommendations_user_filtred(items, x, n=5, similarity=pearson_sim):
    """
    Returns recommendationx for x from the items, based on items from similar users     
    """
    similarities_sum = collections.defaultdict(int)
    sum_prod_sim_score = collections.defaultdict(int)
    for y in items.keys():        
        if x == y: continue #don't compare x with itself
        sim = similarity(items, x, y)
        if sim <= 0: continue #ignore similarities belew or equal 0
        for item, score in items[y].items():
            if item in items[x] and items[x][item] > 0: continue #ignore items x already interacted with
            similarities_sum[item] += sim 
            sum_prod_sim_score[item] += score * sim
    # Divide each total score by total weighting to get an average
    rankings = [(score/similarities_sum[item], item) for item, score in sum_prod_sim_score.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[:n]


def get_recommendations_item_filtred(items, similarity_matrix, x, n=5):
    """
    Returns recommendations for x from items, based on items similar to user's items 
    """
    similarities_sum = collections.defaultdict(int)
    sum_prod_sim_score = collections.defaultdict(int)
    for item, score in items[x].items():#loop over item from x
        for (sim, sim_item) in similarity_matrix[item]:#loop over similar items to item
            if sim_item in items[x]: continue
            # Weighted sum of scores times similarity
            similarities_sum[sim_item] += sim
            sum_prod_sim_score[sim_item] += sim * score
    # Divide each total score by total weighting to get an average
    rankings = [(score/similarities_sum[item], item) for item, score in sum_prod_sim_score.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[:n]        

    
def test_euclidean():
    #people
    print 'user euclidean similarity'
    print euclidean_sim(critics, 'Toy Story (1995)','Twelve Monkeys (1995)')
    print 'user top similarities'
    print top_similars(items=critics, x='99', similarity=euclidean_sim)
    print 'user recommendations'
    print get_recommendations_user_filtred(items=critics, x='99', similarity=euclidean_sim)
    #movies
    movies = transform_items(critics)
    print 'movies euclidean similarity'
    print euclidean_sim(movies, 'Toy Story (1995)','Twelve Monkeys (1995)')
    print 'movies top similarities'
    print top_similars(items=movies, x='Twelve Monkeys (1995)', similarity=euclidean_sim)
    print 'movies recommendations'
    print get_recommendations_user_filtred(items=movies, x='Twelve Monkeys (1995)', similarity=euclidean_sim)
    print 'similar items'
    similarity_matrix = similar_items(items=movies, similarity=euclidean_sim)
    print get_recommendations_item_filtred(items=critics, similarity_matrix=similarity_matrix, x='99')  
    

def test_pearson():
    #people
    print 'pearson sim'
    print pearson_sim(critics, 'Toy Story (1995)','Twelve Monkeys (1995)')
    print 'user top sim'
    print top_similars(items=critics, x='99')
    
    print 'user recommendations'
    print get_recommendations_user_filtred(items=critics, x='99')
    #movies
    movies = transform_items(critics)        
    print 'movies pearson sim'
    print pearson_sim(movies, 'Toy Story (1995)','Twelve Monkeys (1995)')
    print 'movies top similarities'
    print top_similars(items=movies, x='Twelve Monkeys (1995)')
    print 'movies recommendations'
    print get_recommendations_user_filtred(items=movies, x='Twelve Monkeys (1995)')    
    print 'similar items'
    similarity_matrix = similar_items(items=movies, similarity=pearson_sim)  
    print get_recommendations_item_filtred(items=critics, similarity_matrix=similarity_matrix, x='99')
