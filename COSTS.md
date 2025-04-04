# Cost Analysis and Optimization

## Cost Breakdown

### 1. Transcription (Whisper)

- Model: "base"
- Cost: $0.006 per minute
- Examples:
  - 5-minute podcast: $0.03
  - 30-minute podcast: $0.18
  - 60-minute podcast: $0.36
  - 2-hour podcast: $0.72

### 2. Knowledge Base Creation

- Uses OpenAI Embeddings (text-embedding-ada-002)
- Cost: $0.0001 per 1,000 tokens
- Token estimates:
  - 5 minutes ≈ 1,000 tokens ($0.0001)
  - 30 minutes ≈ 6,000 tokens ($0.0006)
  - 60 minutes ≈ 12,000 tokens ($0.0012)
  - 2 hours ≈ 24,000 tokens ($0.0024)

### 3. Querying (GPT-3.5-turbo)

- Cost: $0.002 per 1,000 tokens
- Per query estimate:
  - Question: ~50-100 tokens
  - Retrieved context: ~500-1,000 tokens
  - Answer: ~100-500 tokens
  - Total per query: ~$0.001-$0.003

## Total Cost Examples

### 5-Minute Podcast

- Transcription: $0.03
- Knowledge base: $0.0001
- 10 queries: $0.01-$0.03
- **Total**: $0.04-$0.06

### 30-Minute Podcast

- Transcription: $0.18
- Knowledge base: $0.0006
- 10 queries: $0.01-$0.03
- **Total**: $0.19-$0.21

### 60-Minute Podcast

- Transcription: $0.36
- Knowledge base: $0.0012
- 10 queries: $0.01-$0.03
- **Total**: $0.37-$0.39

### 2-Hour Podcast

- Transcription: $0.72
- Knowledge base: $0.0024
- 10 queries: $0.01-$0.03
- **Total**: $0.73-$0.75

## Cost Optimization Strategies

### 1. Transcription Optimization

- Use smaller Whisper models:
  - "tiny": ~1/4 the cost of "base"
  - "small": ~1/2 the cost of "base"
  - Trade-off: Slightly lower accuracy

### 2. Knowledge Base Optimization

- Reduce chunk size:
  - Current: 1,000 tokens
  - Could reduce to: 500 tokens
  - Impact: Smaller context windows but more precise retrieval
- Filter content:
  - Remove irrelevant sections
  - Focus on key content
  - Impact: Reduced token count, more focused answers

### 3. Query Optimization

- Limit retrieved documents:
  - Current: All relevant chunks
  - Could limit to: Top 3-5 most relevant
  - Impact: Reduced token usage, potentially less context
- Use shorter questions:
  - Be more concise
  - Focus on specific topics
  - Impact: Reduced input tokens

### 4. Model Selection

- Use cheaper models:
  - GPT-3.5-turbo (current): $0.002/1K tokens
  - GPT-3.5-turbo-instruct: $0.0015/1K tokens
  - Impact: Lower cost but potentially lower quality

## Implementation Notes

To implement these optimizations, you can modify the following parameters in the code:

```python
# In transcribe.py
model = whisper.load_model("tiny")  # or "small" for better quality

# In llm.py
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Reduced from 1000
    chunk_overlap=100  # Reduced from 200
)

# In llm.py
retriever = self.vectorstore.as_retriever(
    search_kwargs={"k": 3}  # Limit to top 3 results
)
```

## Monitoring Costs

To monitor actual costs:

1. Check OpenAI usage dashboard: https://platform.openai.com/account/usage
2. Set up billing alerts
3. Consider implementing cost tracking in the code

## Best Practices

1. Start with smaller content to test
2. Use appropriate model sizes for content length
3. Monitor usage patterns
4. Implement cost-saving measures based on your specific needs
5. Consider caching frequently asked questions
6. Batch process transcripts when possible
