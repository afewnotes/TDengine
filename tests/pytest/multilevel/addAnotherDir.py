###################################################################
#       Copyright (c) 2016 by TAOS Technologies, Inc.
#             All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-

import sys
import taos
from util.log import *
from util.cases import *
from util.sql import *
from util.dnodes import *


class TDTestCase:
    
    def init(self, conn, logSql):
        tdLog.debug("start to execute %s" % __file__)
        tdSql.init(conn.cursor(), logSql)

    def run(self):        
        cfg={
            'monitor': 1,
            '/mnt/data1 0 1' : 'dataDir'
        }
        tdSql.createDir('/mnt/data1')

        tdLog.info("================= step1")
        tdDnodes.stop(1)
        tdDnodes.deploy(1,cfg)
        tdDnodes.start(1)

        tdSql.execute("create database db")
        tdSql.execute("create table db.tb (ts timestamp, f1 int)")
        sql = "insert into db.tb values "
        ts = 1622390400000
        for i in range(1000):
            sql += "(%d, %d)" % (ts + i, i)
        tdSql.execute(sql)

        tdDnodes.stop(1)
        tdDnodes.cfg(1, 'dataDir', '/mnt/data2 0 0')
        tdSql.createDir('/mnt/data2')
        tdDnodes.start(1)

        tdSql.query("select * from db.tb")
        tdSql.checkRows(1000)
              

    def stop(self):
        tdSql.close()
        os.system("rm -rf /mnt/data1")
        os.system("rm -rf /mnt/data2")
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
