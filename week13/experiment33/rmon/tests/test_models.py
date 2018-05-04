from rmon.models import Server
from rmon.common.rset import RsetException

class TestServer(object):

    def test_save(self,db):
        assert Server.query.count() == 0
        server = Server(name='test',host='127.0.0.1')
        server.save()

        assert Server.query.count() == 1
        assert Server.query.first() == server

    def test_delete(self,db,server):
        assert Server.query.count() == 1
        server.delete()
        assert Server.query.count() == 0

    def test_ping_success(self,db,server):
        assert server.ping() is True

    def test_ping_failed(seff,db):
        server = Server(name='test',host='127.0.0.1',port='6379')

        try:
            server.ping()
        except RsetException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host

    def test_get_metrics_success(self,db,server):
        info = server.get_metrics()
        assert isinstance(info,dict)

    def test_get_metrics_failed(self,db):
        server = Server(name='test',host='127.0.0.1',port='6379')
        try:
            server.get_metrics()
        except RsetException as e:
            assert e.code == 400
            assert e.message == 'redis server %s can not connected' % server.host

