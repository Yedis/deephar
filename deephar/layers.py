import numpy as np

from keras import backend as K

from keras.layers import Input
from keras.layers import Lambda
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Activation
from keras.layers import Conv1D
from keras.layers import Conv2D
from keras.layers import Conv3D
from keras.layers import SeparableConv2D
from keras.layers import Conv2DTranspose
from keras.layers import BatchNormalization
from keras.layers import SimpleRNN
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.layers import multiply
from keras.layers import average
from keras.layers import concatenate
from keras.layers import add

from keras.layers import AveragePooling2D
from keras.layers import MaxPooling2D
from keras.layers import MaxPooling3D
from keras.layers import GlobalMaxPooling1D
from keras.layers import GlobalMaxPooling2D
from keras.layers import GlobalMaxPooling3D
from keras.layers import GlobalAveragePooling1D
from keras.layers import GlobalAveragePooling2D
from keras.layers import ZeroPadding2D

from keras.layers import UpSampling2D
from keras.layers import UpSampling3D

from keras.constraints import unit_norm
from keras.regularizers import l1

from deephar.utils.math import linspace_2d
from deephar.activations import channel_softmax_1d
from deephar.activations import channel_softmax_2d



def conv(x, filters, size, strides=(1, 1), padding='same', name=None):
    x = Conv2D(filters, size, strides=strides, padding=padding,
            use_bias=False, name=name)(x)
    return x


def deconv(x, filters, size, strides=(1, 1), padding='same', name=None):
    x = Conv2DTranspose(filters, size, strides=strides, padding=padding,
            data_format=K.image_data_format(), use_bias=False, name=name)(x)
    return x


def conv_bn(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        conv_name = name + '_conv'
    else:
        conv_name = None

    x = conv(x, filters, size, strides, padding, conv_name)
    x = BatchNormalization(axis=-1, scale=False, name=name)(x)
    return x


def conv_act(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        conv_name = name + '_conv'
    else:
        conv_name = None

    x = conv(x, filters, size, strides, padding, conv_name)
    x = Activation('relu', name=name)(x)
    return x


def conv_bn_act(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        conv_name = name + '_conv'
        bn_name = name + '_bn'
    else:
        conv_name = None
        bn_name = None

    x = conv(x, filters, size, strides, padding, conv_name)
    x = BatchNormalization(axis=-1, scale=False, name=bn_name)(x)
    x = Activation('relu', name=name)(x)
    return x


def bn_act_conv(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        bn_name = name + '_bn'
        act_name = name + '_act'
    else:
        bn_name = None
        act_name = None

    x = BatchNormalization(axis=-1, scale=False, name=bn_name)(x)
    x = Activation('relu', name=act_name)(x)
    x = conv(x, filters, size, strides, padding, name)
    return x


def act_conv_bn(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        conv_name = name + '_conv'
        act_name = name + '_act'
    else:
        conv_name = None
        act_name = None

    x = Activation('relu', name=act_name)(x)
    x = conv(x, filters, size, strides, padding, conv_name)
    x = BatchNormalization(axis=-1, scale=False, name=name)(x)
    return x


def separable_conv_bn_act(x, filters, size, strides=(1, 1), padding='same',
        name=None):
    if name is not None:
        conv_name = name + '_conv'
        bn_name = name + '_bn'
    else:
        conv_name = None
        bn_name = None

    x = SeparableConv2D(filters, size, strides=strides, padding=padding,
            use_bias=False, name=conv_name)(x)
    x = BatchNormalization(axis=-1, scale=False, name=bn_name)(x)
    x = Activation('relu', name=name)(x)
    return x


def separable_act_conv_bn(x, filters, size, strides=(1, 1), padding='same',
        name=None):
    if name is not None:
        conv_name = name + '_conv'
        act_name = name + '_act'
    else:
        conv_name = None
        act_name = None

    x = Activation('relu', name=act_name)(x)
    x = SeparableConv2D(filters, size, strides=strides, padding=padding,
            use_bias=False, name=conv_name)(x)
    x = BatchNormalization(axis=-1, scale=False, name=name)(x)
    return x


def separable_conv_bn(x, filters, size, strides=(1, 1), padding='same',
        name=None):
    if name is not None:
        conv_name = name + '_conv'
    else:
        conv_name = None

    x = SeparableConv2D(filters, size, strides=strides, padding=padding,
            use_bias=False, name=conv_name)(x)
    x = BatchNormalization(axis=-1, scale=False, name=name)(x)
    return x


def act_conv(x, filters, size, strides=(1, 1), padding='same', name=None):
    if name is not None:
        act_name = name + '_act'
    else:
        act_name = None

    x = Activation('relu', name=act_name)(x)
    x = conv(x, filters, size, strides, padding, name)
    return x

def bn_act_conv3d(x, filters, size, strides=(1, 1, 1), padding='same',
        name=None):

    if name is not None:
        bn_name = name + '_bn'
        act_name = name + '_act'
    else:
        bn_name = None
        act_name = None

    x = BatchNormalization(axis=-1, scale=False, name=bn_name)(x)
    x = Activation('relu', name=act_name)(x)
    x = Conv3D(filters, size, strides=strides, padding=padding,
            use_bias=False, name=name)(x)
    return x


def dense(x, filters, name=None):
    x = Dense(filters, kernel_regularizer=l1(0.001), name=name)(x)
    return x


def bn_act_dense(x, filters, name=None):
    if name is not None:
        bn_name = name + '_bn'
        act_name = name + '_act'
    else:
        bn_name = None
        act_name = None

    x = BatchNormalization(axis=-1, scale=False, name=bn_name)(x)
    x = Activation('relu', name=act_name)(x)
    x = Dense(filters, kernel_regularizer=l1(0.001), name=name)(x)
    return x


def act_channel_softmax(x, name=None):
    x = Activation(channel_softmax_2d(), name=name)(x)
    return x


def act_depth_softmax(x, name=None):
    x = Activation(channel_softmax_1d(), name=name)(x)
    return x


def aggregate_position_probability(inp):
    y,p = inp

    p = concatenate([p, p], axis=-1)
    yp = p * y
    yn = (1 - p) * y
    y = concatenate([yp, yn], axis=-1)

    return y


def fc_aggregation_block(y, p, name=None):
    dim = K.int_shape(y)[-1]

    x = Lambda(aggregate_position_probability, name=name)([y, p])
    x = Dense(2*dim, use_bias=False, kernel_regularizer=l1(0.0002),
            name=name + '_fc1')(x)
    x = Activation('relu', name=name + '_act')(x)
    x = Dense(dim, kernel_regularizer=l1(0.0002), name=name + '_fc2')(x)

    return x


def sparse_fc_mapping(x, input_idxs):

    num_units = len(input_idxs)
    d = Dense(num_units, use_bias=False)
    d.trainable = False
    x = d(x)

    w = d.get_weights()
    w[0].fill(0)
    for i in range(num_units):
        w[0][input_idxs[i], i] = 1.
    d.set_weights(w)

    return x

def max_min_pooling(x, strides=(2, 2), padding='same', name=None):
    if 'max_min_pool_cnt' not in globals():
        global max_min_pool_cnt
        max_min_pool_cnt = 0

    if name is None:
        name = 'MaxMinPooling2D_%d' % max_min_pool_cnt
        max_min_pool_cnt += 1

    def _max_plus_min(x):
        x1 = MaxPooling2D(strides, padding=padding)(x)
        x2 = MaxPooling2D(strides, padding=padding)(-x)
        return x1 - x2

    return Lambda(_max_plus_min, name=name)(x)

def global_max_min_pooling(x, name=None):
    if 'global_max_min_pool_cnt' not in globals():
        global global_max_min_pool_cnt
        global_max_min_pool_cnt = 0

    if name is None:
        name = 'GlobalMaxMinPooling2D_%d' % global_max_min_pool_cnt
        global_max_min_pool_cnt += 1

    def _global_max_plus_min(x):
        x1 = GlobalMaxPooling2D()(x)
        x2 = GlobalMaxPooling2D()(-x)
        return x1 - x2

    return Lambda(_global_max_plus_min, name=name)(x)


def kl_divergence_regularizer(x, rho=0.01):

    def _kl_regularizer(y_pred):
        _, rows, cols, _ = K.int_shape(y_pred)
        vmax = K.max(y_pred, axis=(1, 2))
        vmax = K.expand_dims(vmax, axis=(1))
        vmax = K.expand_dims(vmax, axis=(1))
        vmax = K.tile(vmax, [1, rows, cols, 1])
        y_delta = K.cast(K.greater_equal(y_pred, vmax), 'float32')
        return rho * K.sum(y_pred *
                (K.log(K.clip(y_pred, K.epsilon(), 1.))
                - K.log(K.clip(y_delta, K.epsilon(), 1.))) / (rows * cols)
            )

    # Build an auxiliary non trainable layer, just to use the activity reg.
    num_filters = K.int_shape(x)[-1]
    aux_conv = Conv2D(num_filters, (1, 1), use_bias=False,
            activity_regularizer=_kl_regularizer)
    aux_conv.trainable = False
    x = aux_conv(x)

    # Set identity weights
    w = aux_conv.get_weights()
    w[0].fill(0)

    for i in range(num_filters):
        w[0][0,0,i,i] = 1.

    aux_conv.set_weights(w)

    return x


def kronecker_prod(h, f, name='Kronecker_prod'):
    """ # Inputs: inp[0] (heatmaps) and inp[1] (visual features)
    """
    inp = [h, f]
    def _combine_heatmaps_visual(inp):
        hm = inp[0]
        x = inp[1]
        nj = K.int_shape(hm)[-1]
        nf = K.int_shape(x)[-1]
        hm = K.expand_dims(hm, axis=-1)
        hm = K.tile(hm, (1, 1, 1, 1, 1, nf))
        x = K.expand_dims(x, axis=-2)
        x = K.tile(x, (1, 1, 1, 1, nj, 1))
        x = hm * x
        x = K.sum(x, axis=(2, 3))
        return x
    return Lambda(_combine_heatmaps_visual, name=name)(inp)


def lin_interpolation_1d(inp):

    depth, num_filters = K.int_shape(inp)[1:]
    conv = Conv1D(num_filters, depth, use_bias=False)
    x = conv(inp)

    w = conv.get_weights()
    w[0].fill(0)

    linspace = np.linspace(0.0, 1.0, num=depth)

    for i in range(num_filters):
        w[0][:, i, i] = linspace[:]

    conv.set_weights(w)
    conv.trainable = False

    def _traspose(x):
       x = K.squeeze(x, axis=-2)
       x = K.expand_dims(x, axis=-1)
       return x
    x = Lambda(_traspose)(x)

    return x

def lin_interpolation_2d(inp, dim):

    num_rows, num_cols, num_filters = K.int_shape(inp)[1:]
    conv = SeparableConv2D(num_filters, (num_rows, num_cols), use_bias=False)
    x = conv(inp)

    w = conv.get_weights()
    w[0].fill(0)
    w[1].fill(0)
    linspace = linspace_2d(num_rows, num_cols, dim=dim)

    for i in range(num_filters):
        w[0][:,:, i, 0] = linspace[:,:]
        w[1][0, 0, i, i] = 1.

    conv.set_weights(w)
    conv.trainable = False

    x = Lambda(lambda x: K.squeeze(x, axis=1))(x)
    x = Lambda(lambda x: K.squeeze(x, axis=1))(x)
    x = Lambda(lambda x: K.expand_dims(x, axis=-1))(x)

    return x

