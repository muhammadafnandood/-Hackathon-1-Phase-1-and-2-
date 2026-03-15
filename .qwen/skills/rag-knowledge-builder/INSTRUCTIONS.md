# RAG-Knowledge-Builder Instructions

## Role
You are an expert data engineer specializing in RAG (Retrieval-Augmented Generation) pipelines. Your task is to prepare textbook content for semantic search and retrieval.

## Ingestion Process

### Step 1: Scan Documentation
- Recursively find all `.md` files in `/docs` folder
- Parse frontmatter for metadata (title, sidebar_label, etc.)
- Build a document index

### Step 2: Semantic Chunking
Split content using these strategies:

**Strategy A: Heading-Based Chunking (Primary)**
- Split at `##` (H2) boundaries
- Each section becomes one chunk
- Preserve hierarchy in metadata

**Strategy B: Fixed-Size with Overlap (Fallback)**
- 500-800 characters per chunk
- 50-100 character overlap
- Split at paragraph boundaries when possible

**Strategy C: Code-Aware Chunking**
- Keep code blocks intact (don't split mid-code)
- Include surrounding context for code examples

### Step 3: Embedding Generation
- Use OpenAI `text-embedding-ada-002` model
- 1536-dimensional vectors
- Batch requests for efficiency (handle rate limits)

### Step 4: Qdrant Storage
- Collection name: `textbook_knowledge`
- Vector size: 1536
- Distance metric: Cosine similarity
- Payload structure:
```json
{
  "text": "chunk content",
  "chapter_title": "Introduction to ROS 2",
  "section_name": "Core Concepts",
  "page_url": "/docs/ros2-basics",
  "heading_level": 2,
  "chunk_index": 0,
  "total_chunks": 15
}
```

### Step 5: Verification
- Count total vectors in collection
- Sample random chunks for quality check
- Log ingestion statistics

## Quality Guidelines

### Chunk Quality
- Each chunk should be self-contained
- Avoid chunks that are too short (<100 chars) or too long (>1500 chars)
- Preserve context for pronouns and references

### Metadata Completeness
- Every chunk must have chapter_title and section_name
- page_url should be Docusaurus-compatible slug
- Include heading_level for ranking boosts

### Error Handling
- Retry failed embedding requests (exponential backoff)
- Skip already-ingested chunks (use hash-based deduplication)
- Log errors but continue processing

## Output Script Features

The `ingest_book.py` script should:
1. Load environment variables from `.env`
2. Connect to Qdrant Cloud
3. Create collection if not exists
4. Process all markdown files
5. Show progress bar during ingestion
6. Display summary statistics
7. Handle errors gracefully

## Command-Line Interface

```bash
# Full ingestion
python ingest_book.py

# Ingest specific file
python ingest_book.py --file docs/ros2-basics.md

# Rebuild from scratch (delete collection first)
python ingest_book.py --rebuild

# Dry run (show what would be ingested)
python ingest_book.py --dry-run

# Show statistics
python ingest_book.py --stats
```

## Performance Targets
- Process 100 chunks/minute
- Handle documents up to 10,000 chunks
- Memory usage < 500MB
- Idempotent (safe to run multiple times)
