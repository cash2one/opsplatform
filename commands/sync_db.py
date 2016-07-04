# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: sync_db.py
@time: 16-7-4 上午11:10
"""
import MySQLdb


def update_dashboard_graph():
    #连接
    dashboard_db = MySQLdb.connect(host="172.16.60.23", user="root", passwd="", db="dashboard", charset="utf8")
    cursor = dashboard_db.cursor()
    ops_db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='opsplatform', charset="utf8")
    cur_ops = ops_db.cursor()

    #写入
    sql = "select * from dashboard_graph"
    cursor.execute(sql)
    for row in cursor.fetchall():
        print '''INSERT INTO monitor_dashboardgraph(id, title, hosts, counters, screen_id, timespan, graph_type, method, position) VALUES (%s, '%s', '%s', '%s', %s, %s, '%s', '%s', %s)''' % \
              (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] if row[7] else '', row[8])
        cur_ops.execute('''INSERT INTO monitor_dashboardgraph(id, title, hosts, counters, screen_id, timespan, graph_type, method, position) VALUES (%s, '%s', '%s', '%s', %s, %s, '%s', '%s', %s)'''%
                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] if row[7] else '', row[8]))
    cur_ops.close()
    ops_db.commit()
    ops_db.close()
    print 'All Done.'


def update_dashboard_screen():
    #连接
    dashboard_db = MySQLdb.connect(host="172.16.60.23", user="root", passwd="", db="dashboard", charset="utf8")
    cursor = dashboard_db.cursor()
    ops_db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='opsplatform', charset="utf8")
    cur_ops = ops_db.cursor()

    #写入
    sql = "select * from dashboard_screen"
    cursor.execute(sql)
    for row in cursor.fetchall():
        print '''INSERT INTO monitor_dashboardscreen(id, pid, name, time) VALUES (%s, '%s', '%s', '%s')''' % \
              (row[0], row[1], row[2], row[3])
        cur_ops.execute('''INSERT INTO monitor_dashboardscreen(id, pid, name, time) VALUES (%s, '%s', '%s', '%s')'''%
                        (row[0], row[1], row[2], row[3]))
    cur_ops.close()
    ops_db.commit()
    ops_db.close()
    print 'All Done.'


if __name__ == '__main__':
    update_dashboard_graph()
    update_dashboard_screen()

