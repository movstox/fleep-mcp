"""
Create Conversation Tool

Implements the create_conversation MCP tool for creating new Fleep conversations.
"""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

class CreateConversationRequest(BaseModel):
    """Request model for creating a conversation."""
    topic: Optional[str] = Field(None, description="Optional topic for the conversation")
    member_emails: Optional[str] = Field(
        None,
        description="List of email addresses to invite to the conversation"
    )
    is_invite: Optional[bool] = Field(
        True, 
        description="Whether to send invitations to members"
    )
    is_autojoin: Optional[bool] = Field(
        False, 
        description="Whether members should auto-join the conversation"
    )

class CreateConversationTool:
    """Tool for creating new Fleep conversations."""
    
    def __init__(self, fleep_client):
        self.fleep_client = fleep_client
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return the MCP tool definition."""
        return {
            "name": "create_conversation",
            "description": "Create a new Fleep conversation with specified members and optional topic",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Optional topic for the conversation"
                    },
                    "member_emails": {
                        "type": "string",
                        "description": "List of email addresses to invite to the conversation",
                    },
                    "is_invite": {
                        "type": "boolean",
                        "description": "Whether to send invitations to members (default: true)",
                        "default": True
                    },
                    "is_autojoin": {
                        "type": "boolean", 
                        "description": "Whether members should auto-join the conversation (default: false)",
                        "default": False
                    }
                },
                "required": []
            }
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the create_conversation tool.
        
        Args:
            arguments: Tool arguments containing conversation parameters
            
        Returns:
            Dictionary containing the created conversation details
            
        Raises:
            ValidationError: If the arguments are invalid
            Exception: If the API call fails
        """
        try:
            # Validate input arguments
            request = CreateConversationRequest(**arguments)
            
            # Call the Fleep API
            result = await self.fleep_client.create_conversation(
                topic=request.topic,
                member_emails=request.member_emails,
                is_invite=request.is_invite,
                is_autojoin=request.is_autojoin
            )
            
            # Format the response
            member_count = len(request.member_emails.split(',')) if request.member_emails else 0
            response = {
                "success": True,
                "conversation": result,
                "message": f"Successfully created conversation with {member_count} members"
            }
            
            if request.topic:
                response["message"] += f" and topic '{request.topic}'"
            
            return response
            
        except ValidationError as e:
            return {
                "success": False,
                "error": "Invalid arguments",
                "details": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "error": "Failed to create conversation",
                "details": str(e)
            }
