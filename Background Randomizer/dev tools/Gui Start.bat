@echo off
cd /D %~dp0
cd..
cd python

set gui=True

python Startup.py %1 %gui%
