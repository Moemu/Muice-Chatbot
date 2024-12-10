@echo off
::���ļ����ڰ�װMuice-Chatbot����Ļ���������ΪANSI/GB 2312,������ı����ʽ��::
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
echo %GN%[INFO]%WT% ���������...
if not exist install_env\aria2c.exe (
    echo %RD%[ERROR]%WT% aria2c.exe δ�ҵ������������ԡ�
    exit
)
if not exist install_env\7z.exe (
    echo %RD%[ERROR]%WT% 7z.exe δ�ҵ������������ԡ�
    exit
)
echo %GN%[INFO]%WT% ����������ʱ...
python --version
if errorlevel 1 (
    set python_installed=0
) else (
    set python_installed=1
)
python --version|findstr /r /i "3.12" > NUL && echo %YW%[WARN]%WT% ���python���ܲ�����pytorch����ж�غ����´򿪳��� && exit
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
    echo %GN%[INFO]%WT% CUDA�Ѱ�װ������װPyTorch-cuda�汾��
    set cuda_installed=1
)
set /p enable_ofa="�Ƿ�װOFA������[Y/N]:"
if /i "%enable_ofa%"=="y" (
    set enable_ofa=1
) else (
    set enable_ofa=0
)
set /p enable_audio="�Ƿ�װ��Ƶ����������[Y/N]:"
if /i "%enable_audio%"=="y" (
    set enable_audio=1
) else (
    set enable_audio=0
)
echo %GN%[INFO]%WT% �����г��������Ƿ���ȷ�����д������޸�install_env.bat�е�config��
echo.
echo     �Ƿ�����python venv = %enable_venv%
echo     aria2c��������� = %max_connection%
echo     aria2c��С��Ƭ��С = %min_split_size%
echo     pipԴ = %pip_source%
echo     gitԴ = %git_source%
echo     �Ƿ�װOFA���� = %enable_ofa%
echo     �Ƿ�װ��Ƶ�������� = %enable_audio%
echo %BL%    pip���ⰲװ�� = %pip_extra_install_packages%
if %python_installed%==0 (
    echo %RD%    δ�ҵ�python�������԰�װ��
    echo %WT%    python��װ�� = %python_installer%
) else (    
    echo %GN%    python�Ѱ�װ��
)
if %git_installed%==0 (
    echo %RD%    δ�ҵ�git�������԰�װ��
    echo %WT%    git��װ�� = %git_installer%
) else (
    echo %GN%    git�Ѱ�װ��
)
if %gcc_installed%==0 (
    echo %RD%    δ�ҵ�gcc�������԰�װ��
    echo %WT%    gcc��װ�� = %gcc_installer%
) else (
    echo %GN%    gcc�Ѱ�װ��
)
if %cuda_installed%==0 (
    echo %YW%    δ�ҵ�CUDA��PyTorch��ֻ��װCPU�汾��%WT%
) else (
    echo %GN%    CUDA�Ѱ�װ,����װPyTorch-cuda�汾��%WT%
)
echo.
install_env\sleepx -p "���Ҫֹͣ��װ������10���ڰ��������..." -k 10
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ��ֹͣ��װ��
    echo %WT%��������˳���
    pause>nul
    exit
)
echo %GN%[INFO]%WT% ��ʼ��װ...
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
    echo %GN%[INFO]%WT% ����python venv...
    if not exist Muice\Scripts\activate.bat python -m venv Muice
    call Muice\Scripts\activate.bat
)
echo %GN%[INFO]%WT% ��װ����...
ping -n 2 127.1 > nul
call :install_req
echo %GN%[INFO]%WT% ��װPyTorch...
ping -n 2 127.1 > nul
call :install_pytorch
echo %GN%[INFO]%WT% ��װextra��...
ping -n 2 127.1 > nul
if not "%pip_extra_install_packages%"=="" (
    pip install %pip_extra_install_packages% -i %pip_source%
)
echo %GN%[INFO]%WT% ��װ��ɣ�
echo %GN%[INFO]%WT% �������������ű�...
ping -n 2 127.1 > nul
echo @echo off>start.bat
if %enable_venv%==1 echo call Muice\Scripts\activate.bat>>start.bat
echo python main.py>>start.bat
echo pause>>start.bat
echo %GN%[INFO]%WT% �����ʹ��start.bat����main.py��
if %enable_venv%==1 echo %GN%[INFO]%WT% ��Ҫ�������ʹ��"call Muice\Scripts\activate.bat"��
echo %GN%[INFO]%WT% ��������˳���
pause>nul
exit



:install_pytorch
if %cuda_installed%==0 goto :eof
echo %GN%[INFO]%WT% ���CUDA�汾...
set cudaver=
nvcc --version|findstr /r /i "11.8" > NUL && set cudaver=cu118
nvcc --version|findstr /r /i "12.1" > NUL && set cudaver=cu121
nvcc --version|findstr /r /i "12.4" > NUL && set cudaver=cu124
if "%cudaver%"=="" (
    echo %RD%[ERROR]%WT% δ֪��֧�ֵ�CUDA�汾����ж�ز���װ11.8/12.1/12.4�汾��CUDA��
    echo %WT%��������˳���
    pause>nul
    exit
)
pip install torch==2.4.1+%cudaver% torchvision torchaudio -i %pip_source% --extra-index-url https://download.pytorch.org/whl/%cudaver%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ��װPyTorchʧ�ܡ�
    echo %WT%��������˳���
    pause>nul
    exit
)
goto :eof

:install_req
pip install -r requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ��װ����ʧ�ܡ�
    echo %WT%��������˳���
    pause>nul
    exit
    )
if %enable_ofa%==0 goto :eof
pip install -r ofa_requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ��װofa����ʧ�ܡ�
    echo %WT%��������˳���
    pause>nul
    exit
    )
if %enable_audio%==0 goto :eof
pip install -r audio_requirements.txt -i %pip_source%
if errorlevel 1 (
    echo %RD%[ERROR]%WT% ��װ��Ƶ��������ʧ�ܡ�
    echo %WT%��������˳���
    pause>nul
    exit
    )
goto :eof

:installpy
md software
echo %GN%[INFO]%WT% ��������python...
if exist software\python-installer.exe (
    if not exist software\python-installer.exe.aria2 (
       del /q software\python-installer.exe
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out python-installer.exe %python_installer%
echo %GN%[INFO]%WT% ���ڰ�װpython...
echo %YW%[WARN]%WT% ��ȴ���װ��ɺ����´򿪳���
echo %YW%[WARN]%WT% ����װ����δ���У������Ϊ����ʧ�ܣ������´򿪳���
software\python-installer.exe /passive AppendPath=1 PrependPath=1 InstallAllUsers=1
echo ��������˳���
pause>nul
exit

:installgit
md software
echo %GN%[INFO]%WT% ��������git...
if exist software\git-installer.exe (
    if not exist software\git-installer.exe.aria2 (
       del /q software\git-installer.exe
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out git-installer.exe %git_installer%
echo %GN%[INFO]%WT% ���ڰ�װgit...
echo %YW%[WARN]%WT% ��ȴ���װ��ɺ����´򿪳���
echo %YW%[WARN]%WT% ����װ����δ���У������Ϊ����ʧ�ܣ������´򿪳���
software\git-installer.exe /SILENT /NORESTART
echo ��������˳���
pause>nul
exit

:installgcc
md software
echo %GN%[INFO]%WT% ��������gcc...
if exist software\gcc.7z (
    if not exist software\gcc.7z.aria2 (
       del /q software\gcc.7z
    )
  )
install_env\aria2c --max-connection-per-server=%max_connection% --min-split-size=%min_split_size% --dir software --out gcc-installer.exe %gcc_installer%
echo %GN%[INFO]%WT% ���ڰ�װgcc...
echo %YW%[WARN]%WT% ��װ��ɺ����´򿪳���
install_env\7z x software\gcc-installer.exe
echo %YW%[WARN]%WT% ɱ������ͬ�⡣
setx PATH "%PATH%;%~dp0MinGW\bin"
set X_MEOW=%~dp0MinGW\include;%~dp0MinGW\include\freetype2
if defined C_INCLUDE_PATH (setx C_INCLUDE_PATH "%X_MEOW%;%C_INCLUDE_PATH%") else (setx C_INCLUDE_PATH "%X_MEOW%")
if defined CPLUS_INCLUDE_PATH (setx CPLUS_INCLUDE_PATH "%X_MEOW%;%CPLUS_INCLUDE_PATH%") else (setx CPLUS_INCLUDE_PATH "%X_MEOW%")
set X_MEOW=
echo ��������˳���
pause>nul
exit