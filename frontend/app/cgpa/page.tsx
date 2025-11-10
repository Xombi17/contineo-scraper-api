'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import useSWR from 'swr'
import Sidebar from '@/components/Sidebar'
import { Calculator, Plus, Trash2, TrendingUp, Award, Edit2, RotateCcw } from 'lucide-react'
import { calculateSGPA } from '@/lib/api'

interface Semester {
  id: number
  sgpa: number
  credits: number
}

interface SubjectMark {
  code: string
  name: string
  marks: number
  credits: number
  grade: string
  grade_point: number
}

export default function CGPACalculator() {
  const router = useRouter()
  const [username, setUsername] = useState('')
  const [semesters, setSemesters] = useState<Semester[]>([
    { id: 1, sgpa: 0, credits: 0 }
  ])
  const [subjects, setSubjects] = useState<SubjectMark[]>([])
  const [editMode, setEditMode] = useState(false)

  useEffect(() => {
    const stored = localStorage.getItem('username')
    if (!stored) {
      router.push('/')
    } else {
      setUsername(stored)
    }
  }, [router])

  const { data: sgpaData } = useSWR(
    username ? `sgpa-${username}` : null,
    () => calculateSGPA(username),
    { 
      revalidateOnFocus: false,
      onSuccess: (data) => {
        if (data && data.subjects) {
          setSubjects(data.subjects.map((s: any) => ({
            code: s.code,
            name: s.name,
            marks: s.marks,
            credits: s.credits,
            grade: s.grade,
            grade_point: s.grade_point
          })))
        }
      }
    }
  )

  const handleLogout = () => {
    localStorage.removeItem('username')
    router.push('/')
  }

  const addSemester = () => {
    setSemesters([...semesters, { id: semesters.length + 1, sgpa: 0, credits: 0 }])
  }

  const removeSemester = (id: number) => {
    if (semesters.length > 1) {
      setSemesters(semesters.filter(s => s.id !== id))
    }
  }

  const updateSemester = (id: number, field: 'sgpa' | 'credits', value: number) => {
    setSemesters(semesters.map(s => 
      s.id === id ? { ...s, [field]: value } : s
    ))
  }

  const calculateCurrentSGPA = () => {
    if (subjects.length === 0) return 0
    const totalCredits = subjects.reduce((sum, s) => sum + s.credits, 0)
    if (totalCredits === 0) return 0
    const weightedSum = subjects.reduce((sum, s) => sum + (s.grade_point * s.credits), 0)
    return weightedSum / totalCredits
  }

  const calculateCGPA = () => {
    const totalCredits = semesters.reduce((sum, s) => sum + s.credits, 0)
    if (totalCredits === 0) return 0
    const weightedSum = semesters.reduce((sum, s) => sum + (s.sgpa * s.credits), 0)
    return weightedSum / totalCredits
  }

  const updateSubjectMarks = (code: string, newMarks: number) => {
    setSubjects(subjects.map(s => {
      if (s.code === code) {
        const percentage = (newMarks / 100) * 100
        let grade = 'F'
        let gradePoint = 0
        
        if (percentage >= 90) { grade = 'O'; gradePoint = 10 }
        else if (percentage >= 80) { grade = 'A+'; gradePoint = 9 }
        else if (percentage >= 70) { grade = 'A'; gradePoint = 8 }
        else if (percentage >= 60) { grade = 'B+'; gradePoint = 7 }
        else if (percentage >= 50) { grade = 'B'; gradePoint = 6 }
        else if (percentage >= 45) { grade = 'C'; gradePoint = 5 }
        else if (percentage >= 40) { grade = 'P'; gradePoint = 4 }
        
        return { ...s, marks: newMarks, grade, grade_point: gradePoint }
      }
      return s
    }))
  }

  const resetToOriginal = () => {
    if (sgpaData && sgpaData.subjects) {
      setSubjects(sgpaData.subjects.map((s: any) => ({
        code: s.code,
        name: s.name,
        marks: s.marks,
        credits: s.credits,
        grade: s.grade,
        grade_point: s.grade_point
      })))
    }
  }

  const currentSGPA = calculateCurrentSGPA()
  const cgpa = calculateCGPA()
  const totalCredits = semesters.reduce((sum, s) => sum + s.credits, 0)

  if (!username) return null

  return (
    <div className="flex min-h-screen bg-gray-950">
      <Sidebar username={username} onLogout={handleLogout} />
      
      <main className="ml-64 flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-1">🧮 CGPA Calculator</h1>
          <p className="text-gray-400">Calculate your cumulative grade point average</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Calculator Section */}
          <div className="lg:col-span-2 space-y-4">
            {/* Current SGPA Section */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Current Semester Performance</h2>
                <div className="flex gap-2">
                  <button
                    onClick={() => setEditMode(!editMode)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
                      editMode ? 'bg-green-600 hover:bg-green-700' : 'bg-blue-600 hover:bg-blue-700'
                    } text-white`}
                  >
                    <Edit2 className="w-4 h-4" />
                    {editMode ? 'Done Editing' : 'Edit Marks'}
                  </button>
                  {editMode && (
                    <button
                      onClick={resetToOriginal}
                      className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition"
                    >
                      <RotateCcw className="w-4 h-4" />
                      Reset
                    </button>
                  )}
                </div>
              </div>

              <div className="space-y-3 mb-6">
                {subjects.map((subject) => (
                  <div key={subject.code} className="bg-gray-800 rounded-lg p-4">
                    <div className="flex items-center gap-4">
                      <div className="flex-1">
                        <p className="font-bold text-white">{subject.name}</p>
                        <p className="text-sm text-gray-400">{subject.code}</p>
                      </div>
                      
                      {editMode ? (
                        <div className="flex items-center gap-3">
                          <input
                            type="number"
                            min="0"
                            max="100"
                            step="0.1"
                            value={subject.marks}
                            onChange={(e) => updateSubjectMarks(subject.code, parseFloat(e.target.value) || 0)}
                            className="w-24 bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                          />
                          <span className="text-gray-400">/100</span>
                        </div>
                      ) : (
                        <div className="text-right">
                          <p className="text-2xl font-bold text-white">{subject.marks.toFixed(1)}</p>
                          <p className="text-sm text-gray-400">marks</p>
                        </div>
                      )}
                      
                      <div className="text-center min-w-[60px]">
                        <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                          subject.grade === 'O' ? 'bg-purple-600 text-white' :
                          subject.grade === 'A+' ? 'bg-blue-600 text-white' :
                          subject.grade === 'A' ? 'bg-green-600 text-white' :
                          subject.grade === 'B+' ? 'bg-yellow-600 text-white' :
                          'bg-gray-700 text-white'
                        }`}>
                          {subject.grade}
                        </span>
                        <p className="text-xs text-gray-400 mt-1">{subject.grade_point}/10</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-white/80 text-sm">Current SGPA</p>
                    <p className="text-4xl font-bold text-white">{currentSGPA.toFixed(2)}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-white/80 text-sm">Total Credits</p>
                    <p className="text-2xl font-bold text-white">{subjects.reduce((sum, s) => sum + s.credits, 0)}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Multi-Semester CGPA Calculator */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-white">Multi-Semester CGPA</h2>
                <button
                  onClick={addSemester}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
                >
                  <Plus className="w-4 h-4" />
                  Add Semester
                </button>
              </div>

              <div className="space-y-4">
                {semesters.map((semester) => (
                  <div key={semester.id} className="bg-gray-800 rounded-lg p-4 flex items-center gap-4">
                    <div className="flex-shrink-0 w-24">
                      <p className="text-sm text-gray-400 mb-1">Semester</p>
                      <p className="text-lg font-bold text-white">{semester.id}</p>
                    </div>

                    <div className="flex-1">
                      <label className="block text-sm text-gray-400 mb-1">SGPA</label>
                      <input
                        type="number"
                        min="0"
                        max="10"
                        step="0.01"
                        value={semester.sgpa || ''}
                        onChange={(e) => updateSemester(semester.id, 'sgpa', parseFloat(e.target.value) || 0)}
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        placeholder="0.00"
                      />
                    </div>

                    <div className="flex-1">
                      <label className="block text-sm text-gray-400 mb-1">Credits</label>
                      <input
                        type="number"
                        min="0"
                        step="1"
                        value={semester.credits || ''}
                        onChange={(e) => updateSemester(semester.id, 'credits', parseInt(e.target.value) || 0)}
                        className="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-blue-500"
                        placeholder="0"
                      />
                    </div>

                    <button
                      onClick={() => removeSemester(semester.id)}
                      disabled={semesters.length === 1}
                      className="flex-shrink-0 p-2 text-red-400 hover:bg-red-600/10 rounded-lg transition disabled:opacity-30 disabled:cursor-not-allowed"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* Grade Scale Reference */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-xl font-bold text-white mb-4">📋 Grade Scale Reference</h2>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                {[
                  { grade: 'O', points: '10', range: '90-100' },
                  { grade: 'A+', points: '9', range: '80-89' },
                  { grade: 'A', points: '8', range: '70-79' },
                  { grade: 'B+', points: '7', range: '60-69' },
                  { grade: 'B', points: '6', range: '50-59' },
                ].map((item) => (
                  <div key={item.grade} className="bg-gray-800 rounded-lg p-3 text-center">
                    <p className="text-2xl font-bold text-blue-400">{item.grade}</p>
                    <p className="text-sm text-white mt-1">{item.points} Points</p>
                    <p className="text-xs text-gray-400 mt-1">{item.range}%</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {/* Current SGPA Card */}
            <div className="bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl p-6 shadow-xl">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-8 h-8 text-white" />
                <h2 className="text-xl font-bold text-white">Current SGPA</h2>
              </div>
              <p className="text-6xl font-bold text-white mb-2">{currentSGPA.toFixed(2)}</p>
              <p className="text-white/80">This Semester</p>
            </div>

            {/* Multi-Semester CGPA Result */}
            {totalCredits > 0 && (
              <div className="bg-gradient-to-br from-blue-600 to-purple-700 rounded-xl p-6 shadow-xl">
                <div className="flex items-center gap-3 mb-4">
                  <Calculator className="w-8 h-8 text-white" />
                  <h2 className="text-xl font-bold text-white">Overall CGPA</h2>
                </div>
                <p className="text-6xl font-bold text-white mb-2">{cgpa.toFixed(2)}</p>
                <p className="text-white/80">Across {semesters.length} Semesters</p>
              </div>
            )}

            {/* Total Credits */}
            <div className="bg-gradient-to-br from-purple-600 to-pink-700 rounded-xl p-6 shadow-xl">
              <div className="flex items-center gap-3 mb-4">
                <Award className="w-8 h-8 text-white" />
                <h2 className="text-xl font-bold text-white">Total Credits</h2>
              </div>
              <p className="text-6xl font-bold text-white mb-2">{subjects.reduce((sum, s) => sum + s.credits, 0)}</p>
              <p className="text-white/80">Current Semester</p>
            </div>

            {/* Performance Indicator */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-6 h-6 text-blue-400" />
                <h2 className="text-lg font-bold text-white">Performance</h2>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Grade</span>
                  <span className="font-bold text-white">
                    {cgpa >= 9 ? 'O (Outstanding)' :
                     cgpa >= 8 ? 'A+ (Excellent)' :
                     cgpa >= 7 ? 'A (Very Good)' :
                     cgpa >= 6 ? 'B+ (Good)' :
                     cgpa >= 5 ? 'B (Average)' : 'Below Average'}
                  </span>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-3">
                  <div
                    className={`h-3 rounded-full transition-all ${
                      cgpa >= 9 ? 'bg-gradient-to-r from-purple-500 to-pink-500' :
                      cgpa >= 8 ? 'bg-gradient-to-r from-blue-500 to-purple-500' :
                      cgpa >= 7 ? 'bg-gradient-to-r from-green-500 to-blue-500' :
                      cgpa >= 6 ? 'bg-gradient-to-r from-yellow-500 to-green-500' :
                      'bg-gradient-to-r from-red-500 to-yellow-500'
                    }`}
                    style={{ width: `${(cgpa / 10) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>

            {/* Tips */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-xl">
              <h2 className="text-lg font-bold text-white mb-4">💡 Tips</h2>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>• Enter SGPA for each semester</li>
                <li>• Add credits earned per semester</li>
                <li>• CGPA is weighted by credits</li>
                <li>• Add more semesters as needed</li>
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
