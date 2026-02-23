# AI Message Router

An n8n workflow that routes and processes messages through an AI assistant with calendar and email capabilities.

## Features

- **AI-Powered Message Processing**: Uses GPT-4o-mini via OpenRouter
- **Conversation Memory**: Maintains conversation history across sessions
- **Calendar Management**: Create, find, update, and delete calendar events
- **Email Integration**: Send and draft emails via Gmail
- **Multi-Interface Support**: Can be called from various messaging interfaces

## Architecture

This workflow acts as a central routing and processing hub for AI-assisted tasks:

```
Message Input → Get Conversation History → AI Assistant → Tools
                                                         ├─ Send Email
                                                         ├─ Draft Email
                                                         ├─ Check Calendar
                                                         ├─ Create Event
                                                         ├─ Find Event
                                                         ├─ Update Event
                                                         └─ Delete Event
```

## Prerequisites

- n8n instance (self-hosted or cloud)
- OpenRouter API key
- Google Calendar API credentials
- Gmail API credentials
- Conversation Memory Service workflow (ID: jZ26iaV1hcAJTmiq)
- Calendar Service workflow (ID: nEH1yjfFeIJBazA2)
- Gmail Service workflow (ID: fbfzBFXzHwQzcKrw)

## Installation

1. **Import Workflow**
   - In n8n, go to Workflows → Import from File
   - Import `workflow.json`

2. **Configure Credentials**
   - OpenRouter API
   - Google Calendar OAuth2
   - Gmail OAuth2

3. **Update Workflow References**
   - Update workflow IDs to match your installed sub-workflows:
     - Conversation Memory Service
     - Calendar Service
     - Gmail Service

4. **Activate Workflow**
   - Activate all dependent workflows first
   - Then activate this workflow

## Configuration

### Timezone
Default timezone is `America/New_York`. To change it, update the system message in the AI Personal Assistant node.

### LLM Model
Default model is `openai/gpt-4o-mini`. You can change this in the OpenRouter LLM node.

## Usage

This workflow is designed to be called by other workflows (Telegram bot, Slack bot, etc.). It expects the following input:

```json
{
  "message_text": "User's message text",
  "user_id": "unique_user_identifier"
}
```

## Troubleshooting

### "Workflow not found" errors
Ensure all dependent workflows are:
- Imported correctly
- Using the correct IDs in the workflow configuration
- Activated

### Invalid credentials
Re-authenticate credentials in n8n settings.

## License

MIT

## Author

Created for n8n workflow automation.
