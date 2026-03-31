# [mnist-canvas page](https://ruiyangju.github.io/mnist-canvas/)

<p align="center">
  <img src="mnist.jpg" width="640" title="mnist">
</p>

## Introduction
A web canvas that you can draw and see the MNIST classification result distribution.

## Requirements
* Python 3.6+
* Pytorch 0.4.0+
* Pandas 0.23.4+
* NumPy 1.14.3+

## Usage
  Train the model:
  
      python3 main.py
  
  Convert pth to onnx:
  
      python3 convert.py

  optional arguments:
  
      --lr                default=1e-3    learning rate
      --epoch             default=30      number of epochs tp train for
      --trainBatchSize    default=128     training batch size
      --testBatchSize     default=128     test batch size
      --optimizer         default=adam    optimizer
