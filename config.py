# config.py
import os

# --- Neon PostgreSQL Configuration (Active) ---
NEON_PASSWORDLESS_AUTH = os.environ.get("NEON_PASSWORDLESS_AUTH", "false").lower() == "true"
NEON_DB_HOST = os.environ.get("NEON_DB_HOST", "pg.neon.tech")

# Legacy password-based auth (fallback)
NEON_DB_PASSWORD = os.environ.get("NEON_DB_PASSWORD")
NEON_DB_URI = os.environ.get("NEON_DB_URI", "ep-spring-voice-a1yre8if-pooler.ap-southeast-1.aws.neon.tech")
PG_DBNAME = os.environ.get("PG_DBNAME", "neondb")
PG_USER = os.environ.get("PG_USER", "neondb_owner")

# Build connection string based on auth method
if NEON_PASSWORDLESS_AUTH:
    NEON_CONNECTION_STRING = f"postgresql://{NEON_DB_HOST}?sslmode=require"
else:
    if NEON_DB_PASSWORD is None:
        import sys
        sys.exit("Database password not configured and passwordless auth not enabled. Exiting.")
    NEON_CONNECTION_STRING = f"postgresql://{PG_USER}:{NEON_DB_PASSWORD}@{NEON_DB_URI}/{PG_DBNAME}?sslmode=require"

# MCP Server configuration
MCP_SERVER_CONFIG = {
    "mcpServers": {
        "Neon": {
            "url": "https://mcp.neon.tech/mcp",
            "headers": {}
        }
    }
}

# --- Portal Configuration ---
LOGIN_URL = "https://crce-students.contineo.in/parents/index.php?option=com_studentdashboard&controller=studentdashboard&task=dashboard"
FORM_ACTION_URL = LOGIN_URL

# --- Form Field Names ---
PRN_FIELD_NAME = "username"
DAY_FIELD_NAME = "dd"
MONTH_FIELD_NAME = "mm"
YEAR_FIELD_NAME = "yyyy"
PASSWORD_FIELD_NAME = "passwd"

# --- Subject Code Mapping ---
SUBJECT_CODE_TO_NAME_MAP = {
    "CSC601": "SPCC (System Programming & Compiler Construction)",
    "CSC602": "CSS (Cryptography and System Security)",
    "CSC603": "MC (Mobile Computing)",
    "CSC604": "AI (Artificial Intelligence)",
    "CSL601": "SPCC Lab",
    "CSL602": "CSS Lab",
    "CSL603": "MC Lab",
    "CSL604": "AI Lab",
    "CSL605": "Skill-Based Lab",
    "CSM601": "Mini Project 2B",
    "CSDL06013": "QA (Quantitative Analysis)",
    "CSC702" : "BDA",
    "CSC701" : "ML",
    "CSDC7013" : "NLP",
    "CSDC7023" : "IR",
    "CSL701" : "ML LAB",
    "CSL702" : "BDA LAB",
    "CSDL7013" : "NLP LAB",
    "CSDL7023" : "IR LAB",
    "CSDC7022" : "Blockchain",
    "CSDL7022" : "Blockchain Lab",
    "MEC702" : "Logistics & Supply Chain Management",
    "MEC701" : "Design of Mechanical system",
    "MEL701" : "Design of Mechanical system lab",
    "MEL702" : "Maintainence Engineering",
    "MEL703" : "Industrial Skills",
    "MEDLO7032" : "Renewable Energy System",
    "MEDLO7041" : "Machinery Diagnostics",
    "ILO7017" : "Disaster Management and Mitigation Measures",
    "CSP701" : "Major Project",
    "25PCC13CE11" : "Computer Network",
    "25PCC13CE12" : "TCS",
    "25PCC13CE13" : "OS",
    "25PCC13CE14" : "DWM",
    "25PEC13CE16" : "HMI",
    "25MDM42" : "Emotional And Spiritual Intelligence",
    "25PECL13CE14" : "Innovative Product Development Lab Phase 1",
    "25OE13CE43" : "SUpply Chain Management",
    "25BSC12CE05" : "DSGT",
    "25PCC12CE05" : "COA",
    "25PCC12CE06" : "Data Structures",
    "25PCC12CE07" : "Object Oriented Programming",
    "25VEC12CE01" : "Human Values And Professional Ethics",
    "25AEC12CE021" : "Sanskrit",
    "25MDMBM1" : "Financial Accounting",
    "25OE13CE12" : "Financial Planning Taxation And Investment",
    "25MDMBM2" : "Economics For Businees"

}

# --- Credit Hours Configuration ---
# Default credit structure based on Mumbai University norms
DEFAULT_THEORY_CREDITS = 4
DEFAULT_LAB_CREDITS = 2
DEFAULT_PROJECT_CREDITS = 4
DEFAULT_SKILL_CREDITS = 1

# Subject-specific credit mappings
SUBJECT_CREDITS = {
    # Theory subjects (4 credits each)
    "CSC601": 4, "CSC602": 4, "CSC603": 4, "CSC604": 4,
    "CSC701": 4, "CSC702": 4,
    "CSDC7013": 3, "CSDC7023": 3, "CSDC7022": 3,
    
    # Lab subjects (2 credits each)
    "CSL601": 2, "CSL602": 2, "CSL603": 2, "CSL604": 2,
    "CSL701": 2, "CSL702": 2,
    "CSDL7013": 1, "CSDL7023": 1, "CSDL7022": 1,
    
    # Skill-based labs (1 credit)
    "CSL605": 1,
    
    # Projects
    "CSM601": 4,
    "CSP701": 8,
    
    # Other subjects
    "CSDL06013": 3,  # QA
    "MEC702": 3, "MEC701": 4,
    "MEL701": 1, "MEL702": 1, "MEL703": 1,
    "MEDLO7032": 3, "MEDLO7041": 3,
    "ILO7017": 2,
    
    # New semester subjects
    "25PCC13CE11": 4,  # Computer Network
    "25PCC13CE12": 4,  # TCS
    "25PCC13CE13": 4,  # OS
    "25PCC13CE14": 4,  # DWM
    "25PEC13CE16": 3,  # HMI
    "25MDM42": 2,      # Emotional And Spiritual Intelligence
    "25PECL13CE14": 2, # Innovative Product Development Lab Phase 1
    "25OE13CE43": 3,   # Supply Chain Management
    "25BSC12CE05": 4,  # DSGT
    "25PCC12CE05": 4,  # COA
    "25PCC12CE06": 4,  # Data Structures
    "25PCC12CE07": 4,  # OOP
    "25VEC12CE01": 2,  # Human Values
    "25AEC12CE021": 1, # Sanskrit
    "25MDMBM1": 2,     # Financial Accounting
    "25OE13CE12": 3,   # Financial Planning
    "25MDMBM2": 2,     # Economics
}

def get_default_credits_by_type(subject_code):
    """
    Get default credits based on subject code pattern if not in SUBJECT_CREDITS map.
    """
    if subject_code.startswith("CSL") or subject_code.startswith("CSDL") or \
       subject_code.startswith("MEL") or subject_code.startswith("25PECL"):
        return DEFAULT_LAB_CREDITS
    elif subject_code.startswith("CSM") or subject_code.startswith("CSP"):
        return DEFAULT_PROJECT_CREDITS
    elif "SKILL" in subject_code.upper():
        return DEFAULT_SKILL_CREDITS
    else:
        return DEFAULT_THEORY_CREDITS