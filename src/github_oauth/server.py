import asyncio
from typing import Any, Optional
from contextlib import AsyncExitStack
import os
from mcp.server.fastmcp import FastMCP
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("github_oauth")

# GitHub API Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
GITHUB_API_BASE = "https://api.github.com"
USER_AGENT = "github-weather-app/1.0"

# Global variable to store access token
access_token: Optional[str] = None


async def make_request(url: str, headers: dict[str, str], params: dict[str, str] = None) -> Optional[dict[str, Any]]:
    """Make an HTTP GET request with error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Request failed: {e}")
            return None


@mcp.tool()
async def authorize_github() -> str:
    """Generate GitHub authorization URL for user authorization."""
    global access_token

    if access_token:
        return "Already authorized with an access token."

    authorization_url = (
        f"https://github.com/login/oauth/authorize?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=repo"
    )
    return (
        f"Please authorize the application by visiting this URL:\n\n{authorization_url}\n\n"
        "Once authorized, provide the code you receive."
    )


@mcp.tool()
async def get_access_token_from_code(code: str) -> str:
    """Exchange authorization code for an access token."""
    global access_token

    url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            access_token = data.get("access_token", "")
            if access_token:
                return "Authorization successful! Access token obtained."
            return "Failed to obtain access token."
        except Exception as e:
            print(f"Error fetching access token: {e}")
            return "Failed to fetch access token."


@mcp.tool()
async def get_user_repositories() -> str:
    """Fetch the repositories of the authenticated user."""
    global access_token

    if not access_token:
        return "You are not authorized. Please authorize first."

    url = f"{GITHUB_API_BASE}/user/repos"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github.v3+json",
    }
    data = await make_request(url, headers)
    if not data:
        return "Unable to fetch repositories."

    if isinstance(data, list):
        repos = []
        for repo in data:
            repos.append(f"Name: {repo['name']}, URL: {repo['html_url']}, Language: {repo.get('language', 'Unknown')}")
        return "\n---\n".join(repos)

    return "No repositories found."


@mcp.tool()
async def get_user_profile() -> str:
    """Fetch the authenticated user's GitHub profile."""
    global access_token

    if not access_token:
        return "You are not authorized. Please authorize first."

    url = f"{GITHUB_API_BASE}/user"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": USER_AGENT,
    }
    data = await make_request(url, headers)
    if not data:
        return "Unable to fetch user profile."

    return (
        f"Username: {data.get('login', 'N/A')}\n"
        f"Name: {data.get('name', 'N/A')}\n"
        f"Email: {data.get('email', 'N/A')}\n"
        f"Public Repositories: {data.get('public_repos', 'N/A')}\n"
        f"Followers: {data.get('followers', 'N/A')}\n"
        f"Following: {data.get('following', 'N/A')}\n"
        f"Profile URL: {data.get('html_url', 'N/A')}"
    )


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="stdio")
