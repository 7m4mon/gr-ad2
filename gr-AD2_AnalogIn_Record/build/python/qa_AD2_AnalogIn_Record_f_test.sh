#!/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/nomura/gr-ad2/gr-AD2_AnalogIn_Record/python
export PATH=/home/nomura/gr-ad2/gr-AD2_AnalogIn_Record/build/python:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export PYTHONPATH=/home/nomura/gr-ad2/gr-AD2_AnalogIn_Record/build/swig:$PYTHONPATH
/usr/bin/python2 /home/nomura/gr-ad2/gr-AD2_AnalogIn_Record/python/qa_AD2_AnalogIn_Record_f.py 
