# -*- coding: utf-8 -*-
__author__ = 'Chason'
class Node:
    def __init__(self, id, tag = '', value = 0):
        self.id = id
        self.value = value
        self.tag = tag

    def __eq__(self, other):
        return self.id == other.id and self.tag == other.tag