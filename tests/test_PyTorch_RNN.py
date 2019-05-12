# Run from home directory with python -m pytest tests
import shutil
import pytest
import torch
import random
import numpy as np
import torch.nn as nn

from nn_builder.pytorch.RNN import RNN
import torch.optim as optim
from torchvision import datasets, transforms


def test_user_hidden_layers_input_rejections():
    """Tests whether network rejects invalid hidden_layers inputted from user"""

    inputs_that_should_fail = [[["linearr", 33]], [["linear", 12, 33]], [["gru", 2, 33]], [["lstm", 2, 33]], [["lstmr", 33]],
                               [["gruu", 33]], [["gru", 33], ["xxx", 33]] ]
    for input in inputs_that_should_fail:
        with pytest.raises(AssertionError):
            RNN(input_dim=1, layers=input, hidden_activations="relu",
                output_activation="relu")

def test_user_hidden_layers_input_acceptances():
    """Tests whether network rejects invalid hidden_layers inputted from user"""
    inputs_that_should_work = [[["linear", 33]], [["linear", 12]], [["gru", 2]], [["lstm", 2]], [["lstm", 1]],
                               [["gru", 330]], [["gru", 33], ["linear", 2]] ]
    for input in inputs_that_should_work:
        assert  RNN(input_dim=1, layers=input, hidden_activations="relu",
                output_activation="relu")


def test_hidden_layers_created_correctly():
    """Tests that create_hidden_layers works correctly"""
    layers = [["gru", 25], ["lstm", 23], ["linear", 5], ["linear", 10]]

    rnn = RNN(input_dim=5, layers=layers, hidden_activations="relu",
              output_activation="relu")

    assert type(rnn.hidden_layers[0]) == nn.GRU
    assert rnn.hidden_layers[0].input_size == 5
    assert rnn.hidden_layers[0].hidden_size == 25

    assert type(rnn.hidden_layers[1]) == nn.LSTM
    assert rnn.hidden_layers[1].input_size == 25
    assert rnn.hidden_layers[1].hidden_size == 23

    assert type(rnn.hidden_layers[2]) == nn.Linear
    assert rnn.hidden_layers[2].in_features == 23
    assert rnn.hidden_layers[2].out_features == 5

    assert type(rnn.output_layers[0]) == nn.Linear
    assert rnn.output_layers[0].in_features == 5
    assert rnn.output_layers[0].out_features == 10


def test_output_layers_created_correctly():
    """Tests that create_output_layers works correctly"""
    layers = [["gru", 25], ["lstm", 23], ["linear", 5], ["linear", 10]]

    rnn = RNN(input_dim=5, layers=layers, hidden_activations="relu", output_activation="relu")

    assert rnn.output_layers[0].in_features == 5
    assert rnn.output_layers[0].out_features == 10

    layers = [["gru", 25], ["lstm", 23], ["lstm", 10]]

    rnn = RNN(input_dim=5, layers=layers, hidden_activations="relu",
              output_activation="relu")

    assert rnn.output_layers[0].input_size == 23
    assert rnn.output_layers[0].hidden_size == 10

    layers = [["gru", 25], ["lstm", 23], [["lstm", 10], ["linear", 15]]]
    rnn = RNN(input_dim=5, layers=layers, hidden_activations="relu",
              output_activation="relu")

    assert rnn.output_layers[0].input_size == 23
    assert rnn.output_layers[0].hidden_size == 10

    assert rnn.output_layers[1].in_features == 23
    assert rnn.output_layers[1].out_features == 15
