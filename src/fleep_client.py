"""
Fleep API Client

Handles authentication and API requests to the Fleep.io service.
"""

import os
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class FleepAuthenticationError(Exception):
    """Raised when authentication with Fleep API fails."""
    pass


class FleepAPIError(Exception):
    """Raised when Fleep API returns an error."""
    pass


class FleepClient:
    """Client for interacting with the Fleep.io API."""
    
    def __init__(self, base_url: str = "https://fleep.io/api"):
        self.base_url = base_url
        self.session_token: Optional[str] = None
        self.ticket: Optional[str] = None
        self._client = httpx.AsyncClient()
        
        # Get credentials from environment variables
        self.email = os.getenv("FLEEP_EMAIL")
        self.password = os.getenv("FLEEP_PASSWORD")
        
        if not self.email or not self.password:
            raise FleepAuthenticationError(
                "FLEEP_EMAIL and FLEEP_PASSWORD environment variables must be set"
            )
    
    async def authenticate(self) -> None:
        """Authenticate with the Fleep API and obtain a session token."""
        auth_url = f"{self.base_url}/account/login"
        
        auth_data = {
            "email": self.email,
            "password": self.password
        }
        
        try:
            response = await self._client.post(auth_url, json=auth_data)
            response.raise_for_status()
            
            # Get token from cookies and ticket from JSON response
            result = response.json()
            print(f"Login response cookies: {response.cookies}")
            print(f"Login response JSON: {result}")
            
            # Extract token_id from cookies
            if "token_id" in response.cookies:
                self.session_token = response.cookies["token_id"]
            else:
                raise FleepAuthenticationError(f"No token_id cookie received in authentication response: {response.cookies}")
            
            # Extract ticket from JSON response
            if "ticket" in result:
                self.ticket = result["ticket"]
            else:
                raise FleepAuthenticationError(f"No ticket received in authentication response: {result}")
                
        except httpx.HTTPError as e:
            raise FleepAuthenticationError(f"Authentication failed: {str(e)}")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Fleep API."""
        if not self.session_token or not self.ticket:
            await self.authenticate()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = {
            "Content-Type": "application/json"
        }
        
        # Send session token as 'token_id' in cookies as required by Fleep API
        cookies = {}
        if self.session_token:
            cookies["token_id"] = self.session_token
        
        # Embed ticket in JSON data as required by Fleep API
        if data is None:
            data = {}
        if self.ticket:
            data["ticket"] = self.ticket
        
        print(f"Making {method} request to {url} with data: {data} and cookies: {cookies}")
        try:
            response = await self._client.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                cookies=cookies
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPError as e:
            if response.status_code == 401:
                # Token might have expired, try to re-authenticate
                self.session_token = None
                self.ticket = None
                await self.authenticate()
                # Retry the request with refreshed token and ticket
                cookies = {}
                if self.session_token:
                    cookies["token_id"] = self.session_token
                
                # Re-embed ticket in JSON data for retry
                if self.ticket:
                    data["ticket"] = self.ticket
                    
                response = await self._client.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    cookies=cookies
                )
                response.raise_for_status()
                return response.json()
            else:
                raise FleepAPIError(f"API request failed: {str(e)}")
    async def create_conversation(
        self,
        topic: Optional[str] = None,
        member_emails: Optional[str] = None,
        is_invite: bool = True,
        is_autojoin: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new conversation in Fleep.
        
        Args:
            topic: Optional topic for the conversation
            member_emails: List of email addresses to invite
            is_invite: Whether to send invitations to members
            is_autojoin: Whether members should auto-join the conversation
            
        Returns:
            Dictionary containing the created conversation details
        """
        data = {}
        
        if topic:
            data["topic"] = topic
        
        if member_emails:
            data["emails"] = member_emails
        
        if is_invite is not None:
            data["is_invite"] = is_invite
            
        if is_autojoin is not None:
            data["is_autojoin"] = is_autojoin
        
        return await self._make_request("POST", "conversation/create", data)
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
