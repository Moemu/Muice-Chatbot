@echo off
::´ËÎÄ¼þÓÃÓÚ°²×°Muice-ChatbotËùÐèµÄ»·¾³£¬±àÂëÎªANSI/GB 2312,ÇëÎð¸ü¸Ä±àÂë¸ñÊ½¡£::
::install config::
set git_source=https://mirror.ghproxy.com/https://github.com
set pip_source=https://pypi.tuna.tsinghua.edu.cn/simple

set python_installer=https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
set git_installer=%git_source%/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe
set gcc_installer=https://nuwen.net/files/mingw/mingw-19.0.exe

set enable_venv=1

set max_connection=16
set min_split_size=1M

set pip_extra_install_packages=llmtuner
:::::::::::::::::

cd /d %~dp0
set ESC=
set RD=%ESC%[31m
set GN=%ESC%[32m
set YW=%ESC%[33m
set BL=%ESC%[34m
set WT=%ESC%[37m
set RN=%ESC%[0m
echo %GN%[INFO]%WT% ¼ì²âÍêÕûÐÔ...
if not exist install_env\aria2c.exe (
    echo %RD%[ERROR]%WT% aria2c.exe Î´ÕÒµ½£¬Çë¼ì²éÍêÕûÐÔ¡£
    exit
)
if not exist install_env\7z.exe (
    echo %RD%[ERROR]%WT% 7z.exe Î´ÕÒµ½£¬Çë¼ì²éÍêÕûÐÔ¡£
    exit
)
echo %GN%[INFO]%WT% ¼ì²â³ÌÐòÔËÐÐÊ±...
python --version
if errorlevel 1 (
    set python_installed=0
) else (
    set python_installed=1
)
python --version|findstr /r /i "3.12" > NUL && echo %YW%[WARN]%WT% ÄãµÄpython¿ÉÄÜ²»¼æÈÝpytorch£¬ÇëÐ¶ÔØºóÖØÐÂ´ò¿ª³ÌÐò¡£ && exit
git --version
if errorlevel 1 (
    set git_installed=0
) else (
    set git_installed=1
)
gcc --version
if errorlevel 1 (
    set gcc_installed=0
) else (
    set gcc_installed=1
)
nvcc --version
if errorlevel 1 (
    set cuda_installed=0
) else (
    echo %GN%[INFO]%WT% CUDAÒÑ°²×°£¬½«°²×°PyTorch-cuda°æ±¾¡£
    set cuda_installed=1
)
set /p enable_ofa="ÊÇ·ñ°²×°OFAÒÀÀµ£¿[Y/N]:"
if /i "%enable_ofa%"=="y" (
    set enable_ofa=1
) else (
    set enable_ofa=0
)
set /p enable_audio="ÊÇ·ñ°²×°ÒôÆµ´¦ÀíÒÀÀµ£¿[Y/N]:"
if /i "%enable_audio%"=="y" (
    set enable_audio=1
) else (
    set enable_audio=0
)
echo %GN%[INFO]%WT% Çë¼ì²éÁÐ³öµÄÅäÖÃÊÇ·ñÕýÈ·£¬ÈçÓÐ´íÎóÇëÐÞ¸Äinstall_env.batÖÐµÄconfig¡£
echo.
echo     ÊÇ·ñÆôÓÃpython venv = %enable_venv%
echo     aria2c×î´óÁ¬½ÓÊý = %max_connection%
echo     aria2c×îÐ¡·ÖÆ¬´óÐ¡ = %min_split_size%
echo     pipÔ´ = %pip_source%
echo     gitÔ´ = %git_source%
echo     ÊÇ·ñ°²×°OFAÒÀÀµ = %enable_ofa%
echo     ÊÇ·ñ°²×°ÒôÆµ´¦ÀíÒÀÀµ = %enable_audio%
echo %BL%    pip¶îÍâ°²×°°ü = %pip_extra_install_packages%
if %python_installed%==0 (
    echo %RD%    Î´ÕÒµ½python£¬½«³¢ÊÔ°²×°¡£
    echo %WT%    python°²×°°ü = %python_installer%
) else (    
    echo %GN%    pythonÒÑ°²×°¡£
)
if %git_installed%==0 (
    echo %RD%    Î´ÕÒµ½git£¬½«³¢ÊÔ°²×°¡£
    echo %WT%    git°²×°°ü = %git_installer%
) else (
    echo %GN%    gitÒÑ°²×°¡£
)
if %gcc_installed%==0 (
    echo %RD%    Î´ÕÒµ½gcc£¬½«³¢ÊÔ°²×°¡£
    echo %WT%    gcc°²×°°ü = %gcc_installer%
) else (
    echo %GN%    gccÒÑ°²×°¡£
)
if %cuda_installed%==0 (
    echo %YW%    Î´ÕÒµ½CUDA£¬PyTorch½«Ö»°²×°CPU°æ±¾¡£%WT%
) else (
    echo %GN%    CUDAÒÑ°²×°,½«°²×°PyTorch-cuda°æ±¾¡£%WT%
)
echo.
install_env\sleepx -p "Èç¹ûÒªÍ£Ö¹°²×°£¬ÇëÔÚ10ÃëÄÚ°´ÏÂÈÎÒâ¼ü..." -k 10
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ÒÑÍ£Ö¹°²×°¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
)
echo %GN%[INFO]%WT% ¿ªÊ¼°²×°...
if %python_installed%==0 (
    call :installpy
)
if %git_installed%==0 (
    call :installgit
)
if %gcc_installed%==0 (
    call :installgcc
)
if %enable_venv%==1 (
    echo %GN%[INFO]%WT% ÆôÓÃpython venv...
    if not exist Muice\Scripts\activate.bat python -m venv Muice
    call Muice\Scripts\activate.bat
)
echo %GN%[INFO]%WT% °²×°ÒÀÀµ...
ping -n 2 127.1 > nul
call :install_req
echo %GN%[INFO]%WT% °²×°PyTorch...
ping -n 2 127.1 > nul
call :install_pytorch
echo %GN%[INFO]%WT% °²×°extra°ü...
ping -n 2 127.1 > nul
if not "%pip_extra_install_packages%"=="" (
    pip install %pip_extra_install_packages% -i %pip_source%
)
echo %GN%[INFO]%WT% °²×°Íê³É£¡
echo %GN%[INFO]%WT% ÕýÔÚÉú³ÉÆô¶¯½Å±¾...
ping -n 2 127.1 > nul
echo @echo off>start.bat
if %enable_venv%==1 echo call Muice\Scripts\activate.bat>>start.bat
echo python main.py>>start.bat
echo pause>>start.bat
echo %GN%[INFO]%WT% Äã¿ÉÒÔÊ¹ÓÃstart.batÆô¶¯main.py¡£
if %enable_venv%==1 echo %GN%[INFO]%WT% ÈôÒª¼¤»î»·¾³£¬Ê¹ÓÃ"call Muice\Scripts\activate.bat"¡£
echo %GN%[INFO]%WT% °´ÈÎÒâ¼üÍË³ö¡£
pause>nul
exit



:install_pytorch
if %cuda_installed%==0 goto :eof
echo %GN%[INFO]%WT% ¼ì²âCUDA°æ±¾...
set cudaver=
nvcc --version|findstr /r /i "11.8" > NUL && set cudaver=cu118
nvcc --version|findstr /r /i "12.1" > NUL && set cudaver=cu121
nvcc --version|findstr /r /i "12.4" > NUL && set cudaver=cu124
if "%cudaver%"=="" (
    echo %RD%[ERROR]%WT% Î´Öª»ò²»Ö§³ÖµÄCUDA°æ±¾£¬ÇëÐ¶ÔØ²¢°²×°11.8/12.1/12.4°æ±¾µÄCUDA¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
)
pip install torch==2.4.1+%cudaver% torchvision torchaudio -i %pip_source% --extra-index-url https://download.pytorch.org/whl/%cudaver%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% °²×°PyTorchÊ§°Ü¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
)
goto :eof

:install_req
pip install -r requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% °²×°ÒÀÀµÊ§°Ü¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
    )
if %enable_ofa%==0 goto :eof
pip install -r ofa_requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% °²×°ofaÒÀÀµÊ§°Ü¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
    )
if %enable_audio%==0 goto :eof
pip install -r audio_requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% °²×°ÒôÆµ´¦ÀíÒÀÀµÊ§°Ü¡£
    echo %WT%°´ÈÎÒâ¼üÍË³ö¡£
    pause>nul
    exit
    )
goto :eof

:installpy
md software
echo %GN%[INFO]%WT% ÕýÔÚÏÂÔØpython...
if exist software\python-installer.exe (
    if not exist software\python-installer.exe.aria2 (
       del /q software\python-installer.exe
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out python-installer.exe %python_installer%
echo %GN%[INFO]%WT% ÕýÔÚ°²×°python...
echo %YW%[WARN]%WT% ÇëµÈ´ý°²×°Íê³ÉºóÖØÐÂ´ò¿ª³ÌÐò¡£
echo %YW%[WARN]%WT% Èô°²×°³ÌÐòÎ´ÔËÐÐ£¬´ó¸ÅÂÊÎªÏÂÔØÊ§°Ü£¬ÇëÖØÐÂ´ò¿ª³ÌÐò¡£
software\python-installer.exe /passive AppendPath=1 PrependPath=1 InstallAllUsers=1
echo °´ÈÎÒâ¼üÍË³ö¡£
pause>nul
exit

:installgit
md software
echo %GN%[INFO]%WT% ÕýÔÚÏÂÔØgit...
if exist software\git-installer.exe (
    if not exist software\git-installer.exe.aria2 (
       del /q software\git-installer.exe
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out git-installer.exe %git_installer%
echo %GN%[INFO]%WT% ÕýÔÚ°²×°git...
echo %YW%[WARN]%WT% ÇëµÈ´ý°²×°Íê³ÉºóÖØÐÂ´ò¿ª³ÌÐò¡£
echo %YW%[WARN]%WT% Èô°²×°³ÌÐòÎ´ÔËÐÐ£¬´ó¸ÅÂÊÎªÏÂÔØÊ§°Ü£¬ÇëÖØÐÂ´ò¿ª³ÌÐò¡£
software\git-installer.exe /SILENT /NORESTART
echo °´ÈÎÒâ¼üÍË³ö¡£
pause>nul
exit

:installgcc
md software
echo %GN%[INFO]%WT% ÕýÔÚÏÂÔØgcc...
if exist software\gcc.7z (
    if not exist software\gcc.7z.aria2 (
       del /q software\gcc.7z
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out gcc-installer.exe %gcc_installer%
echo %GN%[INFO]%WT% ÕýÔÚ°²×°gcc...
echo %YW%[WARN]%WT% °²×°Íê³ÉºóÖØÐÂ´ò¿ª³ÌÐò¡£
install_env\7z x software\gcc-installer.exe
echo %YW%[WARN]%WT% É±Èí±¨´íÇëÍ¬Òâ¡£
setx PATH "%PATH%;%~dp0MinGW\bin"
set X_MEOW=%~dp0MinGW\include;%~dp0MinGW\include\freetype2
if defined C_INCLUDE_PATH (setx C_INCLUDE_PATH "%X_MEOW%;%C_INCLUDE_PATH%") else (setx C_INCLUDE_PATH "%X_MEOW%")
if defined CPLUS_INCLUDE_PATH (setx CPLUS_INCLUDE_PATH "%X_MEOW%;%CPLUS_INCLUDE_PATH%") else (setx CPLUS_INCLUDE_PATH "%X_MEOW%")
set X_MEOW=
echo °´ÈÎÒâ¼üÍË³ö¡£
pause>nul
exit