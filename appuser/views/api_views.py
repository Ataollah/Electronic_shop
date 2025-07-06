from Utility.VerificationMessageSender import VerificationMessageSender
from appuser.models import AppUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status




def send_verification_code(username, is_new_user):
    username_already_taken = AppUser.objects.filter(username__iexact=username).exists()
    sender = VerificationMessageSender(username)

    if is_new_user and not username_already_taken:
        sender.sendCode()
        return status.HTTP_200_OK
    elif not is_new_user and username_already_taken:
        sender.sendCode()
        return status.HTTP_200_OK

    return status.HTTP_400_BAD_REQUEST


class SendCode(APIView):

    # if user is a new user send verification code
    # else return error message
    def post(self, request):
        username = request.data['username']
        sender = VerificationMessageSender(username)
        sender.sendCode()
        return Response(status=status.HTTP_200_OK)

class SendCodeToCandidUser(APIView):

    # if user is a new user send verification code
    # else return error message
    def post(self, request):
        username = request.data['username']
        return Response( status=send_verification_code(username, True))


class SendCodeToUser(APIView):

    # if user already exists send verification code
    # else return error message
    def post(self, request):
        username = request.data['username']
        return Response( status=send_verification_code(username, False))

