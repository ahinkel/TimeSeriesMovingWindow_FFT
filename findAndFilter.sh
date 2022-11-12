echo ' '
echo 'Begin...'
echo ' '

dummyFile="tempFile.csv"
echo $dummyFile
touch $dummyFile

find DataDirectory/*.csv -type f | while IFS= read -r file; do
    newFile="./FilteredDataDirectory/"$file"output.csv"
    tr -d '"' <$file >$dummyFile
    echo $newFile
    touch $newFile
    #delete ending @@ from ASCII type files:
    testString=$(tail -1 $dummyFile)
    if [ $testString = $'@@,,,\r' ]
    then
        sed -i '' -e '$ d' $dummyFile
    fi
    python TSMW_FFT.py $dummyFile > $newFile
done


echo ' '
echo 'Finished'
echo ' '