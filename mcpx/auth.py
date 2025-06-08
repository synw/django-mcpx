from django.conf import settings
from fastmcp.server.dependencies import get_http_headers
from django.core.exceptions import PermissionDenied
from typing import Optional


def mcp_auth(auth_token: Optional[str] = None) -> None:
    """
    Authenticate a request based on the MCP_AUTH setting or an optional auth_token parameter.

    This function checks if the `MCP_AUTH` setting is defined and verifies the authorization token from the HTTP headers against the configured token.
    If an auth_token parameter is provided, it will be used instead of the MCP_AUTH setting.

    Args:
        auth_token (Optional[str]): An optional authorization token to use for authentication. Defaults to None.

    Raises:
        AttributeError: If the `MCP_AUTH` setting is not defined in the settings and no auth_token is provided.
        PermissionDenied: If the authorization token is missing or invalid.

    Example:
        .. code-block:: python

            from mcpservers.auth import mcp_auth
            from django.core.exceptions import PermissionDenied

            try:
                mcp_auth()
            except AttributeError as e:
                # Handle the case where MCP_AUTH is not defined and no auth_token provided
                print(f"Configuration error: {e}")
            except PermissionDenied as e:
                # Handle the case where the authorization token is missing or invalid
                print(f"Authentication error: {e}")
            except Exception as e:
                # Handle any other unexpected errors
                print(f"An unexpected error occurred: {e}")

    """
    headers = get_http_headers()
    auth_header = headers.get("authorization", "")

    if auth_token is not None:
        expected_token = auth_token
        # If a token parameter is provided, only validate the header if it exists
        if auth_header and auth_header.replace("Bearer ", "") != expected_token:
            raise PermissionDenied("Invalid authorization token")
        return
    else:
        if not hasattr(settings, "MCP_AUTH"):
            raise AttributeError("MCP_AUTH is not defined in settings")
        expected_token = settings.MCP_AUTH

    if not auth_header or auth_header.replace("Bearer ", "") != expected_token:
        # await ctx.warning("Empty data list provided")
        raise PermissionDenied("Invalid or missing authorization token")
