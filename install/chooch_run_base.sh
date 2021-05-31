#!/bin/sh -
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64/
python3 {app_path}/chooch_service.py 