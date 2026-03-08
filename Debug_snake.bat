@echo off
set "ROOT=%~dp0"
cd /d "%ROOT%"


set "PYTHONPATH=%ROOT%lib"


".\python_runtime\python.exe" "snake.py"
pause