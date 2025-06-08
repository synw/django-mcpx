# Django MCPX

Compose MCP servers in Django using [FastMcp](https://github.com/jlowin/fastmcp)

## Installation

```bash
pip install django-mcpx
```

## Usage

### 1. Configuration

First, you need to add `mcpx` to your `INSTALLED_APPS` in your Django settings file (`settings.py`):

```python settings.py (20-25)
INSTALLED_APPS = [
    # ... other installed apps ...
    'mcpx',
]
```

Next, configure the MCP settings in your `settings.py`. Here is an example configuration:

```python settings.py (148-156)
MCP_SERVERS = ["myapp.mcpserver.mcp_server"]

MCP_AUTH = "fefe865fe4856ferqsijjfhe-fre5qxpokjnEEZ5" # your auth token
MCP_PORT = 8397
MCP_HOST = "localhost"
```

### 2. Example Implementation

Let's create a simple MCP server using the `User` model from Django's authentication system.

Create a file named `mcpserver.py` in your app:

```py mcpserver.py (1-54)
from typing import Any, Dict
from fastmcp import FastMCP
from pydantic import Field
from django.core.exceptions import PermissionDenied
from mcpx.auth import mcp_auth
from django.contrib.auth.models import User

name = "User Mcp Server"
mcp = FastMCP(name=name)


@mcp.tool()
async def get_user_by_username(
    username: str = Field(description="The username of the user to retrieve")
) -> Dict[str, Any]:
    """Retrieve a user by their username"""
    try:
        mcp_auth()
    except PermissionDenied as e:
        print(f"Mcp authentication error: {e}")
        return {"error": "undefined"}
    
    try:
        user = await User.objects.aget(username=username)
        return {"result": {"username": user.username, "email": user.email}}
    except User.DoesNotExist:
        return {"error": "User not found"}


@mcp.tool()
async def list_users(
    limit: int = Field(description="Maximum number of users to retrieve", default=10),
) -> Dict[str, Any]:
    """List all users"""
    try:
        mcp_auth()
    except PermissionDenied as e:
        print(f"Mcp authentication error: {e}")
        return {"error": "undefined"}
    
    results = []
    async for user in User.objects.all()[:limit]:
        results.append({"username": user.username, "email": user.email})
    return {"result": results}


mcp_server = {
    "name": name,
    "mcp": mcp,
}
```

### 3. Running the MCP Server

To run the MCP servers listed in settings use the `mcp` management command provided by Django MCPX:

```bash
python manage.py mcpx --host localhost --port 8397
```

This will start the MCP servers on `localhost` at port `8397`.

Test it with a client or Mcp inspector:

```json
{
    "My Mcp server": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8397/mcp",
        "--header",
        "Authorization: Bearer fefe865fe4856ferqsijjfhe-fre5qxpokjnEEZ5"
      ]
    }
}
```

## Warning

Use with caution: you are responsible for what data and what powers you give to which model
