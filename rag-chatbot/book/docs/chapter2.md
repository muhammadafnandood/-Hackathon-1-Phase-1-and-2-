# Chapter 2: Vector Databases and Embeddings

## Understanding Embeddings

Embeddings are numerical representations of text that capture semantic meaning. Similar texts have similar vector representations in the embedding space.

### Popular Embedding Models

- **OpenAI Ada-002**: 1536 dimensions, general purpose
- **Sentence Transformers**: Open source, various sizes
- **Cohere**: Optimized for search applications

## Vector Databases

Vector databases store and index embeddings for efficient similarity search.

### Qdrant Features

- Written in Rust for high performance
- Supports filtering and payload-based queries
- Scalable with distributed deployment
- RESTful API and multiple SDK clients

## Similarity Metrics

- **Cosine Similarity**: Measures angle between vectors
- **Dot Product**: Efficient for normalized vectors
- **Euclidean Distance**: Straight-line distance
