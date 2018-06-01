from keras.models import model_from_json
import tensorflow as tf
from keras import backend as K
import argparse
import os
import imp

parser = argparse.ArgumentParser(description='set input arguments')
parser.add_argument('-input_file', action="store",
                    dest='input_file', type=str, default='model.json')
parser.add_argument('-output_file', action="store",
                    dest='output_file', type=str, default='model.pbtxt')
args = parser.parse_args()
input_file = args.input_file
output_file = args.output_file

K.set_learning_phase(0)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))))

output_fld = BASE_DIR + '/media/'

with open(output_fld + input_file, 'r') as f:
    json_str = f.read()

json_str = json_str.strip("'<>() ").replace('\'', '\"')
lrn = imp.load_source('LRN', BASE_DIR + '/keras_app/custom_layers/lrn.py')
model = model_from_json(json_str, {'LRN': lrn.LRN})

sess = K.get_session()
tf.train.write_graph(sess.graph.as_graph_def(add_shapes=True), output_fld,
                     output_file + '.pbtxt', as_text=True)
