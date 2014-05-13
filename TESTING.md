First, run a little mysql server in your home directory.
*NOTE:* The below setup is quite insecure and should be shutdown and deleted when testing is concluded.

    mkdir -p ~/tmp/mysqldb-test-server/
    cd !$

    mysql_install_db --no-defaults --user=$USER --datadir=$PWD/data --socket=$PWD/mysql.sock --force
    /usr/sbin/mysqld --no-defaults --user=$USER --datadir=$PWD/data --socket=$PWD/mysql.sock --port 33060


In another terminal, ensure that there exists a `test` database.
If you get an error saying the test database already exists, just skip this step.

    echo 'create database test;' | mysql --port 33060 -h 0.0.0.0 -u root


In your MySQLdb1 directory (this directory), run the tests:

    virtualenv mysql-venv
    source mysql-venv/bin/activate
    pip install nose
    nosetests


To run a single test:

    nosetests tests.test_MySQLdb_dbapi20:test_MySQLdb.test_executemany


When you're done, stop the server and remove its data:

    cd ~/tmp/mysqldb-test-server && cat data/*.pid | xargs kill
    rm -rf data
