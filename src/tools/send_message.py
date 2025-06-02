"""
Send Message Tool

Implements the send_message MCP tool for sending messages to Fleep conversations.
"""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

class SendMessageRequest(BaseModel):
    """Request model for sending a message."""
    conversation_id: str = Field(
        description="Conversation ID where to send the message"
    )
    message: str = Field(
        description="Message content to send"
    )
    attachments: Optional[List[str]] = Field(
        None, 
        description="Optional list of attachment URLs"
    )

class SendMessageTool:
    """Tool for sending messages to Fleep conversations."""
    
    def __init__(self, fleep_client):
        self.fleep_client = fleep_client
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return the MCP tool definition."""
        return {
            "name": "send_message",
            "description": "Send a message to a Fleep conversation by conversation ID",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "conversation_id": {
                        "type": "string",
                        "description": "Conversation ID where to send the message"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content to send"
                    },
                    "attachments": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of attachment URLs"
                    }
                },
                "required": ["conversation_id", "message"]
            }
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the send_message tool.
        
        Args:
            arguments: Tool arguments containing message parameters
            
        Returns:
            Dictionary containing the message send result
            
        Raises:
            ValidationError: If the arguments are invalid
            Exception: If the API call fails
        """
        try:
            # Validate input arguments
            request = SendMessageRequest(**arguments)
            
            # Call the Fleep API
            result = await self.fleep_client.send_message(
                conversation_id=request.conversation_id,
                message=request.message,
                attachments=request.attachments
            )
            
            # Format the response
            response = {
                "success": True,
                "result": result,
                "message": f"Successfully sent message to conversation {request.conversation_id}"
            }
            
            if request.attachments:
                attachment_count = len(request.attachments)
                response["message"] += f" with {attachment_count} attachment{'s' if attachment_count > 1 else ''}"
            
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
                "error": "Failed to send message",
                "details": str(e)
            }
