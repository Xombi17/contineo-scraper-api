'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Sidebar from '@/components/Sidebar'

export default function CGPA() {
  const router = useRouter()
  const [username, setUsername] = useState('')

  useEffect(() => {
    const stored = localStorage.getItem('username')
    if (!stored) {
      router.push('/')
    } else {
      setUsername(stored)
    }
  }, [router])

  const handleLogout = () => {
    localStorage.removeItem('username')
    router.push('/')
  }

  if (!username) return null

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar username={username} onLogout={handleLogout} />
      
      <main className="ml-64 flex-1 p-8">
        <h1 className="text-3xl font-bold text-white mb-4">CGPA Calculator</h1>
        <p className="text-gray-400">CGPA calculator coming soon...</p>
      </main>
    </div>
  )
}
