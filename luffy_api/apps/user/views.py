import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from django_redis import get_redis_connection
from rest_framework import status
from luffy_api.utils.geetest.geetest import get_bypass_cache, run_thread
from luffy_api.utils.geetest.sdk.geetest_lib import GeetestLib
from luffy_api.utils.geetest.geetest_config import GEETEST_ID, GEETEST_KEY
from .utils import get_user
from luffy_api.utils.sms import send_sms_single


class MyTokenObtainPairView(TokenObtainPairView):
    """ 自定义token """
    serializer_class = MyTokenObtainPairSerializer


class GeetestAPIView(APIView):
    """验证初始化接口，GET请求"""
    def get(self, request):
        run_thread()
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
        print("post请求")
        challenge = request.data.get(GeetestLib.GEETEST_CHALLENGE, None)
        validate = request.data.get(GeetestLib.GEETEST_VALIDATE, None)
        seccode = request.data.get(GeetestLib.GEETEST_SECCODE, None)
        bypass_status = get_bypass_cache()
        gt_lib = GeetestLib(GEETEST_ID, GEETEST_KEY)
        if bypass_status == "success":
            result = gt_lib.successValidate(challenge, validate, seccode)
        else:
            result = gt_lib.failValidate(challenge, validate, seccode)
        # 注意，不要更改返回的结构和值类型
        if result.status == 1:
            response = {"status": True, "version": GeetestLib.VERSION}
        else:
            response = {"status": False, "version": GeetestLib.VERSION, "msg": result.msg}
        return Response(response)


class SendSMSAPIView(APIView):
    def get(self, request):
        mobile = request.query_params.get("username")
        if get_user(mobile):
            return Response({"status": False, "msg": "手机号已注册！"}, status=status.HTTP_400_BAD_REQUEST)
        conn = get_redis_connection("sms_code")
        ret = conn.get(mobile)
        if ret:
            return Response({"status": False, "msg": "对不起，60秒内不能重复发送！"}, status=status.HTTP_400_BAD_REQUEST)
        code = random.randint(1000, 9999)
        sms = send_sms_single(mobile, '1445434', [code, ])
        if sms['result'] != 0:
            return Response({"status": False, "msg": "短信发送失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        conn.set(mobile, code, 60)

        return Response({"status": True})