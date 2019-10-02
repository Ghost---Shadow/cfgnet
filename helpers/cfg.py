import nltk
from nltk import CFG, ChartParser, Production, Nonterminal

class CFGHelper:
  def __init__(self, grammar, parser=ChartParser):
    self._grammar = CFG.fromstring(grammar)
    self._parser = parser(self._grammar)

  def string_to_indexes(self, token_array):
    '''
    Takes an array like ['x', '+', 'y'] and returns [1,0,0]
    The length of the returned array depends on the grammar
    '''
    tree = self._parser.parse(token_array)
    # Parser returns a generator, get the first element
    tree = next(tree)
    ordered_productions = self._bfs(tree)
    return self._generate_indexes(ordered_productions)

  def indexes_to_tokens(self,indexes):
    '''
    Takes a sequence of indexes [1,0,0] and returns 
    an array like ['x', '+', 'y'] using the grammar
    '''
    result = []
    queue = [Nonterminal('S')]
    i = 0
    while len(queue):
        lhs = queue.pop(0)
        # If all the indices have been consumed,
        # return whatever result we have so far
        if i == len(indexes):
            return result
        rhs = self._grammar._lhs_index[lhs][indexes[i]].rhs()
        i += 1
        for r in rhs:
            if type(r) == str:
                result.append(r)
            else:
                queue.append(r)

    return result

  def _generate_production(self, t):
    arr = []
    for i in range(len(t)):
        if type(t[i]) == str:
            arr.append(t[i])
        else:
            arr.append(Nonterminal(t[i].label()))
    return Production(Nonterminal(t.label()), tuple(arr))

  def _bfs(self,t):
    queue = [t]
    productions = []

    while len(queue):
        n = queue.pop(0)
        production = self._generate_production(n)
        productions.append(production)

        for i in range(len(n)):
            if type(n[i]) == nltk.tree.Tree:
                queue.append(n[i])

    return productions

  def _generate_indexes(self,ordered_productions):
    indexes = []

    for prod in ordered_productions:
        indexes.append(self._grammar._lhs_index[prod.lhs()].index(prod))

    return indexes
