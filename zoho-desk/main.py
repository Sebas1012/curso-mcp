from mcp.server.fastmcp import FastMCP
from utils.zoho_provider import get_access_token, fetch_zoho_desk_agents
import argparse
import asyncio

parser = argparse.ArgumentParser(description="Zoho Desk Agent Fetcher")

parser.add_argument("--client_id", type=str, help="Zoho Client ID")
parser.add_argument("--client_secret", type=str, help="Zoho Client Secret")
parser.add_argument("--refresh_token", type=str, help="Zoho Refresh Token")
parser.add_argument("--organization_id", type=str, help="Zoho Organization ID")

args = parser.parse_args()

mcp = FastMCP('zoho-desk')

@mcp.tool()
async def fetch_agents() -> list:
    """
    Fetch Zoho Desk agents using the access token.
    :return: A list of agents.
    """
    zoho_access_token = await get_access_token(args.client_id, args.client_secret, args.refresh_token)

    if not zoho_access_token:
        return []

    agents = await fetch_zoho_desk_agents(zoho_access_token, args.organization_id)
    return agents

if __name__ == "__main__":
    mcp.run(transport='stdio')
