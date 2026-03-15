# Vercel deployment configuration for Physical AI RAG API

# Required Environment Variables:
# - OPENAI_API_KEY: Your OpenAI API key
# - DATABASE_URL: PostgreSQL connection string (use Neon or Supabase)
# - QDRANT_URL: Qdrant cloud URL (use Qdrant Cloud)
# - QDRANT_API_KEY: Qdrant API key

# Deployment Instructions:

# 1. Install Vercel CLI
# npm install -g vercel

# 2. Login to Vercel
# vercel login

# 3. Deploy
# cd backend
# vercel

# 4. Set environment variables in Vercel dashboard:
# https://vercel.com/dashboard -> Project -> Settings -> Environment Variables

# 5. Production deployment
# vercel --prod

# Note: Vercel serverless functions have timeout limits (10s-60s depending on plan)
# For long-running LLM requests, consider using Railway instead
