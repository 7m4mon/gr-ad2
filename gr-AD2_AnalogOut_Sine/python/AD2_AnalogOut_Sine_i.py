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
   ++++ AD2_AnalogOut_Sine ++++
   This is the sink block for Digilent's AnalogDiscovery2 AnalogOut
   written by 7m4mon <http://nomulabo.com>

   Based on DWF Python Example 2

   Modified by: MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>   
   Revised: 2016-04-21
   Original Author:  Digilent, Inc.
   Original Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
"""

import dwf
import sys
import numpy
from gnuradio import gr

class AD2_AnalogOut_Sine_i(gr.sync_block):
    """
    docstring for block AD2_AnalogOut_Sine_i
    """
    def __init__(self, channel, amplituide, offset):
        gr.sync_block.__init__(self,
            name="AnalogOut_Sine_i", 
            in_sig=[numpy.int32],
            out_sig=None)
        self.CHANNEL = channel
        self.freqHz = 0
        self.dwf_ao = dwf.DwfAnalogOut()
        self.dwf_ao.nodeEnableSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, True)
        self.dwf_ao.nodeFunctionSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, self.dwf_ao.FUNC.SINE)
        self.dwf_ao.nodeFrequencySet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, int(self.freqHz))
        self.dwf_ao.nodeAmplitudeSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, amplituide)
        self.dwf_ao.nodeOffsetSet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, offset)
        self.dwf_ao.configure(self.CHANNEL, True)
        

    def work(self, input_items, output_items):
        in0 = input_items[0]
        freqHz_work = in0[0]
        if not self.freqHz == freqHz_work:
            self.freqHz = freqHz_work
            self.dwf_ao.nodeFrequencySet(self.CHANNEL, self.dwf_ao.NODE.CARRIER, int(self.freqHz))
            self.dwf_ao.configure(self.CHANNEL, True)
        return len(input_items[0])


    def stop(self):
        self.dwf_ao.close()
        return True

