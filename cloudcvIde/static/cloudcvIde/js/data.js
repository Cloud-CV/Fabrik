export default {
  input: {
    name: 'input',
    color: '#5b80bf',
    endpoint: {
      src: ['RightMiddle'],
      trg: [],
    },
    params: {
      train_source: {
        name: 'Train data source',
        value: '',
        type: 'text',
      },
      train_batch_size: {
        name: 'Train batch size',
        value: '',
        type: 'number',
      },
      backend: {
        name: 'Backend',
        value: 'LMDB',
        type: 'select',
        options: ['LMDB', 'LEVELDB'],
      },
      scale: {
        name: 'Scale',
        value: '',
        type: 'float',
      },
      test_source: {
        name: 'Test data source',
        value: '',
        type: 'text',
      },
      test_batch_size: {
        name: 'Test batch size',
        value: '',
        type: 'number',
      },
    },
  },
  loss: {
    name: 'loss',
    color: '#459046',
    endpoint: {
      src: [],
      trg: ['LeftMiddle'],
    },
    params: {
    },
  },
  conv: {
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
      },
      kernel_size: {
        name: 'Kernel size',
        value: '',
        type: 'number',
      },
      stride: {
        name: 'Stride',
        value: '',
        type: 'number',
      },
      pad: {
        name: 'Padding size',
        value: '',
        type: 'number',
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
      },
    },
  },
  relu: {
    name: 'relu',
    color: '#eadd66',
    endpoint: {
      src: ['RightMiddle'],
      trg: ['LeftMiddle'],
    },
    params: {
    },
  },
  fc: {
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
      },
      weight_filler: {
        name: 'Weight filler',
        value: 'xavier',
        type: 'select',
        options: ['xavier', 'constant'],
      },
      bias_filler: {
        name: 'Bias filler',
        value: 'constant',
        type: 'select',
        options: ['xavier', 'constant'],
      },
    },
  },
  pool: {
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
      },
      kernel_size: {
        name: 'Kernel size',
        value: '',
        type: 'number',
      },
      stride: {
        name: 'Stride',
        value: '',
        type: 'number',
      },
      pool: {
        name: 'Pooling method',
        value: 'MAX',
        type: 'select',
        options: ['MAX', 'AVE', 'STOCHASTIC'],
      },
    },
  },
};
