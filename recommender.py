import os
import errno

import numpy as np
import scipy

import pickle

from itertools import islice

from zillow_hackathon.dataset import Neighborhood

import sklearn.preprocessing
import scipy.spatial.distance
import sklearn.feature_extraction
import sklearn.cluster

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

##
## Data holder
##
class Data(object):
  def __init__(self):
    self.nbrs = list(Neighborhood.get_neighborhoods_in_city('Seattle')) \
                      + list(Neighborhood.get_neighborhoods_in_city('San Francisco'))

##
## Vectorizes features, reduces dimensionality and etc ...
##
class Featurizer(object):
  def __init__(self, data):
    self.data = data
    self.max_dim_count = None

  def featurize(self):
    # Select features
    self.nbrs_features = [self.feature_extractor(n) for n in self.data.nbrs]

    # Vectorize
    self.vectorizer = sklearn.feature_extraction.DictVectorizer(sparse=False)
    self.vectorizer.fit(self.nbrs_features)
    self.nbrs_features = self.vectorizer.transform(self.nbrs_features)

    # Normalize
    self.min_max_scaler = sklearn.preprocessing.MinMaxScaler()
    self.min_max_scaler.fit(self.nbrs_features)
    self.nbrs_features = self.min_max_scaler.transform(self.nbrs_features)

    # Reduce dimensions if requested
    if not self.max_dim_count is None:
      from sklearn.decomposition import TruncatedSVD
      from sklearn.preprocessing import Normalizer
      from sklearn.pipeline import make_pipeline

      self.svd = TruncatedSVD(self.max_dim_count)
      self.lsa = make_pipeline(self.svd, Normalizer(copy=False))

      self.lsa.fit(self.nbrs_features)
      self.nbrs_features = self.reduce_dimensions_(self.nbrs_features)

  def reduce_dimensions_(self, v):
    if self.max_dim_count is None:
      return v
    else:
      return self.lsa.transform(v)

  def featurize_single(self, n):
    return self.reduce_dimensions_(self.min_max_scaler.transform(self.vectorizer.transform(self.feature_extractor(n))))

class SpecFeaturizer(Featurizer):
  def __init__(self, data):
    super(SpecFeaturizer, self).__init__(data)

  def feature_extractor(self, n):
    return n.data['spec_attrs']

class NumFeaturizer(Featurizer):
  def __init__(self, data):
    super(NumFeaturizer, self).__init__(data)

  def feature_extractor(self, n):
    return n.data['num_attrs']

##
## Naive Unsupervised Recommendation service
##
class Recommender(object):
  MODEL_PATH = 'ml_model/recommender.pkl'

  def __init__(self):
    self.max_results = 3

  def train(self):
    self.data = Data()

    self.spec_featurizer = SpecFeaturizer(self.data)
    self.spec_featurizer.max_dim_count = 10
    self.spec_featurizer.featurize()

    self.num_featurizer = NumFeaturizer(self.data)
    self.num_featurizer.max_dim_count = 10
    self.num_featurizer.featurize()

  def find_top_similar(self, n, city, max = 3):
    res = []

    v_spec = self.spec_featurizer.featurize_single(n)
    v_num = self.num_featurizer.featurize_single(n)

    for i in range(len(self.data.nbrs)):
      if self.data.nbrs[i].city == city:
        sim_spec = self.similarity(v_spec, self.spec_featurizer.nbrs_features[i])
        sim_num = self.similarity(v_num, self.num_featurizer.nbrs_features[i])

        sim = 1.0 * sim_spec + 0.0 * sim_num

        res.append((i, sim))

    res =  sorted(res, key=lambda p: [ -p[1] ])
    for r in islice(res, self.max_results):
        id = r[0]
        sim = r[1]

        yield (self.data.nbrs[id], sim)

  @staticmethod
  def load():
    with open(os.path.join(SCRIPT_DIR, Recommender.MODEL_PATH)) as f:
      return pickle.load(f)

  def save(self):
    p = os.path.join(SCRIPT_DIR, self.MODEL_PATH)
    self.make_directory_if_not_exists(os.path.dirname(p))

    with open(p, 'wb') as f:
      pickle.dump(self, f)

  def similarity(self, v1, v2):
    s = 1 - scipy.spatial.distance.cosine(v1, v2)
    # s = 1 - scipy.spatial.distance.euclidean(v1, v2)
    # s = 1 - scipy.spatial.distance.jaccard(v1, v2)
    # s = np.dot(v1, v2)
    return s

  def make_directory_if_not_exists(self, path):
      try:
        os.makedirs(path)
      except OSError as exception:
        if exception.errno != errno.EEXIST:
          raise

##
## Ad Ho Terst
##

def print_top(rec, city, name, where_to_move):
  print 'Searching %s, %s in %s ...' % (name, city, where_to_move)
  n = Neighborhood.get_for_city_and_neighborhood(city, name)
  for m, sim in rec.find_top_similar(n, where_to_move):
    print('%s, %s: %f' % (m.name, m.city, sim))
  print

def ad_hoc_test():
  r = Recommender()
  r.train()

  print_top(r, 'Seattle', 'Capitol Hill', 'Seattle')
  print_top(r, 'Seattle', 'Capitol Hill', 'San Francisco')

  print_top(r, 'Seattle', 'International District', 'Seattle')
  print_top(r, 'Seattle', 'International District', 'San Francisco')

  print_top(r, 'Seattle', 'Northgate', 'Seattle')
  print_top(r, 'Seattle', 'Northgate', 'San Francisco')

  print_top(r, 'Seattle', 'University District', 'Seattle')
  print_top(r, 'Seattle', 'University District', 'San Francisco')

  r.save()

  r2 = Recommender.load()
  print_top(r2, 'Seattle', 'University District', 'Seattle')

if __name__ == '__main__':
  ad_hoc_test()
