#!/bin/bash

RANDOM_PASS=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-8};echo;)

mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'remote_usr'@'%' IDENTIFIED BY '$RANDOM_PASS' WITH GRANT OPTION"
mysql -e "FLUSH PRIVILEGES"

echo ""
echo ""
echo "       Random password for remote user 'remote_usr': $RANDOM_PASS"
echo ""
echo ""
