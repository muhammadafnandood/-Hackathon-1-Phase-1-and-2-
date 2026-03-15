---
sidebar_label: '1. BetterAuth Setup'
---

# Chapter 1: BetterAuth for RAG System

## Authentication Architecture

```
┌─────────────────┐
│   User Request  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   BetterAuth    │ ← Authentication & Authorization
└────────┬────────┘
         │ (Authenticated)
         ▼
┌─────────────────┐
│  RAG Pipeline   │
└─────────────────┘
```

## What is BetterAuth?

BetterAuth is a framework-agnostic authentication and authorization library for TypeScript that provides:

- ✅ **Framework-agnostic** - Works with Express, Next.js, Hono, etc.
- ✅ **Multiple providers** - Email/password, OAuth, magic links, passkeys
- ✅ **Database support** - PostgreSQL, MySQL, MongoDB, etc.
- ✅ **Plugin ecosystem** - 2FA, multi-tenancy, SSO, organization management
- ✅ **Type-safe** - Full TypeScript support

## Installation

```bash
npm install better-auth pg
```

## Basic Setup with PostgreSQL

### 1. Create Auth Instance (`auth.ts`)

```typescript
import { Pool } from "pg";
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  baseURL: "http://localhost:3000",
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
  },
});
```

### 2. Environment Variables (`.env`)

```bash
DATABASE_URL=postgres://user:password@localhost:5432/rag_database
BETTER_AUTH_SECRET=your-secret-key-here
```

### 3. Express Integration (`server.ts`)

```typescript
import express from "express";
import { toNodeHandler } from "better-auth/node";
import { auth } from "./auth";

const app = express();
const port = 3000;

// BetterAuth handles all /api/auth/* routes
app.all("/api/auth/*", toNodeHandler(auth));

// Apply JSON middleware after BetterAuth routes
app.use(express.json());

// Protected RAG API routes
app.post("/api/search", authenticate, async (req, res) => {
  const { query } = req.body;
  // RAG search logic here
  res.json({ results: [] });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

### 4. Authentication Middleware

```typescript
import { Request, Response, NextFunction } from "express";
import { auth } from "./auth";

export async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const session = await auth.api.getSession({
    headers: req.headers,
  });

  if (!session) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  req.user = session.user;
  next();
}
```

## Auth Routes

BetterAuth automatically provides these endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sign-up/email` | Register with email/password |
| POST | `/api/auth/sign-in/email` | Login with email/password |
| POST | `/api/auth/sign-out` | Logout current session |
| GET | `/api/auth/session` | Get current session |
| POST | `/api/auth/forget-password` | Request password reset |
| POST | `/api/auth/reset-password` | Reset password with token |

## Client-Side Usage

```typescript
import { createAuthClient } from "better-auth/react";

const authClient = createAuthClient({
  baseURL: "http://localhost:3000",
});

// Sign up
await authClient.signUp.email({
  email: "user@example.com",
  password: "securePassword123",
  name: "John Doe",
});

// Sign in
const { data: session } = await authClient.signIn.email({
  email: "user@example.com",
  password: "securePassword123",
});

// Sign out
await authClient.signOut();

// Get session
const { data: currentSession } = await authClient.getSession();
```

## Protecting RAG Endpoints

```typescript
import { Router } from "express";
import { authenticate } from "./middleware/auth";
import { searchVectorDB } from "./rag/search";

const router = Router();

// All routes require authentication
router.use(authenticate);

// RAG Search Endpoint
router.post("/search", async (req, res) => {
  const { query, topK = 5 } = req.body;
  const userId = req.user.id;

  try {
    // Search vector DB with user context
    const results = await searchVectorDB({
      query,
      userId,
      topK,
    });

    res.json({
      success: true,
      results,
      user: req.user.email,
    });
  } catch (error) {
    res.status(500).json({ error: "Search failed" });
  }
});

// Upload Documents Endpoint
router.post("/upload", async (req, res) => {
  const { documents } = req.body;
  const userId = req.user.id;

  // Process and store user documents
  // ...

  res.json({ success: true, uploaded: documents.length });
});

export default router;
```

## Next Steps

Next, we'll implement the RAG pipeline with Qdrant vector database.
