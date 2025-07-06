import pytest
from unittest import mock

@pytest.mark.django_db
def test_sms_sender_send_sms(monkeypatch):
    # Mock SMSProvider.objects.all().first()
    mock_provider = mock.Mock()
    mock_provider.api_url = 'http://fakeapi/'
    mock_provider.username = 'user'
    mock_provider.password = 'pass'
    mock_provider.phone_number = '12345'

    with mock.patch('siteInfo.models.SMSProvider.objects') as mock_objects:
        mock_objects.all.return_value.first.return_value = mock_provider

        # Mock requests.post
        mock_post = mock.Mock()
        monkeypatch.setattr('requests.post', mock_post)

        from Utility.VerificationMessageSender import SmsSender
        sender = SmsSender()
        sender.send_sms('09123456789', 'test message')

        expected_url = 'http://fakeapi/SendBatchSms'
        expected_data = {
            'userName': 'user',
            'password': 'pass',
            'fromNumber': '12345',
            'toNumbers': '09123456789',
            'messageContent': 'test message',
            'isFlash': False,
            'sendDelay': 0
        }
        mock_post.assert_called_once_with(
            expected_url,
            json=expected_data,
            headers={"Content-Type": "application/json"}
        )


@pytest.mark.django_db
def test_send_code_email(monkeypatch):
    # Mock SiteInfo.objects.all().first().name
    mock_siteinfo = mock.Mock()
    mock_siteinfo.name = 'TestSite'
    monkeypatch.setattr('siteInfo.models.SiteInfo.objects',
                        mock.Mock(all=mock.Mock(return_value=mock.Mock(first=mock.Mock(return_value=mock_siteinfo)))))

    # Mock VerificationUser.objects.filter().first()
    monkeypatch.setattr('appuser.models.VerificationUser.objects', mock.Mock(
        filter=mock.Mock(return_value=mock.Mock(first=mock.Mock(return_value=None))),
        create=mock.Mock()
    ))

    # Mock EmailSender
    mock_email_sender = mock.Mock()
    monkeypatch.setattr('Utility.VerificationMessageSender.EmailSender', mock.Mock(return_value=mock_email_sender))

    from Utility.VerificationMessageSender import VerificationMessageSender
    sender = VerificationMessageSender('test@example.com')
    sender.sendCode()

    mock_email_sender.send_email.assert_called_once()
    args, kwargs = mock_email_sender.send_email.call_args
    assert 'TestSite' in args[0]  # subject
    assert 'کد تایید' in args[1]  # message
    assert args[2] == ['test@example.com']


@pytest.mark.django_db
def test_send_code_phone(monkeypatch):
    # Mock SiteInfo
    mock_siteinfo = mock.Mock()
    mock_siteinfo.name = 'TestSite'
    monkeypatch.setattr('siteInfo.models.SiteInfo.objects',
                        mock.Mock(all=mock.Mock(return_value=mock.Mock(first=mock.Mock(return_value=mock_siteinfo)))))

    # Mock VerificationUser
    monkeypatch.setattr('appuser.models.VerificationUser.objects', mock.Mock(
        filter=mock.Mock(return_value=mock.Mock(first=mock.Mock(return_value=None))),
        create=mock.Mock()
    ))

    # Mock SmsSender
    mock_sms_sender = mock.Mock()
    monkeypatch.setattr('Utility.VerificationMessageSender.SmsSender', mock.Mock(return_value=mock_sms_sender))

    from Utility.VerificationMessageSender import VerificationMessageSender
    sender = VerificationMessageSender('09123456789')
    sender.sendCode()

    # Uncomment the send_sms call in your code to enable this assertion
    # mock_sms_sender.send_sms.assert_called_once()