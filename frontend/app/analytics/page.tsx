'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import useSWR from 'swr'
import Sidebar from '@/components/Sidebar'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ScatterChart, Scatter } from 'recharts'
import { TrendingUp, Users, Award, Target, AlertCircle } from 'lucide-react'

const fetcher = (url: string) => fetch(url).then(r => r.json())

export default function Analytics() {
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

  const { data: analytics, error } = useSWR(
    username ? `http://localhost:8000/analytics/${username}` : null,
    fetcher,
    { revalidateOnFocus: false }
  )

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
            <h2 className="text-xl font-bold text-white mb-2">Failed to Load Analytics</h2>
            <p className="text-gray-400">Unable to fetch analytics data.</p>
          </div>
        </main>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="flex">
        <Sidebar username={username} onLogout={handleLogout} />
        <main className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p className="text-gray-400">Loading analytics...</p>
          </div>
        </main>
      </div>
    )
  }

  const subjectPerformance = analytics.subject_performance?.map((s: any) => ({
    subject: s.subject_code,
    marks: s.marks,
    attendance: s.attendance,
    grade_point: s.grade_point
  })) || []

  const attendanceMarksData = analytics.attendance_marks_correlation?.map((item: any) => ({
    attendance: item.attendance,
    marks: item.marks
  })) || []

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar username={username} onLogout={handleLogout} />
      
      <main className="ml-64 flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-1">📊 Analytics Dashboard</h1>
          <p className="text-gray-400">Deep insights into your academic performance</p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Award className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-3xl font-bold text-white mb-1">{analytics.current_sgpa.toFixed(2)}</p>
            <p className="text-white/80 text-sm">Current SGPA</p>
          </div>

          <div className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <TrendingUp className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-3xl font-bold text-white mb-1">{analytics.predicted_cgpa.toFixed(2)}</p>
            <p className="text-white/80 text-sm">Predicted CGPA</p>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Target className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-3xl font-bold text-white mb-1">{analytics.avg_attendance.toFixed(1)}%</p>
            <p className="text-white/80 text-sm">Avg Attendance</p>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-orange-700 rounded-xl p-6 shadow-xl">
            <div className="flex items-center justify-between mb-4">
              <Users className="w-8 h-8 text-white/80" />
            </div>
            <p className="text-3xl font-bold text-white mb-1">{analytics.class_rank || 'N/A'}</p>
            <p className="text-white/80 text-sm">Class Rank</p>
          </div>
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Subject Performance */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold text-white mb-6">📚 Subject Performance</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={subjectPerformance}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="subject" stroke="#9ca3af" />
                  <YAxis stroke="#9ca3af" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    labelStyle={{ color: '#fff' }}
                  />
                  <Legend />
                  <Bar dataKey="marks" fill="#3b82f6" name="Marks" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="attendance" fill="#10b981" name="Attendance %" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Attendance vs Marks Correlation */}
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
            <h2 className="text-xl font-bold text-white mb-6">📈 Attendance vs Marks</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="attendance" name="Attendance" stroke="#9ca3af" label={{ value: 'Attendance %', position: 'insideBottom', offset: -5, fill: '#9ca3af' }} />
                  <YAxis dataKey="marks" name="Marks" stroke="#9ca3af" label={{ value: 'Marks', angle: -90, position: 'insideLeft', fill: '#9ca3af' }} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                    cursor={{ strokeDasharray: '3 3' }}
                  />
                  <Scatter data={attendanceMarksData} fill="#8b5cf6" />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Insights */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
          <h2 className="text-xl font-bold text-white mb-6">💡 Key Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-bold text-blue-400 mb-2">🎯 Strongest Subject</h3>
              <p className="text-white text-lg">{analytics.subject_performance?.[0]?.subject_code || 'N/A'}</p>
              <p className="text-gray-400 text-sm">
                {analytics.subject_performance?.[0]?.marks ? `${analytics.subject_performance[0].marks.toFixed(1)} marks • ${analytics.subject_performance[0].grade}` : 'No data'}
              </p>
            </div>
            
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-bold text-yellow-400 mb-2">⚠️ Needs Attention</h3>
              <p className="text-white text-lg">
                {analytics.subject_performance?.[analytics.subject_performance.length - 1]?.subject_code || 'N/A'}
              </p>
              <p className="text-gray-400 text-sm">
                {analytics.subject_performance?.[analytics.subject_performance.length - 1]?.marks ? `${analytics.subject_performance[analytics.subject_performance.length - 1].marks.toFixed(1)} marks` : 'No data'}
              </p>
            </div>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-bold text-green-400 mb-2">📊 Performance Trend</h3>
              <p className="text-white text-lg">
                {(analytics.predicted_cgpa && analytics.current_sgpa) ? (analytics.predicted_cgpa > analytics.current_sgpa ? '📈 Improving' : '📉 Declining') : 'N/A'}
              </p>
              <p className="text-gray-400 text-sm">
                Based on current trajectory
              </p>
            </div>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-bold text-purple-400 mb-2">🎓 Grade Distribution</h3>
              <p className="text-white text-lg">
                {analytics.grade_distribution ? Object.keys(analytics.grade_distribution)[0] || 'N/A' : 'N/A'} Grade Majority
              </p>
              <p className="text-gray-400 text-sm">
                Most common grade achieved
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
