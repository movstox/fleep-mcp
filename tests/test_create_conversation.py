"""
Tests for the create_conversation tool.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from src.fleep_client import FleepClient
from src.tools.create_conversation import CreateConversationTool


class TestCreateConversationTool:
    """Test suite for CreateConversationTool."""
    
    @pytest.fixture
    def mock_fleep_client(self):
        """Create a mock Fleep client."""
        client = Mock(spec=FleepClient)
        client.create_conversation = AsyncMock()
        return client
    
    @pytest.fixture
    def create_conversation_tool(self, mock_fleep_client):
        """Create a CreateConversationTool instance with mocked client."""
        return CreateConversationTool(mock_fleep_client)
    
    def test_get_tool_definition(self, create_conversation_tool):
        """Test that the tool definition is correctly formatted."""
        definition = create_conversation_tool.get_tool_definition()
        
        assert definition["name"] == "create_conversation"
        assert "description" in definition
        assert "inputSchema" in definition
        
        schema = definition["inputSchema"]
        assert schema["type"] == "object"
        assert schema["required"] == []  # No required fields in actual implementation
        assert "member_emails" in schema["properties"]
        assert "topic" in schema["properties"]
        assert "is_invite" in schema["properties"]
        assert "is_autojoin" in schema["properties"]
    
    @pytest.mark.asyncio
    async def test_execute_with_valid_arguments(self, create_conversation_tool, mock_fleep_client):
        """Test successful execution with valid arguments."""
        # Mock the API response
        mock_response = {
            "conversation_id": "conv_123",
            "topic": "Test Conversation",
            "members": ["user1@example.com", "user2@example.com"]
        }
        mock_fleep_client.create_conversation.return_value = mock_response
        
        # Execute the tool
        arguments = {
            "topic": "Test Conversation",
            "member_emails": "user1@example.com,user2@example.com",
            "is_invite": True,
            "is_autojoin": False
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        # Verify the result
        assert result["success"] is True
        assert result["conversation"] == mock_response
        assert "Successfully created conversation" in result["message"]
        assert "Test Conversation" in result["message"]
        
        # Verify the client was called correctly
        mock_fleep_client.create_conversation.assert_called_once_with(
            topic="Test Conversation",
            member_emails="user1@example.com,user2@example.com",
            is_invite=True,
            is_autojoin=False
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_minimal_arguments(self, create_conversation_tool, mock_fleep_client):
        """Test execution with only required arguments."""
        # Mock the API response
        mock_response = {
            "conversation_id": "conv_456",
            "members": ["user@example.com"]
        }
        mock_fleep_client.create_conversation.return_value = mock_response
        
        # Execute the tool with minimal arguments
        arguments = {
            "member_emails": "user@example.com"
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        # Verify the result
        assert result["success"] is True
        assert result["conversation"] == mock_response
        assert "Successfully created conversation with 1 members" in result["message"]
        
        # Verify the client was called with defaults
        mock_fleep_client.create_conversation.assert_called_once_with(
            topic=None,
            member_emails="user@example.com",
            is_invite=True,
            is_autojoin=False
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_no_member_emails(self, create_conversation_tool, mock_fleep_client):
        """Test execution with no member_emails (should succeed)."""
        # Mock the API response
        mock_response = {
            "conversation_id": "conv_789",
            "topic": "Test Conversation"
        }
        mock_fleep_client.create_conversation.return_value = mock_response
        
        # Test with missing member_emails (should be allowed)
        arguments = {
            "topic": "Test Conversation"
            # Missing member_emails
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        assert result["success"] is True
        assert result["conversation"] == mock_response
        assert "Successfully created conversation with 0 members" in result["message"]
        
        # Verify the client was called correctly
        mock_fleep_client.create_conversation.assert_called_once_with(
            topic="Test Conversation",
            member_emails=None,
            is_invite=True,
            is_autojoin=False
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_empty_member_emails(self, create_conversation_tool, mock_fleep_client):
        """Test execution with empty member_emails string."""
        # Mock the API response
        mock_response = {
            "conversation_id": "conv_empty",
            "members": []
        }
        mock_fleep_client.create_conversation.return_value = mock_response
        
        arguments = {
            "member_emails": ""  # Empty string should be allowed
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        assert result["success"] is True
        assert result["conversation"] == mock_response
        assert "Successfully created conversation with 0 members" in result["message"]
        
        # Verify the client was called correctly
        mock_fleep_client.create_conversation.assert_called_once_with(
            topic=None,
            member_emails="",
            is_invite=True,
            is_autojoin=False
        )
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_field_type(self, create_conversation_tool):
        """Test execution with invalid field types (should trigger validation error)."""
        arguments = {
            "member_emails": 123,  # Should be string, not int
            "is_invite": "invalid"  # Should be boolean, not string
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        assert result["success"] is False
        assert result["error"] == "Invalid arguments"
        assert "details" in result
    
    @pytest.mark.asyncio
    async def test_execute_with_api_error(self, create_conversation_tool, mock_fleep_client):
        """Test execution when API call fails."""
        # Mock the client to raise an exception
        mock_fleep_client.create_conversation.side_effect = Exception("API Error")
        
        arguments = {
            "member_emails": "user@example.com"
        }
        
        result = await create_conversation_tool.execute(arguments)
        
        assert result["success"] is False
        assert result["error"] == "Failed to create conversation"
        assert "API Error" in result["details"]
