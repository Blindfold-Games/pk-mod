#!/usr/bin/env python3

import common, subprocess

def main():
    subprocess.check_call(r'''
        cd $MOD_HOME
        adb pull /data/app/com.silvermoon.client-1.apk
    ''', shell=True, executable='/bin/bash')


if __name__ == '__main__':
    main()
