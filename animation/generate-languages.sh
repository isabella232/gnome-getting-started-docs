for file in po/*po;
do
        lang=`echo $file | sed 's/po\/\(.*\)\.po/\1/gi'`
        echo $lang
        xml2po -a -p $file translations.xml > translations/$lang.xml
done
