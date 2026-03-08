@echo off
set "ROOT=%~dp0"
cd /d "%ROOT%"


set "PYTHONPATH=%ROOT%lib"


".\python_runtime\python.exe" "flappy_bird.py"
pause