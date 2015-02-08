
# coding: utf-8

# In[353]:

import pandas
import numpy as np
import scipy

import pickle

from itertools import islice

from zillow_hackathon.dataset import Neighborhood

import sklearn.preprocessing
import scipy.spatial.distance
import sklearn.feature_extraction
import sklearn.cluster

from sklearn.externals import joblib

import pylab as plt
from mpl_toolkits.mplot3d import Axes3D

get_ipython().magic(u'matplotlib inline')


## Vectorize Data

# In[339]:

def get_features(n):
    # return dict(n.data['num_attrs'].items())
    return dict(n.data['spec_attrs'].items())    
    # return dict(n.data['num_attrs'].items() + n.data['spec_attrs'].items())    
    # return { 'price': + n.data['num_attrs']['median_list_price'] }


# In[340]:

sea_nbrs = list(Neighborhood.get_neighborhoods_in_city('Seattle'))
sf_nbrs = list(Neighborhood.get_neighborhoods_in_city('San Francisco'))

nbrs = sea_nbrs + sf_nbrs
sf_start_idx = len(sea_nbrs)

nbrs_features = [get_features(n) for n in nbrs]
vectorizer = sklearn.feature_extraction.DictVectorizer(sparse=False) 

vectorizer.fit(nbrs_features)
nbrs_features = vectorizer.transform(nbrs_features)


## Normalize

# In[341]:

min_max_scaler = sklearn.preprocessing.MinMaxScaler()
min_max_scaler.fit(nbrs_features)
nbrs_features = min_max_scaler.transform(nbrs_features)


## Reduce Dimensionality

# In[342]:

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline

LSA_DIMENSIONS = 10
 
svd = TruncatedSVD(LSA_DIMENSIONS)
lsa = make_pipeline(svd, Normalizer(copy=False))
# lsa = svd

LSA_ENABLED = True

if LSA_ENABLED:
    lsa.fit(nbrs_features)

def reduce_dim(v):
    if LSA_ENABLED:
        return lsa.transform(v)
    else:
        return v

nbrs_features_reduced = reduce_dim(nbrs_features)


## Find Similar Items

# In[343]:

def find_similar(v1, where):
    res = []

    for i, v2 in enumerate(where):
        d = 1 - scipy.spatial.distance.cosine(v1, v2)
        # d = 1 - scipy.spatial.distance.euclidean(v1, v2)        
        # d = 1 - scipy.spatial.distance.jaccard(v1, v2)        
        # d = np.dot(v1, v2)
        
        res.append((i, d))

    return sorted(res, key=lambda p: [ -p[1] ])  

def find_top_similar(city, name, start_idx = 0):
    x = Neighborhood.get_for_city_and_neighborhood(city, name)
    x = reduce_dim(min_max_scaler.transform(vectorizer.transform(get_features(x))))      

    top_similar = find_similar(x, nbrs_features_reduced[start_idx:])
    nbrs_attrs = nbrs[start_idx:]

    print "Results for %s" % name
    for r in islice(top_similar, 5):
        id = r[0]
        d = r[1]

        print "#%d: %s, %s: %f" % (id, nbrs_attrs[id].name, nbrs_attrs[id].city, d)    
    print
    
find_top_similar('Seattle', 'Capitol Hill')
find_top_similar('Seattle', 'University District')
find_top_similar('Seattle', 'Northgate')
find_top_similar('Seattle', 'International District')
find_top_similar('Seattle', 'Ballard')

find_top_similar('Seattle', 'Capitol Hill', sf_start_idx)
find_top_similar('Seattle', 'University District', sf_start_idx)
find_top_similar('Seattle', 'Northgate', sf_start_idx)
find_top_similar('Seattle', 'International District', sf_start_idx)
find_top_similar('Seattle', 'Ballard', sf_start_idx)


## Clustering Helpers

# In[344]:

#
# Creates dictionary of cluster-to-item mapping
#
def map_clusters_to_items(cls):
    cluster_to_item_map = dict()

    for item_id in range(len(cls.labels_)):
        cluster_id = cls.labels_[item_id]

        if not cluster_id in cluster_to_item_map:
            cluster_to_item_map[cluster_id] = []

        cluster_to_item_map[cluster_id].append(item_id)

    return cluster_to_item_map

#
# Print clusters
#
def print_clusters(cls):
    clusters = map_clusters_to_items(cls)
    for cluster_id, items in sorted(clusters.iteritems(), key = lambda kv: [ -len(kv[1]) ]):
        print("Cluster #%d: %d items" % (cluster_id, len(items)))

        for item_id in islice(items, 5):
            item = nbrs[item_id]
            print("\t%s, %s" % (item.data['name'], item.data['city']))
            print
        print


## Run DBSCAN Clustering (No Fixed # of Clusters)

# In[351]:

from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.3, min_samples=3)
dbscan.fit(nbrs_features_reduced)

print_clusters(dbscan)


## Run K-Means Clustering (Fixed # of Clusters)

# In[345]:




# In[346]:

km = sklearn.cluster.KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1,
                verbose=True)

km.fit(nbrs_features_reduced)
print_clusters(km)


## Plotting using 3 first dimensions

# In[347]:

fig = plt.figure("", figsize=(10, 10))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)

plt.cla()
labels = km.labels_

ax.scatter(nbrs_features_reduced[:, 0], nbrs_features_reduced[:, 1], nbrs_features_reduced[:, 2], c=labels.astype(np.float))

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])


## Persisting the Models

# In[354]:

joblib.dump(min_max_scaler, 'data/output/min_max_scaler.pkl')
joblib.dump(lsa, 'data/output/lsa.pkl')
joblib.dump(vectorizer, 'data/output/vectorizer.pkl')
joblib.dump(vectorizer, 'data/output/vectorizer.pkl')


# In[ ]:



