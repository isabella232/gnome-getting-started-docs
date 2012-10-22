xml2po -o template.pot translations.xml
for file in po/*po;
do
        lang=`echo $file | sed 's/po\/\(.*\)\.po/\1/gi'`
        echo $lang
        #xml2po -a -p $file translations.xml > translations/$lang.xml
	msgmerge $file template.pot > temp.po
	mv temp.po $file
done
