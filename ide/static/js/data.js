export default {
  Data: {
    name: 'data',
    color: 'rgb(255, 204, 60)',
    endpoint: {
      src: ['RightMiddle'],
      trg: [],
    },
    params: {
      source: {
        name: 'Data source',
        value: '',
        type: 'text',
        required: true,
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true,
      },
      backend: {
        name: 'Backend',
        value: 'LMDB',
        type: 'select',
        options: ['LMDB', 'LEVELDB'],
        required: true,
      },
      scale: {
        name: 'Scale',
        value: '',
        type: 'float',
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  SoftmaxWithLoss: {
    name: 'loss',
    color: 'rgb(38, 105, 40)',
    endpoint: {
      src: [],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Convolution: {
    name: 'conv',
    color: 'rgb(87, 160, 17)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true,
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: true,
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true,
      },
      stride_h: {
        name: 'Stride height',
        value: '',
        type: 'number',
        required: false,
      },
      stride_w: {
        name: 'Stride width',
        value: '',
        type: 'number',
        required: false,
      },
      pad_h: {
        name: 'Padding height',
        value: '',
        type: 'number',
        required: false,
      },
      pad_w: {
        name: 'Padding width',
        value: '',
        type: 'number',
        required: false,
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Deconvolution: {
    name: 'deconv',
    color: 'rgb(87, 100, 17)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true,
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: true,
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true,
      },
      stride_h: {
        name: 'Stride height',
        value: '',
        type: 'number',
        required: false,
      },
      stride_w: {
        name: 'Stride width',
        value: '',
        type: 'number',
        required: false,
      },
      pad_h: {
        name: 'Padding height',
        value: '',
        type: 'number',
        required: false,
      },
      pad_w: {
        name: 'Padding width',
        value: '',
        type: 'number',
        required: false,
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  ReLU: {
    name: 'relu',
    color: 'rgb(77, 101, 214)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      inplace: {
        name: 'Inplace operation',
        value: true,
        type: 'checkbox',
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Accuracy: {
    name: 'acc',
    color: 'rgb(164, 218, 35)',
    endpoint: {
      src: [],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  InnerProduct: {
    name: 'fc',
    color: 'rgb(144, 29, 204)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true,
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Pooling: {
    name: 'pool',
    color: 'rgb(228, 50, 50)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      pad_h: {
        name: 'Padding height',
        value: '',
        type: 'number',
        required: false,
      },
      pad_w: {
        name: 'Padding width',
        value: '',
        type: 'number',
        required: false,
      },
      kernel_h: {
        name: 'Kernel height',
        value: '',
        type: 'number',
        required: true,
      },
      kernel_w: {
        name: 'Kernel width',
        value: '',
        type: 'number',
        required: true,
      },
      stride_h: {
        name: 'Stride height',
        value: '',
        type: 'number',
        required: false,
      },
      stride_w: {
        name: 'Stride width',
        value: '',
        type: 'number',
        required: false,
      },
      pool: {
        name: 'Pooling method',
        value: 'MAX',
        type: 'select',
        options: ['MAX', 'AVE', 'STOCHASTIC'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Dropout: {
    name: 'dropout',
    color: 'rgb(222, 29, 189)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Concat: {
    name: 'concat',
    color: 'rgb(255, 146, 52)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Eltwise: {
    name: 'eltwise',
    color: 'rgb(255, 146, 100)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      operation: {
        name: 'Eltwise method',
        value: 'SUM',
        type: 'select',
        options: ['SUM', 'PROD', 'Max'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Crop: {
    name: 'crop',
    color: 'rgb(255, 250, 100)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      axis: {
        name: 'axis',
        value: '2',
        type: 'number',
        required: false,
      },
      offset: {
        name: 'offset',
        value: '0',
        type: 'number',
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  LRN: {
    name: 'lrn',
    color: 'rgb(29, 177, 222)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Softmax: {
    name: 'softmax',
    color: 'rgb(167, 163, 163)',
    endpoint: {
      src: [],
      trg: ['LeftMiddle'],
    },
    params: {
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  Input: {
    name: 'input',
    color: 'rgb(255, 204, 60)',
    endpoint: {
      src: ['RightMiddle'],
      trg: [],
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  LSTM: {
    name: 'lstm',
    color: 'rgb(1, 116, 121)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true,
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Embed: {
    name: 'embed',
    color: 'rgb(23, 212, 90)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      num_output: {
        name: 'No of outputs',
        value: '',
        type: 'number',
        required: true,
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
        required: false,
      },
      bias_term: {
        name: 'Bias Term',
        value: 'False',
        type: 'select',
        options: ['True', 'False'],
        required: false,
      },
      input_dim: {
        name: 'Input Dimensions',
        value: '',
        type: 'number',
        required: true,
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Reshape: {
    name: 'reshape',
    color: 'rgb(134, 44, 44)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      dim: {
        name: 'Dim',
        value: '',
        type: 'text',
        required: true,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  HDF5Data: {
    name: 'hdf5data',
    color: 'rgb(241, 206, 38)',
    endpoint: {
      src: ['RightMiddle'],
      trg: [],
    },
    params: {
      source: {
        name: 'HDF5 Data source',
        value: '',
        type: 'text',
        required: true,
      },
      batch_size: {
        name: 'Batch size',
        value: '',
        type: 'number',
        required: true,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: false,
  },
  BatchNorm: {
    name: 'batchnorm',
    color: 'rgb(31, 218, 45)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      use_global_stats: {
        name: 'Use Global Stats',
        value: '',
        type: 'select',
        options: ['true', 'false'],
        required: true,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Scale: {
    name: 'scale',
    color: 'rgb(243, 75, 214)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      bias_term: {
        name: 'Bias term',
        value: '',
        type: 'select',
        options: ['true', 'false'],
        required: true,
      },
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
  Eltwise: {
    name: 'elementwise',
    color: 'rgb(162, 146, 27)',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      operation: {
        name: 'Operation',
        value: '',
        type: 'select',
        options: ['Product', 'Sum', 'Max'],
        required: true,
      }
    },
    props: {
      name: {
        name: 'Name',
        value: '',
        type: 'text',
      },
    },
    learn: true,
  },
};
