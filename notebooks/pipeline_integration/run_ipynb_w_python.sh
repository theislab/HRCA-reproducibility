nb_name=$1;
jupyter nbconvert --to script $1.ipynb
python $1.py