#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   DWF Python Example
   Author:  Digilent, Inc.
   Revision: 10/17/2013

   Requires:                       
       Python 2.7, 3.3 or later
       numpy, matplotlib
"""

import dwf
import time
import numpy
from gnuradio import gr

class AD2_AnalogIn_Record_f(gr.sync_block):
    """
    """
    def __init__(self,channel, v_range, hz_acq, n_samples):
        gr.sync_block.__init__(self,
            name="AD2_AnalogIn_Record_f",
            in_sig=None,
            out_sig=[numpy.float32])
        #print DWF version
        print("DWF Version: " + dwf.FDwfGetVersion())

        #open device with configure
        self.hdwf = dwf.Dwf(-1,1)   # 1:Scope Buffer Size 16k

        #set up acquisition
        self.dwf_ai = dwf.DwfAnalogIn(self.hdwf)
        self.dwf_ai.channelEnableSet(channel, True)
        self.dwf_ai.channelRangeSet(channel, v_range)
        self.dwf_ai.acquisitionModeSet(self.dwf_ai.ACQMODE.RECORD)
        self.dwf_ai.frequencySet(hz_acq)
        self.dwf_ai.recordLengthSet(-1)             #infinite time
        buffer_size = self.dwf_ai.bufferSizeGet()
        print ("BufferSize " + str(buffer_size))

        #wait at least 2 seconds for the offset to stabilize
        time.sleep(2)

        #begin acquisition
        self.dwf_ai.configure(False, True)
        print("begin acquisition")

        self.rgdSamples = [0.0] * n_samples
        self.cSamples = 0
        self.fLost = False
        self.fCorrupted = False
    
    def work(self, input_items, output_items):
        out = output_items[0]
        out_len = len(output_items[0])
        sts = self.dwf_ai.status(True)
        if self.cSamples == 0 and sts in (self.dwf_ai.STATE.CONFIG,
                                     self.dwf_ai.STATE.PREFILL,
                                     self.dwf_ai.STATE.ARMED):
            print ("Acquisition not yet started.")
            out = [0.0] * out_len

        cAvailable, cLost, cCorrupted = self.dwf_ai.statusRecord()
        self.cSamples += cLost
            
        if cLost > 0:
            print ("cLost" + str(cLost))
            self.fLost = True
        if cCorrupted > 0:
            print ("cCorrupted" + str(cCorrupted))
            self.fCorrupted = True
        if cAvailable == 0:
            print ("cAvailable == 0")
            out = [0.0] * out_len
            
        else :
            # get samples
            self.rgdSamples.extend(self.dwf_ai.statusData(0, cAvailable))
            self.cSamples += cAvailable
            
            #print "out_len " + str(out_len)
            #print "cAvailable " + str(cAvailable)
            #print "len_rgdSamples " + str(len(self.rgdSamples))
            if out_len < len(self.rgdSamples):
                out[:] = self.rgdSamples[:out_len]
                self.rgdSamples = self.rgdSamples[out_len:]
            else:
                print ("!!! buffer skipped !!!")
                out = [0.0] * out_len
            
        return len(output_items[0])

    def stop(self):
        self.dwf_ai.close()
        print("finished")
        if self.fLost:
            print("Samples were lost! Reduce frequency")
        if self.fCorrupted:
            print("Samples could be corrupted! Reduce frequency")
        return True
