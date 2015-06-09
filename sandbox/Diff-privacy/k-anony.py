#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np


def main():

    loc, scale = 0., 4.
    s = np.random.laplace(loc, scale, 1000)

    count, bins, ignored = plt.hist(s, 30, normed=True)
    x = np.arange(-8., 8., .01)
    pdf = np.exp(-abs(x-loc)/scale)/(2.*scale)
    plt.plot(x, pdf)
    plt.show()


if __name__ == '__main__':
    main()
