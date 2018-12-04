from keras.models import model_from_json
from keras.utils import plot_model
import sys

try:
    json_file = sys.argv[1]
    output_file = sys.argv[2]
except KeyError:
    print("Usage: python print_keras_model.py <json file name> <image name>")

with open(json_file, 'r') as f:
    loaded_model = model_from_json(f.read())

plot_model(loaded_model,
           to_file=json_file + '.png',
           rankdir='LR',
           show_shapes=True,
           show_layer_names=False)
