# How to Use Prisma Database - Complete Guide

## 🎯 Quick Start

### 1. View Your Database (GUI)
```bash
npx prisma studio
```
This opens a web interface at `http://localhost:5555` where you can:
- View all tables
- Add/edit/delete records
- Run queries visually

---

## 🐍 Using Prisma with Python (Current Backend)

### Option 1: Switch API to Use Prisma Database

**Update `api.py`:**
```python
# Change this line:
import db_utils_neon as db_utils

# To this:
import db_utils_prisma as db_utils
```

That's it! Your entire API now uses Prisma Postgres instead of Neon.

### Option 2: Test Prisma Database

Create a test script:
```python
# test_prisma.py
from dotenv import load_dotenv
load_dotenv()

import db_utils_prisma as db

# Test connection
print("Testing Prisma connection...")
db.create_db_and_table_pg()

# Add a test user
success = db.add_user_to_db_pg(
    "testuser",
    "Test User",
    "2021TEST",
    "15",
    "08",
    "2003"
)

if success:
    print("✅ User added successfully!")
    
    # Retrieve user
    user = db.get_user_from_db_pg("testuser")
    print(f"✅ Retrieved user: {user['full_name']}")
else:
    print("❌ Failed to add user")
```

Run it:
```bash
python test_prisma.py
```

---

## 🎨 Using Prisma with Next.js (Your Frontend)

### Step 1: Setup Prisma Client

In your Next.js project:

```bash
# Install Prisma Client
npm install @prisma/client

# Copy schema from backend
cp ../contineo-scraper/prisma/schema.prisma ./prisma/

# Generate client
npx prisma generate
```

### Step 2: Create Prisma Client Instance

**`lib/prisma.ts`:**
```typescript
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: ['query', 'error', 'warn'],
})

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### Step 3: Use in Your App

#### Example 1: Get User with All Data

**`app/api/user/[username]/route.ts`:**
```typescript
import { prisma } from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function GET(
  request: Request,
  { params }: { params: { username: string } }
) {
  try {
    const user = await prisma.user.findUnique({
      where: {
        firstName: params.username
      },
      include: {
        cieMarks: {
          orderBy: {
            scrapedAt: 'desc'
          }
        },
        semesters: {
          orderBy: {
            semesterNumber: 'asc'
          }
        }
      }
    })

    if (!user) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      )
    }

    return NextResponse.json(user)
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch user' },
      { status: 500 }
    )
  }
}
```

#### Example 2: Create User

**`app/api/register/route.ts`:**
```typescript
import { prisma } from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    
    const user = await prisma.user.create({
      data: {
        firstName: body.username,
        fullName: body.fullName,
        prn: body.prn,
        dobDay: body.dobDay,
        dobMonth: body.dobMonth,
        dobYear: body.dobYear
      }
    })

    return NextResponse.json(user, { status: 201 })
  } catch (error) {
    if (error.code === 'P2002') {
      return NextResponse.json(
        { error: 'Username or PRN already exists' },
        { status: 409 }
      )
    }
    
    return NextResponse.json(
      { error: 'Failed to create user' },
      { status: 500 }
    )
  }
}
```

#### Example 3: Get Leaderboard

**`app/api/leaderboard/[subject]/[exam]/route.ts`:**
```typescript
import { prisma } from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function GET(
  request: Request,
  { params }: { params: { subject: string; exam: string } }
) {
  const leaderboard = await prisma.cieMark.findMany({
    where: {
      subjectCode: params.subject,
      examType: params.exam,
      marks: {
        not: null
      }
    },
    include: {
      user: {
        select: {
          fullName: true
        }
      }
    },
    orderBy: {
      marks: 'desc'
    },
    take: 10
  })

  return NextResponse.json(leaderboard)
}
```

#### Example 4: Add CIE Marks

**`app/api/marks/add/route.ts`:**
```typescript
import { prisma } from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  
  // Add multiple marks at once
  const marks = await prisma.cieMark.createMany({
    data: body.marks.map((mark: any) => ({
      userId: body.userId,
      subjectCode: mark.subjectCode,
      examType: mark.examType,
      marks: mark.marks,
      scrapedAt: new Date()
    })),
    skipDuplicates: true // Skip if already exists
  })

  return NextResponse.json({ 
    message: `Added ${marks.count} marks` 
  })
}
```

#### Example 5: Save Semester Record

**`app/api/semester/save/route.ts`:**
```typescript
import { prisma } from '@/lib/prisma'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  
  const semester = await prisma.semesterRecord.upsert({
    where: {
      userId_semesterNumber: {
        userId: body.userId,
        semesterNumber: body.semesterNumber
      }
    },
    update: {
      sgpa: body.sgpa,
      totalCredits: body.totalCredits,
      academicYear: body.academicYear
    },
    create: {
      userId: body.userId,
      semesterNumber: body.semesterNumber,
      semesterName: body.semesterName,
      sgpa: body.sgpa,
      totalCredits: body.totalCredits,
      academicYear: body.academicYear
    }
  })

  return NextResponse.json(semester)
}
```

---

## 🔍 Common Prisma Queries

### Find One
```typescript
const user = await prisma.user.findUnique({
  where: { firstName: 'username' }
})
```

### Find Many
```typescript
const users = await prisma.user.findMany({
  where: {
    prn: {
      startsWith: '2021'
    }
  },
  orderBy: {
    fullName: 'asc'
  }
})
```

### Create
```typescript
const user = await prisma.user.create({
  data: {
    firstName: 'newuser',
    fullName: 'New User',
    prn: '2021XXXX',
    dobDay: '15',
    dobMonth: '08',
    dobYear: '2003'
  }
})
```

### Update
```typescript
const user = await prisma.user.update({
  where: { firstName: 'username' },
  data: {
    fullName: 'Updated Name'
  }
})
```

### Delete
```typescript
await prisma.user.delete({
  where: { firstName: 'username' }
})
```

### Count
```typescript
const count = await prisma.user.count()
```

### Aggregate
```typescript
const stats = await prisma.cieMark.aggregate({
  where: {
    subjectCode: 'CSC601',
    examType: 'MSE'
  },
  _avg: {
    marks: true
  },
  _max: {
    marks: true
  },
  _min: {
    marks: true
  }
})
```

---

## 🎨 Using in React Components

### Server Component (Recommended)
```typescript
// app/dashboard/page.tsx
import { prisma } from '@/lib/prisma'

export default async function DashboardPage() {
  const users = await prisma.user.findMany({
    include: {
      cieMarks: true
    }
  })

  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => (
        <div key={user.id}>
          <h2>{user.fullName}</h2>
          <p>Marks: {user.cieMarks.length}</p>
        </div>
      ))}
    </div>
  )
}
```

### Client Component with API Route
```typescript
// app/dashboard/page.tsx
'use client'

import { useEffect, useState } from 'react'

export default function DashboardPage() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data))
  }, [])

  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => (
        <div key={user.id}>
          <h2>{user.fullName}</h2>
        </div>
      ))}
    </div>
  )
}
```

### With SWR (Better)
```typescript
'use client'

import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function DashboardPage() {
  const { data: users, error, isLoading } = useSWR('/api/users', fetcher)

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error loading users</div>

  return (
    <div>
      <h1>Dashboard</h1>
      {users.map(user => (
        <div key={user.id}>
          <h2>{user.fullName}</h2>
        </div>
      ))}
    </div>
  )
}
```

---

## 🛠️ Useful Prisma Commands

### View Database
```bash
npx prisma studio
```

### Generate Client (after schema changes)
```bash
npx prisma generate
```

### Push Schema Changes
```bash
npx prisma db push
```

### Create Migration
```bash
npx prisma migrate dev --name add_new_field
```

### Reset Database
```bash
npx prisma db push --force-reset
```

### Seed Database
```bash
npx prisma db seed
```

---

## 📊 Prisma Studio Features

When you run `npx prisma studio`:

1. **View Tables**: See all your data in a spreadsheet-like interface
2. **Add Records**: Click "Add record" to insert new data
3. **Edit Records**: Click any cell to edit
4. **Delete Records**: Select rows and delete
5. **Filter**: Use filters to find specific records
6. **Sort**: Click column headers to sort
7. **Relations**: Click relation fields to navigate

---

## 🔄 Migrate Data from Neon to Prisma

If you want to move your data:

```bash
python migrate_to_prisma.py
```

This will:
1. Connect to both databases
2. Copy all users
3. Copy all CIE marks
4. Copy all semester records
5. Maintain relationships

---

## ⚠️ Important Notes

### 1. Claim Your Database
Your Prisma database expires in 24 hours. Claim it:
👉 https://create-db.prisma.io/claim?projectID=proj_cmhtj549u04mezzf251o38c3l

### 2. Environment Variables
Make sure your Next.js `.env.local` has:
```env
DATABASE_URL="prisma+postgres://accelerate.prisma-data.net/?api_key=..."
DIRECT_URL="postgresql://...@db.prisma.io:5432/postgres?sslmode=require"
```

### 3. Prisma Client Generation
After any schema changes, run:
```bash
npx prisma generate
```

### 4. Type Safety
Prisma provides full TypeScript types:
```typescript
// TypeScript knows all fields!
const user: User = await prisma.user.findUnique({
  where: { firstName: 'username' }
})

// Autocomplete works!
console.log(user.fullName) // ✅
console.log(user.invalidField) // ❌ TypeScript error
```

---

## 🎯 Best Practices

### 1. Use Transactions for Multiple Operations
```typescript
await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.cieMark.createMany({ data: marksData })
])
```

### 2. Handle Errors Properly
```typescript
try {
  const user = await prisma.user.create({ data })
} catch (error) {
  if (error.code === 'P2002') {
    // Unique constraint violation
  }
}
```

### 3. Use Select to Optimize Queries
```typescript
const user = await prisma.user.findUnique({
  where: { firstName: 'username' },
  select: {
    id: true,
    fullName: true,
    // Only fetch what you need
  }
})
```

### 4. Use Pagination
```typescript
const users = await prisma.user.findMany({
  skip: 0,
  take: 10,
  orderBy: { fullName: 'asc' }
})
```

---

## 📚 Resources

- [Prisma Docs](https://www.prisma.io/docs)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Next.js + Prisma](https://www.prisma.io/docs/guides/other/troubleshooting-orm/help-articles/nextjs-prisma-client-dev-practices)
- [Prisma Examples](https://github.com/prisma/prisma-examples)

---

**You're all set to use Prisma! 🚀**
