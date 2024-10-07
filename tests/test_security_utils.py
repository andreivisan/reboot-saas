import pytest
import pytest_asyncio
from fastapi import HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, ExpiredSignatureError
from unittest.mock import Mock, patch
from security.utils import get_current_user, _refresh_access_token, _handle_authentication_failure

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "mock_supabase_key")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "mock_jwt_secret")

@pytest.fixture
def mock_oauth2_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")

@pytest.fixture
def mock_request():
    return Mock(spec=Request)

@pytest.fixture
def mock_response():
    return Mock(spec=Response)

# Test get_current_user function
@patch('security.utils.jwt.decode')
@pytest.mark.asyncio
async def test_get_current_user_valid_token(mock_jwt_decode, mock_oauth2_scheme, mock_request, mock_response):
    mock_jwt_decode.return_value = {"sub": "user123"}
    user_id = await get_current_user(mock_request, mock_response, "valid_token")
    assert user_id == "user123"

@patch('security.utils.jwt.decode')
@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_jwt_decode, mock_oauth2_scheme, mock_request, mock_response):
    mock_jwt_decode.side_effect = PyJWTError()
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(mock_request, mock_response, "invalid_token")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid access token"

@patch('security.utils.jwt.decode')
@patch('security.utils._refresh_access_token')
@pytest.mark.asyncio
async def test_get_current_user_expired_token(mock_refresh_token, mock_jwt_decode, mock_oauth2_scheme, mock_request, mock_response):
    mock_jwt_decode.side_effect = [ExpiredSignatureError, {"sub": "user123"}]
    mock_refresh_token.return_value = ("new_access_token", "new_refresh_token")
    user_id = await get_current_user(mock_request, mock_response, "expired_token")
    assert user_id == "user123"
    assert mock_request.state.new_tokens == ("new_access_token", "new_refresh_token")

# Test _refresh_access_token function
@patch('security.utils.supabase.auth.refresh_session')
@pytest.mark.asyncio
async def test_refresh_access_token_success(mock_refresh_session, mock_request):
    mock_request.cookies = {"refresh_token": "valid_refresh_token"}
    mock_refresh_session.return_value.session.access_token = "new_access_token"
    mock_refresh_session.return_value.session.refresh_token = "new_refresh_token"
    
    new_access_token, new_refresh_token = await _refresh_access_token(mock_request)
    assert new_access_token == "new_access_token"
    assert new_refresh_token == "new_refresh_token"

@pytest.mark.asyncio
async def test_refresh_access_token_no_refresh_token(mock_request):
    mock_request.cookies = {}
    with pytest.raises(HTTPException) as exc_info:
        await _refresh_access_token(mock_request)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"

@patch('security.utils.supabase.auth.refresh_session')
@pytest.mark.asyncio
async def test_refresh_access_token_error(mock_refresh_session, mock_request):
    mock_request.cookies = {"refresh_token": "valid_refresh_token"}
    mock_refresh_session.side_effect = Exception("Refresh error")
    
    with pytest.raises(HTTPException) as exc_info:
        await _refresh_access_token(mock_request)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"

# Test _handle_authentication_failure function
@pytest.mark.asyncio
async def test_handle_authentication_failure():
    with pytest.raises(HTTPException) as exc_info:
        _handle_authentication_failure()
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"