# Gemini Name Corrections

## Auto-Corrected Names

The Gemini notes linking system automatically corrects these common transcription errors:

| Gemini Transcription | Correct Name |
|---------------------|--------------|
| Deian, Dian, Dean | Deann Evans |
| Burke | Birk Angermann |

## How It Works

When linking Gemini notes, the system:
1. Reads Gemini transcript content
2. Applies name corrections before extraction
3. All summaries and action items use correct names

**Example:**
- Gemini says: "Deian and Eamon discussed priorities"
- Auto-corrected to: "Deann Evans and Eamon discussed priorities"

## Adding New Corrections

When you notice a new transcription error:

1. **Open:** `automation/link_gemini_notes.py`

2. **Find:** `NAME_CORRECTIONS` dictionary (around line 27)

3. **Add entry:**
```python
NAME_CORRECTIONS = {
    "Burke": "Birk Angermann",
    "Deian": "Deann Evans",
    "Dian": "Deann Evans",
    "Dean": "Deann Evans",
    "NewWrongName": "Correct Full Name",  # Add here
}
```

4. **Save** - corrections apply automatically on next run

## Common Gemini Errors

Based on usage, watch for:
- **Similar sounding names** (Deian/Dean/Deann)
- **Uncommon names** (Birk → Burke)
- **Non-English names** (may be misspelled)
- **Titles mixed with names** (VP mixed into name)

## Manual Corrections

If you need to manually fix a meeting note:

1. Open the meeting file
2. Find the "Meeting Notes" section
3. Edit the summary/action items directly
4. Save

The auto-correction only applies to NEW links, not existing ones.

## Testing Corrections

After adding new corrections, test:

```
"Link Gemini notes for [date]"
```

Check the output to verify names are corrected properly.

---

**Current Status:** ✅ Active  
**Corrections:** 2 names (4 variants)

