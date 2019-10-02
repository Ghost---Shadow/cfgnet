from nltk import Nonterminal
from helpers.cfg import CFGHelper

sample_grammar = '''
S -> S O S | V | '(' S ')'
V -> 'x' | 'y' | 'z' | 'w'
O -> '+' | '-' | '*' | '/'
'''

def test_string_to_indexes():
  cfg = CFGHelper(sample_grammar)
  token_array = 'x + ( y / w ) + x'.split(' ')
  assert cfg.string_to_indexes(token_array) == [0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 1, 3, 1, 1, 3]

def test_indexes_to_tokens():
  cfg = CFGHelper(sample_grammar)
  indexes = [0, 0, 0, 1, 1, 0, 2, 0, 0, 0, 1, 3, 1, 1, 3]
  token_array = 'x + ( y / w ) + x'.split(' ')
  assert cfg.indexes_to_tokens(indexes) == token_array

def test_inversion():
  cfg = CFGHelper(sample_grammar)
  token_array = 'x + ( y / w ) + x'.split(' ')
  assert cfg.indexes_to_tokens(cfg.string_to_indexes(token_array)) == token_array

def test_weird_indices():
  cfg = CFGHelper(sample_grammar)
  indexes = [1,1,1,1,1,1,1,1,1]
  assert cfg.indexes_to_tokens(indexes) == ['y']

  indexes = [1]
  assert cfg.indexes_to_tokens(indexes) == [Nonterminal('V')]
