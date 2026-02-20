# Writing Style Guide for Bradan

**Purpose:** Help users of the Bradan task management system understand and apply consistent writing patterns when working with AI assistants (like Cursor/Claude).

**Last Updated:** February 20, 2026

---

## 🎯 Overview

This guide captures the writing style patterns, documentation conventions, and communication preferences that make working with AI assistants more effective in the Bradan system.

These patterns are designed to:
- Create consistent, scannable documents
- Enable effective AI collaboration
- Build a knowledge graph through linking
- Adapt communication to audience needs
- Maintain pragmatic, grounded tone

---

## 📋 Quick Reference

### Before Writing Any Document

1. **Identify Audience**
   - Executive (VP/Director): <100 lines, strategic summary
   - Manager/Lead: 100-200 lines, context + tactics
   - IC/Collaborator: 200+ lines, full detail embedded

2. **Check Tone**
   - ✅ Use: "important", "relevant", "ongoing", "pending"
   - ❌ Never: "CRITICAL", "HIGH PRIORITY", "urgent" (unless life-threatening)
   - ✅ Irish pragmatism: practical, grounded, no drama

3. **Structure Document**
   - Use standard metadata header
   - Include section dividers (`---`)
   - Use emojis in headers for visual scanning
   - Tag key entities with `[[double brackets]]`

---

## 📝 Document Structure

### Standard Template

```markdown
# Document Title

**Date:** YYYY-MM-DD  
**Type:** [[Meeting Notes]] / [[Project Document]] / [[Workshop Synthesis]]  
**Participants:** [[Name One]], [[Name Two]]  
**Related:** [[Project Name]], [[Concept]]  
**Status:** Active / Complete / Archived

---

## 🎯 Executive Summary / Quick Reference
[High-level overview for quick scanning]

---

## 📋 Detailed Content
[Comprehensive sections with full context]

---

## ✅ Action Items / Next Steps
[Clear ownership and timelines]

---

## 🔗 Related Documents
- [[work/projects/RELATED-FILE.md]]
- [[work/meetings/RELATED-MEETING.md]]
```

---

## 🎨 Visual Organization

### Emoji Usage

Use emojis strategically for quick visual scanning:

- 🎯 Strategic focus / priorities
- 📋 Lists / summaries
- ✅ Completed / working
- ⚠️ Warnings / concerns
- 🔴 High priority / urgent
- 🟡 Medium priority / important
- 🟢 Low priority / normal
- 🔄 In progress / ongoing
- 📊 Data / metrics
- 💡 Insights / ideas
- 🤝 Collaboration / stakeholders
- 🔧 Operational / tactical

**Guidelines:**
- Use in headers and lists, not in prose
- Use status indicators (✅ ⚠️ ❌) for quick scanning
- Be consistent across documents

### Status Tables

Use tables for organized information:

| Project | Status | Owner | Timeline |
|---------|--------|-------|----------|
| [[Project Name]] | 🟢 On track | [[Owner Name]] | Target date |

---

## 🔗 Linking & Tagging

### Logseq-Style Linking

Use `[[double brackets]]` for:
- **People:** `[[Fabian Muessig]]`, `[[Olivia Rossetti]]`
- **Projects:** `[[SE-NTRAL]]`, `[[Mission Control]]`
- **Concepts:** `[[Solution Integrity]]`, `[[Launch]]`, `[[Handoff]]`
- **Tools:** `[[SE-Assistant]]`, `[[Salesforce]]`
- **Locations:** `[[Dublin]]`, `[[EMEA]]`

**Rules:**
- Tag on first mention of key entities
- Use plain text for subsequent mentions (unless creating different context)
- Don't tag generic words or acronyms explained inline

### Cross-Document References

- Format: `[[work/projects/FILENAME]]` or `[[work/meetings/FILENAME]]`
- Include section anchors: `[[work/projects/FILE#section]]`
- Use relative paths from workspace root

---

## 💬 Tone & Voice

### Irish Pragmatism

- **Practical and grounded** - no dramatic urgency language
- **Realistic timelines** - no false urgency
- **Calm, assured tone** - confident without being press release-like

### Language Patterns

✅ **Use:**
- "important", "relevant", "ongoing", "pending", "outstanding"
- "This needs attention" (not "This is CRITICAL")
- "Let's prioritize this" (not "This is HIGH PRIORITY")

❌ **Never use:**
- "CRITICAL", "HIGH PRIORITY", "urgent" (unless literally life-threatening)
- Dramatic urgency language for tech work
- Corporate buzzwords or press release language

### Example Contrasts

❌ "We're thrilled to announce this game-changing initiative!"  
✅ "This initiative addresses a key gap in our process."

❌ "This is a critical priority that requires immediate attention!"  
✅ "This is important and needs attention this week."

---

## 👥 Audience Adaptation

### Executive Level (VP, Director, Managing Director)

**Characteristics:**
- **Length:** <100 lines (aim for 60-80)
- **Reading time:** 2-minute scan
- **Style:** Strategic summaries, high-level outcomes
- **Detail:** Link to external resources (Vault, Google Docs)
- **Format:** Simple tables, clear ownership, bottom-line summaries

**What to include:**
- Current status and outcomes
- Clear ownership
- Links to detailed resources
- Bottom-line summary (1 sentence)

**What to exclude:**
- Detailed tactical information
- Step-by-step processes
- Granular metrics (unless critical)

### Manager/Lead Level

**Characteristics:**
- **Length:** 100-200 lines
- **Reading time:** 5-10 minutes
- **Style:** Strategic context + tactical details
- **Detail:** Key context embedded, some external links
- **Format:** Sections with context, reasoning, actionable items

### IC/Collaborator Level

**Characteristics:**
- **Length:** 200+ lines as needed
- **Reading time:** 15-30 minutes
- **Style:** Actionable, detailed, execution-focused
- **Detail:** Full context embedded (minimize link-clicking)
- **Format:** Comprehensive sections with explicit next actions

**What to include:**
- Full context and background
- Specific next actions with timelines
- Explicit ownership for each item
- Current status with granular metrics
- All relevant details embedded

---

## 🔗 Link Accessibility

### Always Verify Links

✅ **Use:**
- Vault pages
- Google Docs/Drive
- Fellow notes
- Figma
- Company-accessible links

❌ **Never use:**
- Local workspace file paths (e.g., `work/projects/file.md`)
- Links that require special access without explanation

**If no public link exists:** Note "Available from [Owner] if needed"

### Link Strategy by Audience

- **Executive:** Links for drill-down detail
- **IC:** Embed context directly (minimize link-clicking)

---

## 🧠 Strategic Thinking Patterns

### Framework Approach

- **Design for reuse** - create frameworks others can use
- **Scalable structures** - build systems, not one-offs
- **Pattern recognition** - highlight patterns across documents
- **Outcome-focused** - always include success criteria

### Documentation Philosophy

- **Comprehensive context** - full background before recommendations
- **Memory bank approach** - document for future self
- **Living documents** - update as context evolves
- **Explicit connections** - show how ideas relate

---

## ✅ Key Principles

1. **Comprehensive context** - full background before recommendations
2. **Framework thinking** - design for reuse and scalability
3. **Strategic focus** - big picture over tactical execution
4. **Outcome-focused** - always include success criteria
5. **Self-aware** - acknowledge limitations and compensation strategies
6. **Audience-aware** - adjust detail level by role
7. **Pragmatic tone** - practical, grounded, no drama

---

## 🚀 Using with AI Assistants

### Cursor Rules

The `.cursor/rules/` directory contains rule files that automatically guide AI assistants:

- `writing-style.mdc` - Visual organization and structure
- `tone-and-voice.mdc` - Communication preferences
- `documentation-patterns.mdc` - Linking and knowledge graph patterns
- `strategic-thinking.mdc` - Framework and systems thinking
- `writing-quick-reference.mdc` - Quick checklist (manual reference)

These rules are automatically applied when working with Cursor/Claude, ensuring consistent document generation.

### Best Practices

1. **Reference the rules** when asking AI to generate documents
2. **Specify audience** when requesting document creation
3. **Use templates** from this guide for consistency
4. **Tag entities** to build knowledge graph connections
5. **Update rules** as your style evolves

---

## 📚 Related Resources

- `.cursor/rules/` - Cursor rule files for AI guidance
- `system/memory/DOCUMENT-STYLE-GUIDE.md` - Detailed style guide
- `system/memory/LOGSEQ-TAGGING-CONVENTIONS.md` - Tagging conventions

---

**Questions?** This guide is a living document - update it as patterns evolve.
