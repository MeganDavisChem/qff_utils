"""Makes latex tables"""
# import json
from sys import argv
import panda_qff as pq

inp = argv[1]
inp2 = argv[1]
qff = pq.QFF(inp, "cc3", "h2o")
qff2 = pq.QFF(inp2, "notcc3", "h2o")
qff.join_qff(qff2)
qff.print_latex("test.tex")
qff.print_latex_sep(qff.molecule)
