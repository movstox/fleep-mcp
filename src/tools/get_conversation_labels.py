"""
Get Conversation Labels Tool

Implements the get_conversation_labels MCP tool for retrieving labels from Fleep conversations.
"""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

class GetConversationLabelsRequest(BaseModel):
    """Request model for getting conversation labels."""
    conversation_id: str = Field(description="The ID of the conversation to get labels from")

class GetConversationLabelsTool:
    """Tool for retrieving labels from Fleep conversations."""
    
    def __init__(self, fleep_client):
        self.fleep_client = fleep_client
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return the MCP tool definition."""
        return {
            "name": "get_conversation_labels",
            "description": "Get the current labels applied to a Fleep conversation",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "conversation_id": {
                        "type": "string",
                        "description": "The ID of the conversation to get labels from"
                    }
                },
                "required": ["conversation_id"]
            }
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the get_conversation_labels tool.
        
        Args:
            arguments: Tool arguments containing conversation_id
            
        Returns:
            Dictionary containing the conversation labels
            
        Raises:
            ValidationError: If the arguments are invalid
            Exception: If the API call fails
        """
        try:
            # Validate input arguments
            request = GetConversationLabelsRequest(**arguments)
            
            # Call the Fleep API to get conversation info
            result = await self.fleep_client.get_conversation_info(
                conversation_id=request.conversation_id,
                detail_level="ic_header"  # Only need header info for labels
            )
            
            # Extract conversation info from the response
            conv_info = result.get("header", {})
            labels = conv_info.get("labels", [])
            label_ids = conv_info.get("label_ids", [])
            topic = conv_info.get("topic", "")
            conversation_id = conv_info.get("conversation_id", request.conversation_id)
            
            # Format the response
            response = {
                "success": True,
                "conversation_id": conversation_id,
                "labels": labels,
                "label_ids": label_ids,
                "topic": topic,
                "label_count": len(labels)
            }
            
            if labels:
                response["message"] = f"Found {len(labels)} label(s): {', '.join(labels)}"
            else:
                response["message"] = "No labels found for this conversation"
            
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
                "error": "Failed to get conversation labels",
                "details": str(e)
            }
