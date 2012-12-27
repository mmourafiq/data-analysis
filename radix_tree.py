# -*- coding: utf-8 -*-
'''
Created on Dec 01, 2012

@author: Mourad Mourafiq

About: This is an attempt to implement the radix tree algo.
	   Features : 
			-> insert
			-> remove
			-> search
'''
NOK = "{'':[]}"


class Prefixer():
    def __init__(self):
        self.__data = {}

    def __repr__(self):
        return 'Prefixer(%s)' % (self.__data,)

    def __eq__(self, other):
        return self.__data == other.__data

    def get_data(self):
        return self.__data

    def insert(self, word, item_id):
        node = self.__data
        while word:
            prefix, key = self.longest_prefix(word, node.keys())
            if not prefix:
                break
            len_prefix = len(prefix)
            if prefix != key:
                # split key into prefix:suffix, move data
                suffix = key[len_prefix:]
                current_node = node[key]
                node[prefix] = {suffix: current_node}
                del node[key]
            word = word[len_prefix:]
            node = node[prefix]
        if word:
            node[word] = eval(NOK)
            node[word][''].append(item_id)
        else:
            try:
                node[word].append(item_id)
            except:
                node[word] = []
                node[word].append(item_id)
        return True

    def remove(self, word, item_id):
        node = self.__data
        while word:
            prefix, key = self.longest_prefix(word, node.keys())
            if not prefix:
                return False
            node = node.get(prefix, None)
            if not node:
                return False
            word = word[len(prefix):]
        try:
            node[''].remove(item_id)
            return True
        except:
            return False

    def _search_dico(self, word):
        node = self.__data
        while word:
            prefix, key = self.longest_prefix(word, node.keys())
            if not prefix:
                return False
            if not key:
                return False
            if prefix != key:
                if prefix == word:
                    return node[key]
                else:
                    return False
            node = node[prefix]
            word = word[len(prefix):]
        return node

    def search(self, word):
        dico = self._search_dico(word)
        if dico != False:
            return self.traverse_dico(dico)
        return []

    @staticmethod
    def traverse_dico(dico):
        results = []
        for key, value in dico.iteritems():
            if key == '':
                results += value
            else:
                results += Prefixer.traverse_dico(value)
        return results

    @staticmethod
    def longest_prefix(word, candidates):
        """
        return the longest prefix match between word and any of the
        candidates, if any. Only one candidate will much.
        """
        if word:
            wc = word[0]
            for c in candidates:
                if c.startswith(wc):
                    for i in reversed(xrange(1, min(len(word), len(c)) + 1)):
                        if c.startswith(word[:i]):
                            return (word[:i], c)
        return ('', None)
