# gr-ad2
### GRC (GNU Radio Companion) Blocks for Digilent's Analog Discovery 2  
by 7M4MON

    Based on DWF Python Example, DWF library wrapper  
    [PyPi - dwf](https://pypi.org/project/dwf/)  
    Modified by: MURAMATSU Atsushi  
    Original Author:  Digilent, Inc.  

## How to install

### Linux (tested on Ubuntu and Raspbian)
1, You need to install the following packages 

    $ sudo apt install git cmake libboost-all-dev gnuradio doxygen python-pip

2, Clone this repository

    $ git clone https://github.com/7m4mon/gr-ad2
    $ cd gr-ad2/

3, Build each module at their "gr-AD2_AnalogXx_Xxxxxx" directory

    $ cd gr-AD2_AnalogXx_Xxxxxx/
    $ mkdir build  
    $ cd build  
    $ cmake ../  
    $ make  
    $ sudo make install

4, Download [Adept 2 Runtime](https://reference.digilentinc.com/reference/software/adept/start) and [Waveforms installers](https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/start) from Digilent

5, Install them both, and PyPI - dwf python package

    $ sudo dpkg -i digilent.adept.runtime_2.19.2-amd64.deb  
    $ sudo dpkg -i digilent.waveforms_3.12.1_amd64.deb  
    $ pip install dwf  

### Windows (tested on Windows 10)

If you want to use on Windows, please refer to [here](https://github.com/7m4mon/gr-ad2/issues/1#issuecomment-586614708).

## How to run the flow graph
Start up the GNURadio Companion, and load any of the .brc files in this repo.

Select the Run / Execute command or press F6 to run the graph.

When you stop a flow graph, please close with not kill button but GUI 'x' button.  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/do_not_abort_with_kill_button.png" alt="" title="">  
The device would be locked because the stop function was not called.

### GNURadio flow graphs
There are several flow graph samples in this repo for different use cases.

#### AnalogIn_Record  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AD2_AnalogFM_Demod_450kHz.png" alt="AD2_AnalogFM_Demod_450kHz" title="">  
450kHz FM Demod (5th nyquist zone)
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AD2_AnalogFM_Demod_450kHz_Photo.jpg" alt="AD2_AnalogFM_Demod_450kHz_Photo" title="">
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogIn_Record_FM_Demod.grc.png" alt="AnalogIn_Record_FM_Demod.grc" title="">
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogIn_Record.grc.png" alt="AnalogIn_Record" title="">

#### AnalogOut_Play  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogOut_Play_AM_Mod.grc.png" alt="AnalogOut_Play_AM_Mod" title="">  
40kHz AM Modulation.
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogOut_Play_AM_Mod_Photo.jpg" alt="AnalogOut_Play_AM_Mod_Photo" title="">
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogOut_Play.grc.png" alt="AnalogOut_Play" title="">

#### AnalogIn_Shift  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogIn_Shift.grc.png" alt="AnalogIn_Shift" title="">

#### AnalogOut_Custom  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogOut_Custom.grc.png" alt="AnalogOut_Custom" title="">

#### AnalogOut_Sine  
<img src="https://github.com/7m4mon/gr-ad2/blob/master/AnalogOut_Sine.grc.png" alt="AnalogOut_Sine" title="">

