from time import time

from numpy import arange, mean


def set_time(times, sample_rate, samples):
    """
    times = time stamps by fifo in each payload
    sample_rate = sample rate
    samples = number of data samples
    """

    fifos = len(times)
    differences = []

    if fifos > 1:
        for index, time in enumerate(times[0:-1]):
            differences.append(times[index + 1] - time)
        delta = mean(differences) / (samples / fifos)
    else:
        delta = 1 / sample_rate
        times.append(times[0] + samples * delta)

    return arange(times[0] - ((samples / fifos)) * delta, times[-1] + delta, delta).tolist()


def get_current_timestamp():
    return time()
