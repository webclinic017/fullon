import pytest
from run.user_manager import UserManager
from unittest.mock import patch

# User Manager fixture
@pytest.fixture
def user_manager():
    return UserManager()


@pytest.mark.order(1)
def test_add_exchange(user_manager, monkeypatch, db_session):
    mock_exchange = {'key': 'value'}
    mock_result = 1

    with patch('libs.database.Database._run_default', return_value=mock_result) as mock_run_default:
        result = user_manager.add_exchange(mock_exchange)
        assert result == mock_result
        mock_run_default.assert_called_once()


@pytest.mark.order(4)
def test_add_bot(user_manager):
    mock_bot = {'key': 'value'}
    mock_result = 1

    with patch('libs.database.Database._run_default', return_value=mock_result) as mock_run_default:
        result = user_manager.add_bot(mock_bot)
        assert result == mock_result
        mock_run_default.assert_called_once()


@pytest.mark.order(5)
def test_add_bot_exchange(user_manager):
    mock_bot_id = 1
    mock_exchange = {'key': 'value'}
    mock_result = True

    with patch('libs.database.Database._run_default', return_value=mock_result) as mock_run_default:
        result = user_manager.add_bot_exchange(mock_bot_id, mock_exchange)
        assert result == mock_result
        mock_run_default.assert_called_once()



@pytest.mark.order(6)
def test_user_set_secret_key(user_manager):
    user_id = 0
    key = "key1"
    exchange = "kraken"
    secret = "secret"
    res = user_manager.set_secret_key(user_id=user_id,
                                      exchange=exchange,
                                      key=key,
                                      secret=secret)
    assert res is True
    key = "key2"
    exchange = "kucoin"
    res = user_manager.set_secret_key(user_id=user_id,
                                      exchange=exchange,
                                      key=key,
                                      secret=secret)
    assert res is True
    key = "key2"
    exchange = "kucoin"
    res = user_manager.set_secret_key(user_id=user_id,
                                      exchange=exchange,
                                      key=key,
                                      secret=secret)
    assert res is True
    exchange = "kraken"
    res = user_manager.del_secret_key(user_id=user_id,
                                      exchange=exchange)
    assert res is True
    exchange = "kraken"
    res = user_manager.del_secret_key(user_id=user_id,
                                      exchange=exchange)
    assert res is False
    exchange = "kucoin"
    res = user_manager.del_secret_key(user_id=user_id,
                                      exchange=exchange)
    assert res is True



@pytest.mark.order(7)
def test_get_user_id(user_manager, test_mail):
    user = user_manager.get_user_id(mail=test_mail)
    assert isinstance(user, int)


@pytest.mark.order(8)
def test_user_list(user_manager):
    users = user_manager.list_users(page=1, page_size=10, all=False)
    assert isinstance(users, list)

@pytest.mark.order(9)
def test_get_user_exchange(user_manager, test_mail, uid,  exchange1):
    _uid = user_manager.get_user_id(mail=test_mail)
    assert _uid == uid
    res = user_manager.get_user_exchanges(uid=_uid)
    assert isinstance(res, list)
    assert isinstance(res[0], dict)
    assert res[0]['cat_ex_id'] == exchange1[1]
    _uid = user_manager.get_user_id(mail='notreal@noexists.com')
    assert _uid is None
    res = user_manager.get_user_exchanges(uid=_uid)
    assert res == []

'''

@pytest.mark.order(10)
def test_del_strategy(user_manager):
    res = user_manager.del_bot_strategy(bot_id=0)
    assert res is False
'''