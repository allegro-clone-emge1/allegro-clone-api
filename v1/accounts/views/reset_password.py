from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from v1.accounts.models.reset_password_code import ResetPasswordCode
from v1.utils import constants


class ResetPasswordView(APIView):
    authentication_classes = ()
    permission_classes = ()

    @staticmethod
    def post(request):
        """
        Reset password using reset password code
        """

        code = request.data.get('code')
        password = request.data.get('password')

        reset_password_code = ResetPasswordCode.objects.filter(code=code).first()
        if not reset_password_code:
            return Response({constants.ERROR: "Invalid reset code"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = reset_password_code.user
            validate_password(password)
            user.set_password(password)
            user.save()
            reset_password_code.delete()
            return Response({constants.SUCCESS: 'Password has been updated'})
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as error:
            return Response({constants.ERROR: error}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
