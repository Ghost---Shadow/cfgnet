from nltk.parse.generate import generate as gen
import nltk
import numpy as np
import random

from helpers.cfg import CFGHelper

sample_grammar = '''
S -> '(' S ')' | S O S | V | '(' S ')'
V -> 'x' | 'y' | 'z' | 'w'
O -> '+' | '-' | '*' | '/'
'''

def _index_to_one_hot(index_vector, vector_size):
  one_hots = []

  for index in index_vector:
    one_hot = np.eye(vector_size)[index]
    one_hots.append(one_hot)

  return np.stack(one_hots)

def generate_dataset(grammar, n, depth, pick_chance):
  cfg = CFGHelper(grammar)

  # Assuming number of generations is same for all non terminals
  vector_size = len(cfg._grammar.productions(lhs=cfg._grammar.start()))

  all_one_hots = []

  i = 0
  p = int(0.01 * n)
  sentences = []
  for sentence in gen(cfg._grammar, n=n, depth=depth):
    i += 1

    if i % p == 0:
      print(*sentences,sep='\n')
      sentences = []
    
    if random.random() > pick_chance:
      continue
    sentences.append(sentence)
    indexes = cfg.string_to_indexes(sentence)
    one_hots = _index_to_one_hot(indexes, vector_size)

    all_one_hots.append(one_hots)

  print(*sentences,sep='\n')
  print('i',i)
  return np.array(all_one_hots)

def demo():
  dataset = generate_dataset(sample_grammar, 10000000, 6, 0.01)
  np.save('./data.npy', dataset)
  data = np.load('./data.npy')
  print(data.shape)

  import winsound
  winsound.Beep(440, 1000)

##demo()

