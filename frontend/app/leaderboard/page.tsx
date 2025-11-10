'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import useSWR from 'swr'
import Sidebar from '@/components/Sidebar'
import { Trophy, Medal, Award, TrendingUp, Crown } from 'lucide-react'

const fetcher = (url: string) => fetch(url).then(r => r.json())

interface LeaderboardEntry {
  rank: number
  username: string
  full_name: string
  sgpa: number
  total_credits: number
  avg_attendance: number
}

export default function Leaderboard() {
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

  const { data: leaderboardData, error } = useSWR(
    'http://localhost:8000/leaderboard',
    fetcher,
    { revalidateOnFocus: false }
  )

  // Ensure leaderboard is always an array
  const leaderboard: LeaderboardEntry[] = Array.isArray(leaderboardData) ? leaderboardData : []

  const handleLogout = () => {
    localStorage.removeItem('username')
    router.push('/')
  }

  if (!username) return null

  if (error) {
    return (
      <div className="flex">
        <Sidebar username={username} onLogout={handleLogout} />
        <main className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="bg-gray-900 border border-gray-800 p-8 rounded-xl text-center max-w-md">
            <Trophy className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">Failed to Load Leaderboard</h2>
            <p className="text-gray-400">Unable to fetch leaderboard data.</p>
          </div>
        </main>
      </div>
    )
  }

  if (!leaderboardData) {
    return (
      <div className="flex">
        <Sidebar username={username} onLogout={handleLogout} />
        <main className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading leaderboard...</p>
          </div>
        </main>
      </div>
    )
  }

  if (leaderboard.length === 0) {
    return (
      <div className="flex">
        <Sidebar username={username} onLogout={handleLogout} />
        <main className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="bg-gray-900 border border-gray-800 p-8 rounded-xl text-center max-w-md">
            <Trophy className="w-16 h-16 text-gray-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">No Data Available</h2>
            <p className="text-gray-400">Leaderboard data is not available yet.</p>
          </div>
        </main>
      </div>
    )
  }

  const currentUser = leaderboard.find(entry => entry.username === username)
  const topThree = leaderboard.slice(0, 3)
  const rest = leaderboard.slice(3)

  const getRankIcon = (rank: number) => {
    if (rank === 1) return <Crown className="w-6 h-6 text-yellow-400" />
    if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />
    if (rank === 3) return <Medal className="w-6 h-6 text-orange-400" />
    return <Award className="w-5 h-5 text-gray-500" />
  }

  const getRankBg = (rank: number) => {
    if (rank === 1) return 'from-yellow-600 to-yellow-700'
    if (rank === 2) return 'from-gray-600 to-gray-700'
    if (rank === 3) return 'from-orange-600 to-orange-700'
    return ''
  }

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar username={username} onLogout={handleLogout} />
      
      <main className="ml-64 flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-1">🏆 Leaderboard</h1>
          <p className="text-gray-400">Top performers ranked by SGPA</p>
        </div>

        {/* Your Rank Card */}
        {currentUser && (
          <div className="bg-gradient-to-br from-blue-600 to-purple-700 rounded-xl p-6 shadow-xl mb-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="bg-white/20 rounded-full p-4">
                  <TrendingUp className="w-8 h-8 text-white" />
                </div>
                <div>
                  <p className="text-white/80 text-sm">Your Rank</p>
                  <p className="text-3xl font-bold text-white">#{currentUser.rank}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-white/80 text-sm">Your SGPA</p>
                <p className="text-3xl font-bold text-white">{currentUser.sgpa.toFixed(2)}</p>
              </div>
            </div>
          </div>
        )}

        {/* Top 3 Podium */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {topThree.map((entry) => (
            <div
              key={entry.rank}
              className={`bg-gradient-to-br ${getRankBg(entry.rank)} rounded-xl p-6 shadow-xl ${
                entry.rank === 1 ? 'md:order-2 transform md:scale-105' : 
                entry.rank === 2 ? 'md:order-1' : 'md:order-3'
              }`}
            >
              <div className="flex items-center justify-center mb-4">
                {getRankIcon(entry.rank)}
              </div>
              <div className="text-center">
                <p className="text-4xl font-bold text-white mb-2">#{entry.rank}</p>
                <p className="text-lg font-bold text-white mb-1">{entry.full_name}</p>
                <p className="text-white/80 text-sm mb-4">@{entry.username}</p>
                <div className="bg-white/20 rounded-lg p-3">
                  <p className="text-2xl font-bold text-white">{entry.sgpa.toFixed(2)}</p>
                  <p className="text-white/80 text-xs">SGPA</p>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-3">
                  <div className="bg-white/10 rounded-lg p-2">
                    <p className="text-sm font-bold text-white">{entry.total_credits}</p>
                    <p className="text-white/70 text-xs">Credits</p>
                  </div>
                  <div className="bg-white/10 rounded-lg p-2">
                    <p className="text-sm font-bold text-white">{entry.avg_attendance.toFixed(1)}%</p>
                    <p className="text-white/70 text-xs">Attendance</p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Rest of Rankings */}
        {rest.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl shadow-xl overflow-hidden">
            <div className="p-6 border-b border-gray-800">
              <h2 className="text-xl font-bold text-white">All Rankings</h2>
            </div>
            <div className="divide-y divide-gray-800">
              {rest.map((entry) => (
                <div
                  key={entry.rank}
                  className={`p-6 hover:bg-gray-800/50 transition ${
                    entry.username === username ? 'bg-blue-600/10 border-l-4 border-blue-600' : ''
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4 flex-1">
                      <div className="flex items-center justify-center w-12 h-12 bg-gray-800 rounded-full">
                        <span className="text-lg font-bold text-gray-400">#{entry.rank}</span>
                      </div>
                      <div className="flex-1">
                        <p className="font-bold text-white text-lg">{entry.full_name}</p>
                        <p className="text-gray-400 text-sm">@{entry.username}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-8">
                      <div className="text-right">
                        <p className="text-2xl font-bold text-white">{entry.sgpa.toFixed(2)}</p>
                        <p className="text-gray-400 text-xs">SGPA</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-white">{entry.total_credits}</p>
                        <p className="text-gray-400 text-xs">Credits</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-bold text-white">{entry.avg_attendance.toFixed(1)}%</p>
                        <p className="text-gray-400 text-xs">Attendance</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
