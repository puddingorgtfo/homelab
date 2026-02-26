# Gmail Auto Response Agent

An n8n sub-workflow that monitors incoming insurance-related emails and automatically
drafts a professional reply — without sending it. Each draft is threaded to the original
email conversation and left for a licensed agent to review, edit, and send.

## What It Does

1. Receives an incoming Gmail message (forwarded from a parent trigger workflow)
2. Reads the full email thread for context
3. Uses an AI agent to draft an appropriate insurance-industry reply
4. Creates the draft in Gmail, threaded to the original sender's conversation
5. Outputs a structured summary of the email and the draft for review

**The workflow never sends email.** Every response is staged as an unsent draft.

## Key Behaviors

- **Always requests declarations page** — for any email involving quotes, policy changes,
  renewals, claims, or comparisons, the draft asks the client to forward their current
  declarations page or renewal offer (unless one is already in the thread)
- **Draft-only** — if it ever sent email automatically, it would be removed
- **One draft per email** — never creates duplicate drafts for the same message
- **Disclaimer control** — only adds policy disclaimers when the email topic warrants it
  (quotes, binders, coverage questions), not on routine replies

## Architecture

This is a **sub-workflow** — it is triggered by a parent workflow that handles the Gmail
polling trigger. It is not meant to be activated standalone.

```
[Parent: Gmail Trigger]
       │
       ▼
[executeWorkflowTrigger] → [AI Agent] → drafts reply in Gmail
```

The AI agent has access to the full thread history passed in from the parent.

## Output Format

After processing each email, the workflow produces:

```
📧 NEW EMAIL PROCESSED - DRAFT READY FOR REVIEW
FROM: [Sender]
SUBJECT: [Subject]
RECEIVED: [Date/Time]
PRIORITY: [Level]
FLAGS: [Any flags]
━━━━━━━━━━━━━━━━━━━━━━
ORIGINAL EMAIL THREAD:
[...full thread...]
━━━━━━━━━━━━━━━━━━━━━━
DRAFTED RESPONSE (THREADED AS UNSENT DRAFT ONLY):
[...draft with dec-page request when applicable...]
━━━━━━━━━━━━━━━━━━━━━━
REVIEW NOTES:
- Email Type: [...]
- Priority Level: [...]
- Requires Licensed Agent Review: [Yes/No]
- Missing Information: [e.g., "Waiting on current declarations page"]
```

## Credentials Required

| Credential | Purpose |
|-----------|---------|
| Gmail OAuth2 | Read threads, create draft replies |
| LLM API (Claude/OpenAI via OpenRouter) | Generate draft content |

## Customization

Before deploying, update the AI Agent system prompt with your agency's details:

- **Company name** — appears in the email signature
- **Agent name** — signing the drafts
- **Phone number** — included in signature and call-to-action lines
- **Email address** — reply-from address in signature

The tone, disclaimer rules, and dec-page request language can all be edited in the
system prompt inside the AI Agent node.

## Installation

1. Import `workflow.json` into your n8n instance
2. Configure Gmail OAuth2 credentials
3. Configure your LLM credentials (Claude or OpenRouter)
4. Update the AI Agent system prompt with your agency info
5. Set up a parent workflow with a Gmail Trigger that calls this sub-workflow
6. Activate the parent workflow (not this one directly)
