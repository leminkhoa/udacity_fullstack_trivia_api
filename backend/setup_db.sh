sudo -u postgres bash -c "dropdb trivia"
sudo -u postgres bash -c "createdb trivia"
sudo -u postgres bash -c "psql trivia < ./trivia.psql"