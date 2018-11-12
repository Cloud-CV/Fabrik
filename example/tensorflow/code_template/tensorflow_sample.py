import tensorflow as tf
from google.protobuf import text_format
import sys

# Get the model file name
try:
    model_file_name = sys.argv[1]
except IndexError:
    print('Usage: python tensorflow_sample.py <MODEL_FILE.pbtxt>')

# Read the protobuf text and build a tf.GraphDef
with open(model_file_name, 'r') as model_file:
    model_protobuf = text_format.Parse(model_file.read(),
                                       tf.GraphDef())

# Import the GraphDef built above into the default graph
tf.import_graph_def(model_protobuf)

# You can now add operations on top of the imported graph
