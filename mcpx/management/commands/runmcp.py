from django.conf import settings
from fastmcp import FastMCP
import asyncio
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_string
from mcp.server.session import ServerSession


class Command(BaseCommand):
    help = (
        "Starts the MCP server with configurations from Django settings.\n\n"
        "This command initializes and runs an MCP (Message Control Protocol) server using "
        "the FastMCP library. It reads server configurations from the `MCP_SERVERS` setting, "
        "imports each server module dynamically, and starts the server on the specified host and port.\n\n"
        "Usage:\n"
        "  python manage.py mcp [options]\n\n"
        "Options:\n"
        "  --host HOST    Specify the host to run the MCP server on. Defaults to the value in settings.MCP_HOST.\n"
        "  --port PORT    Specify the port to run the MCP server on. Defaults to the value in settings.MCP_PORT."
    )

    def add_arguments(self, parser):
        # Add optional arguments for host and port
        parser.add_argument(
            "--host",
            type=str,
            help="Specify the host to run the MCP server on.",
        )
        parser.add_argument(
            "--port",
            type=int,
            help="Specify the port to run the MCP server on.",
        )

    def handle(self, *args, **options):
        ####################################################################################
        # Temporary monkeypatch which avoids crashing when a POST message is received
        # before a connection has been initialized, e.g: after a deployment.
        # pylint: disable-next=protected-access
        old__received_request = ServerSession._received_request

        async def _received_request(self, *args, **kwargs):
            try:
                return await old__received_request(self, *args, **kwargs)
            except RuntimeError:
                pass

        # pylint: disable-next=protected-access
        ServerSession._received_request = _received_request
        ####################################################################################
        servers = settings.MCP_SERVERS
        if not servers:
            raise CommandError(
                "No MCP servers found in settings. Please configure MCP_SERVERS in your Django settings."
            )
        mcp = FastMCP(name="DjangoMcpServer")

        async def setup():
            for server in servers:
                try:
                    server_module = import_string(server)
                    await mcp.import_server(server_module["name"], server_module["mcp"])
                except Exception as e:
                    raise CommandError(f"Failed to import server {server}: {e}")

        # Override host and port if provided via command line arguments
        host = options.get("host") or settings.MCP_HOST
        port = options.get("port") or settings.MCP_PORT

        asyncio.run(setup())

        mcp.run(
            transport="streamable-http",
            host=host,
            port=port,
        )
