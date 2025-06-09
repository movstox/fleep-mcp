"""
Tests for the send_message tool

Tests the send_message MCP tool functionality.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from src.tools.send_message import SendMessageTool, SendMessageRequest


class TestSendMessageRequest:
    """Test the SendMessageRequest model."""
    
    def test_valid_request(self):
        """Test creating a valid send message request."""
        request = SendMessageRequest(
            conversation_id="test-conv-123",
            message="Hello, World!"
        )
        assert request.conversation_id == "test-conv-123"
        assert request.message == "Hello, World!"
        assert request.attachments is None
    
    def test_request_with_attachments(self):
        """Test creating a request with attachments."""
        attachments = ["https://example.com/file1.jpg", "https://example.com/file2.pdf"]
        request = SendMessageRequest(
            conversation_id="test-conv-123",
            message="Check out these files!",
            attachments=attachments
        )
        assert request.conversation_id == "test-conv-123"
        assert request.message == "Check out these files!"
        assert request.attachments == attachments
    
    def test_request_missing_conversation_id(self):
        """Test that conversation_id is required."""
        with pytest.raises(ValueError):
            SendMessageRequest(message="Hello!")
    
    def test_request_empty_message(self):
        """Test request with empty message."""
        request = SendMessageRequest(
            conversation_id="test-conv-123",
            message=""
        )
        assert request.conversation_id == "test-conv-123"
        assert request.message == ""


class TestSendMessageTool:
    """Test the SendMessageTool class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_fleep_client = AsyncMock()
        self.tool = SendMessageTool(self.mock_fleep_client)
    
    def test_tool_definition(self):
        """Test the tool definition matches expected schema."""
        definition = self.tool.get_tool_definition()
        
        assert definition["name"] == "send_message"
        assert "description" in definition
        assert "inputSchema" in definition
        
        schema = definition["inputSchema"]
        assert schema["type"] == "object"
        assert "conversation_id" in schema["properties"]
        assert "message" in schema["properties"]
        assert "attachments" in schema["properties"]
        assert schema["required"] == ["conversation_id", "message"]
    
    @pytest.mark.asyncio
    async def test_execute_successful_message(self):
        """Test successful message sending."""
        # Mock the API response
        mock_response = {
            "conversation": {"id": "test-conv-123"},
            "messages": [{"content": "Hello, World!", "message_nr": 1}]
        }
        self.mock_fleep_client.send_message.return_value = mock_response
        
        arguments = {
            "conversation_id": "test-conv-123",
            "message": "Hello, World!"
        }
        
        result = await self.tool.execute(arguments)
        
        assert result["success"] is True
        assert "Successfully sent message to conversation test-conv-123" in result["message"]
        assert result["result"] == mock_response
        
        # Verify the client was called correctly
        self.mock_fleep_client.send_message.assert_called_once_with(
            conversation_id="test-conv-123",
            message="Hello, World!",
            attachments=None
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_attachments(self):
        """Test sending message with attachments."""
        mock_response = {
            "conversation": {"id": "test-conv-123"},
            "messages": [{"content": "Check this out!", "message_nr": 1}]
        }
        self.mock_fleep_client.send_message.return_value = mock_response
        
        attachments = ["https://example.com/file.jpg"]
        arguments = {
            "conversation_id": "test-conv-123",
            "message": "Check this out!",
            "attachments": attachments
        }
        
        result = await self.tool.execute(arguments)
        
        assert result["success"] is True
        assert "with 1 attachment" in result["message"]
        
        # Verify the client was called correctly
        self.mock_fleep_client.send_message.assert_called_once_with(
            conversation_id="test-conv-123",
            message="Check this out!",
            attachments=attachments
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_multiple_attachments(self):
        """Test sending message with multiple attachments."""
        mock_response = {
            "conversation": {"id": "test-conv-123"},
            "messages": [{"content": "Multiple files!", "message_nr": 1}]
        }
        self.mock_fleep_client.send_message.return_value = mock_response
        
        attachments = ["https://example.com/file1.jpg", "https://example.com/file2.pdf"]
        arguments = {
            "conversation_id": "test-conv-123",
            "message": "Multiple files!",
            "attachments": attachments
        }
        
        result = await self.tool.execute(arguments)
        
        assert result["success"] is True
        assert "with 2 attachments" in result["message"]
    
    @pytest.mark.asyncio
    async def test_execute_invalid_arguments(self):
        """Test execution with invalid arguments."""
        arguments = {
            "message": "Hello!"
            # Missing conversation_id
        }
        
        result = await self.tool.execute(arguments)
        
        assert result["success"] is False
        assert result["error"] == "Invalid arguments"
        assert "details" in result
        
        # Client should not be called
        self.mock_fleep_client.send_message.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_execute_api_error(self):
        """Test execution when API call fails."""
        self.mock_fleep_client.send_message.side_effect = Exception("API Error")
        
        arguments = {
            "conversation_id": "test-conv-123",
            "message": "Hello, World!"
        }
        
        result = await self.tool.execute(arguments)
        
        assert result["success"] is False
        assert result["error"] == "Failed to send message"
        assert "API Error" in result["details"]
