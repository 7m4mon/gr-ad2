#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2020 7M4MON.
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
   DWF Python ExampleExample
   Author:  Digilent, Inc.
   Revision: 11/22/2017

   Requires:                       
       Python 2.7
"""
import numpy
import ctypes
from ctypes import *
import sys

from gnuradio import gr

class AD2_AnalogOut_Play_f(gr.sync_block):
    """
    docstring for block AD2_AnalogOut_Play_f
    """
    def __init__(self,channel,amplituide,rate, n_samples):
        gr.sync_block.__init__(self,
            name="AD2_AnalogOut_Play_f",
            in_sig=[numpy.float32],
            out_sig=None)
        
        if sys.platform.startswith("win"):
            self.dwf = cdll.dwf
        elif sys.platform.startswith("darwin"):
            self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
            self.dwf = cdll.LoadLibrary("libdwf.so")
        
        # declare ctype variables
        self.hdwf = c_int()
        self.channel = c_int(channel)
        
        # print DWF version
        version = create_string_buffer(16)
        self.dwf.FDwfGetVersion(version)
        print "DWF Version: "+version.value
        
        # open device
        print "Opening first device..."
        #elf.dwf.FDwfDeviceOpen(c_int(-1), byref(self.hdwf))
        self.dwf.FDwfDeviceConfigOpen(c_int(-1), c_int(2), byref(self.hdwf))   #configure wavegen 2x16k buff size
        
        if self.hdwf.value == 0:
            print "Failed to open device"
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print szerr.value
            quit()
        

        print "Playing audio..."
        self.iPlay = 0
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, self.channel, 0, c_bool(True))
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, self.channel, 0, c_int(31)) #funcPlay
        self.dwf.FDwfAnalogOutRepeatSet(self.hdwf, self.channel, c_int(1))
        self.dwf.FDwfAnalogOutRunSet(self.hdwf, self.channel, c_double(-1)) #sRun
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, self.channel, 0, c_double(rate))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, self.channel, 0, c_double(amplituide))
        # prime the buffer with the first chunk of data
        self.cBuffer = c_int(0)     #cBuffer may be buffer size of AD2
        self.dwf.FDwfAnalogOutNodeDataInfo(self.hdwf, self.channel, 0, 0, byref(self.cBuffer))
        print "pnSamplesMax " + str(self.cBuffer.value)
        self.data_c = [0.0] *  self.cBuffer.value
        self.dwf.FDwfAnalogOutNodeDataSet(self.hdwf, self.channel, 0, (ctypes.c_double * len(self.data_c))(*self.data_c), self.cBuffer.value)
        self.iPlay += self.cBuffer.value
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, self.channel, c_bool(True))
        
        self.dataLost = c_int(0)
        self.dataFree = c_int(0)
        self.dataCorrupted = c_int(0)
        self.sts = c_ubyte(0)
        self.totalLost = 0
        self.totalCorrupted = 0
        self.data_c.extend([0.0]*n_samples)




    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        in_len = len(in0)
        self.data_c.extend(in0)
        
        #print "len data_c " + str(len(self.data_c))
        # fetch analog in info for the self.channel
        if self.dwf.FDwfAnalogOutStatus(self.hdwf, self.channel, byref(self.sts)) != 1:
            print "Error"
            szerr = create_string_buffer(512)
            self.dwf.FDwfGetLastErrorMsg(szerr)
            print szerr.value
        
        if self.sts.value != 3: 
            print "!!! DwfStatIsNotRunning!!!" # not running !DwfStateRunning
        
        self.dwf.FDwfAnalogOutNodePlayStatus(self.hdwf, self.channel, 0, byref(self.dataFree), byref(self.dataLost), byref(self.dataCorrupted))
        self.totalLost += self.dataLost.value
        if self.dataLost.value > 0 :
            print "dataLost " + str(self.dataLost.value)
        self.totalCorrupted += self.dataCorrupted.value
        if self.dataCorrupted.value > 0 :
            print "dataCorrupted " + str(self.dataCorrupted.value)
        
        if self.dataFree.value < len(self.data_c):
            if self.dwf.FDwfAnalogOutNodePlayData(self.hdwf, self.channel, 0, (ctypes.c_double * len(self.data_c))(*self.data_c), self.dataFree.value) != 1: 
                print "DataWriteError"
            self.data_c = self.data_c[self.dataFree.value:]
            self.iPlay += self.dataFree.value
        else:
            print "!!!Buffer Skipped!!!"
            
        return len(input_items[0])
        
    def stop(self):
        print "Lost: "+str(self.totalLost)
        print "Corrupted: "+str(self.totalCorrupted)
        
        print "done"
        self.dwf.FDwfDeviceClose(self.hdwf)
        return True
        

