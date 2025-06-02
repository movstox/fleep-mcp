"""
Set Conversation Labels Tool

Implements the set_conversation_labels MCP tool for applying labels to Fleep conversations.
"""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

class SetConversationLabelsRequest(BaseModel):
    """Request model for setting conversation labels."""
    conversation_id: str = Field(description="The ID of the conversation to set labels on")
    labels: List[str] = Field(description="List of label strings to apply to the conversation")

class SetConversationLabelsTool:
    """Tool for setting labels on Fleep conversations."""
    
    def __init__(self, fleep_client):
        self.fleep_client = fleep_client
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return the MCP tool definition."""
        return {
            "name": "set_conversation_labels",
            "description": "Set labels on a Fleep conversation. This will replace any existing labels.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "conversation_id": {
                        "type": "string",
                        "description": "The ID of the conversation to set labels on"
                    },
                    "labels": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of label strings to apply to the conversation",
                        "examples": [["urgent", "project-alpha"], ["meeting", "important"]]
                    }
                },
                "required": ["conversation_id", "labels"]
            }
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the set_conversation_labels tool.
        
        Args:
            arguments: Tool arguments containing conversation_id and labels
            
        Returns:
            Dictionary containing the result of setting labels
            
        Raises:
            ValidationError: If the arguments are invalid
            Exception: If the API call fails
        """
        try:
            # Validate input arguments
            request = SetConversationLabelsRequest(**arguments)
            
            # Call the Fleep API to set labels
            result = await self.fleep_client.set_conversation_labels(
                conversation_id=request.conversation_id,
                labels=request.labels
            )
            
            # Format the response
            response = {
                "success": True,
                "conversation_id": request.conversation_id,
                "labels_set": request.labels,
                "label_count": len(request.labels),
                "api_response": result
            }
            
            if request.labels:
                response["message"] = f"Successfully set {len(request.labels)} label(s): {', '.join(request.labels)}"
            else:
                response["message"] = "Successfully cleared all labels from the conversation"
            
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
                "error": "Failed to set conversation labels",
                "details": str(e)
            }
