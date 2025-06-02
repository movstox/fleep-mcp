"""
Tests for the get_conversation_labels tool.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.get_conversation_labels import GetConversationLabelsTool


@pytest.fixture
def mock_fleep_client():
    """Create a mock Fleep client."""
    client = MagicMock()
    client.get_conversation_info = AsyncMock()
    return client


@pytest.fixture
def get_labels_tool(mock_fleep_client):
    """Create a GetConversationLabelsTool instance with mocked client."""
    return GetConversationLabelsTool(mock_fleep_client)


@pytest.mark.asyncio
async def test_get_conversation_labels_success(get_labels_tool, mock_fleep_client):
    """Test successful retrieval of conversation labels."""
    # Mock API response
    mock_response = {
        "header": {
            "conversation_id": "conv-123",
            "topic": "Project Discussion",
            "labels": ["urgent", "project-alpha"],
            "label_ids": ["uuid1", "uuid2"]
        }
    }
    mock_fleep_client.get_conversation_info.return_value = mock_response
    
    # Execute the tool
    arguments = {"conversation_id": "conv-123"}
    result = await get_labels_tool.execute(arguments)
    
    # Verify the result
    assert result["success"] is True
    assert result["conversation_id"] == "conv-123"
    assert result["labels"] == ["urgent", "project-alpha"]
    assert result["label_ids"] == ["uuid1", "uuid2"]
    assert result["topic"] == "Project Discussion"
    assert result["label_count"] == 2
    assert "Found 2 label(s)" in result["message"]
    
    # Verify API was called correctly
    mock_fleep_client.get_conversation_info.assert_called_once_with(
        conversation_id="conv-123",
        detail_level="ic_header"
    )


@pytest.mark.asyncio
async def test_get_conversation_labels_no_labels(get_labels_tool, mock_fleep_client):
    """Test retrieval when conversation has no labels."""
    # Mock API response with no labels
    mock_response = {
        "header": {
            "conversation_id": "conv-456",
            "topic": "Empty Discussion",
            "labels": [],
            "label_ids": []
        }
    }
    mock_fleep_client.get_conversation_info.return_value = mock_response
    
    # Execute the tool
    arguments = {"conversation_id": "conv-456"}
    result = await get_labels_tool.execute(arguments)
    
    # Verify the result
    assert result["success"] is True
    assert result["conversation_id"] == "conv-456"
    assert result["labels"] == []
    assert result["label_ids"] == []
    assert result["label_count"] == 0
    assert result["message"] == "No labels found for this conversation"


@pytest.mark.asyncio
async def test_get_conversation_labels_missing_conversation_id(get_labels_tool):
    """Test error handling when conversation_id is missing."""
    # Execute the tool without conversation_id
    arguments = {}
    result = await get_labels_tool.execute(arguments)
    
    # Verify error response
    assert result["success"] is False
    assert result["error"] == "Invalid arguments"
    assert "details" in result


@pytest.mark.asyncio
async def test_get_conversation_labels_api_error(get_labels_tool, mock_fleep_client):
    """Test error handling when API call fails."""
    # Mock API to raise an exception
    mock_fleep_client.get_conversation_info.side_effect = Exception("API Error")
    
    # Execute the tool
    arguments = {"conversation_id": "conv-789"}
    result = await get_labels_tool.execute(arguments)
    
    # Verify error response
    assert result["success"] is False
    assert result["error"] == "Failed to get conversation labels"
    assert "API Error" in result["details"]


def test_get_conversation_labels_tool_definition(get_labels_tool):
    """Test the tool definition."""
    definition = get_labels_tool.get_tool_definition()
    
    # Verify tool definition
    assert definition["name"] == "get_conversation_labels"
    assert "description" in definition
    assert "inputSchema" in definition
    assert definition["inputSchema"]["type"] == "object"
    assert "conversation_id" in definition["inputSchema"]["properties"]
    assert "conversation_id" in definition["inputSchema"]["required"]
