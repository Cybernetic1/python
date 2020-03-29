# Neuromancer --- a permutation-invariant ANN module

## Acknowledgement

The genetic algorithm for evolving neural networks is adopted from the Github [NeuralGenetic](https://github.com/ahmedfgad/NeuralGenetic) repository by Ahmed Fawzy Gad.   He has written a detailed tutorial about this technique.

## Running

Requires `Python 3`, `numpy`, and `pickle`, also:

    pip3 install matplotlib
    
 To execute:
 
     python3 evolve_Neuromancer.py
     
## Parameters

In file `evolve_Neuromancer.py`:

* `num_generations`

* `method` can be "sigmoid" or "ReLU" 

* **topology of the ANN** is defined in the beginning section, `HL1_neurons`,  etc...

In file `ANN.py`:

* N = dimension of input / output vectors of the ANN

* in function `joint_penalty`, k = "steepness" can be adjusted from 1.0 to > 30.0

## About the loss function

