# AI Implementation Notes

## What AI Was Used For

### 1. **Action Item Extraction (Production Feature)**
- **Model:** OpenAI GPT-4o-mini
- **Purpose:** Extract structured action items from unstructured meeting transcripts
- **Implementation:** `app/llm.py`
- **Input:** Raw meeting transcript text
- **Output:** JSON array of tasks with owner and due_date fields

**Why GPT-4o-mini:**
- Cost-effective for production use (~$0.15 per 1M input tokens)
- Sufficient accuracy for task extraction
- Fast response times (<2 seconds typically)
- Supports JSON mode for structured output

### 2. **Development Assistance**
- Used Claude (Anthropic) for:
  - Initial project scaffolding
  - Code generation
  - Documentation writing
  - Best practices recommendations

## Manual Verification Required

### ✅ Always Verify:
1. **LLM Extraction Accuracy:**
   - Review extracted tasks match the transcript
   - Verify owner names are correctly identified
   - Check due dates are properly parsed (YYYY-MM-DD format)
   - Confirm no hallucinated tasks

2. **Edge Cases:**
   - Empty transcripts → Should return empty array
   - Transcripts with no action items → Should return empty array
   - Malformed dates → Should return null for due_date
   - Ambiguous ownership → Should return null for owner

3. **API Responses:**
   - Validate JSON structure matches expected schema
   - Handle OpenAI API failures gracefully
   - Check rate limits aren't exceeded

4. **Database Integrity:**
   - Verify tasks are linked to correct transcripts
   - Ensure cascade deletes work (deleting transcript deletes tasks)
   - Check datetime fields are UTC

### ⚠️ Known Limitations:

1. **Context Window:**
   - GPT-4o-mini has 128k token context
   - Very long transcripts (>100k tokens) may be truncated
   - Recommended max transcript length: ~50,000 characters

2. **Extraction Quality:**
   - Accuracy depends on transcript clarity
   - Vague statements may not be extracted ("someone should...")
   - Implicit action items may be missed
   - Works best with explicit language ("John will prepare report by Friday")

3. **Date Parsing:**
   - Relative dates ("tomorrow", "next week") may not convert correctly
   - Ambiguous dates may be missed
   - Timezone assumptions (assumes user's local timezone context)

4. **Cost Considerations:**
   - Each transcript processing costs ~$0.01-0.05 depending on length
   - Monitor usage if processing large volumes
   - Consider caching for repeated transcripts

## LLM Prompt Engineering

### Current Approach:
- **System Prompt:** Sets context as an action item extractor
- **User Prompt:** Provides transcript and example output format
- **JSON Mode:** Enforces structured output
- **Temperature:** 0.3 (balanced between consistency and flexibility)

### Prompt Structure:
```
System: "You are an AI assistant that extracts action items..."
User: "Extract action items from this transcript: [text]"
Response Format: Strict JSON schema
```

### Why This Works:
- Clear role definition reduces hallucinations
- Example output format improves consistency
- JSON mode ensures parseable responses
- Low temperature maintains deterministic behavior

## Testing Recommendations

### Unit Tests:
```python
# Test LLM extraction with known transcripts
def test_extract_simple_action():
    transcript = "John will prepare the Q4 report by Friday."
    items = extract_action_items(transcript)
    assert len(items) == 1
    assert items[0]["owner"] == "John"
    assert "Q4 report" in items[0]["task"]
```

### Integration Tests:
- Test full API flow: POST transcript → GET tasks
- Verify database persistence
- Test error handling (invalid API key, network failures)

### Manual Testing Checklist:
- [ ] Process simple transcript with clear action items
- [ ] Process transcript with no action items
- [ ] Process transcript with dates in different formats
- [ ] Process very long transcript (10k+ words)
- [ ] Test with special characters, emojis
- [ ] Verify tasks appear in UI immediately
- [ ] Test edit/delete/complete workflows

## Future Improvements

### 1. **Confidence Scores:**
Add confidence scoring to extracted items:
```json
{
  "task": "Prepare report",
  "owner": "John",
  "confidence": 0.95
}
```

### 2. **Multi-Language Support:**
- Currently optimized for English
- Could add language detection
- Adjust prompts for other languages

### 3. **Fine-Tuning:**
- Collect user feedback on extraction quality
- Fine-tune model on domain-specific transcripts
- Improve accuracy for industry jargon

### 4. **Alternative Models:**
- Test Anthropic Claude for comparison
- Evaluate open-source models (Llama, Mistral)
- Consider hybrid approach (local + cloud)

### 5. **Smarter Parsing:**
- Extract priority levels
- Identify dependencies between tasks
- Categorize tasks by type

## Monitoring in Production

### Key Metrics to Track:
1. **LLM Performance:**
   - Response time (p50, p95, p99)
   - Error rate
   - Cost per transcript
   - Token usage

2. **Extraction Quality:**
   - Tasks per transcript (avg)
   - User edit frequency (indicates poor extraction)
   - Deletion rate (indicates hallucinations)

3. **User Behavior:**
   - Transcripts processed per day
   - Task completion rate
   - Time to first edit (proxy for quality)

### Logging:
```python
# Log LLM calls for debugging
logger.info(f"Processing transcript {id}, length: {len(text)}")
logger.info(f"Extracted {len(items)} items in {elapsed}ms")
logger.info(f"Cost: ${cost:.4f}")
```

## Security Considerations

### Data Privacy:
- ⚠️ **Transcripts are sent to OpenAI** (3rd party)
- Not suitable for confidential meetings without data processing agreement
- Consider self-hosted models for sensitive data

### API Key Security:
- Never commit API keys to version control
- Use environment variables
- Rotate keys regularly
- Monitor for unusual usage patterns

### Input Validation:
- Sanitize transcript input
- Limit transcript length (prevent DoS via huge inputs)
- Rate limit API endpoints

## Conclusion

The AI integration is production-ready for **non-confidential meeting transcripts**. The main trade-off is sending data to OpenAI vs. accuracy and ease of implementation. For highly sensitive use cases, consider self-hosted alternatives.

**Recommendation:** Start with GPT-4o-mini, monitor quality, and upgrade to GPT-4 only if accuracy issues arise.
