#!/bin/sh

APP_PATH=
PYTHON3=/usr/bin/python3

CLIENT_PATH=$APP_PATH/client
SERVER_PATH=$APP_PATH/server
LOG_FILE=$SERVER_PATH/server.log

cd $SERVER_PATH
$PYTHON3 gen_puzzle_data.py >> $LOG_FILE
ln -sf $SERVER_PATH/data.bin $CLIENT_PATH/data.bin
chmod a+r-wx data.bin $CLIENT_PATH/data.bin
chmod u+w $SERVER_PATH/data.bin
