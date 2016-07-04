export default {
  Data: {
    name: 'input',
    color: '#5b80bf',
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
    color: '#459046',
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
    color: '#8cc556',
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
      kernel_size: {
        name: 'Kernel size',
        value: '',
        type: 'number',
        required: true,
      },
      stride: {
        name: 'Stride',
        value: '',
        type: 'number',
        required: false,
      },
      pad: {
        name: 'Padding size',
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
    color: '#eadd66',
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
    color: '#d28240',
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
    color: '#ac4cc5',
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
    color: '#e15e4f',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
      pad: {
        name: 'Padding size',
        value: '',
        type: 'number',
        required: false,
      },
      kernel_size: {
        name: 'Kernel size',
        value: '',
        type: 'number',
        required: true,
      },
      stride: {
        name: 'Stride',
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
};
