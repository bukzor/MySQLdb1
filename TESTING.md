First, run a little mysql server in your home directory.

*NOTE:* The below setup is quite insecure and should be shutdown and deleted when testing is concluded.

    mkdir -p ~/tmp/mysqldb-test-server/
    cd !$

    mysql_install_db --no-defaults --user=$USER --datadir=$PWD/data --socket=$PWD/mysql.sock --force
    /usr/sbin/mysqld --no-defaults --user=$USER --datadir=$PWD/data --socket=$PWD/mysql.sock --port 33060


Now edit tests/default.cnf to add the port and change the user to 'root':

    port = 33060
    user = root


Finally, run the tests:

    nosetests


When you're done, stop the server:

    cat data/*.pid | xargs kill


Remove its data:

    rm -rf data
