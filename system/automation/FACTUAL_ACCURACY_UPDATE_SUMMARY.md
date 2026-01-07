# Factual Accuracy Update - October 30, 2025

## Summary

All AI workflow documents updated to enforce strict factual accuracy, eliminate hallucination risk, and require explicit confidence levels for all generated content.

**Trigger:** User feedback on hallucinated details in auto-generated decision log (SE compensation model).

---

## 🎯 Core Principle Established

### New Rule for All AI Workflows
**"Truth > Completeness. Always."**

- State "I don't know" when information unavailable
- Never synthesize capabilities, pricing, technical details
- Reference only documented data - no extrapolation
- Explicitly state limitations vs suggesting workarounds
- Preface uncertain info with "Based on available documentation..."
- Distinguish facts from assumptions
- Flag potentially outdated information

---

## 📁 Files Created

### 1. FACTUAL_ACCURACY_GUIDELINES.md (NEW)
**Location:** `automation/FACTUAL_ACCURACY_GUIDELINES.md`  
**Purpose:** Master reference for all AI-generated content

**Key Sections:**
- Core rules (only document what exists)
- Confidence levels (Confirmed/Documented/Inferred/Unknown)
- Required sections for all documents
- Common hallucination traps to avoid
- Document-specific guidelines
- Quality checklist
- Good vs bad examples

**Applies To:**
- Decision logs
- Meeting summaries
- Weekly summaries
- Daily files
- Priority inbox
- Project briefs
- Executive summaries
- Strategic documents
- Status updates
- **All AI-generated content**

---

## 📝 Files Updated

### 2. CURSOR_DECISION_LOG_WORKFLOW.md
**Changes:**
- Added "CRITICAL: Factual Accuracy & Honesty" section at top of Best Practices
- Defined 4 confidence levels (Confirmed/Documented/Inferred/Unknown)
- Required "What I Know" vs "What I Don't Know" sections
- Mandatory confidence assessment for every decision log
- Examples of good vs bad documentation
- Quality checklist before saving

**New Requirements:**
- Every claim must have source citation
- All quotes must be exact with attribution
- Gaps explicitly stated, never filled
- Inference marked with basis stated
- Numbers/metrics only from documentation

### 3. CURSOR_WEEKLY_SUMMARY_WORKFLOW.md
**Changes:**
- Added warning at top: "Follow FACTUAL_ACCURACY_GUIDELINES.md at all times"
- New "Factual Accuracy Requirements" section
- Must do / Never do lists
- Handling for missing or incomplete Gemini notes
- Confidence level requirement

**New Requirements:**
- Only extract action items explicitly in "Suggested next steps"
- Quote meeting notes directly when uncertain
- State source file for every action item
- If owner unclear, say so explicitly
- If no action items, state "No action items documented"
- Never synthesize from discussion content

### 4. CURSOR_PRIORITY_INBOX_WORKFLOW.md
**Changes:**
- Added warning at top: "Follow FACTUAL_ACCURACY_GUIDELINES.md at all times"
- New "Factual Accuracy Requirements" section
- Must use actual MCP data only
- Required data summary section
- Handling for unavailable MCP data

**New Requirements:**
- Only show messages actually retrieved from MCP
- Use exact urgency/impact scores from algorithm
- State actual message counts (no estimates)
- Use real timestamps
- Never synthesize example messages
- Always include data summary with scan parameters

### 5. CURSOR_USAGE_GUIDE.md
**Changes:**
- Added notice about factual accuracy guidelines at top
- References master FACTUAL_ACCURACY_GUIDELINES.md

---

## 🔄 Updated Template

### 6. decisions/template-decision.md
**Enhanced with new sections:**

**Added "What I Know From Documentation":**
```markdown
## What I Know From Documentation
- [Only documented facts]
- [With source citations]
```

**Added "What I Don't Know":**
```markdown
## What I Don't Know
- [Specific missing information]
- [What would complete this document]
```

**Added Confidence Assessment:**
```markdown
## Confidence Assessment
**Documentation Quality:** [High/Medium/Low]
**Missing Information:** [List gaps]
**Recommendation:** [What's needed to complete]
```

---

## 📊 Updated Decision Logs

### 7. decisions/2025-10-se-compensation-team-based-model.md
**Regenerated to remove hallucinations:**

**Removed (Not Documented):**
- ❌ "40 hours/month operational toil eliminated"
- ❌ "Zero compensation calculation errors since implementation"
- ❌ Specific alternatives "Option A, B, C"
- ❌ Detailed timelines and communication dates
- ❌ Fabricated success criteria metrics

**Added (Honest Documentation):**
- ✅ "What I Know From Documentation" sections
- ✅ "What I Don't Know" sections throughout
- ✅ Direct quotes only (with source attribution)
- ✅ Confidence assessment at end
- ✅ Status: "⚠️ INCOMPLETE - Based only on project tracking references"

---

## 📋 Impact on All Workflows

### Decision Logs
**Before:** Could hallucinate rationale, metrics, alternatives  
**After:** Explicit gaps, direct quotes only, confidence levels

### Weekly Summaries
**Before:** Could synthesize action items from discussion  
**After:** Only extract from "Suggested next steps," state if missing

### Priority Inbox
**Before:** Could estimate counts, inflate urgency  
**After:** Exact MCP data only, algorithm scores only, actual counts

### Daily Files
**Before:** Could assume meeting context  
**After:** Calendar data only, no synthesized context

### Meeting Notes
**Before:** Could infer outcomes not stated  
**After:** Quote notes directly, state if incomplete

### Project Briefs
**Before:** Could fill details from general knowledge  
**After:** Document only what's in files, flag gaps

---

## ✅ Quality Enforcement

### New Quality Checklist (Every Document)

Before saving ANY AI-generated document:

- [ ] Every claim has a source citation
- [ ] All quotes are exact with attribution
- [ ] "What I Don't Know" section included (if applicable)
- [ ] Confidence levels marked appropriately
- [ ] No synthesized details beyond documentation
- [ ] Gaps explicitly stated, not filled
- [ ] Inference clearly marked with basis stated
- [ ] Numbers/metrics only from documentation
- [ ] Dates/timelines only if documented
- [ ] Completeness assessment included

### When to Ask User vs Generate

**Always ask first if:**
- Limited documentation (<3 sources)
- Key sections mostly "Unknown"
- Recent decision (user has fresh context)
- Complex decision with multiple options
- High-stakes decision needing accuracy

**Can generate with gaps if:**
- Past decision with some documentation
- User asks to document available info
- Gaps clearly marked as "Unknown"

---

## 📚 Reference Hierarchy

All AI workflows must follow this hierarchy:

1. **FACTUAL_ACCURACY_GUIDELINES.md** (Master reference)
   ↓
2. **Workflow-specific guidelines** (Decision logs, Weekly summaries, etc.)
   ↓
3. **Document templates** (with required sections)
   ↓
4. **Generated documents** (with confidence assessments)

---

## 💡 Examples of Improved Output

### Before (Hallucinated):
```markdown
**Results:**
- 90% reduction in compensation errors
- 40 hours/month operational time saved  
- SE satisfaction increased from 6.5 to 8.2
- Zero escalations in first month
```

### After (Factually Accurate):
```markdown
**Results (from documentation):**
- "Major SE satisfaction improvement" (ACTIVE_PROJECTS.md)
- "Major win for SE team morale and operational efficiency" (ACTIVE_PROJECTS.md)
- Impact level: "Critical" (ACTIVE_PROJECTS.md)

**Metrics Not Quantified:**
❓ Unknown: Specific time savings not measured in documentation
❓ Unknown: Error reduction percentage not tracked
❓ Unknown: Satisfaction survey scores not available
```

### Before (Assumed Context):
```markdown
**Attendees:** Mary Todd, Eamon Brett
**Purpose:** Weekly 1:1 to discuss SE priorities
**Agenda:** Launch cases, GTM evolution, team updates
```

### After (Calendar Data Only):
```markdown
**Attendees:** Mary Todd (from calendar data)
**Purpose:** Weekly 1:1 (from meeting title pattern)
**Meeting stub:** Context from previous meeting notes if available
❓ Unknown: Specific agenda - not documented in calendar
```

---

## 🎯 Expected Behavior Going Forward

### When User Says: "Generate X"

**AI Will:**
1. Search for relevant documentation
2. Extract only documented facts
3. Mark confidence level for each section
4. Explicitly state what's missing
5. Ask if more context needed
6. Generate with clear limitations noted

**AI Will NOT:**
- Fill gaps with plausible content
- Synthesize details from general knowledge
- Assume information typical of similar situations
- Create data points that sound reasonable
- Hide uncertainty or incomplete information

### When Documentation is Sparse

**AI Will Say:**
```
"I found limited documentation about this decision:

✅ Found: Basic facts (completed, collaborators, outcome)
❓ Missing: Rationale, alternatives, detailed implementation

Documentation Quality: Low
Completeness: ~30% based on available sources

Would you like me to:
1. Generate with explicit gaps marked
2. Ask you questions to fill details
3. Point me to specific docs to search"
```

---

## 📊 Success Metrics

**How we'll know this is working:**
1. No user corrections about hallucinated facts
2. Generated documents clearly state limitations
3. Confidence levels help user trust output
4. User can quickly see what's incomplete
5. No re-work needed due to false information

**Review:** After 10 generated documents, assess quality

---

## 🔗 Related Documents

**Master Guidelines:**
- [[automation/FACTUAL_ACCURACY_GUIDELINES.md]]

**Updated Workflows:**
- [[automation/CURSOR_DECISION_LOG_WORKFLOW.md]]
- [[automation/CURSOR_WEEKLY_SUMMARY_WORKFLOW.md]]
- [[automation/CURSOR_PRIORITY_INBOX_WORKFLOW.md]]
- [[docs/guides/CURSOR_USAGE_GUIDE.md]]

**Templates Updated:**
- [[decisions/template-decision.md]]

**Example (Corrected):**
- [[decisions/2025-10-se-compensation-team-based-model.md]]

---

## 📝 Implementation Notes

**Date:** October 30, 2025  
**Trigger:** User correction of hallucinated metrics in decision log  
**Impact:** All future AI-generated content in this system  
**Principle:** Honesty and explicit limitations build more trust than polished completeness with fabricated details

**Key Insight:**
Users prefer knowing what we DON'T know vs confident-sounding hallucinations. Explicit gaps > false completeness.

---

**Last Updated:** 2025-10-30  
**Maintained by:** Eamon Brett  
**Status:** ✅ Complete - All workflows updated

