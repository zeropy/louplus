from flask import request, g
from rmon.common.rest import RestView
from rmon.models import Server, ServerSchema
from rmon.common.decorators import ObjectMustBeExist

class ServerList(RestView):
    """Redis 服务器列表
    """

    def get(self):
        servers = Server.query.all()
        return ServerSchema().dump(servers,many=True).data

    def post(self):
        """创建Redis服务器
        """
        data = request.get_json()
        server, errors = ServerSchema().load(data)
        if errors:
            return errors, 400
        server.ping()
        server.save()
        return {'ok':True}, 201

class ServerDetail(RestView):
    """ Redis 服务器列表
    """

    method_decorators = (ObjectMustBeExist(Server), )

    def get(self, object_id):
        """获取服务器详情
        """
        data, _ = ServerSchema().dump(g.instance)
        return data

    def put(self, object_id):
        """更新服务器
        """
        schema = ServerSchema(context={'instance': g.instance})
        data = request.get_json()
        server, errors = schema.load(data, partial=True)
        if errors:
            return errors, 400
        server.save()
        return {'ok': True}

    def delete(self, object_id):
        """删除服务器
        """
        g.instance.delete()
        return {'ok': True}, 204

class ServerMetrics(RestView):
    method_decorators = (ObjectMustBeExist(Server),)
    def get(self,object_id):
        return g.instance.get_metrics()
