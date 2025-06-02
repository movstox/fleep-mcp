# Fleep MCP Server

This project implements an unofficial MCP (Model Context Protocol) server to interact with the Fleep.io API.

## Setup

### Prerequisites

- Python 3.8 or higher
- `uv` package manager (recommended) or `pip`
- A Fleep.io account

### Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd fleep-mcp
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

3. Copy the environment file and configure your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Fleep credentials:
   ```
   FLEEP_EMAIL=your-email@example.com
   FLEEP_PASSWORD=your-password
   ```

### Running the Server

```bash
python -m src.main
```

## MCP Client Configuration

Once the server is running, you can configure MCP clients to use it. The server uses stdio transport and exposes tools for interacting with the Fleep.io API.

### Claude Desktop Configuration

To use this MCP server with Claude Desktop, add the following configuration to your Claude Desktop settings:

**On macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**On Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fleep-mcp": {
      "command": "python",
      "args": ["-m", "src.main"],
      "cwd": "/path/to/your/fleep-mcp",
      "env": {
        "FLEEP_EMAIL": "your-email@example.com",
        "FLEEP_PASSWORD": "your-password"
      }
    }
  }
}
```

**Important Notes:**
- Replace `/path/to/your/fleep-mcp` with the actual path to your fleep-mcp directory
- Replace the email and password with your actual Fleep credentials
- Ensure the Python environment has all required dependencies installed
- Restart Claude Desktop after adding the configuration

### Alternative: Using uv with Claude Desktop

If you're using `uv` for dependency management, you can configure Claude to use it:

```json
{
  "mcpServers": {
    ad
}
```

### Other MCP Clients

For other MCP clients that support stdio transport:

1. **Command:** `python -m src.main`
2. **Working Directory:** The fleep-mcp project directory
3. **Environment Variables:**
   - `FLEEP_EMAIL`: Your Fleep.io email address
   - `FLEEP_PASSWORD`: Your Fleep.io password
4. **Transport:** stdio
5. **Server Name:** fleep-mcp
6. **Server Version:** 0.1.0

### Available Tools

Once configured, the following tools will be available in your MCP client:

- **create_conversation**: Create new Fleep conversations with specified members and topics
- **send_message**: Send messages to existing Fleep conversations
- **get_conversation_labels**: Retrieve labels applied to a Fleep conversation
- **set_conversation_labels**: Apply labels to a Fleep conversation

### Troubleshooting

- **Server not connecting:** Ensure the path to the fleep-mcp directory is correct and Python can find the modules
- **Authentication errors:** Verify your Fleep credentials are correct in the environment variables
- **Missing dependencies:** Run `uv sync` or `pip install -e .` to ensure all dependencies are installed
- **Permission issues:** Ensure the MCP client has permission to execute Python and access the project directory

### Running Tests

```bash
pytest tests/
```

## Implemented Tools

### `create_conversation`

Create a new Fleep conversation with specified members and optional topic.

**Parameters:**
- `member_emails` (required): List of email addresses to invite to the conversation
- `topic` (optional): Topic for the conversation
- `is_invite` (optional, default: true): Whether to send invitations to members
- `is_autojoin` (optional, default: false): Whether members should auto-join the conversation

**Example Usage:**
```json
{
  "topic": "Project Discussion",
  "member_emails": "alice@example.com, bob@example.com",
  "is_invite": true,
  "is_autojoin": false
}
```

**Returns:**
- Success response with conversation details
- Error response with details if the operation fails

### `send_message`

Send a message to an existing Fleep conversation.

**Parameters:**
- `conversation_id` (required): The ID of the conversation to send the message to
- `message` (required): Message content to send
- `attachments` (optional): List of attachment URLs

**Example Usage:**
```json
{
  "conversation_id": "conv-123-456-789",
  "message": "Hello everyone! How is the project going?"
}
```

**With attachments:**
```json
{
  "conversation_id": "conv-123-456-789",
  "message": "Please review these documents",
  "attachments": [
    "https://example.com/document1.pdf",
    "https://example.com/image.jpg"
  ]
}
```

**Returns:**
- Success response with message details and conversation sync data
- Error response with details if the operation fails

**Note:** You can get the `conversation_id` from the response of the `create_conversation` tool, or you'll need to implement conversation lookup functionality to find conversations by topic.

### `get_conversation_labels`

Retrieve the current labels applied to a Fleep conversation.

**Parameters:**
- `conversation_id` (required): The ID of the conversation to get labels from

**Example Usage:**
```json
{
  "conversation_id": "conv-123-456-789"
}
```

**Returns:**
```json
{
  "success": true,
  "conversation_id": "conv-123-456-789",
  "labels": ["urgent", "project-alpha", "meeting"],
  "label_ids": ["uuid1", "uuid2", "uuid3"],
  "topic": "Project Planning Meeting",
  "label_count": 3,
  "message": "Found 3 label(s): urgent, project-alpha, meeting"
}
```

- Success response with current labels and conversation info
- Error response with details if the operation fails

### `set_conversation_labels`

Apply labels to a Fleep conversation. This will replace any existing labels.

**Parameters:**
- `conversation_id` (required): The ID of the conversation to set labels on
- `labels` (required): Array of label strings to apply to the conversation

**Example Usage:**
```json
{
  "conversation_id": "conv-123-456-789",
  "labels": ["urgent", "project-alpha", "meeting"]
}
```

**Clear all labels:**
```json
{
  "conversation_id": "conv-123-456-789",
  "labels": []
}
```

**Returns:**
```json
{
  "success": true,
  "conversation_id": "conv-123-456-789",
  "labels_set": ["urgent", "project-alpha", "meeting"],
  "label_count": 3,
  "message": "Successfully set 3 label(s): urgent, project-alpha, meeting"
}
```

- Success response with confirmation of labels set
- Error response with details if the operation fails

## API Documentation

For more information about the Fleep API, see: https://fleep.io/fleepapi/

## Development

See `Plan.md` for the full development roadmap and implementation status.
