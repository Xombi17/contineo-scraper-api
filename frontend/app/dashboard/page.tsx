'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import useSWR from 'swr'
import { fetchStudentData, calculateSGPA } from '@/lib/api'
import Sidebar from '@/components/Sidebar'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend } from 'recharts'
import { RefreshCw, TrendingUp, BookOpen, Award, Calendar, AlertCircle } from 'lucide-react'

export default function Dashboard() {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('username')
    if (!stored) {
      router.push('/')
    } else {
      setUsername(stored)
    }
  }, [router])

  const { data: studentData, error, mutate } = useSWR(
    username ? `student-${username}` : null,
    () => fetchStudentData(username),
    { revalidateOnFocus: false }
  )

  const { data: sgpaData } = useSWR(
    username ? `sgpa-${username}` : null,
    () => calculateSGPA(username),
    { revalidateOnFocus: false }
  )

  const handleRefresh = async () => {
    setRefreshing(true)
    await mutate()
    setRefreshing(false)
  }

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
            <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-bold text-white mb-2">Failed to Load Data</h2>
            <p className="text-gray-400 mb-6">Unable to fetch your data. Please try again.</p>
            <button
              onClick={handleRefresh}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition"
            >
              Retry
            </button>
          </div>
        </main>
      </div>
    )
  }

  if (!studentData || !sgpaData) {
    return (
      <div className="flex">
        <Sidebar username={username} onLogout={handleLogout} />
        <main className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading your data...</p>
          </div>
        </main>
      </div>
    )
  }

  const avgAttendance = studentData.attendance.length > 0
    ? studentData.attendance.reduce((sum, r) => sum + r.percentage, 0) / studentData.attendance.length
    : 0

  const chartData = studentData.attendance
    .filter(r => r.subject !== 'CSM601')
    .map(r => ({
      subject: r.subject,
      percentage: r.percentage,
      color: r.percentage >= 85 ? '#10b981' : r.percentage >= 75 ? '#f59e0b' : '#ef4444'
    }))

  const gradeData = Object.entries(sgpaData.grade_distribution).map(([grade, count]) => ({
    name: grade,
    value: count,
    color: grade === 'O' ? '#8b5cf6' : grade === 'A+' ? '#3b82f6' : grade === 'A' ? '#10b981' : '#f59e0b'
  }))

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar username={username} onLogout={handleLogout} />
      
      <main className="ml-64 flex-1 p-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">Dashboard</h1>
            <p className="text-gray-400">{studentData.user.full_name} • {studentData.user.prn}</p>
          </div>
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50 shadow-lg shadow-blue-600/30"
          >
            <RefreshCw className={`w-5 h-5 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh Data
          </button>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8 text-white/80" />
              <span className={`text-xs font-bold px-3 py-1 rounded-full ${
                avgAttendance >= 75 ? 'bg-white/20 text-white' : 'bg-red-500 text-white'
              }`}>
                {avgAttendance >= 75 ? 'GOOD' : 'LOW'}
              </span>
            </div>
            <p className="text-4xl font-bold text-white mb-1">{avgAttendance.toFixed(1)}%</p>
            <p className="text-white/80 text-sm">Average Attendance</p>
          </div>

          <div className="bg-gradient-to-br from-blue-600 to-purple-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Award className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-4xl font-bold text-white mb-1">{sgpaData.sgpa.toFixed(2)}</p>
            <p className="text-white/80 text-sm">Current SGPA</p>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-pink-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <BookOpen className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-4xl font-bold text-white mb-1">{sgpaData.total_credits}</p>
            <p className="text-white/80 text-sm">Credits Earned</p>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-red-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Calendar className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-4xl font-bold text-white mb-1">{sgpaData.subjects.length}</p>
            <p className="text-white/80 text-sm">Total Subjects</p>
          </div>
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Attendance Chart */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold text-white mb-6">📊 Attendance Overview</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="subject" stroke="#9ca3af" />
                  <YAxis domain={[0, 100]} stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Bar dataKey="percentage" radius={[8, 8, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Grade Distribution */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold text-white mb-6">🏆 Grade Distribution</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={gradeData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {gradeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Subjects Grid */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6">📚 Subject Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sgpaData.subjects.map((subject) => (
              <div key={subject.code} className="bg-gray-900 border border-gray-800 rounded-xl p-6 hover:border-blue-600 transition shadow-xl">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="font-bold text-white text-lg">{subject.name}</h3>
                    <p className="text-sm text-gray-500">{subject.code}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                    subject.grade === 'O' ? 'bg-purple-600 text-white' :
                    subject.grade === 'A+' ? 'bg-blue-600 text-white' :
                    subject.grade === 'A' ? 'bg-green-600 text-white' :
                    subject.grade === 'B+' ? 'bg-yellow-600 text-white' :
                    'bg-gray-700 text-white'
                  }`}>
                    {subject.grade}
                  </span>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Marks</span>
                    <span className="font-bold text-white">{subject.marks.toFixed(1)}/100</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Percentage</span>
                    <span className="font-bold text-white">{subject.percentage.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Grade Point</span>
                    <span className="font-bold text-blue-400">{subject.grade_point}/10</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Credits</span>
                    <span className="font-bold text-white">{subject.credits}</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-gray-800">
                  <div className="w-full bg-gray-800 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all"
                      style={{ width: `${subject.percentage}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
