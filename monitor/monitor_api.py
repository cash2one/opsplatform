# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: monitor_api.py
@time: 16-6-23 上午11:17
"""
from monitor.store import graph_db_conn as db_conn


class Endpoint(object):
    def __init__(self, id, endpoint, ts):
        self.id = str(id)
        self.endpoint = endpoint
        self.ts = ts

    def __repr__(self):
        return "<Endpoint id=%s, endpoint=%s>" %(self.id, self.id)
    __str__ = __repr__

    @classmethod
    def search(cls, qs, start=0, limit=100, deadline=0):
        args = [deadline, ]
        for q in qs:
            args.append("%"+q+"%")
        args += [start, limit]

        sql = '''select id, endpoint, ts from endpoint where ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''
        sql += ''' limit %s,%s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def search_in_ids(cls, qs, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)

        args = ids + [deadline, ]
        for q in qs:
            args.append("%"+q+"%")

        sql = '''select id, endpoint, ts from endpoint where id in (''' + placeholder + ''') and ts > %s '''
        for q in qs:
            sql += ''' and endpoint like %s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint(cls, endpoints, deadline=0):
        if not endpoints:
            return []

        holders = ["%s" for x in endpoints]
        placeholder = ",".join(holders)
        args = endpoints + [deadline, ]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where endpoint in (''' + placeholder + ''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [deadline, ]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where id in (''' + placeholder + ''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]


class EndpointCounter(object):
    def __init__(self, id, endpoint_id, counter, step, type_):
        self.id = str(id)
        self.endpoint_id = str(endpoint_id)
        self.counter = counter
        self.step = step
        self.type_ = type_

    def __repr__(self):
        return "<EndpointCounter id=%s, endpoint_id=%s, counter=%s>" %(self.id, self.endpoint_id, self.counter)
    __str__ = __repr__

    @classmethod
    def search_in_endpoint_ids(cls, qs, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)

        args = endpoint_ids
        for q in qs:
            args.append("%"+q+"%")
        args += [start, limit]

        sql = '''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in (''' +placeholder+ ''') '''
        for q in qs:
            sql += ''' and counter like %s'''
        sql += ''' limit %s,%s'''

        cursor = db_conn.execute(sql, args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets_by_endpoint_ids(cls, endpoint_ids, start=0, limit=100):
        if not endpoint_ids:
            return []

        holders = ["%s" for x in endpoint_ids]
        placeholder = ",".join(holders)
        args = endpoint_ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint_id, counter, step, type from endpoint_counter where endpoint_id in ('''+placeholder+''') limit %s, %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]

    @classmethod
    def gets(cls, ids, deadline=0):
        if not ids:
            return []

        holders = ["%s" for x in ids]
        placeholder = ",".join(holders)
        args = ids + [start, limit]

        cursor = db_conn.execute('''select id, endpoint, ts from endpoint where id in ('''+placeholder+''') and ts > %s''', args)
        rows = cursor.fetchall()
        cursor and cursor.close()

        return [cls(*row) for row in rows]


class TagEndpoint(object):
    def __init__(self, id, tag, endpoint_id):
        self.id = str(id)
        self.tag = tag
        self.endpoint_id = str(endpoint_id)

    @classmethod
    def get_endpoint_ids(cls, tags, limit=200):
        if not tags:
            return []

        holders = ["%s" for x in tags]
        placeholder = ",".join(holders)
        args = tags
        cursor = db_conn.execute('''select distinct endpoint_id from tag_endpoint where tag in (''' + placeholder + ''')''', args)
        rows = cursor.fetchall()
        ids = [x[0] for x in rows]

        if not ids:
            return []

        res = None
        for t in tags:
            holders = ["%s" for x in ids]
            placeholder = ",".join(holders)
            args = list(ids) + [t, ]
            sql = '''select endpoint_id from tag_endpoint where endpoint_id in (''' + placeholder + ''') and tag=%s'''
            cursor = db_conn.execute(sql, args)
            rows = cursor.fetchall()
            cursor and cursor.close()

            if not rows:
                return []

            if res is None:
                res = set([row[0] for row in rows])
            else:
                res.intersection_update(set([row[0] for row in rows]))

        ret = list(res) if res else []
        return ret[:limit]
