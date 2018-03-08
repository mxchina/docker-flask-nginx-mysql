#!/bin/bash

# **********************************************************
# * Author        : MX
# * Email         : 274819450@qq.com
# * Create time   : 2018-03-08 07:07
# * Filename      : init_data.sh
# **********************************************************

mysql -uroot -p$MYSQL_ROOT_PASSWORD <<EOF
source $WORK_PATH/$FILE_0;
source $WORK_PATH/$FILE_1;
