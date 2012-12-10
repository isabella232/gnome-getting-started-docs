case $1 in
	osx)
	  export PYTHONPATH="/Users/jimmac/.blender/scripts"
          blender="/Applications/blender.app/Contents/MacOS/blender";;
	linux)
          export PYTHONPATH=$PYTHONPATH:/usr/lib64/python3.3/site-packages
	  blender="blender";;
esac

for script in *py
  do blend=`basename $script py`blend
  $blender -b $blend -P $script
done
