"""
Tests for the set_conversation_labels tool.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.set_conversation_labels import SetConversationLabelsTool

@pytest.fixture
def mock_fleep_client():
    """Create a mock Fleep client."""
    client = MagicMock()
    client.set_conversation_labels = AsyncMock()
    return client

@pytest.fixture
def set_labels_tool(mock_fleep_client):
    """Create a SetConversationLabelsTool instance with mocked client."""
    return SetConversationLabelsTool(mock_fleep_client)

@pytest.mark.asyncio
async def test_set_conversation_labels_success(set_labels_tool, mock_fleep_client):
    """Test successful setting of conversation labels."""
    # Mock API response
    mock_response = {"status": "success", "conversation_id": "conv-123"}
    mock_fleep_client.set_conversation_labels.return_value = mock_response
    
    # Execute the tool
    arguments = {
        "conversation_id": "conv-123",
        "labels": ["urgent", "project-alpha", "meeting"]
    }
    result = await set_labels_tool.execute(arguments)
    
    # Verify the result
    assert result["success"] is True
    assert result["conversation_id"] == "conv-123"
    assert result["labels_set"] == ["urgent", "project-alpha", "meeting"]
    assert result["label_count"] == 3
    assert "Successfully set 3 label(s)" in result["message"]
    assert result["api_response"] == mock_response
    
    # Verify API was called correctly
    mock_fleep_client.set_conversation_labels.assert_called_once_with(
        conversation_id="conv-123",
        labels=["urgent", "project-alpha", "meeting"]
    )

@pytest.mark.asyncio
async def test_set_conversation_labels_empty_list(set_labels_tool, mock_fleep_client):
    """Test setting empty labels list (clearing labels)."""
    # Mock API response
    mock_response = {"status": "success", "conversation_id": "conv-456"}
    mock_fleep_client.set_conversation_labels.return_value = mock_response
    
    # Execute the tool with empty labels
    arguments = {
        "conversation_id": "conv-456",
        "labels": []
    }
    result = await set_labels_tool.execute(arguments)
    
    # Verify the result
    assert result["success"] is True
    assert result["conversation_id"] == "conv-456"
    assert result["labels_set"] == []
    assert result["label_count"] == 0
    assert result["message"] == "Successfully cleared all labels from the conversation"

@pytest.mark.asyncio
async def test_set_conversation_labels_single_label(set_labels_tool, mock_fleep_client):
    """Test setting a single label."""
    # Mock API response
    mock_response = {"status": "success", "conversation_id": "conv-789"}
    mock_fleep_client.set_conversation_labels.return_value = mock_response
    
    # Execute the tool with single label
    arguments = {
        "conversation_id": "conv-789",
        "labels": ["important"]
    }
    result = await set_labels_tool.execute(arguments)
    
    # Verify the result
    assert result["success"] is True
    assert result["conversation_id"] == "conv-789"
    assert result["labels_set"] == ["important"]
    assert result["label_count"] == 1
    assert "Successfully set 1 label(s): important" in result["message"]

@pytest.mark.asyncio
async def test_set_conversation_labels_missing_conversation_id(set_labels_tool):
    """Test error handling when conversation_id is missing."""
    # Execute the tool without conversation_id
    arguments = {"labels": ["test"]}
    result = await set_labels_tool.execute(arguments)
    
    # Verify error response
    assert result["success"] is False
    assert result["error"] == "Invalid arguments"
    assert "details" in result

@pytest.mark.asyncio
async def test_set_conversation_labels_missing_labels(set_labels_tool):
    """Test error handling when labels are missing."""
    # Execute the tool without labels
    arguments = {"conversation_id": "conv-123"}
    result = await set_labels_tool.execute(arguments)
    
    # Verify error response
    assert result["success"] is False
    assert result["error"] == "Invalid arguments"
    assert "details" in result

@pytest.mark.asyncio
async def test_set_conversation_labels_api_error(set_labels_tool, mock_fleep_client):
    """Test error handling when API call fails."""
    # Mock API to raise an exception
    mock_fleep_client.set_conversation_labels.side_effect = Exception("API Error")
    
    # Execute the tool
    arguments = {
        "conversation_id": "conv-error",
        "labels": ["test"]
    }
    result = await set_labels_tool.execute(arguments)
    
    # Verify error response
    assert result["success"] is False
    assert result["error"] == "Failed to set conversation labels"
    assert "API Error" in result["details"]

def test_set_conversation_labels_tool_definition(set_labels_tool):
    """Test the tool definition."""
    definition = set_labels_tool.get_tool_definition()
    
    # Verify tool definition
    assert definition["name"] == "set_conversation_labels"
    assert "description" in definition
    assert "inputSchema" in definition
    assert definition["inputSchema"]["type"] == "object"
    
    # Check properties
    properties = definition["inputSchema"]["properties"]
    assert "conversation_id" in properties
    assert "labels" in properties
    assert properties["labels"]["type"] == "array"
    assert properties["labels"]["items"]["type"] == "string"
    
    # Check required fields
    required = definition["inputSchema"]["required"]
    assert "conversation_id" in required
    assert "labels" in required
