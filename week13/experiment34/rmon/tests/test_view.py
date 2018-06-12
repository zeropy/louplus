import json
from flask import url_for

from rmon.models import Server


class TestServerList:
    """测试 Redis 服务器列表 API
    """

    endpoint = 'api.server_list'

    def test_get_servers(self, server, client):
        """获取 Redis 服务器列表
        """
        resp = client.get(url_for(self.endpoint))

        # RestView 视图基类会设置 HTTP 头部 Content-Type 为 json
        assert resp.headers['Content-Type'] == 'application/json; charset=utf-8'
        # 访问成功后返回状态码 200 OK
        assert resp.status_code == 200

        servers = resp.json

        # 由于当前测试环境中只有一个 Redis 服务器，所以返回的数量为 1
        assert len(servers) == 1

        h = servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self, db, client):
        """测试创建 Redis 服务器成功
        """
        # 自行补充
        resp = client.post(url_for(self.endpoint),data=json.dumps(dict(
                name='legion',host='127.0.0.1',port=6380
        )),content_type='application/json')
        assert resp.status_code == 201
        assert resp.json['ok'] == True


    def test_create_server_failed_with_invalid_host(self, db, client):
        """无效的服务器地址导致创建 Redis 服务器失败
        """
        # 自行补充
        resp = client.post(url_for(self.endpoint),data=json.dumps(dict(
                name='legion',host='127.0.0.1.0',port=6380
        )),content_type='application/json')
        assert resp.status_code == 400
        assert resp.json['ok'] == False

    def test_create_server_failed_with_duplciate_server(self, server, client):
        """创建重复的服务器时将失败
        """
        # 自行补充
        resp = client.post(url_for(self.endpoint),data=json.dumps(dict(
                name='legion',host='127.0.0.1',port=6379
        )),content_type='application/json')
        resp = client.post(url_for(self.endpoint),data=json.dumps(dict(
                name='legion',host='127.0.0.1',port=6379
        )),content_type='application/json')
        assert resp.status_code == 400
        assert resp.json['ok'] == False

class TestServerDetail:
    """测试 Redis 服务器详情 API
    """

    endpoint = 'api.server_detail'

    def test_get_server_success(self, server, client):
        """测试获取 Redis 服务器详情
        """
        server = Server(name='test',host='127.0.0.1')
        server.save()
        resp = client.get(url_for(self.endpoint,object_id=server.id))
        servers = resp.json
        h = servers
        assert h['name'] == 'test'
        assert h['host'] == '127.0.0.1'
        assert h['port'] == 6379

    def test_get_server_failed(self, db, client):
        """获取不存在的 Redis 服务器详情失败
        """
        servers = db.session.query(Server).filter_by(id=9999).all()
        assert servers == []
        resp = client.get(url_for(self.endpoint,object_id=9999))
        result = resp.json
        assert result['ok'] == False
        assert result['message'] == 'object not exist'

    def test_update_server_success(self, server, client):
        """更新 Redis 服务器成功
        """
        resp = client.put(url_for(self.endpoint,object_id=server.id),data=json.dumps(dict(
                    name='legion1'
        )),content_type='application/json')
        result = resp.json
        assert resp.status_code == 200
        assert result['ok'] == True

    def test_update_server_success_with_duplicate_server(self, server, client):
        """更新服务器名称为其他同名服务器名称时失败
        """
        server_test = Server(name='test',host='127.0.0.1')
        server_test.save()
        resp = client.put(url_for(self.endpoint,object_id=server.id),data=json.dumps(dict(
                    name='test'
        )),content_type='application/json')
        print(resp.data)
        assert resp.status_code == 400
        result = resp.json
        assert result['ok'] == False
        assert result['message'] == 'Redis server already exist'

    def test_delete_success(self, server, client):
        """删除 Redis 服务器成功
        """
        resp = client.delete(url_for(self.endpoint,object_id=server.id))
        assert resp.status_code == 204
        # print(resp.data)
        # assert 1 == 2

    def test_delete_failed_with_host_not_exist(self, db, client):
        """删除不存在的 Redis 服务器失败
        """
        servers = db.session.query(Server).filter_by(id=9999).all()
        assert servers == []
        resp = client.delete(url_for(self.endpoint,object_id=9999))
        assert resp.status_code == 404
        assert resp.json['ok'] == False
        assert resp.json['message'] == 'object not exist'
