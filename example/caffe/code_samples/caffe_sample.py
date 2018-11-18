import subprocess
import sys


# Get the command line arguments
model_file = ''
try:
    model_file = sys.argv[1]
except IndexError:
    print('Usage: python caffe_sample.py PATH_TO_MODEL')
    exit()

solver = [
    'net: "{}"'.format(model_file),
    'test_iter: 200',
    'test_interval: 500',
    'base_lr: 1e-5',
    'lr_policy: "step"',
    'gamma: 0.1',
    'stepsize: 5000',
    'display: 20',
    'max_iter: 450000',
    'momentum: 0.9',
    'weight_decay: 0.0005',
    'snapshot: 2000',
    'snapshot_prefix: "model/caffe_sample"',
    'solver_mode: GPU',
]

# Create solver.prototxt
with open('solver.prototxt', 'w') as file:
    for line in solver:
        file.write(line + '\n')

# Train the model
subprocess.call(['caffe', 'train', '-gpu', '0', '-solver', 'solver.prototxt'])
