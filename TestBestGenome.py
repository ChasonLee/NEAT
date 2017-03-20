# -*- coding: utf-8 -*-
__author__ = 'Chason'
from TestTictactoe import *

with open("test.gen", "rb") as file_in:
    model = pickle.load(file_in)
tt = TictactoeTest()
tt.test_case(model)