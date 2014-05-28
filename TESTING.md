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
    pip install pytest
    py.test tests


To run a single test:

    py.test tests -k test_executemany


When you're done, stop the server and remove its data:

    cd ~/tmp/mysqldb-test-server && cat data/*.pid | xargs kill
    rm -rf data


Checking Refcounts
==================

    git clone git://git.fedorahosted.org/gcc-python-plugin.git
    cd gcc-python-plugin
    make plugin
    export CC=$PWD/gcc-with-cpychecker

    cd /path/to/MySQLdb1
    git checkout gh-pages
    git pull origin development
    python setup.py build
    git add -f build/temp.linux-x86_64-2.7/_mysql.*html
    git commit
    git push origin HEAD

Now you'll see the updated results at (for example):
    http://bukzor.github.io/MySQLdb1/build/temp.linux-x86_64-2.7//_mysql.c.get_string-refcount-errors.html
