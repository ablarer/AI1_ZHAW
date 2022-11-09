import pickle
import numpy as np
import matplotlib.pyplot as plt


def load_data(path, train_fraction=0.25):
    """ load nasa features 
    
    """
    with open(path, "rb") as pfile:
        data = pickle.load(pfile)

    # calculate novelty signal with the given novelty predictor
    num_samples = data.shape[0]

    num_train = int(num_samples * train_fraction)
    num_sensor = 1

    X_train = data[:num_train, : , :]
    #X_test = data[num_train:,:,:]
    X_test = data[:,:,:]
    return X_train, X_test


def scale(X, samples=None, robust=True, axis=0):
    """
    Scales the data by a (robust) z-transformation over the axis 0 ("over time")

    :param X: data to be scaled
    :param samples: number of samples for None, take all
    :param robust: use median/mad or mean/std for the transformation
    :param axis: scale over the given axis
    :return:
    """
    orgType = X.dtype
    X = np.asarray(X, dtype='float64')
    if samples is None or axis == 1:
        samples = np.shape(X)[0]
    if axis == 1:
        X = np.transpose(X)
    if robust:
        center = np.median(X[0:samples], axis=0)
        # For the scaling factor 1.4826 see e.g. https://en.wikipedia.org/wiki/Median_absolute_deviation
        scaled = 1.4826 * np.median(np.absolute(X[0:samples] - center), axis=0)
    else:
        center = np.average(X[0:samples], axis=0)
        scaled = np.std(X[0:samples], axis=0)
    XS = (X - center) / (scaled + 1E-10) #small constant for numerical stability
    if axis == 1:
        XS = np.transpose(XS)
    if orgType != np.dtype('float64'):
        XS = np.asarray(XS, dtype=orgType)
    return XS


def gen_minibatches(inputs, targets, batchsize, shuffle=False):
    """
    Generator that yield mini-batches.

    :param inputs:
    :param targets:
    :param batchsize:
    :param shuffle:
    :return:
    """
    assert len(inputs) == len(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)
        yield inputs[excerpt], targets[excerpt]


def plot_spectrogram_features(features, start_idx=0, title=""):
    """
    :param features: spectrogram features
    :param title: Plot title
    :return: 
    """

    num_sensors = features.shape[2]
    fig, axarr = plt.subplots(num_sensors, sharex=False, figsize=(12, 4 * np.ceil(num_sensors / 2.0)))
    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.08)

    for sensor in range(num_sensors):
        Xd = np.asarray(features[:, :, sensor])
        curr_sensor = axarr[sensor].imshow(np.log(np.transpose(np.abs(Xd))), aspect='auto', cmap='jet')
        axarr[sensor].set_title("Sensor {}".format(sensor))
        axarr[sensor].set_xlabel("time (in frames)")
        axarr[sensor].set_ylabel("features")
        axarr[sensor].set_xlim(start_idx,features.shape[0])
        plt.colorbar(curr_sensor, ax=axarr[sensor])

    fig.tight_layout()
    plt.show()


def plot_reconstruction_error(errors):
    fig, axarr = plt.subplots(sharex=False, figsize=(12, 8))
    fig.suptitle("Reconstruction error", fontsize=14, fontweight='bold', y=1.08)

    axarr.plot(np.abs(errors)[5:-5])
    axarr.set_ylim(0, 85)
    axarr.set_xlim(0, 850)
    axarr.set_xlabel('frame')
    axarr.set_ylabel("error")

    plt.show()
