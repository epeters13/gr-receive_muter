#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <Edwin G. W. Peters -- edwin.g.w.peters<at>gmail.com>.
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
# 

import numpy as np
from gnuradio import gr
import pmt

class transmit_level_detector_cc(gr.sync_block):
    """
    Sends mute or unmute commands out based on the signal magnitude of the input.
    This works best when the signal is pre-padded and post-padded with low power white noise
    The commands can be routed to the 'Receive mute' block
    """
    def __init__(self, threshold):
        gr.sync_block.__init__(self,
                               name="transmit_level_detector_cc",
                               in_sig=[np.complex64],
                               out_sig=[np.complex64])

        self.message_port_register_out(pmt.intern('set_mute'))
        self.message_port_register_out(pmt.intern('clear_mute'))
        self.threshold = threshold



        
    def work(self, input_items, output_items):

        output_items[0][:] = input_items[0]
        n = len(output_items[0][:])
        mval = np.max(np.abs(input_items[0]))
        if mval > self.threshold:
            self.message_port_pub(pmt.intern('set_mute'),pmt.to_pmt(n))
        else:
            self.message_port_pub(pmt.intern('clear_mute'),pmt.to_pmt(n))
            
        return len(output_items[0])

