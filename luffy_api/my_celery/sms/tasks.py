from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework import status

from ..config import SMS_APP_ID, SMS_APP_KEY, TEMPLATE_ID
from luffy_api.my_celery.main import app

@app.task(name="send_sms")
def send_sms(phone_num, template_param_list):
    appid = SMS_APP_ID
    appkey = SMS_APP_KEY
    sms_sign = "动物行为故事与科普"
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(86, phone_num, TEMPLATE_ID, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    if response['result'] != 0:
        return Response({"status": False, "msg": "短信发送失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    code = template_param_list[0]
    print(code)
    conn = get_redis_connection("sms_code")
    conn.set(phone_num, code, 60)
    