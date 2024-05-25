echo "BUILD START"
python3.9 -m ensurepip
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install psycopg2-binary
python3.9 manage.py collectstatic --noinput
echo "BUILD END"