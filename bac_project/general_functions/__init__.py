from __future__ import division
import sys

__author__ = 'caro'



def complete_mechanismdir(mechanism_dir):
    if sys.maxsize > 2**32:
        mechanism_dir += '/x86_64/.libs/libnrnmech.so'
    else:
        mechanism_dir += '/i686/.libs/libnrnmech.so'
    return mechanism_dir


def time2idx(time, dt):
    """
    Transforms a given time into an index given that data is sampled by dt.
    :param time: Time to transform.
    :type time: float
    :param dt: Time step.
    :type dt: float
    :return: Index
    :rtype: int
    """
    assert time % dt == 0
    return int(time / dt)