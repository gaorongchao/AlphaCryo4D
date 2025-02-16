#!/bin/env python

import os
import argparse
import time
import mrcfile as mf
import numpy as np
from sklearn.preprocessing import StandardScaler


if __name__ == '__main__':
    starttime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', type=str, default='./maps_aligned/',
                        help='folder of maps')
    parser.add_argument('--std', '-s', type=bool, default=True,
                        help='if standardize the maps')
    args = parser.parse_args()
    path = args.folder # the folder of maps

    pwd = os.getcwd()
    print(pwd)
    files = list(filter(lambda f: os.path.splitext(f)[1] == '.mrc', os.listdir(path)))
    os.chdir(path)
    with mf.open(files[0], mode='r') as mrc:
        n = mrc.data.shape[0] # box size of maps
    fp = np.memmap(pwd + '/rdata.dat', dtype='float32', mode='w+', shape=(len(files), n**3))
    fp3d = np.memmap(pwd + '/rdata_3d.dat', dtype='float32', mode='w+', shape=(len(files), n, n, n))

    for n,file in enumerate(files):
        if os.path.isfile(file):
            mrc = mf.mrcfile.MrcFile(file,mode='r')
            nmrc = mrc.data
            fp3d[n] = nmrc
            nmrc=np.reshape(nmrc,(-1,1))
            if args.std:
                scaler = StandardScaler().fit(nmrc) # normalization
                nmrc_norm = scaler.transform(nmrc)
            fp[n] = np.ravel(nmrc_norm)
            with open(pwd + '/data.log', mode='a+') as f:
                f.write('%d %s\n' % (n+1, file))

    os.chdir(pwd)
    np.save('rdata_3d.npy', fp3d) # output npy file
    np.save('rdata.npy', fp)

    endtime=time.time()
    print('time spent:', endtime-starttime)
