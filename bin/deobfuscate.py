#!/usr/bin/env python3

import sys
import subprocess
import os
import tempfile
from common import HOME, LINE_PREFIX

def deobfuscate(apk):
        class_path = '.:'
        for root, dirs, files in os.walk(os.path.join(HOME, 'lib', 'd2j')):
            class_path += ':'.join(os.path.join(root, file) for file in filter(lambda f: f.endswith('.jar'), files))
        subprocess.check_call(r'''
        java -Xms512m -Xmx1024m -classpath "{_classpath}" "com.googlecode.dex2jar.tools.Dex2jarCmd" -f -o {temp_dir}/__temp.jar {input_apk}
        java -Xms512m -Xmx1024m -classpath "{_classpath}" "com.googlecode.dex2jar.tools.JarRemap" -f -c $MOD_HOME/build/obj.d2j-map -o {temp_dir}/__remap.jar {temp_dir}/__temp.jar
        java -Xms512m -Xmx1024m -classpath "{_classpath}" "com.googlecode.dex2jar.tools.Jar2Dex" -f -o {temp_dir}/classes.dex {temp_dir}/__remap.jar
        cp {input_apk} {temp_dir}/__temp.apk
        pushd {temp_dir}
        zip __temp.apk classes.dex
        rm __temp.jar
        rm __remap.jar
        rm classes.dex
        popd
        rm -rf $MOD_HOME/deobf
        java -jar $MOD_HOME/lib/apktool.jar d -d -o $MOD_HOME/deobf --debug-line-prefix '{line_prefix}' "{temp_dir}/__temp.apk"
        mkdir -p $MOD_HOME/deobf  # to not mess up everything if apktool fail
        cp $MOD_HOME/res/app.gitignore $MOD_HOME/deobf/.gitignore

        pushd $MOD_HOME/deobf
        git init
        git add -f .
        git commit -m "Import."
        git gc
        popd
        rm {temp_dir}/__temp.apk

    '''.format(_classpath=class_path, input_apk=apk, line_prefix=LINE_PREFIX, temp_dir=tempfile.gettempdir()), shell=True, executable='/bin/bash')

if __name__ == '__main__':
    deobfuscate(sys.argv[1])
