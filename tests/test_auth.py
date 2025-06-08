import pytest
from django.core.exceptions import PermissionDenied
from django.test import override_settings
from mcpx.auth import mcp_auth

# Mocking the get_http_headers function from fastmcp
def mock_get_http_headers():
    return {"authorization": "Bearer test-token"}

@override_settings(MCP_AUTH="test-token")
@pytest.mark.django_db
def test_mcp_auth_success():
    """Test that mcp_auth passes when the correct token is provided"""
    # Mock the get_http_headers function to return our test header
    import mcpx.auth
    mcpx.auth.get_http_headers = mock_get_http_headers

    # Call the function - should not raise an exception
    mcp_auth()

@override_settings(MCP_AUTH="test-token")
@pytest.mark.django_db
def test_mcp_auth_invalid_token():
    """Test that mcp_auth raises PermissionDenied with an invalid token"""
    # Mock the get_http_headers function to return an incorrect token
    import mcpx.auth
    def invalid_header():
        return {"authorization": "Bearer wrong-token"}
    mcpx.auth.get_http_headers = invalid_header

    # Call the function - should raise PermissionDenied
    with pytest.raises(PermissionDenied):
        mcp_auth()

@override_settings(MCP_AUTH="test-token")
@pytest.mark.django_db
def test_mcp_auth_missing_header():
    """Test that mcp_auth raises PermissionDenied when auth header is missing"""
    # Mock the get_http_headers function to return no auth header
    import mcpx.auth
    def missing_header():
        return {}
    mcpx.auth.get_http_headers = missing_header

    # Call the function - should raise PermissionDenied
    with pytest.raises(PermissionDenied):
        mcp_auth()

@override_settings(MCP_AUTH="test-token")
@pytest.mark.django_db
def test_mcp_auth_with_param():
    """Test that mcp_auth accepts a token parameter"""
    # Mock the get_http_headers function to return an empty header
    import mcpx.auth
    def empty_header():
        return {}
    mcpx.auth.get_http_headers = empty_header

    # Call the function with a correct token param - should not raise exception
    mcp_auth(auth_token="test-token")
