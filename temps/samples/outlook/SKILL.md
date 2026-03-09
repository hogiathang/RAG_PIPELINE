---
name: outlook
description: Microsoft Outlook for macOS integration via MCP. Manage emails, calendar, and contacts without API requirements. Uses your existing Outlook SSO session.
isolated-context: false
allowed-tools: execute, bash, read_file, write_file
mcp-server: outlook-macos
---

# Microsoft Outlook for macOS

## Overview

This skill provides integration with Microsoft Outlook for macOS using the MCP server. It allows you to manage emails, calendar events, and contacts without requiring API access - it uses your existing Outlook application and SSO session.

## When to Use

Use this skill when:
- Reading or sending emails through Outlook
- Checking calendar events or creating meetings
- Searching for contacts
- Managing email folders
- Working with Outlook in corporate environments (no API needed)

## Prerequisites

- **macOS** with Microsoft Outlook installed
- **Outlook for Mac** (Classic edition recommended for best compatibility)
- **Outlook must be signed in** with your SSO account
- **Bun** JavaScript runtime installed
- **MCP Server configured** in mcp_config.json

## MCP Server Setup

The outlook-macos MCP server should be configured in your mcp_config.json:

```json
{
  "mcpServers": {
    "outlook-macos": {
      "command": "/Users/fufrankyuanjie/.bun/bin/bun",
      "args": ["run", "/Users/fufrankyuanjie/Documents/metaforge_dtt/external/mcp-servers/outlook-for-macos/index.ts"]
    }
  }
}
```

## Capabilities

### Email Operations

**Read emails:**
```
Check my unread emails in Outlook
```

**Search emails:**
```
Search my Outlook emails for "quarterly report"
```

**Send emails:**
```
Send an email to john@example.com with subject "Meeting Tomorrow"
```

**Send HTML emails:**
```
Send an HTML email to team@example.com with subject "Update" and body "<h1>Update</h1><p>Progress made on project.</p>"
```

**Send with attachments:**
```
Send an email to jane@example.com with subject "Report" and attach the reports/march.pdf file
```

### Calendar Operations

**View today's events:**
```
What events do I have today?
```

**Create events:**
```
Create a calendar event for a team meeting tomorrow from 2pm to 3pm
```

**View upcoming events:**
```
Show me my upcoming events for the next 2 weeks
```

**Search events:**
```
Search for "budget meeting" in my calendar
```

### Contact Operations

**List contacts:**
```
List all my Outlook contacts
```

**Search contacts:**
```
Find contact information for Jane Smith
```

## Best Practices

### Email Composition
- Use clear subject lines
- Specify recipients explicitly (to, cc, bcc)
- Use HTML format for rich formatting when needed
- Provide absolute file paths for attachments

### Calendar Events
- Specify clear start and end times
- Include event titles and descriptions
- Mention attendees when creating meetings

### File Attachments
- Use absolute paths: `/Users/username/Documents/report.pdf`
- Ensure files exist and are accessible
- Check file permissions

## Common Workflows

### Workflow 1: Process Morning Emails

```
1. Check unread emails
2. Identify priority messages
3. Draft replies for important emails
4. Flag items needing follow-up
```

### Workflow 2: Schedule Meeting

```
1. Check calendar for availability
2. Find contact details for attendees
3. Create calendar event with details
4. Send invitation email to attendees
```

### Workflow 3: Search and Reference

```
1. Search emails for specific topic
2. Review relevant messages
3. Extract key information
4. Reference in new communication
```

## Limitations

- **Mac only**: This MCP server only works on macOS
- **Outlook required**: Outlook application must be installed and running
- **Classic Outlook recommended**: New Outlook may have limited AppleScript support
- **Local only**: Uses local Outlook app, not cloud API
- **Permissions**: May need to grant Accessibility permissions on first use

## Troubleshooting

### Outlook Not Responding
- Ensure Outlook application is running
- Check that you're signed in to Outlook
- Try restarting the MCP server

### Permission Errors
- Go to System Preferences > Privacy & Security > Accessibility
- Grant Terminal or your terminal app accessibility permissions
- Restart the MCP server after granting permissions

### "New Outlook" Issues
- New Outlook for Mac has limited AppleScript support
- Switch to Classic Outlook: Help > Revert to Classic Outlook
- Or use Outlook Web (OWA) as alternative

## Integration with Other Skills

- **web-search**: Research before composing emails
- **markitdown**: Convert email content to Markdown
- **docx**: Create Word documents from email content
- **xlsx**: Export data to Excel spreadsheets

## Resources

- **GitHub**: https://github.com/syedazharmbnr1/claude-outlook-mcp
- **MCP Server**: outlook-macos (configured in mcp_config.json)
- **License**: MIT License
