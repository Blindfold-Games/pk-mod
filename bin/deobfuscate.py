__author__ = 'blindfold'

def main():
        subprocess.check_call(r'''
        builddir="$MOD_HOME/build"

        rm -rf $builddir/ifc $builddir/src $builddir/proguard $builddir/dex.apk $builddir/smali $MOD_HOME/app/smali/broot $MOD_HOME/app/smali/a/*.smali
        mkdir -p $builddir/ifc $builddir/src

        javac -Xlint:-options -g:none -source 6 -target 6 -cp $MOD_HOME/lib/android.jar:$MOD_HOME/lib/gdx.jar -d $builddir/ifc `find -H $MOD_HOME/ifc -type f -iname "*.java"`
        javac -Xlint:-options -g -source 6 -target 6 -cp $builddir/ifc:$MOD_HOME/lib/android.jar:$MOD_HOME/lib/gdx.jar -d $builddir/src `find -H $MOD_HOME/src -type f -iname "*.java" -not -name BuildConfig.java` $MOD_HOME/build/BuildConfig.java

        proguard.sh @$MOD_HOME/res/%s.pg

        dx --dex --output=$builddir/dex.apk $builddir/proguard.zip
        java -jar $MOD_HOME/lib/baksmali.jar $builddir/dex.apk -o $builddir/smali

        cp -r $builddir/smali/* $MOD_HOME/app/smali/
        java -jar $MOD_HOME/lib/apktool.jar b%s $MOD_HOME/app
        $MOD_HOME/bin/sign_apk.py `ls $MOD_HOME/app/dist/*.apk` %s
    ''' % (('release', '', 'release') if release else ('debug', ' -d', 'debug')), shell=True)

if __name__ == '__main__':
    main()
