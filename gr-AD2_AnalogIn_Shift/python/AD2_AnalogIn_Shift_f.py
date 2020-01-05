#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 <7m4mon>.
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
   ++++ AD2_AnalogIn_Shift ++++
   This is the sink block for Digilent's AnalogDiscovery2 AnalogIn
   written by 7m4mon <http://nomulabo.com>

   Based on DWF Python Example

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 1/11/2016

   Requires:                       
       Python 2.7, 3.3 or later
       numpy
"""

import dwf
import time
import numpy
from gnuradio import gr

class AD2_AnalogIn_Shift_f(gr.sync_block):
    """
    docstring for block AD2_AnalogIn_Shift_f
    """
    def __init__(self, channel, v_range, hz_acq, n_samples):
        gr.sync_block.__init__(self,
            name="AD2_AnalogIn_Shift_f",
            in_sig=None,
            out_sig=[numpy.float32])

        #open device
        print("Opening first device")
        self.hdwf = dwf.Dwf()
        #set up acquisition
        self.dwf_ai = dwf.DwfAnalogIn(self.hdwf)
        self.dwf_ai.channelEnableSet(channel, True)
        self.dwf_ai.channelRangeSet(channel, v_range)
        self.dwf_ai.acquisitionModeSet(self.dwf_ai.ACQMODE.SCAN_SHIFT)
        self.dwf_ai.frequencySet(hz_acq)
        self.dwf_ai.bufferSizeSet(n_samples)
        self.rgdSamples = []
        self.ary_num = 0

        print("wait at 2 seconds for the offset to stabilize")
        time.sleep(2)

        #begin acquisition
        self.dwf_ai.configure(False, True)


    def work(self, input_items, output_items):
        out = output_items[0]
        sts = self.dwf_ai.status(True)
        out_len = len(output_items[0])
        while self.ary_num < out_len:
            cValid = self.dwf_ai.statusSamplesValid()
            self.rgdSamples.extend(self.dwf_ai.statusData(0, cValid) )
            self.ary_num += cValid
            print cValid

        self.ary_num -= out_len
        if self.ary_num == 0:
            self.rgdSamples = []
        else:
            self.rgdSamples = self.rgdSamples[out_len + 1:]
        out[:] = self.rgdSamples[:out_len]
        
        return len(output_items[0])

    def stop(self):
        self.dwf_ai.close()
        return True

