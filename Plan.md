# Fleep MCP Server Development Plan

This document outlines the plan for developing an MCP server to interact with the Fleep.io API.

Fleep API Documentation: [https://fleep.io/fleepapi/](https://fleep.io/fleepapi/)

## I. Project Setup and Initialization
- [ ] Initialize a new project directory for the MCP server.
- [ ] Set up the basic project structure (e.g., `src`, `tests`, `docs`).
- [ ] Initialize a version control system (e.g., Git).
- [ ] Define project dependencies (e.g., HTTP client, MCP SDK if available).
- [ ] Create a README.md with project description and setup instructions.

## II. Authentication
- [ ] Implement Fleep API authentication (OAuth or token-based).
- [ ] Securely store and manage API credentials/tokens.
- [ ] Create helper functions for making authenticated API requests.
- [ ] Implement token refresh logic if applicable.

## III. Core MCP Server Tools (Priority 1 - Essential)

### 1. `send_message`
    - **Description**: Send a message to a specified Fleep conversation.
    - **Fleep API Endpoint(s)**: `message/send/CONV_ID`
    - **Inputs**: `conversation_id`, `message_content`, `attachments (optional)`
    - **Outputs**: Confirmation of message sent, message details.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 2. `list_conversations`
    - **Description**: Retrieve a list of all conversations the authenticated user is part of.
    - **Fleep API Endpoint(s)**: `conversation/list`
    - **Inputs**: `(None)`
    - **Outputs**: List of conversation objects (ID, topic, members, last message snippet).
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 3. `get_conversation_messages`
    - **Description**: Retrieve messages from a specific conversation.
    - **Fleep API Endpoint(s)**: `conversation/sync/CONV_ID`, `conversation/sync_backward/CONV_ID`
    - **Inputs**: `conversation_id`, `limit (optional)`, `before_message_nr (optional for pagination)`
    - **Outputs**: List of message objects (ID, sender, content, timestamp, attachments).
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 4. `create_conversation`
    - **Description**: Create a new Fleep conversation.
    - **Fleep API Endpoint(s)**: `conversation/create`
    - **Inputs**: `topic (optional)`, `member_emails_or_ids`, `is_invite (optional)`, `is_autojoin (optional)`
    - **Outputs**: Newly created conversation object.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 5. `search_messages`
    - **Description**: Search for messages across all user's conversations.
    - **Fleep API Endpoint(s)**: `search`
    - **Inputs**: `query_string`, `conversation_id_filter (optional)`
    - **Outputs**: List of matching message objects with context.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

## IV. Communication Tools (Priority 2)

### 6. `add_conversation_members`
    - **Description**: Add one or more members to an existing conversation.
    - **Fleep API Endpoint(s)**: `conversation/add_members/CONV_ID`
    - **Inputs**: `conversation_id`, `member_emails_or_ids`
    - **Outputs**: Confirmation of members added.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 7. `remove_conversation_members`
    - **Description**: Remove members from a conversation.
    - **Fleep API Endpoint(s)**: `conversation/remove_members/CONV_ID`
    - **Inputs**: `conversation_id`, `member_ids_to_remove`
    - **Outputs**: Confirmation of members removed.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 8. `set_conversation_topic`
    - **Description**: Update the topic of a conversation.
    - **Fleep API Endpoint(s)**: `conversation/set_topic/CONV_ID`
    - **Inputs**: `conversation_id`, `new_topic`
    - **Outputs**: Confirmation of topic change.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 9. `mark_messages_read`
    - **Description**: Mark messages in a conversation as read up to a certain point.
    - **Fleep API Endpoint(s)**: `message/mark_read/CONV_ID`, `conversation/mark_read/CONV_ID`
    - **Inputs**: `conversation_id`, `last_read_message_nr`
    - **Outputs**: Confirmation.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

## V. Advanced Tools (Priority 3)

### 10. `edit_message`
    - **Description**: Edit an existing message sent by the user.
    - **Fleep API Endpoint(s)**: `message/edit/CONV_ID`
    - **Inputs**: `conversation_id`, `message_nr`, `new_message_content`
    - **Outputs**: Updated message object.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 11. `delete_message`
    - **Description**: Delete a message sent by the user.
    - **Fleep API Endpoint(s)**: `message/delete/CONV_ID`
    - **Inputs**: `conversation_id`, `message_nr`
    - **Outputs**: Confirmation of deletion.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 12. `upload_file`
    - **Description**: Upload a file to a conversation.
    - **Fleep API Endpoint(s)**: `file/upload/`
    - **Inputs**: `conversation_id`, `file_path_or_data`, `message_content (optional)`
    - **Outputs**: File info object, confirmation.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 13. `manage_conversation_settings`
    - **Description**: Configure various settings for a conversation (e.g., notifications, autojoin, disclose history).
    - **Fleep API Endpoint(s)**: `conversation/set_alerts/CONV_ID`, `conversation/autojoin` (related, for enabling/disabling), `conversation/disclose/CONV_ID`
    - **Inputs**: `conversation_id`, `setting_name`, `setting_value`
    - **Outputs**: Confirmation of setting change.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 14. `get_contacts`
    - **Description**: Retrieve the user's contact list from Fleep.
    - **Fleep API Endpoint(s)**: `contact/sync`, `contact/sync/list`
    - **Inputs**: `(None)`
    - **Outputs**: List of contact objects.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

## VI. Account Tools (Priority 4)

### 15. `get_account_info`
    - **Description**: Retrieve information about the authenticated user's Fleep account.
    - **Fleep API Endpoint(s)**: `account/poll` (can provide account info as part of sync) or a more specific endpoint if available.
    - **Inputs**: `(None)`
    - **Outputs**: Account information object (name, email, avatar, etc.).
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

### 16. `configure_notifications`
    - **Description**: Manage global notification settings for the Fleep account.
    - **Fleep API Endpoint(s)**: `account/configure` (likely covers notification settings)
    - **Inputs**: `notification_settings_object`
    - **Outputs**: Confirmation of settings updated.
    - [ ] Implement tool logic.
    - [ ] Add unit tests.

## VII. General MCP Server Implementation
- [ ] Define clear input and output schemas for each MCP tool.
- [ ] Implement robust error handling and provide meaningful error messages.
- [ ] Ensure all API calls handle Fleep API rate limits gracefully.
- [ ] Write comprehensive unit tests for all tools and helper functions.
- [ ] Create integration tests to verify end-to-end functionality.
- [ ] Document each tool's usage, parameters, and expected behavior within the MCP server.
- [ ] Consider logging for debugging and monitoring.

## VIII. Deployment and Maintenance
- [ ] Prepare deployment scripts or configurations.
- [ ] Set up a CI/CD pipeline for automated testing and deployment.
- [ ] Plan for ongoing maintenance and updates as the Fleep API evolves.
