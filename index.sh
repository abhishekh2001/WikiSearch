rm -rf $2
mkdir $2
rm -rf tmp/
mkdir tmp
python ind.py $1 $2 $3
