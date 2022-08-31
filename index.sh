rm -rf $2
mkdir $2
rm -rf tmp/
mkdir tmp
python main.py $1 $2 $3
