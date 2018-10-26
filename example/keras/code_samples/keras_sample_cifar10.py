from keras.datasets import cifar10
from keras.models import model_from_json
import sys

# Get the command line arguments
model_file_name = ''
try:
    model_file_name = sys.argv[1]
except IndexError:
    print('Usage: python train.py model_json_file')
    exit()

# Load the dataset (keras.datasets.cifar10)
# To use other datasets from keras.datasets, replace cifar10 in line 1 with your preferred dataset.
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Load the model from JSON file
json_file = open(model_file_name, 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# Print the model summary
loaded_model.summary()

# Configure model for training and testing with accuracy evaluation
loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
loaded_model.fit(x_train, y_train, epochs=150, batch_size=10, verbose=0)

# Evaluate the model
scores = loaded_model.evaluate(x_test, y_test, verbose=0)

# Print final accuracy
print("%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1] * 100))
