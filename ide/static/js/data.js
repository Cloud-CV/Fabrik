export default {
  /* ********** Data Layers ********** */
  ImageData: { // Only Caffe
    name: 'image data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      source: {
        name: 'Data source',
        value: '',
        type: 'text',
        required: true
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true
      },
      rand_skip: {
        name: 'Random Skip',
        value: 0,
        type: 'number',
        required: false
      },
      shuffle: {
        name: 'Shuffle',
        value: false,
        type: 'checkbox',
        required: false
      },
      new_height: {
        name: 'New Height',
        value: 0,
        type: 'number',
        required: false
      },
      new_width: {
        name: 'New Width',
        value: 0,
        type: 'number',
        required: false
      },
      is_color: {
        name: 'Is Color',
        value: true,
        type: 'checkbox',
        required: false
      },
      root_folder: {
        name: 'Root Folder',
        value: '',
        type: 'text',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      mirror: {
        name: 'Mirror',
        value: false,
        type: 'checkbox',
        required: false
      },
      crop_size: {
        name: 'Crop Size',
        value: 0,
        type: 'number',
        required: false
      },
      mean_file: {
        name: 'Mean File',
        value: '',
        type: 'text',
        required: false
      },
      mean_value: {
        name: 'Mean Value',
        value: '',
        type: 'text',
        required: false
      },
      force_color: {
        name: 'Force Color',
        value: false,
        type: 'checkbox',
        required: false
      },
      force_gray: {
        name: 'Force Gray',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Data: { // Only Caffe
    name: 'data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      source: {
        name: 'Data source',
        value: '',
        type: 'text',
        required: true
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true
      },
      backend: {
        name: 'Backend',
        value: 'LEVELDB',
        type: 'select',
        options: ['LMDB', 'LEVELDB'],
        required: false
      },
      rand_skip: {
        name: 'Random Skip',
        value: 0,
        type: 'number',
        required: false
      },
      prefetch: {
        name: 'Prefetch',
        value: 4,
        type: 'number',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      mirror: {
        name: 'Mirror',
        value: false,
        type: 'checkbox',
        required: false
      },
      crop_size: {
        name: 'Crop Size',
        value: 0,
        type: 'number',
        required: false
      },
      mean_file: {
        name: 'Mean File',
        value: '',
        type: 'text',
        required: false
      },
      mean_value: {
        name: 'Mean Value',
        value: '',
        type: 'text',
        required: false
      },
      force_color: {
        name: 'Force Color',
        value: false,
        type: 'checkbox',
        required: false
      },
      force_gray: {
        name: 'Force Gray',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  HDF5Data: { // Only Caffe
    name: 'hdf5data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      source: {
        name: 'HDF5 Data source',
        value: '',
        type: 'text',
        required: true
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true
      },
      shuffle: {
        name: 'Shuffle',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  HDF5Output: { // Only Caffe
    name: 'hdf5output',
    color: '#673ab7',
    endpoint: {
      src: [],
      trg: ['Top']
    },
    params: {
      file_name: {
        name: 'Output Filename',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Input: {
    name: 'input',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  WindowData: { // Only Caffe
    name: 'window data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      source: {
        name: 'Data source',
        value: '',
        type: 'text',
        required: true
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true
      },
      fg_threshold: {
        name: 'Foreground Threshold',
        value: 0.5,
        type: 'float',
        required: false
      },
      bg_threshold: {
        name: 'Background Threshold',
        value: 0.5,
        type: 'float',
        required: false
      },
      fg_fraction: {
        name: 'Foreground Fraction',
        value: 0.25,
        type: 'float',
        required: false
      },
      context_pad: {
        name: 'Context Padding',
        value: 0,
        type: 'number',
        required: false
      },
      crop_mode: {
        name: 'Crop Mode',
        value: 'warp',
        type: 'select',
        options: ['warp', 'square'],
        required: false
      },
      cache_images: {
        name: 'Cache Images',
        value: false,
        type: 'checkbox',
        required: false
      },
      root_folder: {
        name: 'Root Folder',
        value: '',
        type: 'text',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      mirror: {
        name: 'Mirror',
        value: false,
        type: 'checkbox',
        required: false
      },
      crop_size: {
        name: 'Crop Size',
        value: 0,
        type: 'number',
        required: false
      },
      mean_file: {
        name: 'Mean File',
        value: '',
        type: 'text',
        required: false
      },
      mean_value: {
        name: 'Mean Value',
        value: '',
        type: 'text',
        required: false
      },
      force_color: {
        name: 'Force Color',
        value: false,
        type: 'checkbox',
        required: false
      },
      force_gray: {
        name: 'Force Gray',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  MemoryData: { // Only Caffe
    name: 'memory data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      batch_size: {
        name: 'Batch Size',
        value: '',
        type: 'number',
        required: true
      },
      channels: {
        name: 'Channels',
        value: '',
        type: 'number',
        required: true
      },
      height: {
        name: 'Height',
        value: '',
        type: 'number',
        required: true
      },
      width: {
        name: 'Width',
        value: '',
        type: 'number',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  DummyData: { // Only Caffe
    name: 'dummy data',
    color: '#673ab7',
    endpoint: {
      src: ['Bottom'],
      trg: []
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true
      },
      type: {
        name: 'Data Filler Type',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  /* ********** Vision Layers ********** */
  Convolution: {
    name: 'conv',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      layer_type: { // Only Keras
        name: 'Type',
        value: '3D',
        type: 'select',
        options: ['1D', '2D', '3D'],
        required: false
      },
      num_output: { // Maps to: filters(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      pad_h: {
        name: 'Padding height',
        value: 0,
        type: 'number',
        required: false
      },
      pad_w: {
        name: 'Padding width',
        value: 0,
        type: 'number',
        required: false
      },
      pad_d: {
        name: 'Padding depth',
        value: 0,
        type: 'number',
        required: false
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: false
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true
      },
      kernel_d: {
        name: 'Kernel depth',
        value: '',
        type: 'number',
        required: false
      },
      stride_h: {
        name: 'Stride height',
        value: 1,
        type: 'number',
        required: false
      },
      stride_w: {
        name: 'Stride width',
        value: 1,
        type: 'number',
        required: false
      },
      stride_d: {
        name: 'Stride depth',
        value: 1,
        type: 'number',
        required: false
      },
      dilation_h: {
        name: 'Dilation height',
        value: 1,
        type: 'number',
        required: false
      },
      dilation_w: {
        name: 'Dilation width',
        value: 1,
        type: 'number',
        required: false
      },
      dilation_d: {
        name: 'Dilation depth',
        value: 1,
        type: 'number',
        required: false
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Maps to: bias_term(Caffe)
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  Pooling: {
    name: 'pool',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      layer_type: { // Only Keras
        name: 'Type',
        value: '3D',
        type: 'select',
        options: ['1D', '2D', '3D'],
        required: false
      },
      pool: {
        name: 'Pooling method',
        value: 'MAX',
        type: 'select',
        options: ['MAX', 'AVE', 'STOCHASTIC'],
        required: false
      },
      pad_h: {
        name: 'Padding height',
        value: 0,
        type: 'number',
        required: false
      },
      pad_w: {
        name: 'Padding width',
        value: 0,
        type: 'number',
        required: false
      },
      pad_d: {
        name: 'Padding depth',
        value: 0,
        type: 'number',
        required: false
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: false
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true
      },
      kernel_d: {
        name: 'Kernel depth',
        value: '',
        type: 'number',
        required: false
      },
      stride_h: {
        name: 'Stride height',
        value: 1,
        type: 'number',
        required: false
      },
      stride_w: {
        name: 'Stride width',
        value: 1,
        type: 'number',
        required: false
      },
      stride_d: {
        name: 'Stride depth',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Upsample: { // Only Keras
    name: 'upsample',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      layer_type: {
        name: 'Type',
        value: '3D',
        type: 'select',
        options: ['1D', '2D', '3D'],
        required: false
      },
      size_h: {
        name: 'Size height',
        value: 1,
        type: 'number',
        required: false
      },
      size_w: {
        name: 'Size width',
        value: 1,
        type: 'number',
        required: true
      },
      size_d: {
        name: 'Size depth',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  LocallyConnected: { // Only Keras
    name: 'locally connected',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      layer_type: {
        name: 'Type',
        value: '2D',
        type: 'select',
        options: ['1D', '2D'],
        required: false
      },
      filters: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: false
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true
      },
      stride_h: {
        name: 'Stride height',
        value: 1,
        type: 'number',
        required: false
      },
      stride_w: {
        name: 'Stride width',
        value: 1,
        type: 'number',
        required: false
      },
      kernel_initializer: {
        name: 'Kernel Initializer',
        value: 'glorot_uniform',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_initializer: {
        name: 'Bias Initializer',
        value: 'Zeros',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: {
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: {
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: {
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: {
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: {
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: {
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  Crop: { // Only Caffe
    name: 'crop',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      axis: {
        name: 'axis',
        value: '2',
        type: 'number',
        required: false
      },
      offset: {
        name: 'offset',
        value: '0',
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  SPP: { // Only Caffe
    name: 'spp',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      pool: {
        name: 'Pooling method',
        value: 'MAX',
        type: 'select',
        options: ['MAX', 'AVE', 'STOCHASTIC'],
        required: false
      },
      pyramid_height: {
        name: 'Pyramid Height',
        value: '',
        type: 'number',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Deconvolution: {
    name: 'deconv',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: { // Maps to: filters(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: true
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true
      },
      stride_h: {
        name: 'Stride height',
        value: 1,
        type: 'number',
        required: false
      },
      stride_w: {
        name: 'Stride width',
        value: 1,
        type: 'number',
        required: false
      },
      pad_h: {
        name: 'Padding height',
        value: 0,
        type: 'number',
        required: false
      },
      pad_w: {
        name: 'Padding width',
        value: 0,
        type: 'number',
        required: false
      },dilation_h: {
        name: 'Dilation height',
        value: 1,
        type: 'number',
        required: false
      },
      dilation_w: {
        name: 'Dilation width',
        value: 1,
        type: 'number',
        required: false
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Maps to: bias_term(Caffe)
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  DepthwiseConv: { // Only Keras
    name: 'depthwise convolution',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      filters: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: true
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true
      },
      stride_h: {
        name: 'Stride height',
        value: 1,
        type: 'number',
        required: false
      },
      stride_w: {
        name: 'Stride width',
        value: 1,
        type: 'number',
        required: false
      },
      pad_h: {
        name: 'Padding height',
        value: 0,
        type: 'number',
        required: false
      },
      pad_w: {
        name: 'Padding width',
        value: 0,
        type: 'number',
        required: false
      },
      depth_mult: {
        name: 'Depth multiplier',
        value: 1,
        type: 'number',
        required: false
      },
      use_bias: { // Maps to: bias_term(Caffe)
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      depthwise_initializer: {
        name: 'Depthwise Initializer',
        value: 'glorot_uniform',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      pointwise_initializer: {
        name: 'Pointwise Initializer',
        value: 'glorot_uniform',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_initializer: {
        name: 'Bias Initializer',
        value: 'Zeros',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      depthwise_regularizer: {
        name: 'Depthwise regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      pointwise_regularizer: {
        name: 'Pointwise regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: {
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: {
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      depthwise_constraint: {
        name: 'Depthwise constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      pointwise_constraint: {
        name: 'Pointwise constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: {
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  /* ********** Recurrent Layers ********** */
  Recurrent: { // Only Caffe
    name: 'recurrent',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      debug_info: {
        name: 'Degug',
        value: false,
        type: 'checkbox',
        required: false
      },
      expose_hidden: {
        name: 'Expose Hidden',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  RNN: {
    name: 'rnn',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: { // Maps to: units(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      debug_info: { // Only Caffe
        name: 'Degug',
        value: false,
        type: 'checkbox',
        required: false
      },
      expose_hidden: { // Only Caffe
        name: 'Expose Hidden',
        value: false,
        type: 'checkbox',
        required: false
      },
      recurrent_initializer: { // Only Keras
        name: 'Recurrent Initializer',
        value: 'Orthogonal',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 
          'VarianceScaling', 'Orthogonal', 'Identity', 'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      recurrent_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      recurrent_constraint: { // Only Keras
        name: 'Recurrent constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Only Keras
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      dropout: { // Only Keras
        name: 'Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      recurrent_dropout: { // Only Keras
        name: 'Recurrent Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  GRU: { // Only Keras
    name: 'gru',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: { // Maps to: units(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      recurrent_activation: { // Only Keras
        name: 'Recurrent activation',
        value: 'hard_sigmoid',
        type: 'select',
        options: ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear'],
        required: false
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      debug_info: { // Only Caffe
        name: 'Degug',
        value: false,
        type: 'checkbox',
        required: false
      },
      expose_hidden: { // Only Caffe
        name: 'Expose Hidden',
        value: false,
        type: 'checkbox',
        required: false
      },
      recurrent_initializer: { // Only Keras
        name: 'Recurrent Initializer',
        value: 'Orthogonal',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 
          'VarianceScaling', 'Orthogonal', 'Identity', 'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      recurrent_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      recurrent_constraint: { // Only Keras
        name: 'Recurrent constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Only Keras
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      dropout: { // Only Keras
        name: 'Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      recurrent_dropout: { // Only Keras
        name: 'Recurrent Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  LSTM: {
    name: 'lstm',
    color: '#3f51b5',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: { // Maps to: units(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      recurrent_activation: { // Only Keras
        name: 'Recurrent activation',
        value: 'hard_sigmoid',
        type: 'select',
        options: ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear'],
        required: false
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      debug_info: { // Only Caffe
        name: 'Degug',
        value: false,
        type: 'checkbox',
        required: false
      },
      expose_hidden: { // Only Caffe
        name: 'Expose Hidden',
        value: false,
        type: 'checkbox',
        required: false
      },
      recurrent_initializer: { // Only Keras
        name: 'Recurrent Initializer',
        value: 'Orthogonal',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 
          'VarianceScaling', 'Orthogonal', 'Identity', 'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      recurrent_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      recurrent_constraint: { // Only Keras
        name: 'Recurrent constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Only Keras
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      unit_forget_bias: { // Only Keras
        name: 'Use forget bias',
        value: true,
        type: 'checkbox',
        required: false
      },
      dropout: { // Only Keras
        name: 'Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      recurrent_dropout: { // Only Keras
        name: 'Recurrent Dropout',
        value: 0.0,
        type: 'number',
        required: false
      },
      return_sequences: { // Only Keras
        name: 'Return Sequences',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  /* ********** Common Layers ********** */
  InnerProduct: {
    name: 'fc',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: { // Maps to: units(Keras)
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      weight_filler: { // Maps to: kernel_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Maps to: bias_initializer(Keras)
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      kernel_regularizer: { // Only Keras
        name: 'Kernel regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      bias_regularizer: { // Only Keras
        name: 'Bias regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      activity_regularizer: { // Only Keras
        name: 'Activity regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      kernel_constraint: { // Only Keras
        name: 'Kernel constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      bias_constraint: { // Only Keras
        name: 'Bias constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      use_bias: { // Maps to: bias_term(Caffe)
        name: 'Use bias term',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  Dropout: {
    name: 'dropout',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Embed: {
    name: 'embed',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true
      },
      input_dim: {
        name: 'Input Dimensions',
        value: '',
        type: 'number',
        required: true
      },
      weight_filler: { // Maps to: embeddings_initializer(Keras)
        name: 'Weight filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_filler: { // Only Caffe
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_term: { // Only Caffe
        name: 'Bias Term',
        value: false,
        type: 'checkbox',
        required: false
      },
      embeddings_regularizer: { // Only Keras
        name: 'Embeddings regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      embeddings_constraint: { // Only Keras
        name: 'Embeddings constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      mask_zero: { // Only Keras
        name: 'Mask Zero',
        value: false,
        type: 'checkbox',
        required: false
      },
      input_length: { // Only Keras
        name: 'Input Length',
        value: null,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  /* ********** Normalisation Layers ********** */
  LRN: { // Only Caffe
    name: 'lrn',
    color: '#ffeb3b',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      local_size: {
        name: 'Local Size',
        value: 5,
        type: 'number',
        required: false
      },
      alpha: {
        name: 'Alpha',
        value: 1.0,
        type: 'float',
        required: false
      },
      beta: {
        name: 'Beta',
        value: 0.75,
        type: 'float',
        required: false
      },
      k: {
        name: 'K',
        value: 1.0,
        type: 'float',
        required: false
      },
      norm_region: {
        name: 'Norm Region',
        value: 'ACROSS_CHANNELS',
        type: 'select',
        options: ['ACROSS_CHANNELS', 'WITHIN_CHANNEL'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  MVN: { // Only Caffe
    name: 'mvn',
    color: '#ffeb3b',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      normalize_variance: {
        name: 'Normalize Variance',
        value: false,
        type: 'checkbox',
        required: false
      },
      across_channels: {
        name: 'Across Channels',
        value: false,
        type: 'checkbox',
        required: false
      },
      eps: {
        name: 'Epsilon',
        value: 1e-9,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  BatchNorm: {
    name: 'batchnorm',
    color: '#ffeb3b',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      use_global_stats: { // Only Caffe
        name: 'Use Global Stats',
        value: false,
        type: 'checkbox',
        required: true
      },
      moving_average_fraction: { // Maps to: momentum(Keras)
        name: 'Moving Avg. Fraction',
        value: 0.999,
        type: 'float',
        required: false
      },
      eps: {
        name: 'Epsilon',
        value: 1e-5,
        type: 'float',
        required: false
      },
      moving_mean_initializer: { // Only Keras
        name: 'Moving Mean Initializer',
        value: 'Zeros',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity', 
        'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      moving_variance_initializer: { // Only Keras
        name: 'Moving Variance Initializer',
        value: 'Ones',
        type: 'select',
        options: ['Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
        'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  /* ********** Noise Layers ********** */

  GaussianNoise: { // Only Keras
    name: 'gaussian noise',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      stddev: {
        name: 'stddev',
        value: '',
        type: 'number',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  GaussianDropout: { // Only Keras
    name: 'gaussian dropout',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      rate: {
        name: 'rate',
        value: '',
        type: 'number',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  AlphaDropout: { // Only Keras
    name: 'alpha dropout',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      rate: {
        name: 'rate',
        value: '',
        type: 'number',
        required: true
      },
      seed: {
        name: 'seed',
        value: null,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  /* ********** Activation/Neuron Layers ********** */
  ReLU: {
    name: 'relu',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      negative_slope: {
        name: 'Negative slope',
        value: 0,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  PReLU: {
    name: 'prelu',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      channel_shared: {
        name: 'Channel Shared',
        value: false,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  ELU: {
    name: 'elu',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      alpha: {
        name: 'Alpha',
        value: 1,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  ThresholdedReLU: { 
    name: 'Thresholded ReLU',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      theta: {
        name: 'Theta',
        value: 1,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Sigmoid: {
    name: 'sigmoid',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  TanH: {
    name: 'tanh',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  SELU: { // Only Keras
    name: 'selu',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Softplus: { // Only Keras
    name: 'softplus',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Softsign: { // Only Keras
    name: 'softsign',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  HardSigmoid: { // Only Keras
    name: 'hard sigmoid',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  AbsVal: { // Only Caffe
    name: 'absval',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Power: { // Only Caffe
    name: 'power',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      power: {
        name: 'Power',
        value: 1.0,
        type: 'float',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      shift: {
        name: 'Shift',
        value: 0.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Exp: { // Only Caffe
    name: 'exp',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      base: {
        name: 'Base',
        value: -1.0,
        type: 'float',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      shift: {
        name: 'Shift',
        value: 0.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Log: { // Only Caffe
    name: 'log',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      base: {
        name: 'Base',
        value: -1.0,
        type: 'float',
        required: false
      },
      scale: {
        name: 'Scale',
        value: 1.0,
        type: 'float',
        required: false
      },
      shift: {
        name: 'Shift',
        value: 0.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  BNLL: { // Only Caffe
    name: 'bnll',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Threshold: { // Only Caffe
    name: 'threshold',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false
      },
      threshold: {
        name: 'threshold',
        value: 0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Bias: { // Only Caffe
    name: 'bias',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      num_axes: {
        name: 'Number of Axis',
        value: 1,
        type: 'number',
        required: false
      },
      filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  Scale: { // Only Caffe
    name: 'scale',
    color: '#009688',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      num_axes: { // Only Caffe
        name: 'Num Axes',
        value: 1,
        type: 'number',
        required: false
      },
      filler: { // Maps to: gamma_initializer(Keras)
        name: 'Filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      bias_term: { // Maps to: center(Keras)
        name: 'Bias term',
        value: false,
        type: 'checkbox',
        required: false
      },
      scale: { // Only Keras
        name: 'Scale',
        value: true,
        type: 'checkbox',
        required: false
      },
      bias_filler: { // Maps to: beta_initializer(Keras)
        name: 'Bias Filler',
        value: 'constant',
        type: 'select',
        options: [//Caffe
                  'constant', 'gaussian', 'positive_unitball', 'uniform', 'xavier', 'msra', 'bilinear',
                  //Keras
                  'Zeros', 'Ones', 'Constant', 'RandomNormal', 'RandomUniform', 'TruncatedNormal', 'VarianceScaling', 'Orthogonal', 'Identity',
                  'lecun_uniform', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform'],
        required: false
      },
      gamma_regularizer: { // Only Keras
        name: 'Gamma regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      beta_regularizer: { // Only Keras
        name: 'Beta regularizer',
        value: 'None',
        type: 'select',
        options: ['None', 'l1', 'l2', 'l1_l2'],
        required: false
      },
      gamma_constraint: { // Only Keras
        name: 'Gamma constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      beta_constraint: { // Only Keras
        name: 'Beta constraint',
        value: 'None',
        type: 'select',
        options: ['None', 'max_norm', 'non_neg', 'unit_norm'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  /* ********** Utility Layers ********** */
  Flatten: {
    name: 'flatten',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      end_axis: {
        name: 'End Axis',
        value: -1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Reshape: {
    name: 'reshape',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  BatchReindex: { // Only Caffe
    name: 'Batch Reindex',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Split: { // Only Caffe
    name: 'Split',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Concat: {
    name: 'concat',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Slice: { // Only Caffe
    name: 'slice',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg : ['Top']
    },
    params: {
      slice_point: {
        name: 'Slice Point',
        value: '',
        type: 'text',
        required: true
      },
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      slice_dim: {
        name: 'Slice Dim',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Eltwise: {
    name: 'eltwise',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      layer_type: {
        name: 'Eltwise method',
        value: 'Sum',
        type: 'select',
        options: ['Product', 'Sum', 'Maximum', 'Average', 'Dot'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Filter: { // Only Caffe
    name: 'filter',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  // This layer is currently not supported as there is no bottom blob
  Parameter: { // Only Caffe
    name: 'parameter',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg : ['Top']
    },
    params: {
      shape: {
        name: 'Shape',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: true
  },
  Reduction: { // Only Caffe
    name: 'reduction',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      operation: {
        name: 'Reduction operation',
        value: 'SUM',
        type: 'select',
        options: ['SUM', 'ASUM', 'SUMSQ', 'MEAN'],
        required: false
      },
      axis: {
        name: 'Axis',
        value: 0,
        type: 'number',
        required: false
      },
      coeff: {
        name: 'Coefficient',
        value: 1.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Silence: { // Only Caffe
    name: 'silence',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  ArgMax: { // Only Caffe
    name: 'argmax',
    color: '#03a9f4',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      out_max_val: {
        name: 'Output Max Value',
        value: false,
        type: 'checkbox',
        required: false
      },
      top_k: {
        name: 'Top-K',
        value: 1,
        type: 'number',
        required: false
      },
      axis: {
        name: 'Axis',
        value: 0,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Softmax: {
    name: 'softmax',
    color: '#03a9f4',
    endpoint: {
      src: [],
      trg: ['Top']

    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Permute: { // Only Keras
    name: 'permute',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  RepeatVector: { // Only Keras
    name: 'repeat vector',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      n: {
        name: 'Times repeat',
        value: '',
        type: 'number',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Regularization: { // Only Keras
    name: 'regularization',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      l1: {
        name: 'L1',
        value: 0.0,
        type: 'float',
        required: false
      },
      l2: {
        name: 'L2',
        value: 0.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Masking: { // Only Keras
    name: 'masking',
    color: '#ff9800',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      mask_value: {
        name: 'Mask value',
        value: 0.0,
        type: 'float',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: false,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  /* ********** Loss Layers ********** */
  MultinomialLogisticLoss: { // Only Caffe
    name: 'multinomial logistic loss',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']

    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  InfogainLoss: { // Only Caffe
    name: 'infogain loss',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']
    },
    params: {
      source: {
        name: 'source',
        value: '',
        type: 'text',
        required: true
      },
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  SoftmaxWithLoss: { // Only Caffe
    name: 'softmax loss',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']

    },
    params: {
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  EuclideanLoss: { // Only Caffe
    name: 'euclidean loss',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']

    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  HingeLoss: { // Only Caffe
    name: 'hinge loss',
    color: '#f44336',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      norm: {
        name: 'Norm',
        value: 'L1',
        type: 'select',
        options: ['L1', 'L2'],
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  SigmoidCrossEntropyLoss: { // Only Caffe
    name: 'sigmoid cross entropy loss',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']
    },
    params: {
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  Accuracy: { // Only Caffe
    name: 'acc',
    color: '#f44336',
    endpoint: {
      src: [],
      trg: ['Top']

    },
    params: {
      top_k: {
        name: 'Top-K',
        value: 1,
        type: 'number',
        required: false
      },
      axis: {
        name: 'Axis',
        value: 1,
        type: 'number',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  ContrastiveLoss: { // Only Caffe
    name: 'contrastive loss',
    color: '#f44336',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']

    },
    params: {
      legacy_version: {
        name: 'Legacy',
        value: false,
        type: 'checkbox',
        required: false
      },
      margin: {
        name: 'Margin',
        value: 1.0,
        type: 'float',
        required: false
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  },
  /* ********** Python Layer ********** */
  Python: { // Only Caffe
    name: 'python',
    color: '#f44336',
    endpoint: {
      src: ['Bottom'],
      trg: ['Top']
    },
    params: {
      layer: {
        name: 'Layer',
        value: '',
        type: 'text',
        required: true
      },
      module: {
        name: 'Module',
        value: '',
        type: 'text',
        required: true
      },
      param_str: {
        name: 'param_str',
        value: '',
        type: 'text',
        required: true
      },
      caffe: {
        name: 'Available Caffe',
        value: true,
        type: 'checkbox',
        required: false
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text'
      }
    },
    learn: false
  }
};
