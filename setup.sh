echo "Creating settings file..."
cp potwleaderboard/fake-settings.py potwleaderboard/settings.py
echo "Be sure to update the secret keys in potwleaderboard/settings.py"
echo "Creating database migrations"
python manage.py makemigrations
python manage.py makemigrations student
python manage.py makemigrations solution 
python manage.py makemigrations problem
python manage.py makemigrations errorpage
python manage.py makemigrations leaderboard
python manage.py makemigrations contribution
python manage.py migrate

python setup_defaults.py
