# Original Author    : Edwin G. W. Peters @ sdr-Surface-Book-2
#   Creation date    : Tue Jun 16 11:03:51 2020 (+1000)
#   Email            : edwin.g.w.peters<at>gmail.com
# ------------------------------------------------------------------------------
# Last-Updated       : Thu Jun 18 15:12:37 2020 (+1000)
#           By       : Edwin G. W. Peters @ sdr-Surface-Book-2
# ------------------------------------------------------------------------------
# File Name          : send_test_sig.py
# Description        : 
# ------------------------------------------------------------------------------
# Copyright          : 2020 <Edwin G. W. Peters -- edwin.g.w.peters<at>gmail.com>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# ------------------------------------------------------------------------------

import numpy as np
import zmq

def openSocket(addr):

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUSH)
    sock.bind(addr)   
    return sock


sock = openSocket('tcp://*:15512')


Fs = 16*7400

Fc = 1000
Fc2 = 500
Fc3 = 800
sigLen = 2
sigLen2 = 1
sigLen3 = 0.03

lenS = int(Fs * sigLen)
lenS2 = int(Fs * sigLen2)
lenS3 = int(Fs * sigLen3)

sig = np.exp(1j*2*np.pi*np.arange(lenS)*Fc/Fs)
sig3 = np.exp(1j*2*np.pi*np.arange(lenS3)*Fc3/Fs)
sig2 = np.exp(1j*2*np.pi*np.arange(lenS2)*Fc2/Fs)
sig = np.r_[0.00001*sig2,sig,0.00001*sig2,sig3,sig2*0.0001,sig3,sig2*0.0001,sig3,sig2*0.0001,sig3,sig2*0.0001,sig3,sig2*0.0001]
sock.send(sig.astype(np.complex64).tobytes())
