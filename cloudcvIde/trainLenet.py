from pylab import *
import sys
import caffe
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

net_path = BASE_DIR+'/cloudcvIde/media/prototxt/'+sys.argv[1]+'.prototxt'
solver_config_path = BASE_DIR+'/cloudcvIde/media/prototxt/'+sys.argv[1]+'Solver.prototxt'

from caffe.proto import caffe_pb2
s = caffe_pb2.SolverParameter()

s.random_seed = 0xCAFFE
s.net = net_path
s.test_interval = 500
s.test_iter.append(100)
s.max_iter = 10000
s.type = "SGD"
s.base_lr = 0.01
s.momentum = 0.9
s.weight_decay = 5e-4
s.lr_policy = 'inv'
s.gamma = 0.0001
s.power = 0.75
s.display = 100
s.solver_mode = caffe_pb2.SolverParameter.CPU

with open(solver_config_path, 'w') as f:
    f.write(str(s))

solver = None
solver = caffe.get_solver(solver_config_path)
solver.solve()



