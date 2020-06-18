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


class receivee_muter_cc(gr.sync_block):
    """
    This block mutes a signal based on trigger inputs. The triggers can be generated using the 'Transmit level detector' block.

    enabled: if False, the signals are passed straight throug.
    white_noise_var: the variance of the noise if mute_type set to 1
    mute_type: the type of muting to do:
    \t0 -- attenuate the signal with attenuate_dB
    \t1 -- replace with white noise with variance white_noise_var
    \t2 -- replace with zeros
    mute_time_before: time in seconds to mute before the packet
    mute_time_agter: time in seconds to mute after packets    
    """
    muted = False

    mute_log = []


    def __init__(self, enabled ,samp_rate,mute_time_after,mute_time_before,white_noise_var,mute_type,attenuate_dB):
        gr.sync_block.__init__(self,
            name="receivee_muter_cc",
            in_sig=[np.complex64],
            out_sig=[np.complex64])

        self.message_port_register_in(pmt.intern('set_mute'))
        self.message_port_register_in(pmt.intern('clear_mute'))
        # self.message_port_register_out(pmt.intern('mute_cnt'))
        self.set_msg_handler(pmt.intern('set_mute'), self.set_mute)
        self.set_msg_handler(pmt.intern('clear_mute'), self.clear_mute)

        
        self.samp_rate = samp_rate
        self.noise_std = np.sqrt(white_noise_var)
        self.attenuation_lvl = 10**(-attenuate_dB/10)
        self.enabled = enabled
        
        # self.mute_n_samples = int(mute_time*samp_rate)
        self.mute_n_samples_after = int(mute_time_after*samp_rate)
        self.mute_n_samples_before = int(mute_time_before*samp_rate)

        self.mute_type = mute_type

    def set_mute(self,msg):
        """
        check if the last state in the queue is mute. If so increment the count
        else create a new state in the end of the queue and add the count

        """
        if len(self.mute_log) > 0:
            last_state = self.mute_log[-1]['mute'] 
            if last_state == True:
                self.mute_log[-1]['count'] += pmt.to_python(msg)
                return
            else:
                self.mute_log[-1]['count'] -= self.mute_n_samples_before

        # else do
        self.mute_log.append({'mute':True,'count': self.mute_n_samples_before + self.mute_n_samples_after + pmt.to_python(msg)})
                

    def clear_mute(self,msg):
        """
        check if the last state in the queue is mute. If so increment the count
        else create a new state in the end of the queue and add the count

        """
        if len(self.mute_log) > 0:
            last_state = self.mute_log[-1]['mute'] 
            if last_state == False:
                self.mute_log[-1]['count'] += pmt.to_python(msg)
                return
        
        # else do
        self.mute_log.append({'mute':False,'count': pmt.to_python(msg)})

                
    def work(self, input_items, output_items):
        """Check if there are entries in mute_log.
       
        entries are dict:
        mute: True or False
        count: Number of samples to do this action for
        """
        
        if self.enabled and len(self.mute_log) > 0:
            n = len(input_items[0])
            if self.mute_log[0]['mute'] == True: # mute
                if self.mute_type == 0: # attenuate
                    output_items[0][:] = input_items[0] * self.attenuation_lvl
                elif self.mute_type == 1: # Gaussian noise
                    output_items[0][:] = (self.noise_std*(np.random.randn(n) + 1j* np.random.randn(n))).astype(np.complex64)
                else: # zeros
                    output_items[0][:] = np.zeros(n,dtype=np.complex64)

            else:
                output_items[0][:] = input_items[0]
                
            self.mute_log[0]['count'] -= n
            if self.mute_log[0]['count'] <= 0:
                self.mute_log.pop(0)
            
        else:
            output_items[0][:] = input_items[0]

                            
        return len(output_items[0])

