from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from luffy_api.utils.geetest.geetest import get_bypass_cache
from luffy_api.utils.geetest.sdk.geetest_lib import GeetestLib
from luffy_api.utils.geetest.geetest_config import GEETEST_ID, GEETEST_KEY


class MyTokenObtainPairView(TokenObtainPairView):
    """ 自定义token """
    serializer_class = MyTokenObtainPairSerializer


class GeetestAPIView(APIView):
    """验证初始化接口，GET请求"""
    def get(self, request):
        bypass_status = get_bypass_cache()
        gt_lib = GeetestLib(GEETEST_ID, GEETEST_KEY)
        digestmod = "md5"
        user_name = request.query_params.get("username")
        param_dict = {"digestmod": digestmod, "user_name": user_name, "client_type": "web", "ip_address": "127.0.0.1"}
        if bypass_status == "success":
            result = gt_lib.register(digestmod, param_dict)
        else:
            result = gt_lib.local_init()
        # 注意，不要更改返回的结构和值类型
        return Response(result.data, content_type='application/json;charset=UTF-8')

    def post(self, request):
        """二次验证接口，POST请求"""
        challenge = request.form.get(GeetestLib.GEETEST_CHALLENGE, None)
        validate = request.form.get(GeetestLib.GEETEST_VALIDATE, None)
        seccode = request.form.get(GeetestLib.GEETEST_SECCODE, None)
        bypass_status = get_bypass_cache()
        gt_lib = GeetestLib(GEETEST_ID, GEETEST_KEY)
        if bypass_status == "success":
            result = gt_lib.successValidate(challenge, validate, seccode)
        else:
            result = gt_lib.failValidate(challenge, validate, seccode)
        # 注意，不要更改返回的结构和值类型
        if result.status == 1:
            response = {"result": "success", "version": GeetestLib.VERSION}
        else:
            response = {"result": "fail", "version": GeetestLib.VERSION, "msg": result.msg}
        return Response(response)