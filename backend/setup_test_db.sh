sudo -u postgres bash -c "dropdb trivia_test"
sudo -u postgres bash -c "createdb trivia_test"
sudo -u postgres bash -c "psql trivia_test < ./trivia.psql"
