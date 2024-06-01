# echo "BUILD START"
# python3.9 -m ensurepip --upgrade
# python3.9 -m pip install --upgrade pip
# python3.9 -m pip install setuptools
# python3.9 -m pip install -r requirements.txt
# python3.9 -m pip install psycopg2-binary
# python3.9 manage.py collectstatic --noinput
# echo "BUILD END"

echo "BUILD START"

python3.9 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
python3.9 -m ensurepip --upgrade
python3.9 -m pip install --upgrade pip setuptools
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install psycopg2-binary

# Collect static files
python3.9 manage.py collectstatic --noinput

echo "BUILD END"
