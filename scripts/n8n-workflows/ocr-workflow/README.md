# OCR Workflow

An n8n sub-workflow that uses Mistral AI's OCR API to extract structured text from
insurance declaration pages and renewal documents. The extracted content is returned
as clean markdown — tables, headers, and all — ready for manual or automated CRM
data entry.

## What It Does

Takes a PDF (declarations page, renewal offer, or similar insurance document) and
returns fully extracted text and tables in markdown format. The goal is to eliminate
manual re-typing when quoting a policy — you feed it the document, it pulls out the
coverage details, limits, premiums, and carrier info.

## How It Works

```
[Receive PDF binary] → [Upload to Mistral] → [Get signed URL] → [OCR API] → [Return markdown]
```

1. **Upload** — sends the PDF to Mistral's Files API (`/v1/files`) with `purpose: ocr`
2. **Get URL** — retrieves a time-limited signed URL for the uploaded file
3. **OCR** — calls Mistral's OCR endpoint (`/v1/ocr`) with `mistral-ocr-latest`
4. **Return** — passes back the full markdown result including all tables and page structure

## Input / Output

**Input** (passed from parent workflow):
```json
{ "File": "<binary PDF data>" }
```

**Output** — markdown text per page, separated by `---`, e.g.:

```markdown
## Auto Policy — Your Name
**Policy Number**: PA-1234567
**Effective**: 01/01/2026 – 01/01/2027

| Coverage | Limit | Premium |
|----------|-------|---------|
| Bodily Injury | 100/300k | $420 |
| Property Damage | 100k | $180 |
| Comprehensive | $500 ded | $95 |
| Collision | $500 ded | $210 |

---

[next page...]
```

## Architecture

This is a **sub-workflow** — it is called from a parent workflow that handles
receiving/fetching the PDF (e.g., from email attachment, form upload, or manual trigger).

```
[Parent Workflow]
      │  (binary PDF)
      ▼
[executeWorkflowTrigger]
      │
      ▼
[Upload to Mistral] → [Get URL] → [OCR API] → [Return markdown]
```

## Credentials Required

| Credential | Purpose |
|-----------|---------|
| Mistral API key (HTTP Header Auth) | Authenticate all Mistral API calls |

Configure in n8n as an **HTTP Header Auth** credential:
- Header name: `Authorization`
- Value: `Bearer <your-mistral-api-key>`

## Use Case: Insurance Quoting

The intended workflow for quoting:

1. Client emails or uploads a declarations page or renewal offer
2. Parent workflow receives the PDF attachment and calls this sub-workflow
3. This workflow OCRs the document and returns structured markdown
4. A downstream node (or the agent workflow) parses the markdown into fields
5. Fields are entered into the CRM quoting system

This replaces manually reading and typing coverage details from PDFs — the agent
can read the extracted markdown and populate quote fields directly.

## Notes

- Works best on text-based PDFs (digitally generated); handles scanned docs too
  but quality depends on scan resolution
- `include_image_base64: true` is set — embedded images are returned as base64
  if needed for further processing
- Mistral deletes uploaded files automatically after processing (no storage concerns)

## Installation

1. Import `workflow.json` into your n8n instance
2. Add a Mistral API key as an HTTP Header Auth credential named `Mistral OCR`
3. Build or connect a parent workflow that provides the PDF binary as `File`
4. Test with a sample declarations page PDF
