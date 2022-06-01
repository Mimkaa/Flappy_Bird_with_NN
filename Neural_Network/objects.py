from .matrix import Matrix
import pickle
import os
import copy
import random
import math

def sigmoid(x):
    return 1/(1 + math.exp(-x))

def derivative_signoid(y):
    #return sigmoid(x) * (1 - sigmoid(x))
    return y * (1 - y)


class NeuralNetwork:
    def __init__(self, inputs, hidden, outputs):
        self.inputs = inputs
        self.hidden = hidden
        self.outputs = outputs

        self.weights_input_hidden = Matrix(self.hidden, self.inputs)
        self.weights_hidden_output = Matrix(self.outputs, self.hidden)
        self.weights_hidden_output.randomize()
        self.weights_input_hidden.randomize()

        self.bias_hidden = Matrix(self.hidden,1)
        self.bias_output = Matrix(self.outputs,1)
        self.bias_output.randomize()
        self.bias_hidden.randomize()

        self.learning_rate = 0.1

    def feed_forward(self, input_array):
        # generating the hidden outputs
        inputs = Matrix.from_Array(input_array)
        hidden = Matrix.multiply_mats(self.weights_input_hidden, inputs)

        hidden.add(self.bias_hidden)
        # activation function
        hidden.map(sigmoid)

        # generating the output`s outputs
        output = Matrix.multiply_mats(self.weights_hidden_output, hidden)
        output.add(self.bias_output)
        output.map(sigmoid)

        return output.to_Array()

    def train(self, input_array, target_array):
        # generating the hidden outputs
        inputs = Matrix.from_Array(input_array)

        hidden = Matrix.multiply_mats(self.weights_input_hidden, inputs)

        hidden.add(self.bias_hidden)
        # activation function
        hidden.map(sigmoid)

        # generating the output`s outputs
        outputs = Matrix.multiply_mats(self.weights_hidden_output, hidden)
        outputs.add(self.bias_output)
        outputs.map(sigmoid)

        # calculate the error
        # error = target - output
        targets = Matrix.from_Array(target_array)
        output_errors = Matrix.subtract(targets, outputs)
        #gradients = outputs * (1 - outputs)
        # gradient for outputs
        gradients = Matrix.map_static(outputs, derivative_signoid)
        gradients.multiply(output_errors)
        gradients.multiply(self.learning_rate)

        # calculate deltas
        hidden_transposed = Matrix.transpose(hidden)
        weights_hidden_output_deltas = Matrix.multiply_mats(gradients, hidden_transposed)
        # adjust the weights by deltas
        self.weights_hidden_output.add(weights_hidden_output_deltas)
        # adjust its bias by its deltas
        self.bias_output.add(gradients)

        # hidden layer errors
        weights_hidden_output_transposed = Matrix.transpose(self.weights_hidden_output)
        hidden_errors = Matrix.multiply_mats(weights_hidden_output_transposed,output_errors)
        # hidden gradient
        hidden_gradient = Matrix.map_static(hidden, derivative_signoid)
        hidden_gradient.multiply(hidden_errors)
        hidden_gradient.multiply(self.learning_rate)

        # input -> hidden deltas
        inputs_transpose = Matrix.transpose(inputs)
        weights_input_hidden_deltas = Matrix.multiply_mats(hidden_gradient, inputs_transpose)

        self.weights_input_hidden.add(weights_input_hidden_deltas)
        # adjust its bias by its deltas
        self.bias_hidden.add(hidden_gradient)

    def predict(self, inputs_array):
        return self.feed_forward(inputs_array)

    def copy(self):
        return copy.deepcopy(self)

    def mutate(self, rate):
        def mutation(val):
            if random.uniform(0,1) < rate:
                return val + random.gauss(0, 0.1)
            else:
                return val
        self.weights_input_hidden.map(mutation)
        self.weights_hidden_output.map(mutation)
        self.bias_hidden.map(mutation)
        self.bias_output.map(mutation)

    def serialize(self):
        serialized = pickle.dumps(self)
        with open("best_bird.txt", "wb") as f:
            f.write(serialized)

    def deserialize(self):
        with open("best_bird.txt", "rb") as f:
            obj = pickle.load(f)
        return obj





