import pytest
import json
from calvin.utilities.settings import FACEBOOK_CREDENTIALS
from calvin.calvinsys.web.facebook import Facebook, FacebookUser
from facebook import GraphAPIError


def test_correct_credentials():
    js_content = open(FACEBOOK_CREDENTIALS).read()
    credentials = json.loads(js_content)
    fb = Facebook("lol","lol")
    assert fb.set_credentials(credentials) is True


def test_wrong_credentials():
    credentials = {'access_token' : 'nonevalue'}
    fb = Facebook("lol","lol")
    assert fb.set_credentials(credentials) is False


@pytest.mark.slow
def test_correct_post_wall():
    credentials = json.loads(open(FACEBOOK_CREDENTIALS).read())
    fb = FacebookUser(credentials)
    msg = {'attachment': {'caption': 'caption',
                              'description': 'description',
                              'link': '',
                              'name': 'hi',
                              'picture': ''},
               'message': 'message_thisshouldwork'}

    assert fb.fb_user.put_wall_post(msg['message'], msg['attachment']) is not None


@pytest.mark.slow
def test_wrong_post_wall():
    credentials = {'access_token' : 'nonevalue'}
    fb = FacebookUser(credentials)
    msg = {'attachment': {'caption': 'caption',
                              'description': 'description',
                              'link': '',
                              'name': 'hi',
                              'picture': ''},
               'message': 'message_thisshouldwork'}

    with pytest.raises(GraphAPIError):
        fb.fb_user.put_wall_post(msg['message'], msg['attachment'])