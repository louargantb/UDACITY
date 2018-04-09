import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Input
from keras.layers import LSTM
from keras import backend as K
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = [[series[i+j] for j in range(0, window_size)] for i in range(len(series)-window_size)]
    y = [[series[i]] for i in range(window_size, len(series))]

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size, lstm_size=5):
    # Clear session before creating a new model
    K.clear_session()
    inputs = Input(shape=(window_size, 1))
    _lstm = LSTM(lstm_size)(inputs)
    outputs = Dense(1)(_lstm)
    return Model(inputs, outputs)


# TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    text = text.lower() \
        .replace('"', ' ') \
        .replace("'", ' ') \
        .replace('%', ' ') \
        .replace('è', ' ') \
        .replace('â', ' ') \
        .replace('à', ' ') \
        .replace('$', ' ') \
        .replace('@', ' ') \
        .replace('&', ' ') \
        .replace('é', ' ') \
        .replace('*', ' ') \
        .replace('1', ' ') \
        .replace('2', ' ') \
        .replace('3', ' ') \
        .replace('4', ' ') \
        .replace('5', ' ') \
        .replace('6', ' ') \
        .replace('7', ' ') \
        .replace('8', ' ') \
        .replace('9', ' ') \
        .replace('(', ' ') \
        .replace(')', ' ')
    return text


### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    pass
