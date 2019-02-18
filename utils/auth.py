from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
"JWT  session  两种用户验证方式"

my_auth_classes = (JSONWebTokenAuthentication, SessionAuthentication)