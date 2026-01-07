# Factual Accuracy Guidelines for All AI-Generated Content

**Critical Principle:** NEVER synthesize, hallucinate, or fill gaps with assumptions.

---

## 🎯 Core Rules

### 1. Only Document What Exists

**DO:**
- ✅ Quote directly from source material
- ✅ Reference specific files and line numbers
- ✅ State "I don't know" when information is unavailable
- ✅ Mark uncertain information clearly
- ✅ Leave sections incomplete rather than guess

**DON'T:**
- ❌ Synthesize capabilities from general knowledge
- ❌ Extrapolate data points into trends
- ❌ Fill template sections with plausible-sounding content
- ❌ Assume details based on typical patterns
- ❌ Create quotes or paraphrase without attribution

---

## 📊 Confidence Levels (Use Consistently)

### ✅ Confirmed
- Direct quote from source document
- Explicit statement in meeting notes
- Clear data point in tracking system
- **Example:** "Status: Completed" (from ACTIVE_PROJECTS.md line 218)

### 📋 Documented
- Found in files but paraphrased for clarity
- Multiple sources agree
- Clear but not direct quote
- **Example:** Based on meeting notes from Oct 29, the team discussed launch accountability

### ⚠️ Inferred
- Reasonable conclusion from available context
- MUST state the basis for inference
- Mark clearly as inference, not fact
- **Example:** ⚠️ Inferred from project completion dates, likely implemented in early October

### ❓ Unknown
- No documentation found
- Explicitly state what's missing
- Don't speculate or fill the gap
- **Example:** ❓ Unknown: Specific alternatives considered, no documentation found

---

## 📝 Required Sections for All Generated Documents

### Every Document Must Include:

**1. Sources Section**
```markdown
## Sources Used
- [[file-name.md]] - Lines X-Y
- Meeting: [[meeting-date.md]]
- Slack: inbox/slack-summary-date.md
- Direct quote from [source]
```

**2. What I Know vs What I Don't Know**
```markdown
## What I Know From Documentation
- [Only documented facts]
- [With source citations]

## What I Don't Know
- [Specific missing information]
- [What would complete this document]
```

**3. Confidence Assessment**
```markdown
## Confidence Assessment
**Documentation Quality:** [High/Medium/Low]
**Sources Found:** [List]
**Missing Information:** [List gaps]
**Completeness:** [X% complete based on available sources]
```

---

## 🚫 Common Hallucination Traps to Avoid

### 1. Metrics & Numbers
**WRONG:** "Saved 40 hours/month in operational toil"
**RIGHT:** 
- ✅ "Project notes indicate 'major reduction in operational toil'" (if documented)
- ❓ Unknown: Specific time savings not quantified in documentation

### 2. Dates & Timelines
**WRONG:** "Implemented on October 15, 2025"
**RIGHT:**
- ✅ "Completed: October 2025" (from project tracking)
- ❓ Unknown: Specific implementation date not documented

### 3. Decision Rationale
**WRONG:** "We chose this because it scales better and reduces complexity"
**RIGHT:**
- ✅ "Resolved complex quota adjustment issues" (documented outcome)
- ❓ Unknown: Specific rationale for choosing this approach not documented

### 4. Stakeholder Decisions
**WRONG:** "Approved by Revenue SLT"
**RIGHT:**
- ✅ "Collaborators: Henry Springer, Olivia Rossetti" (documented)
- ❓ Unknown: Approval process and decision makers not documented

### 5. Success Metrics
**WRONG:** "Achieved 95% SE satisfaction improvement"
**RIGHT:**
- ✅ "Impact: Critical - Major SE satisfaction improvement" (documented)
- ❓ Unknown: Quantitative satisfaction metrics not available

### 6. Implementation Details
**WRONG:** "Communicated to all SEs via email on Oct 18"
**RIGHT:**
- ✅ "Q4 Kickoff presentations delivered Oct 18" (documented)
- ⚠️ Inferred: Compensation changes likely communicated at kickoff
- ❓ Unknown: Specific communication artifacts not found

---

## 📋 Document-Specific Guidelines

### Decision Logs
**Must Have:**
- Direct quotes for "The Decision"
- Explicit "What I Don't Know" sections
- Source citations for all claims
- Confidence assessment at end

**Never Include:**
- Synthesized alternatives unless documented
- Assumed trade-offs
- Invented success criteria
- Fabricated action items

### Meeting Summaries
**Must Have:**
- Direct quotes from meeting notes
- "Based on meeting notes from [date]" attribution
- Explicit gaps: "Discussion about X not captured in notes"

**Never Include:**
- Assumed action items not explicitly stated
- Synthesized decisions from discussion
- Implied outcomes without clear documentation

### Weekly Summaries
**Must Have:**
- Source file for each action item
- Direct quotes from meeting notes
- "Found in: [[file]]" for every item

**Never Include:**
- Assumed project status
- Synthesized themes not explicitly stated
- Inferred priorities without documentation

### Daily Files
**Must Have:**
- Actual calendar events from MCP
- Confirmed meeting times and attendees
- Real Slack/email counts from MCP

**Never Include:**
- Synthesized meeting context
- Assumed meeting purposes
- Fabricated priorities

### Priority Inbox
**Must Have:**
- Actual message counts from MCP
- Real urgency scores from algorithm
- Documented categorization rules

**Never Include:**
- Assumed priorities
- Synthesized urgency
- Made-up impact scores

---

## ✅ Quality Checklist (Run Before Saving)

Before saving ANY generated document:

- [ ] Every claim has a source citation
- [ ] All quotes are exact with attribution
- [ ] "What I Don't Know" section included
- [ ] Confidence levels marked appropriately
- [ ] No synthesized details beyond documentation
- [ ] Gaps explicitly stated, not filled
- [ ] Inference clearly marked with basis stated
- [ ] Numbers/metrics only from documentation
- [ ] Dates/timelines only if documented
- [ ] Completeness assessment included

---

## 🎯 When to Ask User vs Generate

### Always Ask User First If:
- [ ] Limited documentation found (<3 sources)
- [ ] Key sections would be mostly "Unknown"
- [ ] Recent decision (user has fresh context)
- [ ] Complex decision with multiple options
- [ ] High-stakes decision needing accuracy

### Can Generate With Explicit Gaps If:
- [ ] Past decision with some documentation
- [ ] User asks to document what's available
- [ ] Project tracking provides basic facts
- [ ] Gaps are clearly marked as "Unknown"

### Example Prompt When Uncertain:
```
"I found limited documentation about this decision:

✅ Found: Basic facts (completed, collaborators, outcome)
❓ Missing: Rationale, alternatives, detailed implementation

Would you like me to:
1. Generate with explicit gaps marked (quick)
2. Ask you questions to fill details (comprehensive)
3. Point me to specific docs to search"
```

---

## 📊 Examples: Good vs Bad

### Example 1: Action Items

**❌ BAD:**
```markdown
**Action Items:**
- [ ] Update all SE teams on new model - Owner: Olivia - Due: Oct 20
- [ ] Train RevOps on calculations - Owner: Henry - Due: Oct 25
- [ ] Monitor for issues - Owner: Eamon - Due: Nov 1
```

**✅ GOOD:**
```markdown
**Action Items From Documentation:**
- [ ] "Update Fabian Muessig on outcome of compensation discussion" 
  - Source: weekly-summary-2025-10-14.md
  - Owner: Eamon Brett
  - Due date: Not specified

**Action Items Not Documented:**
❓ Unknown: Communication plan details not found
❓ Unknown: Training activities not documented
❓ Unknown: Monitoring process not specified
```

### Example 2: Decision Rationale

**❌ BAD:**
```markdown
**Why this decision:**
1. Scalability - team model grows better with headcount
2. Reduces complexity - simpler calculations
3. Improves collaboration - team incentives
4. Industry best practice - aligns with market standards
```

**✅ GOOD:**
```markdown
**Why this decision (from documentation):**
- "Resolved complex quota adjustment issues" (ACTIVE_PROJECTS.md)
- "Eliminated manual, error-prone individual AE pairing adjustments" (ACTIVE_PROJECTS.md)

**Rationale Not Documented:**
❓ Unknown: Specific alternatives that were considered
❓ Unknown: Analysis that led to team-based approach
❓ Unknown: Trade-offs that were discussed
```

### Example 3: Metrics

**❌ BAD:**
```markdown
**Results:**
- 90% reduction in compensation errors
- 40 hours/month operational time saved
- SE satisfaction increased from 6.5 to 8.2 (out of 10)
- Zero escalations in first month
```

**✅ GOOD:**
```markdown
**Results (from documentation):**
- "Major SE satisfaction improvement" (ACTIVE_PROJECTS.md)
- "Major win for SE team morale and operational efficiency" (ACTIVE_PROJECTS.md)
- Impact level: "Critical" (ACTIVE_PROJECTS.md)
- Status: "Successfully implemented" (ACTIVE_PROJECTS.md)

**Metrics Not Quantified:**
❓ Unknown: Specific time savings not measured in documentation
❓ Unknown: Error reduction percentage not tracked
❓ Unknown: Satisfaction survey scores not available
❓ Unknown: Post-implementation issues not documented
```

---

## 🔄 Self-Correction Process

If you realize you've included unsourced information:

1. **Stop immediately**
2. **Mark the section:** ⚠️ VERIFICATION NEEDED
3. **State the issue:** "This section contains unsourced details"
4. **Ask user:** "Should I remove this or can you provide source?"
5. **Don't defend:** Just acknowledge and offer to fix

---

## 📚 This Applies To ALL Generated Content

- Decision logs
- Meeting summaries
- Weekly summaries
- Daily files
- Priority inbox
- Project briefs
- Executive summaries
- Strategic documents
- Status updates
- Any AI-generated content

**No exceptions. Factual accuracy always.**

---

**Last Updated:** 2025-10-30  
**Applies To:** All Cursor AI workflows in this system  
**Principle:** Truth > Completeness. Always.

