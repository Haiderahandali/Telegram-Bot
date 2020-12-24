#!/usr/bin/bash
set -e;
convert_to_pdf()
{
	#-----------getting the extension only of a file------------#
        fullfilename="$1"
        filename=$(basename "$fullfilename")
        extname="${filename##*.}"
	#---------------DONE-------------------#

        if [ "$extname" == 'pdf' ]; then
                echo "Error.. the file is already a pdf"
                return 15
        else

                lowriter --headless --convert-to pdf "$fullfilename" --outdir "${HOME}/pdfs" > /dev/null
        fi
}
if [ -e "$1" ]; then
        echo 'converting to pdf ...';
        convert_to_pdf "$1";
	echo "Done. the file is in ${HOME}/pdfs " 
else
        echo 'file does not exist, existing ...';
fi

