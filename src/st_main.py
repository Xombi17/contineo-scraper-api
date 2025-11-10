import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_local_storage import LocalStorage
from datetime import datetime
import pytz
import plotly.graph_objects as go
import plotly.express as px

load_dotenv()

# Local Storage Setup
try:
    _localS = LocalStorage()
except Exception:
    class MockLocalStorage:
        def getItem(self, key): return None
        def setItem(self, key, value): pass
    _localS = MockLocalStorage()

import web_scraper
import config
import db_utils_dual as db_utils
import cgpa_calculator

def get_item(key):
    return _localS.getItem(key)

def set_item(key, value):
    _localS.setItem(key, value)

@st.cache_data(ttl=3600)
def get_processed_student_data(prn, dob_day, dob_month, dob_year, full_name):
    session, html = web_scraper.login_and_get_welcome_page(prn, dob_day, dob_month, dob_year, full_name)
    if not html:
        return None
    attendance_records = web_scraper.extract_attendance_from_welcome_page(html)
    cie_marks_records = web_scraper.extract_cie_marks(html)
    return {
        "data": {"attendance": attendance_records, "cie_marks": cie_marks_records},
        "scraped_at": datetime.now(pytz.utc)
    }

# Initialize DB
if 'db_initialized' not in st.session_state:
    db_utils.create_db_and_table_pg()
    st.session_state.db_initialized = True

# Page Configuration
st.set_page_config(
    page_title="Student Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Mode
st.markdown("""
<style>
    /* Dark theme improvements */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border-left: 4px solid #6366f1;
    }
    
    /* Attendance cards */
    .attendance-excellent {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    .attendance-good {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
    }
    
    .attendance-low {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Improve tab styling for dark mode */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #334155;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        color: #94a3b8;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Session State
if 'first_name' not in st.session_state:
    st.session_state.first_name = get_item(key="last_username") or ""
if 'show_add_user_form' not in st.session_state:
    st.session_state.show_add_user_form = False
if 'student_data_result' not in st.session_state:
    st.session_state.student_data_result = None

# Sidebar
with st.sidebar:
    st.markdown("### 🎓 Student Portal")
    st.markdown("---")
    
    first_name_input = st.text_input(
        "👤 Username",
        value=st.session_state.first_name,
        placeholder="Enter your username",
        key="first_name_key"
    ).strip()
    
    if first_name_input != st.session_state.first_name:
        st.session_state.student_data_result = None
    st.session_state.first_name = first_name_input
    
    if st.session_state.first_name:
        st.success(f"Welcome, **{st.session_state.first_name}**!")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        fetch_button = st.button("🔍 Fetch", type="primary", use_container_width=True)
    with col2:
        force_refresh_button = st.button("🔄 Refresh", use_container_width=True)
    
    st.markdown("---")
    
    if st.button("➕ Register New Student", use_container_width=True):
        st.session_state.show_add_user_form = not st.session_state.show_add_user_form
    
    if st.session_state.show_add_user_form:
        with st.expander("📝 Registration Form", expanded=True):
            with st.form("new_user_form"):
                new_first_name = st.text_input("Username:", key="add_first_name").strip()
                new_full_name = st.text_input("Full Name:", key="add_full_name").strip()
                new_prn = st.text_input("PRN:", key="add_prn").strip()
                
                col_dob1, col_dob2, col_dob3 = st.columns(3)
                with col_dob1:
                    new_dob_day = st.text_input("Day:", key="add_dob_day", placeholder="01").strip()
                with col_dob2:
                    new_dob_month = st.text_input("Month:", key="add_dob_month", placeholder="01").strip()
                with col_dob3:
                    new_dob_year = st.text_input("Year:", key="add_dob_year", placeholder="2005").strip()
                
                submitted_add_user = st.form_submit_button("💾 Register", use_container_width=True)
                
                if submitted_add_user:
                    if not all([new_first_name, new_full_name, new_prn, new_dob_day, new_dob_month, new_dob_year]):
                        st.error("All fields required!")
                    else:
                        with st.spinner("Validating..."):
                            _, validation_html = web_scraper.login_and_get_welcome_page(
                                new_prn, new_dob_day, new_dob_month, new_dob_year, new_full_name
                            )
                        
                        if validation_html:
                            if db_utils.add_user_to_db_pg(new_first_name, new_full_name, new_prn, 
                                                          new_dob_day, new_dob_month, new_dob_year):
                                st.success(f"✅ Registered successfully!")
                                st.session_state.show_add_user_form = False
                                st.rerun()
                            else:
                                st.error("Username/PRN already exists!")
                        else:
                            st.error("Invalid credentials!")

# Main Content - Header
st.markdown("""
<div class="main-header">
    <h1>🎓 Student Academic Portal</h1>
    <p>Track your attendance, marks, and academic performance</p>
</div>
""", unsafe_allow_html=True)

# Data Fetch Logic
should_fetch = False
if first_name_input and not st.session_state.student_data_result:
    should_fetch = True
if fetch_button:
    should_fetch = True
if force_refresh_button:
    st.cache_data.clear()
    st.toast("🔄 Fetching fresh data...", icon="✨")
    st.session_state.student_data_result = None
    should_fetch = True

if should_fetch and first_name_input:
    set_item(key="last_username", value=first_name_input)
    with st.spinner(f"Loading data for {first_name_input}..."):
        user_details = db_utils.get_user_from_db_pg(first_name_input)
        if user_details:
            result = get_processed_student_data(
                user_details["prn"], user_details["dob_day"],
                user_details["dob_month"], user_details["dob_year"],
                user_details["full_name"]
            )
            st.session_state.student_data_result = {
                "user_details": user_details,
                "scraped_data": result
            }
            st.session_state.db_updated_at = None
        else:
            st.error(f"❌ User '{first_name_input}' not found!")
            st.session_state.student_data_result = None

# Display Data
if st.session_state.student_data_result:
    user_details = st.session_state.student_data_result["user_details"]
    result = st.session_state.student_data_result["scraped_data"]
    
    current_user_id = user_details["id"]
    current_full_name = user_details["full_name"]
    current_prn = user_details["prn"]
    
    if result:
        scraped_time_utc = result["scraped_at"]
        
        if 'db_updated_at' not in st.session_state or st.session_state.db_updated_at != scraped_time_utc:
            if result["data"]["cie_marks"]:
                if db_utils.update_student_marks_in_db_pg(current_user_id, result["data"]["cie_marks"], scraped_time_utc):
                    st.toast("🏆 Leaderboard updated!", icon="✨")
                    st.session_state.db_updated_at = scraped_time_utc
        
        # User Info
        col_info1, col_info2, col_info3 = st.columns([2, 1, 1])
        with col_info1:
            st.markdown(f"### 👤 {current_full_name}")
        with col_info2:
            st.markdown(f"**PRN:** {current_prn}")
        with col_info3:
            local_tz = pytz.timezone('Asia/Kolkata')
            scraped_time_local = scraped_time_utc.astimezone(local_tz)
            st.caption(f"🕐 {scraped_time_local.strftime('%I:%M %p')}")
        
        st.markdown("---")
        
        attendance_records = result["data"]["attendance"]
        cie_marks_records = result["data"]["cie_marks"]
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📝 Marks & Leaderboard", "🎯 CGPA Calculator", "📈 Analytics"])
        
        with tab1:
            # Quick Stats
            if cie_marks_records:
                sgpa_result = cgpa_calculator.calculate_sgpa(cie_marks_records)
                
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.markdown("""
                    <div class="metric-card">
                        <h3 style="color: #6366f1; margin: 0;">📚 SGPA</h3>
                        <h1 style="margin: 0.5rem 0; color: white;">{:.2f}</h1>
                        <p style="color: #94a3b8; margin: 0;">Current Semester</p>
                    </div>
                    """.format(sgpa_result['sgpa']), unsafe_allow_html=True)
                
                with col_stat2:
                    st.markdown("""
                    <div class="metric-card">
                        <h3 style="color: #8b5cf6; margin: 0;">🎓 Credits</h3>
                        <h1 style="margin: 0.5rem 0; color: white;">{}</h1>
                        <p style="color: #94a3b8; margin: 0;">Total Earned</p>
                    </div>
                    """.format(sgpa_result['total_credits']), unsafe_allow_html=True)
                
                with col_stat3:
                    avg_attendance = sum(r['percentage'] for r in attendance_records) / len(attendance_records) if attendance_records else 0
                    st.markdown("""
                    <div class="metric-card">
                        <h3 style="color: #10b981; margin: 0;">✅ Attendance</h3>
                        <h1 style="margin: 0.5rem 0; color: white;">{:.1f}%</h1>
                        <p style="color: #94a3b8; margin: 0;">Average</p>
                    </div>
                    """.format(avg_attendance), unsafe_allow_html=True)
                
                with col_stat4:
                    st.markdown("""
                    <div class="metric-card">
                        <h3 style="color: #f59e0b; margin: 0;">📖 Subjects</h3>
                        <h1 style="margin: 0.5rem 0; color: white;">{}</h1>
                        <p style="color: #94a3b8; margin: 0;">This Semester</p>
                    </div>
                    """.format(len(sgpa_result['subjects'])), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Attendance Section
            st.markdown("### 📊 Attendance Overview")
            
            if attendance_records:
                attendance_data = []
                for record in attendance_records:
                    subject_code = record['subject'].strip()
                    if subject_code == "CSM601":
                        continue
                    subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
                    attendance_data.append({
                        'subject': subject_name,
                        'code': subject_code,
                        'percentage': record['percentage']
                    })
                
                # Display as cards
                cols = st.columns(3)
                for idx, att in enumerate(attendance_data):
                    with cols[idx % 3]:
                        status_class = "attendance-excellent" if att['percentage'] >= 85 else \
                                     "attendance-good" if att['percentage'] >= 75 else "attendance-low"
                        status_text = "Excellent" if att['percentage'] >= 85 else \
                                    "Good" if att['percentage'] >= 75 else "Low"
                        
                        st.markdown(f"""
                        <div class="{status_class}">
                            <h4 style="margin: 0; color: white;">{att['subject']}</h4>
                            <p style="margin: 0.25rem 0; color: rgba(255,255,255,0.8); font-size: 0.875rem;">{att['code']}</p>
                            <h1 style="margin: 0.5rem 0; color: white; font-size: 3rem;">{att['percentage']}%</h1>
                            <p style="margin: 0; color: rgba(255,255,255,0.9); font-weight: 600;">{status_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Attendance Chart
                if len(attendance_data) > 0:
                    fig = go.Figure(data=[
                        go.Bar(
                            x=[a['subject'] for a in attendance_data],
                            y=[a['percentage'] for a in attendance_data],
                            marker_color=['#10b981' if a['percentage'] >= 85 else '#f59e0b' if a['percentage'] >= 75 else '#ef4444' 
                                        for a in attendance_data],
                            text=[f"{a['percentage']}%" for a in attendance_data],
                            textposition='outside'
                        )
                    ])
                    fig.update_layout(
                        title="Attendance by Subject",
                        xaxis_title="Subject",
                        yaxis_title="Percentage",
                        yaxis_range=[0, 110],
                        height=400,
                        showlegend=False,
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ No attendance data available")

        
        with tab2:
            st.markdown("### 📝 CIE Marks & Leaderboards")
            
            if cie_marks_records:
                for subject_code, marks_dict in cie_marks_records.items():
                    subject_name = config.SUBJECT_CODE_TO_NAME_MAP.get(subject_code, subject_code)
                    
                    with st.expander(f"📖 {subject_name} ({subject_code})", expanded=False):
                        col_marks1, col_marks2 = st.columns([1, 1])
                        
                        with col_marks1:
                            st.markdown("#### Your Marks")
                            exam_types_to_show = []
                            if subject_code.startswith("CSC") or subject_code.startswith("CSDC"):
                                exam_types_to_show = ["MSE", "TH-ISE1", "TH-ISE2", "ESE"]
                            elif subject_code.startswith("CSL") or subject_code.startswith("CSDL"):
                                exam_types_to_show = ["PR-ISE1", "PR-ISE2"]
                            
                            subject_total = 0.0
                            has_valid_marks = False
                            marks_display = []
                            
                            for exam_type in ["MSE", "TH-ISE1", "TH-ISE2", "ESE", "PR-ISE1", "PR-ISE2"]:
                                if exam_type in marks_dict and (not exam_types_to_show or exam_type in exam_types_to_show):
                                    mark = marks_dict[exam_type]
                                    marks_display.append({"Exam": exam_type, "Marks": mark if mark is not None else "N/A"})
                                    if isinstance(mark, (int, float)):
                                        subject_total += mark
                                        has_valid_marks = True
                            
                            if marks_display:
                                st.dataframe(marks_display, use_container_width=True, hide_index=True)
                                if has_valid_marks:
                                    st.metric("Total Marks", f"{subject_total:.2f}")
                        
                        with col_marks2:
                            st.markdown("#### 🏆 Leaderboard")
                            if st.button(f"Show Rankings", key=f"lb_{subject_code}"):
                                exam_types_for_lb = [e for e, m in marks_dict.items() if isinstance(m, (int, float))]
                                
                                for exam_type in exam_types_for_lb:
                                    leaderboard = db_utils.get_subject_leaderboard_pg(subject_code, exam_type)
                                    if leaderboard:
                                        st.markdown(f"**{exam_type}**")
                                        medals = ["🥇", "🥈", "🥉"]
                                        for i, (name, score) in enumerate(leaderboard):
                                            medal = medals[i] if i < len(medals) else "•"
                                            highlight = "**" if name == current_full_name else ""
                                            st.caption(f"{medal} {highlight}{name}: {score:.2f}{highlight}")
            else:
                st.warning("⚠️ No marks data available")
        
        with tab3:
            st.markdown("### 🎯 CGPA/SGPA Calculator")
            
            calc_subtab1, calc_subtab2, calc_subtab3 = st.tabs(["📊 Current SGPA", "🎓 CGPA Tracker", "🎯 Target Calculator"])
            
            with calc_subtab1:
                if cie_marks_records:
                    sgpa_result = cgpa_calculator.calculate_sgpa(cie_marks_records)
                    
                    col_sgpa1, col_sgpa2, col_sgpa3 = st.columns(3)
                    with col_sgpa1:
                        st.metric("Current SGPA", f"{sgpa_result['sgpa']:.2f}")
                    with col_sgpa2:
                        st.metric("Total Credits", sgpa_result['total_credits'])
                    with col_sgpa3:
                        performance = cgpa_calculator.get_grade_summary_text(sgpa_result['sgpa'])
                        st.metric("Performance", performance)
                    
                    if sgpa_result['grade_distribution']:
                        st.markdown("#### Grade Distribution")
                        grades = list(sgpa_result['grade_distribution'].keys())
                        counts = list(sgpa_result['grade_distribution'].values())
                        
                        fig = go.Figure(data=[
                            go.Pie(labels=grades, values=counts, hole=0.4,
                                  marker_colors=['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
                        ])
                        fig.update_layout(height=300, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander("📋 Subject-wise Details"):
                        for subject in sgpa_result['subjects']:
                            col_sub1, col_sub2, col_sub3, col_sub4 = st.columns(4)
                            col_sub1.caption(f"**{subject['name']}**")
                            col_sub2.caption(f"Marks: {subject['marks']:.1f}/{subject['max_marks']:.0f}")
                            col_sub3.caption(f"Grade: {subject['grade']}")
                            col_sub4.caption(f"GP: {subject['grade_point']}")
                    
                    st.markdown("---")
                    st.markdown("#### 💾 Save Semester Record")
                    with st.form("save_sem"):
                        col_save1, col_save2 = st.columns(2)
                        with col_save1:
                            sem_num = st.number_input("Semester", min_value=1, max_value=8, value=7)
                        with col_save2:
                            acad_year = st.text_input("Academic Year", value="2024-25")
                        
                        if st.form_submit_button("💾 Save", use_container_width=True):
                            if db_utils.save_semester_record_pg(
                                current_user_id, sem_num, f"Semester {sem_num}",
                                sgpa_result['sgpa'], sgpa_result['total_credits'], acad_year
                            ):
                                st.success(f"✅ Saved Semester {sem_num}!")
                                st.rerun()
                else:
                    st.info("No marks data available")
            
            with calc_subtab2:
                semester_records = db_utils.get_user_semester_records_pg(current_user_id)
                
                if semester_records:
                    semester_data = []
                    for sem in semester_records:
                        if sem['sgpa'] is not None:
                            semester_data.append({
                                'sgpa': sem['sgpa'],
                                'total_credits': sem['total_credits'],
                                'total_grade_points': sem['sgpa'] * sem['total_credits']
                            })
                    
                    if semester_data:
                        cgpa_result = cgpa_calculator.calculate_cgpa(semester_data)
                        
                        col_cgpa1, col_cgpa2, col_cgpa3 = st.columns(3)
                        with col_cgpa1:
                            st.metric("Overall CGPA", f"{cgpa_result['cgpa']:.2f}")
                        with col_cgpa2:
                            st.metric("Total Credits", cgpa_result['total_credits'])
                        with col_cgpa3:
                            performance = cgpa_calculator.get_grade_summary_text(cgpa_result['cgpa'])
                            st.metric("Performance", performance)
                        
                        sem_nums = [sem['semester_number'] for sem in semester_records]
                        sem_sgpas = [sem['sgpa'] for sem in semester_records if sem['sgpa']]
                        
                        if len(sem_sgpas) > 0:
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=sem_nums[:len(sem_sgpas)],
                                y=sem_sgpas,
                                mode='lines+markers',
                                name='SGPA',
                                line=dict(color='#6366f1', width=3),
                                marker=dict(size=10)
                            ))
                            fig.update_layout(
                                title="SGPA Progression",
                                xaxis_title="Semester",
                                yaxis_title="SGPA",
                                height=400,
                                template="plotly_dark",
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        st.markdown("#### Semester Records")
                        sem_table = []
                        for sem in semester_records:
                            sem_table.append({
                                "Semester": f"Sem {sem['semester_number']}",
                                "Year": sem['academic_year'] or "N/A",
                                "SGPA": f"{sem['sgpa']:.2f}" if sem['sgpa'] else "N/A",
                                "Credits": sem['total_credits']
                            })
                        st.dataframe(sem_table, use_container_width=True, hide_index=True)
                else:
                    st.info("No semester records. Save your current semester first!")
            
            with calc_subtab3:
                st.markdown("#### Calculate Required Marks for Target SGPA")
                
                if cie_marks_records:
                    target_sgpa = st.slider("Target SGPA", 0.0, 10.0, 8.5, 0.1)
                    
                    if st.button("🔍 Calculate", type="primary"):
                        target_analysis = cgpa_calculator.calculate_required_marks_for_target(
                            cie_marks_records, target_sgpa
                        )
                        
                        if target_analysis['is_achievable']:
                            st.success(f"✅ {target_analysis['message']}")
                        else:
                            st.warning(f"⚠️ {target_analysis['message']}")
                        
                        col_t1, col_t2, col_t3 = st.columns(3)
                        with col_t1:
                            st.metric("Current SGPA", f"{target_analysis['current_sgpa']:.2f}")
                        with col_t2:
                            st.metric("Target SGPA", f"{target_analysis['target_sgpa']:.2f}")
                        with col_t3:
                            gap = target_analysis['target_sgpa'] - target_analysis['current_sgpa']
                            st.metric("Gap", f"{gap:+.2f}")
                        
                        if target_analysis['recommendations']:
                            st.markdown("#### 📝 What You Need")
                            st.info(f"Average GP needed: **{target_analysis['avg_grade_point_needed']:.2f}**/10")
                            
                            for rec in target_analysis['recommendations']:
                                with st.expander(f"📖 {rec['subject']}", expanded=True):
                                    col_r1, col_r2 = st.columns(2)
                                    with col_r1:
                                        st.caption(f"**Grade Point:** {rec['grade_point_needed']:.2f}/10")
                                        st.caption(f"**Target Grade:** {rec['grade_needed']}")
                                    with col_r2:
                                        st.caption(f"**Min Marks:** {rec['minimum_marks_needed']}/100")
                                        st.caption(f"**Credits:** {rec['credits']}")
                else:
                    st.info("No marks data available")

        
        with tab4:
            st.markdown("### 📈 Performance Analytics")
            
            if cie_marks_records and attendance_records:
                sgpa_result = cgpa_calculator.calculate_sgpa(cie_marks_records)
                
                st.markdown("#### Subject Performance Comparison")
                
                subject_perf = []
                for subject in sgpa_result['subjects']:
                    att_record = next((a for a in attendance_records if a['subject'] == subject['code']), None)
                    att_pct = att_record['percentage'] if att_record else 0
                    
                    subject_perf.append({
                        'subject': subject['name'],
                        'marks_pct': subject['percentage'],
                        'attendance': att_pct,
                        'grade_point': subject['grade_point']
                    })
                
                if subject_perf:
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Marks %',
                        x=[s['subject'] for s in subject_perf],
                        y=[s['marks_pct'] for s in subject_perf],
                        marker_color='#6366f1'
                    ))
                    fig.add_trace(go.Bar(
                        name='Attendance %',
                        x=[s['subject'] for s in subject_perf],
                        y=[s['attendance'] for s in subject_perf],
                        marker_color='#10b981'
                    ))
                    fig.update_layout(
                        title="Marks vs Attendance",
                        barmode='group',
                        height=400,
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=[s['grade_point'] for s in subject_perf],
                        theta=[s['subject'] for s in subject_perf],
                        fill='toself',
                        marker_color='#8b5cf6'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                        title="Grade Point Distribution",
                        height=500,
                        template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("#### 💡 Insights")
                    col_ins1, col_ins2 = st.columns(2)
                    
                    with col_ins1:
                        best_subject = max(subject_perf, key=lambda x: x['marks_pct'])
                        st.success(f"🌟 **Best Performance:** {best_subject['subject']} ({best_subject['marks_pct']:.1f}%)")
                    
                    with col_ins2:
                        worst_subject = min(subject_perf, key=lambda x: x['marks_pct'])
                        st.warning(f"⚠️ **Needs Attention:** {worst_subject['subject']} ({worst_subject['marks_pct']:.1f}%)")
            else:
                st.info("Complete data not available for analytics")
    
    else:
        st.error("❌ Failed to fetch data from portal")

elif (fetch_button or force_refresh_button) and not first_name_input:
    st.warning("⚠️ Please enter a username")
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h2 style="color: #e2e8f0;">👋 Welcome to Student Portal</h2>
        <p style="font-size: 1.2rem; color: #94a3b8;">Enter your username in the sidebar to get started</p>
    </div>
    """, unsafe_allow_html=True)
