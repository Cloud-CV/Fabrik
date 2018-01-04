### Using an Exported Caffe Model

In order to export a Caffe Model from Fabrik:

1. Select the 2nd button from the left in the Actions section of the sidebar.
<img src="exportbutton.png">

2. A drop-down list should appear. Select Caffe.
    * This should download a prototxt file to your computer.
<img src="exportcaffe.png">

3. Rename the file to `model.prototxt`.

4. Create a file titled 'solver.prototxt' with the following:
  ```
  net: "path/to/model.prototxt"    # path to the network
  test_iter: 200                   # how many mini-batches to test in each validation phase
  test_interval: 500               # how often do we call the test phase
  base_lr: 1e-5                    # base learning rate
  lr_policy: "step"                # step means to decrease lr after a number of iterations
  gamma: 0.1                       # ratio of decrement in each step
  stepsize: 5000                   # how often do we step (should be called step_interval)
  display: 20                      # how often do we print training loss
  max_iter: 450000                 # maximum amount of iterations
  momentum: 0.9
  weight_decay: 0.0005             # regularization!
  snapshot: 2000                   # taking snapshot is like saving your progress in a game
  snapshot_prefix: "path/to/model" # path to saved model
  solver_mode: GPU                 # choose CPU or GPU for processing, GPU is far faster, but CPU is more supported.
  ```

5. Execute the following using caffe. ```caffe``` is the executable in the caffe folder (./build/tools/caffe). ```solver.prototxt``` should be the path to the file we just created.
  ```
  caffe train \
    -gpu 0 \
    -solver solver.prototxt
  ```