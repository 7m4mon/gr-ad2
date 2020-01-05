#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
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

"""
   ++++ AD2_AnalogOut_Custom ++++
   This is the source block for Digilent's AnalogDiscovery2 AnalogOut
   written by 7m4mon <http://nomulabo.com>

   Based on DWF Python Example 3

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import math
import numpy
from gnuradio import gr

class AD2_AnalogOut_Custom_f(gr.sync_block):
    """
    docstring for block AD2_AnalogOut_Custom_f
    """
    def __init__(self, channel, amplituide, sampl_freq, buff_size):
        gr.sync_block.__init__(self,
            name="AD2_AnalogOut_Custom_f",
            in_sig=[numpy.float32],
            out_sig=None)

        self.rgdSamples = [0] * buff_size
        self.CHANNEL = channel
        self.dwf_ao = dwf.DwfAnalogOut()
        self.dwf_ao.nodeEnableSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, True)
        self.dwf_ao.nodeFunctionSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, self.dwf_ao.FUNC.CUSTOM)
        self.dwf_ao.nodeFrequencySet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, int(frequency/buff_size))
        self.dwf_ao.nodeAmplitudeSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, amplituide)
        self.dwf_ao.nodeDataSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, self.rgdSamples)
        self.dwf_ao.configure(self.CHANNEL, True)
        self.done = 0
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        sample_num = len(in0)
        print sample_num
        for i in range(sample_num):
           self.rgdSamples[i] = in0[i]
        self.dwf_ao.nodeDataSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, self.rgdSamples)
        self.dwf_ao.configure(self.CHANNEL, True)
        return len(input_items[0])

    def stop(self):
        self.dwf_ao.close()
        return True