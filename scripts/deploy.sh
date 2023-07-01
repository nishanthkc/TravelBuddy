cd Travel
git pull https://nishanth-krishna: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@github.com/nishanth-krishna/Travel.git
sudo pip install -r requirements.txt
python3 manage.py makemigrations
killall screen
python3 manage.py migrate
screen -d -m python3 manage.py runserver 0.0.0.0:8000