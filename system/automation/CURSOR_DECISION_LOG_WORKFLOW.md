# Cursor Workflow: Generate Decision Log

**Purpose:** Automate creation of decision logs from meeting notes, Slack discussions, or user context.

**User Command:** `"Create decision log"` or `"Document decision about [topic]"`

---

## Workflow Steps

### 1. Gather Context

**Ask user for input sources (or infer from recent activity):**

```
Which of these describes the decision?
1. From a recent meeting (I'll read the meeting notes)
2. From Slack discussion (I'll analyze messages)  
3. From email thread (I'll review emails)
4. Fresh decision (I'll ask you questions)
5. All of the above (comprehensive)
```

**Sources to check:**
- Recent meeting notes in `meetings/` (last 3 days)
- Recent Slack priority summaries in `inbox/`
- Recent daily files in `daily/`
- User's verbal context

### 2. Extract Decision Information

**Scan sources for:**
- ✅ **Problem statement** - What issue is being addressed?
- ✅ **Decision made** - What was decided? (Look for "we decided", "going with", "the approach is")
- ✅ **Stakeholders** - Who was involved? Who made the call?
- ✅ **Rationale** - Why this approach? (Look for "because", "the reason")
- ✅ **Alternatives** - What else was considered? (Look for "we could", "option A/B", "also considered")
- ✅ **Action items** - What happens next? (Look for "[ ]", "TODO", "will", "needs to")
- ✅ **Timeline** - When does this happen?
- ✅ **Success criteria** - How will we know it worked?

**Key phrases to identify:**
- Decision: "we're going to", "the decision is", "we'll", "agreed to"
- Rationale: "because", "the reason", "this solves", "impact is"
- Alternatives: "we considered", "other options were", "could also", "vs"
- Trade-offs: "downside", "risk", "won't be able to", "have to accept"

### 3. Determine Decision Metadata

**Status:**
- ✅ **Decided** - Clear decision made, communicated
- 🟡 **In Progress** - Decided but implementation ongoing
- ⏳ **Pending** - Discussion complete, awaiting decision
- 🔄 **Revised** - Previous decision changed

**Impact Level:**
- 🔴 **High** - Multiple teams, months of work, significant resources
- 🟠 **Medium** - One team, weeks of work, moderate impact
- 🟢 **Low** - Individual/small group, days of work, limited scope

**Date:** Use meeting date or today's date

**Decision Makers:** Extract from meeting attendees or context

### 4. Generate File Name

**Format:** `YYYY-MM-category-brief-description.md`

**Categories:**
- `launch` - Launch process, implementation
- `partnerships` - Partner relationships, collaboration
- `compensation` - SE comp, SPIF, quota
- `process` - Workflow, operational changes
- `tooling` - Tools, systems, platforms
- `org` - Organizational structure, roles
- `strategy` - Strategic direction, priorities

**Examples:**
- `2025-10-launch-cases-smb-5m-self-serve.md`
- `2025-11-partnerships-post-sales-accountability.md`
- `2025-10-compensation-team-based-model.md`

**Rules:**
- Use date decision was made (or discussed if pending)
- Keep description under 50 chars
- Use hyphens, all lowercase
- Be specific but concise

### 5. Populate Template

**Load:** `decisions/template-decision.md`

**Fill in sections:**

#### Context
```markdown
**Problem Statement:**
[Extract: What problem is being solved? 1-2 sentences max]

**Background:**
[Extract: Key history, previous attempts, what led here]
- Bullet points for readability
- Include relevant dates
- Mention previous solutions that didn't work

**Stakeholders:**
- **Decision Maker(s):** [Who has authority]
- **Consulted:** [Who gave input]
- **Informed:** [Who needs to know]
- **Impacted:** [Who will be affected]
```

#### The Decision
```markdown
**What we decided:**
[Clear, specific statement. Start with action verb: "Treat...", "Implement...", "Change..."]

**Key Details:**
- [Specific detail 1]
- [Specific detail 2]
- [Important constraint or boundary]
```

#### Rationale
```markdown
**Why this decision:**
1. [Primary reason - most important]
2. [Secondary reason]
3. [Supporting evidence or data]

**Alternatives Considered:**
- **Option A:** [What it was] - Rejected because [why]
- **Option B:** [What it was] - Rejected because [why]

**Trade-offs Accepted:**
- ⚠️ [What we're giving up]
- ⚠️ [Risk we're accepting]
```

#### Implementation
```markdown
**Action Items:**
[Extract from meeting notes, Slack, or discussion]
- [ ] Action - Owner: [Name] - Due: [Date]

**Timeline:**
- **Immediate:** [What happens now]
- **Week 1-2:** [Short-term]
- **Month 1:** [Longer-term]

**Communication Plan:**
- [ ] Communicate to [Who] - Owner: [Name]
- [ ] Update docs at [Where] - Owner: [Name]
```

#### Success Criteria
```markdown
**We'll know this is working when:**
1. [Measurable outcome - numbers, percentages]
2. [Observable change - behaviors, processes]
3. [Feedback indicator - surveys, comments]

**Review Date:** [2-4 weeks out typically]
```

#### Related Documents
```markdown
**Meetings:**
- [[meetings/YYYY-MM-DD-meeting-name.md]]

**Slack Discussions:**
- [Link to thread](URL)

**Supporting Docs:**
- [[Link to project, analysis, etc.]]

**Daily Files:**
- [[daily/YYYY-MM-DD.md]] - Context for this decision
```

### 6. Smart Enhancements

**Auto-link related content:**
- If decision references a project → link to `projects/` file
- If from a meeting → link to meeting notes
- If in daily file priorities → link to daily file
- If mentioned in Slack summary → link to that

**Extract key quotes:**
- Look for powerful statements in meeting notes
- Add to Notes section as blockquotes
- Attribute to speaker

**Identify patterns:**
- Is this a recurring issue? Note it
- Was this decided before? Reference previous decision
- Will this affect other decisions? Flag connections

### 7. Save and Confirm

**Save to:** `decisions/[generated-filename].md`

**Confirm to user:**
```
✅ Decision log created: decisions/2025-10-launch-cases-example.md

📋 Summary:
- Decision: [One-line summary]
- Status: 🟡 In Progress
- Impact: 🔴 High
- Owner: [Name]

🔗 Key links created:
- Meeting: [[meetings/2025-10-29-meeting.md]]
- Daily: [[daily/2025-10-30.md]]
- Project: [[projects/project-name.md]]

💡 Next steps:
- Share with stakeholders
- Update daily file to reference this decision
- Set calendar reminder for review date
```

---

## Example Invocations

### Example 1: From Meeting Notes
```
User: "Create decision log from yesterday's Partnerships meeting"

Claude:
1. Reads meetings/2025-10-29-partnerships-post-sales.md
2. Extracts decision context, rationale, stakeholders
3. Generates decisions/2025-10-merchant-experience-closed-won-to-launch.md
4. Links meeting notes, Slack threads, daily files
5. Confirms creation with summary
```

### Example 2: From Slack + Meeting
```
User: "Document the launch cases decision"

Claude:
1. Checks daily/2025-10-30.md for context (Top 3)
2. Reads relevant Slack threads from inbox/slack-priority-summary-2025-10-30.md
3. Scans recent meetings for related discussion
4. Combines all sources
5. Generates comprehensive decision log
6. Asks user to confirm key details
```

### Example 3: From Verbal Context
```
User: "Create decision log - we decided to change SE compensation to team-based model"

Claude:
1. Asks clarifying questions:
   - When was this decided?
   - Who made the decision?
   - Why team-based vs individual?
   - What are the action items?
   - Who needs to be informed?
2. Generates decision log from answers
3. Suggests linking to related docs
```

### Example 4: Comprehensive (All Sources)
```
User: "Create comprehensive decision log about partnerships accountability"

Claude:
1. Scans last 7 days of meetings
2. Reviews Slack priority summaries
3. Checks daily files for mentions
4. Finds: Oct 29 meeting, Slack threads, daily priority
5. Combines all context
6. Generates complete decision log
7. Auto-links all sources
```

---

## Interactive Mode

**When context is unclear, ask:**

```
I found some information, but need clarification:

Decision Context:
✅ Problem: Launch accountability confusion
✅ Stakeholders: SE, CSM, Partners teams
❓ Decision Status: Is this decided or still pending?
❓ Owner: Who owns implementing this?
❓ Timeline: When does this start?

Should I:
1. Generate decision log with what I have + mark unknowns
2. Ask you these questions first
3. Search for more context (check older files)
```

---

## Quality Checks

**Before saving, verify:**
- [ ] File name follows format (YYYY-MM-category-description.md)
- [ ] Status is set (not template placeholder)
- [ ] Decision statement is clear and specific
- [ ] At least one action item with owner
- [ ] Related documents linked
- [ ] Success criteria defined
- [ ] No template placeholders left (no [brackets])

**If missing critical info:**
- Ask user to fill in
- Mark section with ⚠️ TODO
- Save anyway (better to have partial than nothing)

---

## Advanced Features

### Auto-Update Daily File
After creating decision log, offer:
```
"Would you like me to reference this decision in today's daily file?"

If yes:
1. Add to Top 3 priorities (if relevant)
2. Add to Decisions & Follow-ups section
3. Update links
```

### Decision Log Index
Maintain `decisions/INDEX.md` with:
- All decisions by status
- All decisions by category
- All decisions by impact level
- Quick links to active decisions

### Recurring Issue Detection
If decision log mentions recurring issue:
```
"⚠️ This appears to be a recurring issue (mentioned 3+ times in last month).
Would you like me to:
1. Create recurring issue tracker
2. Link to previous decisions on this topic
3. Flag for strategic review"
```

---

## Error Handling

**If no context found:**
```
"I couldn't find context for this decision. Would you like to:
1. Tell me about it (I'll ask questions)
2. Point me to specific meeting/Slack thread
3. Use the blank template"
```

**If ambiguous decision:**
```
"I found multiple possible decisions in that meeting:
1. Launch cases approach
2. Partner attach goal
3. Post-sales slide creation

Which should I document?"
```

**If decision already exists:**
```
"Found existing decision log: decisions/2025-10-topic.md
Would you like to:
1. Update it (add revision)
2. Create new decision log
3. Review existing one first"
```

---

## Best Practices for AI

### CRITICAL: Factual Accuracy & Honesty

**NEVER HALLUCINATE OR SYNTHESIZE:**
1. **Only use documented facts:** If not in source material, don't include it
2. **Quote directly:** Use exact quotes, mark with > blockquote and attribution
3. **State "I don't know":** Explicitly flag missing information
4. **Mark uncertainty:** Use "Based on available documentation..." for inferences
5. **Don't fill gaps:** Leave sections incomplete rather than guess
6. **Distinguish facts from assumptions:** Make it crystal clear

**Confidence Levels to Use:**
- ✅ **Confirmed:** Direct quote or clear documentation
- 📋 **Documented:** Found in files but paraphrased
- ⚠️ **Inferred:** Reasonable conclusion from context (state basis)
- ❓ **Unknown:** No documentation found (explicitly state)

### Standard Practices

1. **Be comprehensive:** Include all available context (but only real context)
2. **Be specific:** Clear, actionable language (from actual sources)
3. **Link liberally:** Connect to all related docs (that actually exist)
4. **Ask when uncertain:** ALWAYS better than guessing
5. **Highlight patterns:** Note if recurring issue (only if documented)
6. **Preserve quotes:** Powerful statements from meetings (exact quotes only)
7. **Think stakeholder:** Who needs to know this?

### Required Sections for Every Decision Log

**"What I Know From Documentation"**
- List only facts found in source files
- Include file names and direct quotes

**"What I Don't Know"**
- Explicitly list missing information
- State what would complete the decision log
- Don't apologize, just be factual

**"Confidence Assessment"**
Add to every decision log:
```markdown
## Confidence Assessment

**Documentation Quality:** [High/Medium/Low]
- High: Comprehensive meeting notes, clear decision record
- Medium: Project tracking only, some context
- Low: Brief mentions, limited detail

**Missing Information:**
- [List specific gaps]

**Recommendation:**
- [What's needed to make this complete]
```

---

**Last Updated:** 2025-10-30  
**Used by:** Claude in Cursor environment  
**Triggers:** "Create decision log", "Document decision"

