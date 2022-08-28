from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status
from django.db import DatabaseError
from .logging import logger


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        # 记录服务器异常
        view = context['view']
        if isinstance(exc, DatabaseError):
            logger.error('[%s] %s' % (view, exc))
            response = Response({'detail': '服务器异常，请重试...'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error('[%s]--->%s' % (view, exc))
            response = Response({'detail': '未知错误！请联系管理员'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
