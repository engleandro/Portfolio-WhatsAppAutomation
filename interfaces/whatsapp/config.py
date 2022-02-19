import os, sys, platform, socket

OS = platform.system()
if OS == 'Windows':
    username = os.environ['USERNAME']
elif OS == 'Linux':
    username = os.environ.get('USERNAME') \
        or os.environ.get('LOGNAME')

session_name='Wtsp'

if OS == 'Linux':
    CHROME_SYSTEM_PATH=f'/home/{username}/.config/google-chrome/{session_name}'
CHROME_PROFILE_PATH=f'user-data-dir={CHROME_SYSTEM_PATH}'
