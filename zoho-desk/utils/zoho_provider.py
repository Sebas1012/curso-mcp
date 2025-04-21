import httpx

BASE_AUTH_URL = 'https://accounts.zoho.com/oauth/v2/token'
BASE_API_URL = 'https://desk.zoho.com/api/v1'

async def get_access_token(client_id: str, client_secret: str, refresh_token: str) -> str | None:
    """
    Get access token using refresh token.
    :param client_id: The client ID of the Zoho application.
    :param client_secret: The client secret of the Zoho application.
    :param refresh_token: The refresh token obtained during the initial authorization.
    :return: The access token.
    """
    url = f'{BASE_AUTH_URL}?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            access_token = data.get('access_token')

            return access_token
        except Exception:
            return None

    
async def fetch_zoho_desk_agents(access_token: str, org_id: str) -> list:
    """
    Fetch Zoho Desk agents using the access token.
    :param access_token: The access token obtained from the authorization process.
    :param org_id: The organization ID for the Zoho Desk account.
    :return: A list of agents.
    """
    url = f'{BASE_API_URL}/agents'
    headers = {'Authorization': f'Zoho-oauthtoken {access_token}', 'orgId': org_id}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            agents = data.get('data', [])

            return agents
        except Exception:
            return []