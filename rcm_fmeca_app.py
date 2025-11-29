"""
FMECA and RCM Analysis Application
Reliability Centered Maintenance for Infrastructure Assets

Based on Murrumbidgee Irrigation RCM Course Materials
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import io
import configparser
import os

# Load configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

# Get configuration values
APP_NAME = config.get('Application', 'name', fallback='FMECA & RCM Analysis Tool')
APP_VERSION = config.get('Application', 'version', fallback='1.0.0')
REGISTRATION_DATE = config.get('Application', 'registration_date', fallback='2025-10-20')
AUTHORITY_NAME = config.get('Organization', 'authority_name', fallback='Organization')
DEPARTMENT = config.get('Organization', 'department', fallback='Asset Management')
CONTACT_EMAIL = config.get('Organization', 'contact_email', fallback='')

# Page configuration
st.set_page_config(
    page_title="FMECA & RCM Analysis Tool",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stage-header {
        background-color: #2196F3;
        color: white;
        padding: 8px;
        border-radius: 5px;
        margin: 10px 0;
        height: 40px;
        display: flex;
        align-items: center;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-left: 5px solid #4caf50;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 15px;
        border-left: 5px solid #ff9800;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Tab styling for attractive light blue selected tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: 500;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 35px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0px 0px;
        border: 1px solid #e9ecef;
        color: #495057;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #e3f2fd !important;
        border-color: #90caf9 !important;
        color: #1565c0 !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f0f8ff;
        color: #1976d2;
    }
    
    /* Green buttons */
    .stButton > button {
        background-color: #2E7D32 !important;
        color: white !important;
        border: 1px solid #2E7D32 !important;
    }
    
    .stButton > button:hover {
        background-color: #1B5E20 !important;
        border-color: #1B5E20 !important;
    }
    
    /* Red delete buttons - higher specificity to override green */
    div[data-testid="column"] > div > div > div > .stButton > button,
    [data-testid="column"]:nth-child(2) .stButton > button {
        background-color: #C62828 !important;
        border-color: #C62828 !important;
        color: white !important;
    }
    
    div[data-testid="column"] > div > div > div > .stButton > button:hover,
    [data-testid="column"]:nth-child(2) .stButton > button:hover {
        background-color: #B71C1C !important;
        border-color: #B71C1C !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = 1
    
    if 'asset_data' not in st.session_state:
        st.session_state.asset_data = {
            'asset_name': '',
            'asset_class': '',
            'asset_type': '',
            'site_location': ''
        }
    
    if 'operating_context' not in st.session_state:
        st.session_state.operating_context = {}
    
    if 'functions' not in st.session_state:
        st.session_state.functions = []
    
    if 'functional_failures' not in st.session_state:
        st.session_state.functional_failures = []
    
    if 'failure_modes' not in st.session_state:
        st.session_state.failure_modes = []
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = []
    
    if 'render_stages' not in st.session_state:
        st.session_state.render_stages = True
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'rcm_navigation'

initialize_session_state()

# Import/Export Helper Functions
def create_export_data():
    """Create export data structure from session state"""
    if not st.session_state.asset_data.get('asset_name'):
        return None
    
    export_data = {
        "application_info": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "authority": AUTHORITY_NAME,
            "department": DEPARTMENT
        },
        "asset_information": st.session_state.asset_data,
        "operating_context": st.session_state.operating_context,
        "components": st.session_state.get('components', []),
        "functions": st.session_state.functions,
        "functional_failures": st.session_state.functional_failures,
        "failure_modes": st.session_state.failure_modes,
        "analysis_results": st.session_state.analysis_results,
        "export_date": datetime.now().isoformat()
    }
    return export_data

def load_import_data(import_data):
    """Load imported data into session state"""
    try:
        # Load asset information
        if "asset_information" in import_data:
            st.session_state.asset_data = import_data["asset_information"]
        
        # Load operating context
        if "operating_context" in import_data:
            st.session_state.operating_context = import_data["operating_context"]
        
        # Load components
        if "components" in import_data:
            st.session_state.components = import_data["components"]
        
        # Load functions
        if "functions" in import_data:
            st.session_state.functions = import_data["functions"]
        
        # Load functional failures
        if "functional_failures" in import_data:
            st.session_state.functional_failures = import_data["functional_failures"]
        
        # Load failure modes
        if "failure_modes" in import_data:
            st.session_state.failure_modes = import_data["failure_modes"]
        
        # Load analysis results
        if "analysis_results" in import_data:
            st.session_state.analysis_results = import_data["analysis_results"]
        
        return True
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return False

# Autosave/Restore Functions
def get_autosave_path():
    """Get the path for the autosave file"""
    return os.path.join(os.path.dirname(__file__), '.autosave.json')

def autosave_session_data():
    """Automatically save session state to a local file"""
    try:
        autosave_path = get_autosave_path()
        
        # Only save if there's meaningful data (asset name is set)
        if not st.session_state.asset_data.get('asset_name'):
            return
        
        save_data = {
            "application_info": {
                "name": APP_NAME,
                "version": APP_VERSION,
                "authority": AUTHORITY_NAME,
                "department": DEPARTMENT
            },
            "asset_information": st.session_state.asset_data,
            "operating_context": st.session_state.operating_context,
            "components": st.session_state.get('components', []),
            "functions": st.session_state.functions,
            "functional_failures": st.session_state.functional_failures,
            "failure_modes": st.session_state.failure_modes,
            "analysis_results": st.session_state.analysis_results,
            "current_stage": st.session_state.current_stage,
            "autosave_date": datetime.now().isoformat()
        }
        
        with open(autosave_path, 'w') as f:
            json.dump(save_data, f, indent=2)
        
    except Exception as e:
        # Silently fail - don't interrupt user workflow
        print(f"Autosave error: {str(e)}")

def restore_session_data():
    """Restore session state from autosave file if it exists"""
    try:
        autosave_path = get_autosave_path()
        
        # Check if autosave file exists
        if not os.path.exists(autosave_path):
            return False
        
        # Only restore if current session is empty (asset name not set)
        if st.session_state.asset_data.get('asset_name'):
            return False
        
        with open(autosave_path, 'r') as f:
            saved_data = json.load(f)
        
        # Load the saved data
        if "asset_information" in saved_data:
            st.session_state.asset_data = saved_data["asset_information"]
        
        if "operating_context" in saved_data:
            st.session_state.operating_context = saved_data["operating_context"]
        
        if "components" in saved_data:
            st.session_state.components = saved_data["components"]
        
        if "functions" in saved_data:
            st.session_state.functions = saved_data["functions"]
        
        if "functional_failures" in saved_data:
            st.session_state.functional_failures = saved_data["functional_failures"]
        
        if "failure_modes" in saved_data:
            st.session_state.failure_modes = saved_data["failure_modes"]
        
        if "analysis_results" in saved_data:
            st.session_state.analysis_results = saved_data["analysis_results"]
        
        if "current_stage" in saved_data:
            st.session_state.current_stage = saved_data["current_stage"]
        
        return True
        
    except Exception as e:
        print(f"Restore error: {str(e)}")
        return False

def clear_autosave():
    """Clear the autosave file"""
    try:
        autosave_path = get_autosave_path()
        if os.path.exists(autosave_path):
            os.remove(autosave_path)
    except Exception as e:
        print(f"Clear autosave error: {str(e)}")

# Sidebar Navigation
def sidebar_navigation():
    """Create sidebar navigation"""
    st.sidebar.markdown("## 🔧 RCM Navigation")
    
    stages = {
        1: "📋 Stage 1: Planning & Preparation",
        2: "🔍 Stage 2: RCM Analysis (FMECA)",
        3: "⚙️ Stage 3: Implementation",
        4: "📊 Stage 4: Reports & Export"
    }
    
    for stage_num, stage_name in stages.items():
        if st.sidebar.button(stage_name, key=f"nav_{stage_num}", use_container_width=True):
            st.session_state.current_stage = stage_num
            st.session_state.current_view = 'rcm_navigation'
            st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 Information")
    
    if st.sidebar.button("ℹ️ About FMECA & RCM", key="nav_about", use_container_width=True):
        st.session_state.current_view = 'about'
        st.rerun()
    
    if st.sidebar.button("❓ FAQ", key="nav_faq", use_container_width=True):
        st.session_state.current_view = 'faq'
        st.rerun()
    
    if st.sidebar.button("🚀 Future Development", key="nav_future", use_container_width=True):
        st.session_state.current_view = 'future'
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Quick Reference")
    
    with st.sidebar.expander("7 RCM Questions"):
        st.markdown("""
        1. What are the functions?
        2. In what ways can it fail?
        3. What causes each failure?
        4. What happens when it fails?
        5. In what way does failure matter?
        6. What can prevent/predict failure?
        7. What if no preventive task?
        """)
    
    with st.sidebar.expander("Consequence Categories"):
        st.markdown("""
        - **Hidden (Safety/Environmental)**
        - **Hidden (Operational)**
        - **Hidden (Non-operational)**
        - **Evident (Safety/Environmental)**
        - **Evident (Operational)**
        - **Evident (Non-operational)**
        """)
    
    with st.sidebar.expander("Task Types"):
        st.markdown("""
        - **CBM**: Condition Based Maintenance
        - **FTM**: Fixed Time Maintenance
        - **FF**: Failure Finding
        - **Redesign**: One-off change
        - **OTF**: Operate to Failure
        """)
    
    # Import/Export Section
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📁 Data Management")
    
    # Export functionality
    if st.sidebar.button("📤 Export Analysis", use_container_width=True):
        export_data = create_export_data()
        if export_data:
            json_str = json.dumps(export_data, indent=2)
            st.sidebar.download_button(
                label="💾 Download JSON",
                data=json_str,
                file_name=f"rcm_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
            st.sidebar.success("✅ Export ready!")
        else:
            st.sidebar.warning("⚠️ No data to export. Complete at least Stage 1.")
    
    # Import functionality
    uploaded_file = st.sidebar.file_uploader(
        "📥 Import Analysis",
        type=['json'],
        help="Upload a previously exported RCM analysis JSON file"
    )
    
    if uploaded_file is not None:
        try:
            import_data = json.load(uploaded_file)
            if st.sidebar.button("🔄 Load Data", use_container_width=True):
                load_import_data(import_data)
                autosave_session_data()
                st.sidebar.success("✅ Data imported successfully!")
                st.rerun()
        except json.JSONDecodeError:
            st.sidebar.error("❌ Invalid JSON file format")
        except Exception as e:
            st.sidebar.error(f"❌ Error loading file: {str(e)}")
    
    # Autosave Management
    if st.sidebar.button("🗑️ Clear Autosave", use_container_width=True, help="Clear automatically saved session data"):
        clear_autosave()
        st.sidebar.success("✅ Autosave cleared!")
    
    # Application Information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Application Info")
    with st.sidebar.expander("Details"):
        st.markdown(f"**Authority:** {AUTHORITY_NAME}")
        st.markdown(f"**Department:** {DEPARTMENT}")
        st.markdown(f"**Version:** {APP_VERSION}")
        st.markdown(f"**Registration Date:** {REGISTRATION_DATE}")
        if CONTACT_EMAIL:
            st.markdown(f"**Contact:** {CONTACT_EMAIL}")

sidebar_navigation()

# Periodic autosave on every page render (as a safety net)
# This ensures data is saved even if a save button was missed
if st.session_state.asset_data.get('asset_name'):
    autosave_session_data()

# Main content area
st.markdown("# 🔧 FMECA & RCM Analysis Tool")
st.markdown("""This tool provides a systematic approach to Failure Mode, Effects and Criticality Analysis (FMECA) 
and Reliability Centered Maintenance (RCM) for infrastructure assets. Identify failure modes, assess criticality, 
and develop optimal maintenance strategies.""")
st.markdown("")
st.markdown(f"""**Developed by:** Odysseus-imc Pty Ltd  
**Technical expertise by:** Cambia Consulting Pty Ltd  
**Registered to:** {AUTHORITY_NAME}  
**Version:** {APP_VERSION}""")
st.markdown("---")

# Conditional content based on current view
if st.session_state.current_view == 'rcm_navigation':
    # RCM Navigation content
    st.markdown("### Welcome to RCM Navigation")
    st.markdown("""
    Use the **sidebar** to navigate between different stages of the RCM analysis:
    
    - **Stage 1**: Planning and Preparation
    - **Stage 2**: RCM Analysis (FMECA)
    - **Stage 3**: Implementation Planning
    - **Stage 4**: Reports and Export
    
    Select a stage from the sidebar to begin your analysis.
    """)
    
    # Mark that we should render stage content
    st.session_state.render_stages = True

elif st.session_state.current_view == 'about':
    # About FMECA & RCM page
    st.markdown("### About FMECA & RCM")
    st.markdown("""
    **Failure Mode, Effects and Criticality Analysis (FMECA)** is a systematic method for identifying 
    potential failure modes within a system, determining their effects on system performance, and 
    prioritizing them according to their criticality.
    
    **Reliability Centered Maintenance (RCM)** is a structured framework for analyzing system functions, 
    identifying failure modes, and determining the most effective maintenance strategies to preserve 
    system functions at the lowest overall cost.
    
    #### Key Benefits:
    - **Proactive Maintenance**: Identify and prevent failures before they occur
    - **Cost Optimization**: Focus resources on critical failure modes
    - **Safety Enhancement**: Systematically address safety and environmental risks
    - **Asset Performance**: Maintain system reliability and availability
    - **Regulatory Compliance**: Document risk management processes
    
    #### The RCM Process:
    1. **Define** operating context and system boundaries
    2. **Identify** system functions and performance standards
    3. **Determine** functional failures and failure modes
    4. **Analyze** failure effects and consequences
    5. **Assess** failure criticality and risk
    6. **Select** appropriate maintenance tasks
    7. **Implement** and monitor the maintenance program
    """)

elif st.session_state.current_view == 'faq':
    # FAQ page
    st.markdown("### Frequently Asked Questions")
    st.markdown("")
    
    with st.expander("What is the difference between FMECA and RCM?"):
        st.markdown("""
        FMECA is a specific analysis technique that focuses on identifying and prioritizing failure modes. 
        RCM is a broader maintenance strategy framework that incorporates FMECA as one of its key tools.
        """)
    
    with st.expander("How long does an RCM analysis take?"):
        st.markdown("""
        The duration depends on system complexity. A simple system may take days, while complex assets 
        can require weeks or months. This tool helps streamline the process.
        """)
    
    with st.expander("Who should be involved in the RCM analysis?"):
        st.markdown("""
        A cross-functional team including operators, maintenance personnel, engineers, and safety experts 
        provides the most comprehensive analysis.
        """)
    
    with st.expander("What assets benefit most from RCM?"):
        st.markdown("""
        Critical assets where failure has significant safety, environmental, operational, or economic 
        consequences benefit most. However, RCM principles can be applied to any asset.
        """)
    
    with st.expander("How do I prioritize which assets to analyze first?"):
        st.markdown("""
        Start with assets that have high failure consequences, high maintenance costs, or frequent 
        failures. Safety-critical systems should be highest priority.
        """)
    
    with st.expander("What maintenance strategies does RCM recommend?"):
        st.markdown("""
        RCM evaluates multiple strategies including:
        - **CBM** (Condition-Based Maintenance): Monitor and predict failures
        - **TBM** (Time-Based Maintenance): Scheduled preventive tasks
        - **FTM** (Failure-Finding): Test hidden functions
        - **RTF** (Run-to-Failure): Accept failure for low-consequence items
        - **Redesign**: Modify equipment to eliminate failure modes
        """)
    
    with st.expander("How often should RCM analysis be updated?"):
        st.markdown("""
        Review analyses when significant changes occur (new equipment, operational changes, incidents) 
        or periodically (every 3-5 years) to ensure continued effectiveness.
        """)
    
    with st.expander("What is the difference between evident and hidden failures?"):
        st.markdown("""
        **Evident failures** are immediately apparent to operators through normal operation (e.g., a pump stops working). 
        **Hidden failures** are not evident until another failure occurs or during testing (e.g., a backup generator that only fails when needed).
        """)
    
    with st.expander("How do I calculate failure criticality?"):
        st.markdown("""
        Criticality is typically calculated by multiplying the severity of the failure consequence by its likelihood of occurrence. 
        This can be expressed as: **Criticality = Consequence × Frequency**. High criticality items require immediate attention.
        """)
    
    with st.expander("What is the RCM decision logic diagram?"):
        st.markdown("""
        The RCM decision logic is a flowchart that guides you through a series of questions about each failure mode to determine 
        the most appropriate maintenance strategy. It considers safety, environmental, operational, and economic consequences.
        """)
    
    with st.expander("Can RCM be applied to new equipment or only existing assets?"):
        st.markdown("""
        RCM can be applied to both new and existing equipment. For new equipment, it helps design an optimal maintenance program 
        from the start. For existing assets, it optimizes current maintenance practices and eliminates unnecessary tasks.
        """)
    
    with st.expander("What are functional failures vs failure modes?"):
        st.markdown("""
        A **functional failure** is the inability of an asset to perform its intended function (e.g., "Unable to pump water"). 
        A **failure mode** is the specific way the asset can fail (e.g., "Bearing seizure", "Impeller damage"). 
        One functional failure can have multiple failure modes.
        """)
    
    with st.expander("How detailed should my FMECA analysis be?"):
        st.markdown("""
        The level of detail depends on asset criticality. High-risk or critical assets warrant detailed analysis down to the 
        component level. Less critical assets may only need system-level analysis. Balance thoroughness with resource availability.
        """)
    
    with st.expander("What is the difference between RCM and traditional preventive maintenance?"):
        st.markdown("""
        Traditional PM uses time-based schedules regardless of actual condition. RCM determines if preventive maintenance is 
        actually needed, and if so, what type. RCM may conclude that run-to-failure is more economical for some failure modes.
        """)
    
    with st.expander("What software or tools do I need for RCM analysis?"):
        st.markdown("""
        Basic RCM can be performed with spreadsheets or this web application. Larger organizations may benefit from dedicated 
        RCM software that integrates with CMMS systems. The most important tool is a knowledgeable, cross-functional team.
        """)
    
    with st.expander("How do I handle failure modes with no effective preventive task?"):
        st.markdown("""
        If no cost-effective preventive task exists, consider: (1) Redesign to eliminate the failure mode, (2) Run-to-failure 
        with contingency plans, or (3) Failure-finding tasks for hidden failures. Document the decision rationale.
        """)
    
    with st.expander("What is the role of failure data and history in RCM?"):
        st.markdown("""
        Historical failure data helps estimate failure frequencies and validate assumptions. However, lack of data shouldn't 
        prevent RCM analysis. Expert judgment and experience can substitute where data is limited or unavailable.
        """)
    
    with st.expander("How do I get management buy-in for RCM?"):
        st.markdown("""
        Present RCM benefits in business terms: reduced downtime, optimized maintenance costs, improved safety, and extended 
        asset life. Start with a pilot project on a critical asset to demonstrate value and build credibility.
        """)
    
    with st.expander("What training is required for RCM facilitators?"):
        st.markdown("""
        RCM facilitators should complete formal RCM training (typically 3-5 days), understand failure analysis methods, 
        have strong facilitation skills, and possess technical knowledge of the assets being analyzed.
        """)
    
    with st.expander("Can RCM reduce my maintenance costs?"):
        st.markdown("""
        Yes, RCM typically reduces overall maintenance costs by eliminating unnecessary tasks, focusing resources on critical 
        items, and preventing costly failures. However, initial analysis requires time investment. Long-term savings often 
        exceed 20-30% of maintenance budgets.
        """)
    
    with st.expander("How do I prioritize which failure modes to analyze first?"):
        st.markdown("""
        Prioritize by consequence severity and likelihood. Focus first on failure modes with safety/environmental impacts, 
        then high operational impact items, followed by economic consequences. Use a risk matrix to visualize priorities.
        """)
    
    with st.expander("What is the difference between condition-based and time-based maintenance?"):
        st.markdown("""
        **Time-based maintenance (TBM)** occurs at fixed intervals regardless of condition (e.g., every 6 months). 
        **Condition-based maintenance (CBM)** is triggered by actual equipment condition monitored through inspections or sensors. 
        CBM is generally more efficient but requires monitoring capability.
        """)
    
    with st.expander("How do I document and present RCM results?"):
        st.markdown("""
        Use standard RCM worksheets documenting functions, failures, effects, consequences, and selected tasks. Create executive 
        summaries highlighting key findings, risk reductions, and implementation plans. Include before/after comparisons of 
        maintenance programs.
        """)
    
    with st.expander("What are common mistakes in RCM implementation?"):
        st.markdown("""
        Common mistakes include: analyzing too much detail for non-critical assets, not involving operators, accepting inadequate 
        tasks without redesign consideration, poor documentation, lack of follow-through on implementation, and treating RCM as 
        a one-time project rather than continuous improvement.
        """)
    
    with st.expander("How does RCM integrate with risk management frameworks?"):
        st.markdown("""
        RCM complements enterprise risk management by systematically identifying and mitigating asset-related risks. It provides 
        documented evidence of due diligence in managing safety and operational risks, supporting ISO 55000 and other standards.
        """)

elif st.session_state.current_view == 'future':
    # Future Development page
    st.markdown("### Future Development")
    st.markdown("#### Planned Enhancements:")
    st.markdown("")
    
    with st.expander("Phase 1 - Enhanced Analytics"):
        st.markdown("""
        **Description:**  
        Enhance the analytical capabilities of the tool with advanced algorithms and data-driven insights to improve 
        decision-making and maintenance optimization.
        
        **Improvements:**
        - Automated criticality scoring algorithms using multi-criteria decision analysis
        - Statistical failure data integration from maintenance management systems
        - Cost-benefit analysis tools for maintenance task evaluation
        - Maintenance optimization calculators for interval determination
        - Risk-based prioritization matrices with dynamic weighting
        
        **Benefits:**
        - Faster, more consistent criticality assessments
        - Data-driven decision making based on actual failure history
        - Quantifiable ROI for maintenance strategies
        - Optimized maintenance intervals reducing costs while maintaining reliability
        - Improved resource allocation based on risk priorities
        """)
    
    with st.expander("Phase 2 - Advanced Features"):
        st.markdown("""
        **Description:**  
        Integrate modern technologies including IoT, predictive analytics, and mobile capabilities to enable 
        real-time monitoring and field-based data collection.
        
        **Improvements:**
        - Seamless integration with CMMS/EAM systems (SAP, Maximo, etc.)
        - Real-time condition monitoring data feeds from sensors and SCADA
        - Predictive analytics and machine learning for failure prediction
        - Mobile app for field data collection and inspections
        - API connectivity for third-party system integration
        
        **Benefits:**
        - Eliminate double data entry through system integration
        - Real-time asset health visibility and predictive maintenance triggers
        - Proactive failure prevention through AI-powered predictions
        - Improved data quality with on-site mobile capture
        - Flexible ecosystem integration with existing tools
        """)
    
    with st.expander("Phase 3 - Collaboration Tools"):
        st.markdown("""
        **Description:**  
        Enable team-based analysis with collaboration features supporting multi-user workflows, review processes, 
        and comprehensive audit trails for compliance.
        
        **Improvements:**
        - Multi-user collaboration features with simultaneous editing
        - Review and approval workflows with role-based permissions
        - Complete audit trail and version control for all changes
        - Team commenting and annotations on analysis items
        - Notification system for task assignments and approvals
        
        **Benefits:**
        - Improved team productivity through collaborative analysis
        - Formal review processes ensuring quality and consistency
        - Full traceability for regulatory compliance and audits
        - Better communication and knowledge sharing across teams
        - Accountability and transparency in decision-making
        """)
    
    with st.expander("Phase 4 - Reporting & Visualization"):
        st.markdown("""
        **Description:**  
        Provide comprehensive reporting and visualization capabilities with interactive dashboards, automated 
        report generation, and customizable templates for professional presentations.
        
        **Improvements:**
        - Advanced dashboard with real-time KPI tracking and metrics
        - Interactive Pareto charts, risk matrices, and trend analysis
        - Automated report generation with scheduled distribution
        - Custom templates and branding for professional reports
        - Export capabilities to PDF, Word, Excel, and PowerPoint
        
        **Benefits:**
        - Real-time visibility of analysis status and key metrics
        - Better understanding of risk distribution and priorities
        - Time savings through automated report production
        - Professional, branded deliverables for stakeholders
        - Flexible reporting formats for different audiences
        """)
    
    with st.expander("Phase 5 - Industry Extensions"):
        st.markdown("""
        **Description:**  
        Extend the tool with industry-specific templates, regulatory compliance features, and best practice 
        libraries tailored to different asset management sectors.
        
        **Improvements:**
        - Industry-specific templates for Water, Energy, Manufacturing, Transport, etc.
        - Regulatory compliance checklists (ISO 55000, PAS 55, industry standards)
        - Best practice libraries with example analyses and maintenance strategies
        - Benchmarking capabilities against industry standards
        - Sector-specific failure mode libraries and consequence criteria
        
        **Benefits:**
        - Faster implementation with pre-built industry templates
        - Ensured compliance with relevant regulations and standards
        - Learning from proven industry best practices
        - Performance comparison against industry benchmarks
        - Reduced learning curve with industry-relevant examples
        """)
    
    st.markdown("")
    st.markdown("---")
    st.markdown("#### Feedback Welcome")
    st.markdown("""
    We continuously improve this tool based on user feedback. Please contact us with suggestions, 
    feature requests, or to report issues.
    """)
    st.markdown("")
    st.markdown(f"""**Software Support:** {config.get('Application', 'software_contact_email', fallback='sm@odysseus-imc.com')}  
**Technical Support:** {config.get('Application', 'technical_contact_email', fallback='adam.hassan@cambia.com.au')}""")

# Render current stage content based on sidebar selection
st.markdown("---")

# Stage function definitions
# Stage 1: Planning and Preparation
def stage_1_planning():
    """Stage 1: Planning and Preparation"""
    st.markdown("## Stage 1: Planning and Preparation")
    st.markdown("")
    st.markdown("**Objective:** Define the asset scope, gather information, and document the operating context.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Asset Identification")
        
        asset_name = st.text_input(
            "Asset Name/ID",
            value=st.session_state.asset_data.get('asset_name', ''),
            help="e.g., Tharbogang PS2 - Jockey Pump Assembly 1"
        )
        
        asset_class = st.selectbox(
            "Asset Class",
            ["Select...", "Pump Station", "Water Treatment Plant", "Pipeline System", 
             "Storage Tank", "Distribution Network", "Control System", "Other"],
            index=0 if not st.session_state.asset_data.get('asset_class') else 
                  ["Select...", "Pump Station", "Water Treatment Plant", "Pipeline System", 
                   "Storage Tank", "Distribution Network", "Control System", "Other"].index(
                      st.session_state.asset_data.get('asset_class', 'Select...'))
        )
        
        asset_type = st.text_input(
            "Asset Type/Sub-Class",
            value=st.session_state.asset_data.get('asset_type', ''),
            help="e.g., Centrifugal Pump Assembly, VFD Motor"
        )
        
        site_location = st.text_input(
            "Site Location",
            value=st.session_state.asset_data.get('site_location', ''),
            help="Physical location of the asset"
        )
        
        if st.button("💾 Save Asset Information", type="primary"):
            st.session_state.asset_data = {
                'asset_name': asset_name,
                'asset_class': asset_class,
                'asset_type': asset_type,
                'site_location': site_location
            }
            autosave_session_data()
            st.success("✅ Asset information saved!")
    
    with col2:
        st.subheader("Components")
        st.markdown("Define the components of this asset:")
        
        if 'components' not in st.session_state:
            st.session_state.components = []
        
        new_component = st.text_input("Add Component", key="new_component")
        if st.button("➕ Add Component"):
            if new_component and new_component not in st.session_state.components:
                st.session_state.components.append(new_component)
                autosave_session_data()
                st.success(f"Added: {new_component}")
        
        if st.session_state.components:
            st.markdown("**Current Components:**")
            for i, comp in enumerate(st.session_state.components):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"• {comp}")
                with col_b:
                    if st.button("🗑️", key=f"del_comp_{i}"):
                        st.session_state.components.pop(i)
                        autosave_session_data()
                        st.rerun()
    
    # Operating Context
    st.markdown("---")
    st.subheader("📝 Operating Context")
    
    st.markdown("Document the circumstances in which this asset operates. This sets the scene for the entire analysis.")
    
    tab1, tab2, tab3 = st.tabs(["Basic Context", "Technical Details", "Environment & Standards"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            redundancy = st.radio(
                "Redundancy",
                ["Stand-alone (no backup)", "Duty/Standby configuration", "N+1 configuration"],
                help="Is there a backup for this asset?"
            )
            
            utilization = st.text_area(
                "Utilization and Loading",
                help="Operating hours, load patterns, capacity utilization"
            )
        
        with col2:
            quality_standards = st.text_area(
                "Quality Standards",
                help="Product quality requirements, tolerances"
            )
            
            seasonal_demands = st.text_area(
                "Seasonal Demands",
                help="Peak demand periods, seasonal variations"
            )
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            skills_availability = st.text_area(
                "Skills Availability",
                help="Available skills on-site, contractor requirements"
            )
            
            spares_availability = st.text_area(
                "Spares Availability",
                help="On-site spares, lead times for ordering"
            )
        
        with col2:
            logistics = st.text_area(
                "Logistics",
                help="Equipment availability, off-site repair requirements"
            )
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            operating_environment = st.text_area(
                "Operating Environment",
                help="Indoor/outdoor, temperature, dust, weather exposure"
            )
            
            safety_standards = st.text_area(
                "Safety Standards",
                help="Relevant safety regulations and standards"
            )
        
        with col2:
            environmental_standards = st.text_area(
                "Environmental Standards",
                help="Environmental regulations and compliance requirements"
            )
    
    if st.button("💾 Save Operating Context", type="primary"):
        st.session_state.operating_context = {
            'redundancy': redundancy,
            'utilization': utilization,
            'quality_standards': quality_standards,
            'seasonal_demands': seasonal_demands,
            'skills_availability': skills_availability,
            'spares_availability': spares_availability,
            'logistics': logistics,
            'operating_environment': operating_environment,
            'safety_standards': safety_standards,
            'environmental_standards': environmental_standards
        }
        autosave_session_data()
        st.success("✅ Operating context saved!")
    
    if st.session_state.asset_data.get('asset_name'):
        st.markdown("---")
        if st.button("➡️ Proceed to Stage 2: RCM Analysis", key="proceed_green", use_container_width=True):
            st.session_state.current_stage = 2
            st.rerun()

# Stage 2: RCM Analysis (FMECA)
def stage_2_analysis():
    """Stage 2: RCM Analysis"""
    st.markdown("## Stage 2: RCM Analysis (FMECA)")
    st.markdown("")
    if not st.session_state.asset_data.get('asset_name'):
        st.warning("⚠️ Please complete Stage 1: Planning and Preparation first!")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    st.markdown(f"**Analyzing Asset:** {st.session_state.asset_data['asset_name']}")
    
    # Analysis Steps Tabs
    analysis_tab = st.tabs([
        "Step 2: Functions",
        "Step 3: Functional Failures", 
        "Step 4: Failure Modes",
        "Step 5: Failure Effects",
        "Step 6: Consequences",
        "Step 7: Task Selection"
    ])
    
    # Step 2: Functions
    with analysis_tab[0]:
        st.subheader("Step 2: Identify Functions")
        
        st.markdown("**Function Format:** [Verb] + [Object] + [Performance Standard]")
        st.markdown("**Example:** 'To pump water from Tank A to Tank B at 800 litres/second'")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            function_type = st.selectbox(
                "Function Type",
                ["Primary Function", "Environmental Integrity", "Safety/Structural Integrity",
                 "Control/Containment/Comfort", "Appearance", "Protection", "Economy/Efficiency"]
            )
            
            function_verb = st.text_input("Verb", placeholder="e.g., To pump, To contain, To protect")
            function_object = st.text_input("Object", placeholder="e.g., water, pressure, personnel")
            performance_std = st.text_input(
                "Performance Standard", 
                placeholder="e.g., at 250 L/s, between 500-600 kPa, within ±5%"
            )
        
        with col2:
            st.markdown("**Performance Standard Types:**")
            st.markdown("""
            - **Quantitative**: Numerical values
            - **Qualitative**: Descriptive
            - **Absolute**: Must be fully met
            - **Variable**: Changes with conditions
            - **Upper/Lower Limits**: Fixed boundaries
            """)
        
        if st.button("➕ Add Function"):
            if function_verb and function_object:
                function = {
                    'id': len(st.session_state.functions) + 1,
                    'type': function_type,
                    'verb': function_verb,
                    'object': function_object,
                    'performance_standard': performance_std,
                    'full_statement': f"{function_verb} {function_object} {performance_std}".strip()
                }
                st.session_state.functions.append(function)
                autosave_session_data()
                st.success(f"✅ Function {function['id']} added!")
                st.rerun()
        
        if st.session_state.functions:
            st.markdown("---")
            st.subheader("Defined Functions")
            
            functions_df = pd.DataFrame(st.session_state.functions)
            st.dataframe(functions_df[['id', 'type', 'full_statement']], use_container_width=True)
            
            # Delete function
            func_to_delete = st.selectbox(
                "Select function to delete",
                ["None"] + [f"Function {f['id']}: {f['full_statement']}" for f in st.session_state.functions]
            )
            if func_to_delete != "None" and st.button("🗑️ Delete Selected Function"):
                func_id = int(func_to_delete.split(":")[0].split()[-1])
                st.session_state.functions = [f for f in st.session_state.functions if f['id'] != func_id]
                autosave_session_data()
                st.success("Function deleted!")
                st.rerun()
    
    # Step 3: Functional Failures
    with analysis_tab[1]:
        st.subheader("Step 3: Identify Functional Failures")
        
        st.markdown("**Functional Failure:** The inability of an asset to fulfill its function at the required standard.")
        st.markdown("**Examples:** 'Unable to pump any water', 'Pumps water at less than 250 L/s'")
        
        if not st.session_state.functions:
            st.warning("⚠️ Please define functions first (Step 2)")
        else:
            selected_function = st.selectbox(
                "Select Function",
                [f"Function {f['id']}: {f['full_statement']}" for f in st.session_state.functions]
            )
            
            func_id = int(selected_function.split(":")[0].split()[-1])
            
            failure_description = st.text_area(
                "Describe the Functional Failure",
                help="How does the asset fail to meet this function?"
            )
            
            failure_category = st.radio(
                "Failure Category",
                ["Complete loss of function", "Partial loss of function", "Exceeds upper limit", "Below lower limit"]
            )
            
            if st.button("➕ Add Functional Failure"):
                if failure_description:
                    failure = {
                        'id': f"FF-{func_id}.{len([f for f in st.session_state.functional_failures if f['function_id'] == func_id]) + 1}",
                        'function_id': func_id,
                        'function_statement': next(f['full_statement'] for f in st.session_state.functions if f['id'] == func_id),
                        'description': failure_description,
                        'category': failure_category
                    }
                    st.session_state.functional_failures.append(failure)
                    autosave_session_data()
                    st.success(f"✅ Functional Failure {failure['id']} added!")
                    st.rerun()
            
            if st.session_state.functional_failures:
                st.markdown("---")
                st.subheader("Defined Functional Failures")
                failures_df = pd.DataFrame(st.session_state.functional_failures)
                st.dataframe(failures_df, use_container_width=True)
    
    # Step 4: Failure Modes
    with analysis_tab[2]:
        st.subheader("Step 4: Identify Failure Modes")
        
        st.markdown("**Failure Mode:** Any event which causes a functional failure.")
        st.markdown("**Format:** [Component] + [What went wrong] + [Why/Cause if known]")
        st.markdown("**Example:** 'Pump impeller worn due to normal wear'")
        
        if not st.session_state.functional_failures:
            st.warning("⚠️ Please define functional failures first (Step 3)")
        else:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                selected_failure = st.selectbox(
                    "Select Functional Failure",
                    [f"{f['id']}: {f['description']}" for f in st.session_state.functional_failures]
                )
                
                failure_id = selected_failure.split(":")[0]
            
            with col2:
                st.markdown("**Failure Categories:**")
                st.markdown("""
                - Deterioration
                - Lubrication Failure
                - Dirt/Contamination
                - Disassembly
                - Human Error
                - Overloading
                """)
            
            component = st.selectbox(
                "Component",
                ["Select..."] + (st.session_state.components if st.session_state.components else ["Define components in Stage 1"])
            )
            
            failure_mode_desc = st.text_area(
                "Failure Mode Description",
                help="What went wrong and why? (e.g., 'Seized bearing due to lack of lubrication')"
            )
            
            failure_mode_category = st.selectbox(
                "Failure Mode Category",
                ["Select...", "Deterioration (wear, corrosion, fatigue)", 
                 "Lubrication failure", "Dirt/contamination", "Disassembly (loose connections)",
                 "Human error", "Overloading", "Other"]
            )
            
            if st.button("➕ Add Failure Mode"):
                if component != "Select..." and failure_mode_desc:
                    mode = {
                        'id': f"FM-{failure_id}-{len([m for m in st.session_state.failure_modes if m['functional_failure_id'] == failure_id]) + 1}",
                        'functional_failure_id': failure_id,
                        'component': component,
                        'description': failure_mode_desc,
                        'category': failure_mode_category
                    }
                    st.session_state.failure_modes.append(mode)
                    autosave_session_data()
                    st.success(f"✅ Failure Mode {mode['id']} added!")
                    st.rerun()
            
            if st.session_state.failure_modes:
                st.markdown("---")
                st.subheader("Defined Failure Modes")
                modes_df = pd.DataFrame(st.session_state.failure_modes)
                st.dataframe(modes_df, use_container_width=True)
    
    # Step 5: Failure Effects
    with analysis_tab[3]:
        st.subheader("Step 5: Identify Failure Effects")
        
        st.markdown("**Failure Effect:** Describes what happens when a failure mode occurs.")
        st.markdown("Document the **worst-case scenario** assuming nothing is being done to prevent the failure.")
        
        if not st.session_state.failure_modes:
            st.warning("⚠️ Please define failure modes first (Step 4)")
        else:
            selected_mode = st.selectbox(
                "Select Failure Mode",
                [f"{m['id']}: {m['component']} - {m['description']}" for m in st.session_state.failure_modes]
            )
            
            mode_id = selected_mode.split(":")[0]
            
            st.markdown("**Describe the failure effects in detail:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                evidence = st.text_area(
                    "Evidence of Failure",
                    help="What signs indicate this failure? How is it detected?"
                )
                
                safety_impact = st.text_area(
                    "Safety/Environmental Impact",
                    help="Could someone be hurt/killed? Any environmental breach?"
                )
            
            with col2:
                operational_impact = st.text_area(
                    "Operational Impact",
                    help="Effect on production, quality, customer service, operating costs"
                )
                
                physical_damage = st.text_area(
                    "Physical Damage",
                    help="Damage to this or other equipment"
                )
            
            repair_action = st.text_area(
                "Repair Action Required",
                help="What must be done to fix it?"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                repair_time = st.number_input("Repair Time (hours)", min_value=0.0, step=0.5)
            with col2:
                downtime = st.number_input("Total Downtime (hours)", min_value=0.0, step=0.5,
                                          help="Includes diagnosis, parts, repair, and recommissioning")
            
            if st.button("➕ Add Failure Effect"):
                # Find the failure mode to update
                for mode in st.session_state.failure_modes:
                    if mode['id'] == mode_id:
                        mode['effects'] = {
                            'evidence': evidence,
                            'safety_impact': safety_impact,
                            'operational_impact': operational_impact,
                            'physical_damage': physical_damage,
                            'repair_action': repair_action,
                            'repair_time': repair_time,
                            'downtime': downtime
                        }
                        autosave_session_data()
                        st.success(f"✅ Failure effects added to {mode_id}")
                        st.rerun()
    
    # Step 6: Consequence Categories
    with analysis_tab[4]:
        st.subheader("Step 6: Categorize Consequences")
        
        st.markdown("**Objective:** Determine the significance of each failure mode by categorizing its consequences.")
        
        # Filter failure modes that have effects defined
        modes_with_effects = [m for m in st.session_state.failure_modes if 'effects' in m]
        
        if not modes_with_effects:
            st.warning("⚠️ Please define failure effects first (Step 5)")
        else:
            selected_mode = st.selectbox(
                "Select Failure Mode to Categorize",
                [f"{m['id']}: {m['component']} - {m['description']}" for m in modes_with_effects],
                key="consequence_mode_select"
            )
            
            mode_id = selected_mode.split(":")[0]
            current_mode = next(m for m in st.session_state.failure_modes if m['id'] == mode_id)
            
            # Display failure effects
            st.markdown("**Failure Effects Summary:**")
            if 'effects' in current_mode:
                effects = current_mode['effects']
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Evidence:** {effects.get('evidence', 'N/A')}")
                    st.markdown(f"**Safety Impact:** {effects.get('safety_impact', 'N/A')}")
                with col2:
                    st.markdown(f"**Operational Impact:** {effects.get('operational_impact', 'N/A')}")
                    st.markdown(f"**Downtime:** {effects.get('downtime', 0)} hours")
            
            st.markdown("---")
            st.markdown("### Consequence Decision Logic")
            
            # Question 1: Evident or Hidden?
            is_evident = st.radio(
                "**Q1: Will the failure become evident to operators under normal circumstances?**",
                ["Yes - Evident", "No - Hidden (failure of protective device)"],
                help="Evident = operators will know it failed. Hidden = failure only discovered when needed or during testing"
            )
            
            # Branch based on evident/hidden
            if "Hidden" in is_evident:
                st.info("This is a **Hidden Failure** - typically protective devices that fail silently")
                
                hidden_consequence = st.radio(
                    "**Q2: If a multiple failure occurs (protected function fails while protective device is failed), what are the consequences?**",
                    ["Safety or Environmental impact", "Operational impact", "Non-operational (just repair cost)"]
                )
                
                if "Safety" in hidden_consequence:
                    consequence_category = "Hidden (Safety/Environmental)"
                    color = "red"
                elif "Operational" in hidden_consequence:
                    consequence_category = "Hidden (Operational)"
                    color = "orange"
                else:
                    consequence_category = "Hidden (Non-operational)"
                    color = "yellow"
            
            else:  # Evident
                st.info("This is an **Evident Failure** - operators will know when it occurs")
                
                evident_consequence = st.radio(
                    "**Q2: What are the consequences of this evident failure?**",
                    ["Safety or Environmental impact", 
                     "Operational impact (affects output, quality, service, or operating costs)", 
                     "Non-operational (only direct repair cost)"]
                )
                
                if "Safety" in evident_consequence:
                    consequence_category = "Evident (Safety/Environmental)"
                    color = "red"
                elif "Operational" in evident_consequence:
                    consequence_category = "Evident (Operational)"
                    color = "orange"
                else:
                    consequence_category = "Evident (Non-operational)"
                    color = "yellow"
            
            st.markdown(f"**Consequence Category:** {consequence_category}")
            st.markdown("---")
            
            # Additional risk assessment for safety consequences
            if "Safety" in consequence_category or "Environmental" in consequence_category:
                st.markdown("")
                st.markdown("#### Risk Assessment")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    consequence_rating = st.select_slider(
                        "Consequence Severity",
                        options=["1-Insignificant", "2-Minor", "3-Moderate", "4-High", "5-Catastrophic"],
                        value="3-Moderate"
                    )
                
                with col2:
                    likelihood_rating = st.select_slider(
                        "Likelihood",
                        options=["1-Rare", "2-Unlikely", "3-Occasional", "4-Likely", "5-Almost Certain"],
                        value="3-Occasional"
                    )
                
                with col3:
                    # Calculate risk score
                    cons_num = int(consequence_rating[0])
                    like_num = int(likelihood_rating[0])
                    risk_score = cons_num + like_num
                    
                    if risk_score >= 8:
                        risk_level = "High"
                        risk_color = "red"
                    elif risk_score >= 6:
                        risk_level = "Medium"
                        risk_color = "orange"
                    else:
                        risk_level = "Low"
                        risk_color = "green"
                    
                    st.markdown(f"""
                    <div style="background-color: {risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <strong>Risk Level: {risk_level}</strong><br>
                    Score: {risk_score}
                    </div>
                    """, unsafe_allow_html=True)
            
            if st.button("💾 Save Consequence Category"):
                for mode in st.session_state.failure_modes:
                    if mode['id'] == mode_id:
                        mode['consequence_category'] = consequence_category
                        if "Safety" in consequence_category or "Environmental" in consequence_category:
                            mode['risk_assessment'] = {
                                'consequence': consequence_rating,
                                'likelihood': likelihood_rating,
                                'risk_score': risk_score,
                                'risk_level': risk_level
                            }
                        autosave_session_data()
                        st.success(f"✅ Consequence category saved for {mode_id}")
                        st.rerun()
    
    # Step 7: Task Selection
    with analysis_tab[5]:
        st.subheader("Step 7: Select Failure Management Tasks")
        
        st.markdown("**Objective:** Determine appropriate maintenance strategy for each failure mode based on its consequences.")
        
        # Filter modes with consequence categories
        modes_with_consequences = [m for m in st.session_state.failure_modes if 'consequence_category' in m]
        
        if not modes_with_consequences:
            st.warning("⚠️ Please categorize consequences first (Step 6)")
        else:
            selected_mode = st.selectbox(
                "Select Failure Mode for Task Selection",
                [f"{m['id']}: {m['component']} - {m['description']}" for m in modes_with_consequences],
                key="task_mode_select"
            )
            
            mode_id = selected_mode.split(":")[0]
            current_mode = next(m for m in st.session_state.failure_modes if m['id'] == mode_id)
            
            # Display context
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Consequence:** {current_mode.get('consequence_category', 'N/A')}")
            with col2:
                if 'risk_assessment' in current_mode:
                    st.markdown(f"**Risk Level:** {current_mode['risk_assessment']['risk_level']}")
            
            st.markdown("---")
            st.markdown("### Task Selection Decision")
            
            task_type = st.selectbox(
                "Select Task Type",
                ["Select...", 
                 "CBM - Condition Based Maintenance", 
                 "FTM - Fixed Time Maintenance",
                 "FF - Failure Finding",
                 "Redesign",
                 "OTF - Operate to Failure"]
            )
            
            if task_type != "Select...":
                st.markdown(f"#### {task_type}")
                
                # Task-specific inputs
                if "CBM" in task_type:
                    st.info("**CBM Task:** Monitor condition to predict when failure might occur")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        potential_failure = st.text_input("Potential Failure Condition", 
                                                         help="What condition indicates failure is starting?")
                        pf_interval = st.number_input("P-F Interval (days/hours)", min_value=0.0,
                                                     help="Time between potential failure detection and functional failure")
                    with col2:
                        inspection_method = st.text_area("Inspection Method",
                                                        help="How will condition be monitored?")
                        inspection_frequency = st.number_input("Inspection Frequency (days/hours)", min_value=0.0,
                                                              help="Should be 1/2 to 1/3 of P-F interval")
                    
                    task_description = f"Monitor {inspection_method} every {inspection_frequency} days/hours. Action when {potential_failure}"
                
                elif "FTM" in task_type:
                    st.info("**FTM Task:** Overhaul or replace at fixed intervals")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        task_action = st.text_input("Task Action", 
                                                   help="e.g., Replace bearing, Lubricate, Clean filter")
                        interval_value = st.number_input("Interval", min_value=0.0)
                    with col2:
                        interval_unit = st.selectbox("Interval Unit", 
                                                    ["hours", "days", "weeks", "months", "years", "operating hours", "cycles"])
                        useful_life = st.number_input("Useful Life / MTBF", min_value=0.0,
                                                     help="Mean time between failures")
                    
                    task_description = f"{task_action} every {interval_value} {interval_unit}"
                
                elif "FF" in task_type:
                    st.info("**FF Task:** Periodically check if hidden failure has occurred")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        test_method = st.text_area("Test Method",
                                                  help="How to check if protective device is functional")
                        ff_interval = st.number_input("Failure Finding Interval (days)", min_value=0.0)
                    with col2:
                        mtbf_protective = st.number_input("MTBF of Protective Device (years)", min_value=0.0)
                        mtbf_protected = st.number_input("MTBF of Protected Device (years)", min_value=0.0)
                    
                    task_description = f"Test {test_method} every {ff_interval} days"
                
                elif "Redesign" in task_type:
                    st.info("**Redesign:** One-off change to equipment, process, or procedure")
                    
                    redesign_type = st.radio("Redesign Type",
                                           ["Equipment modification", "Process change", "Procedure update", "Training"])
                    task_description = st.text_area("Describe the Redesign",
                                                   help="What specific change will be made?")
                
                else:  # OTF
                    st.info("**Operate to Failure:** Conscious decision to let failure occur and repair when it does")
                    
                    st.markdown("**Justification for OTF:**")
                    otf_reason = st.radio("Reason for OTF",
                                        ["No effective proactive task available",
                                         "Cost of proactive maintenance exceeds cost of failure",
                                         "Low consequence failure"])
                    task_description = f"Operate to failure. Reason: {otf_reason}"
                
                # Technical feasibility and worth doing assessment
                st.markdown("---")
                st.markdown("### Task Validation")
                
                col1, col2 = st.columns(2)
                with col1:
                    technically_feasible = st.radio("Technically Feasible?", ["Yes", "No"],
                                                   help="Can this task actually be performed?")
                with col2:
                    worth_doing = st.radio("Worth Doing?", ["Yes", "No"],
                                         help="Does it effectively address the consequences?")
                
                justification = st.text_area("Justification",
                                           help="Explain why this task is feasible and worth doing")
                
                # Cost estimate
                st.markdown("### Cost Estimate")
                col1, col2, col3 = st.columns(3)
                with col1:
                    labour_cost = st.number_input("Labour Cost ($)", min_value=0.0)
                with col2:
                    parts_cost = st.number_input("Parts Cost ($)", min_value=0.0)
                with col3:
                    other_cost = st.number_input("Other Cost ($)", min_value=0.0)
                
                total_cost = labour_cost + parts_cost + other_cost
                st.markdown(f"**Total Task Cost:** ${total_cost:,.2f}")
                
                if st.button("💾 Save Failure Management Task"):
                    if technically_feasible == "Yes" and worth_doing == "Yes":
                        task = {
                            'task_type': task_type,
                            'description': task_description,
                            'technically_feasible': technically_feasible,
                            'worth_doing': worth_doing,
                            'justification': justification,
                            'cost': total_cost
                        }
                        
                        # Add to failure mode
                        for mode in st.session_state.failure_modes:
                            if mode['id'] == mode_id:
                                mode['management_task'] = task
                                
                                # Also add to analysis results
                                result = {
                                    'failure_mode_id': mode_id,
                                    'component': mode['component'],
                                    'failure_mode': mode['description'],
                                    'consequence': mode.get('consequence_category', 'N/A'),
                                    'task_type': task_type,
                                    'task_description': task_description,
                                    'frequency': task_description,
                                    'cost': total_cost
                                }
                                st.session_state.analysis_results.append(result)
                                autosave_session_data()
                                st.success(f"✅ Task saved for {mode_id}")
                                st.rerun()
                    else:
                        st.error("Task must be both technically feasible and worth doing!")

# Stage 3: Implementation
def stage_3_implementation():
    """Stage 3: Implementation Planning"""
    st.markdown("## Stage 3: Implementation Planning")
    st.markdown("")
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available. Please complete Stage 2 first.")
        if st.button("← Go to Stage 2"):
            st.session_state.current_stage = 2
            st.rerun()
        return
    
    st.markdown("**Objective:** Plan implementation of the failure management tasks identified in the analysis.")
    
    tab1, tab2, tab3 = st.tabs(["Maintenance Schedule", "One-off Changes", "Implementation Checklist"])
    
    with tab1:
        st.subheader("Maintenance Schedule")
        
        # Filter for CBM, FTM, and FF tasks
        maintenance_tasks = [r for r in st.session_state.analysis_results 
                           if any(t in r['task_type'] for t in ['CBM', 'FTM', 'FF'])]
        
        if maintenance_tasks:
            df = pd.DataFrame(maintenance_tasks)
            st.dataframe(df, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Schedule Summary")
            
            # Group by task type
            col1, col2, col3 = st.columns(3)
            with col1:
                cbm_count = len([t for t in maintenance_tasks if 'CBM' in t['task_type']])
                st.metric("CBM Tasks", cbm_count)
            with col2:
                ftm_count = len([t for t in maintenance_tasks if 'FTM' in t['task_type']])
                st.metric("FTM Tasks", ftm_count)
            with col3:
                ff_count = len([t for t in maintenance_tasks if 'FF' in t['task_type']])
                st.metric("FF Tasks", ff_count)
            
            # Total annual cost
            total_annual_cost = sum([t['cost'] for t in maintenance_tasks])
            st.markdown(f"**Estimated Annual Maintenance Cost:** ${total_annual_cost:,.2f}")
        else:
            st.info("No scheduled maintenance tasks defined yet.")
    
    with tab2:
        st.subheader("One-off Changes (Redesign Tasks)")
        
        redesign_tasks = [r for r in st.session_state.analysis_results if 'Redesign' in r['task_type']]
        
        if redesign_tasks:
            for i, task in enumerate(redesign_tasks):
                with st.expander(f"Redesign {i+1}: {task['component']} - {task['failure_mode']}"):
                    st.markdown(f"**Task:** {task['task_description']}")
                    st.markdown(f"**Estimated Cost:** ${task['cost']:,.2f}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        priority = st.selectbox(f"Priority", ["High", "Medium", "Low"], key=f"priority_{i}")
                    with col2:
                        target_date = st.date_input(f"Target Completion", key=f"date_{i}")
                    
                    responsible_person = st.text_input(f"Responsible Person", key=f"person_{i}")
                    notes = st.text_area(f"Implementation Notes", key=f"notes_{i}")
        else:
            st.info("No redesign tasks identified.")
    
    with tab3:
        st.subheader("Implementation Checklist")
        
        st.markdown("""
        Use this checklist to track implementation progress:
        """)
        
        checklist_items = [
            "Review and approve all identified tasks",
            "Update CMMS with new maintenance tasks",
            "Schedule initial execution dates",
            "Assign resources and responsibilities",
            "Order necessary parts and materials",
            "Update standard operating procedures",
            "Conduct training for operations and maintenance staff",
            "Set up condition monitoring systems (for CBM tasks)",
            "Establish spare parts inventory",
            "Create job plans and work instructions",
            "Set up performance tracking and KPIs",
            "Schedule first review date for continuous improvement"
        ]
        
        for i, item in enumerate(checklist_items):
            st.checkbox(item, key=f"checklist_{i}")

# Stage 4: Reports and Export
def stage_4_reports():
    """Stage 4: Reports and Export"""
    st.markdown("## Stage 4: Reports and Export")
    st.markdown("")
    if not st.session_state.analysis_results:
        st.warning("⚠️ No analysis results available.")
        return
    
    tab1, tab2, tab3 = st.tabs(["Summary Report", "Detailed Analysis", "Export Data"])
    
    with tab1:
        st.subheader("RCM Analysis Summary Report")
        
        # Asset information
        st.markdown("### Asset Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Asset:** {st.session_state.asset_data.get('asset_name', 'N/A')}")
            st.markdown(f"**Class:** {st.session_state.asset_data.get('asset_class', 'N/A')}")
        with col2:
            st.markdown(f"**Type:** {st.session_state.asset_data.get('asset_type', 'N/A')}")
            st.markdown(f"**Location:** {st.session_state.asset_data.get('site_location', 'N/A')}")
        with col3:
            st.markdown(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}")
            st.markdown(f"**Components:** {len(st.session_state.components)}")
        
        # Analysis statistics
        st.markdown("---")
        st.markdown("### Analysis Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Functions", len(st.session_state.functions))
        with col2:
            st.metric("Functional Failures", len(st.session_state.functional_failures))
        with col3:
            st.metric("Failure Modes", len(st.session_state.failure_modes))
        with col4:
            st.metric("Management Tasks", len(st.session_state.analysis_results))
        
        # Consequence breakdown
        st.markdown("---")
        st.markdown("### Consequence Breakdown")
        
        consequence_counts = {}
        for mode in st.session_state.failure_modes:
            if 'consequence_category' in mode:
                cat = mode['consequence_category']
                consequence_counts[cat] = consequence_counts.get(cat, 0) + 1
        
        if consequence_counts:
            col1, col2 = st.columns(2)
            with col1:
                for cat, count in consequence_counts.items():
                    st.markdown(f"**{cat}:** {count}")
            
            with col2:
                # Simple visualization
                df_cons = pd.DataFrame(list(consequence_counts.items()), columns=['Category', 'Count'])
                st.bar_chart(df_cons.set_index('Category'))
        
        # Task type breakdown
        st.markdown("---")
        st.markdown("### Task Type Breakdown")
        
        task_counts = {}
        total_cost = 0
        for result in st.session_state.analysis_results:
            task_type = result['task_type'].split('-')[0].strip()
            task_counts[task_type] = task_counts.get(task_type, 0) + 1
            total_cost += result['cost']
        
        col1, col2 = st.columns(2)
        with col1:
            for task, count in task_counts.items():
                st.markdown(f"**{task}:** {count} tasks")
        
        with col2:
            st.markdown(f"**Total Annual Cost:** ${total_cost:,.2f}")
    
    with tab2:
        st.subheader("Detailed FMECA Analysis")
        
        # Complete analysis table
        detailed_data = []
        for mode in st.session_state.failure_modes:
            row = {
                'Failure Mode ID': mode['id'],
                'Component': mode['component'],
                'Failure Mode': mode['description'],
                'Consequence Category': mode.get('consequence_category', 'Not categorized'),
            }
            
            if 'effects' in mode:
                row['Safety Impact'] = mode['effects'].get('safety_impact', 'None')
                row['Operational Impact'] = mode['effects'].get('operational_impact', 'None')
                row['Downtime (hrs)'] = mode['effects'].get('downtime', 0)
            
            if 'management_task' in mode:
                row['Task Type'] = mode['management_task']['task_type']
                row['Task Description'] = mode['management_task']['description']
                row['Annual Cost ($)'] = mode['management_task']['cost']
            
            detailed_data.append(row)
        
        if detailed_data:
            df_detailed = pd.DataFrame(detailed_data)
            st.dataframe(df_detailed, use_container_width=True)
    
    with tab3:
        st.subheader("Export Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export to CSV")
            
            if st.session_state.analysis_results:
                df_export = pd.DataFrame(st.session_state.analysis_results)
                csv = df_export.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv,
                    file_name=f"rcm_analysis_{st.session_state.asset_data.get('asset_name', 'asset')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("#### Export to JSON")
            
            # Complete export including all data
            export_data = {
                'asset_information': st.session_state.asset_data,
                'operating_context': st.session_state.operating_context,
                'components': st.session_state.components,
                'functions': st.session_state.functions,
                'functional_failures': st.session_state.functional_failures,
                'failure_modes': st.session_state.failure_modes,
                'analysis_results': st.session_state.analysis_results,
                'export_date': datetime.now().isoformat()
            }
            
            json_str = json.dumps(export_data, indent=2)
            
            st.download_button(
                label="📥 Download Complete Analysis as JSON",
                data=json_str,
                file_name=f"rcm_complete_{st.session_state.asset_data.get('asset_name', 'asset')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("#### Import Previous Analysis")
        
        uploaded_file = st.file_uploader("Upload JSON analysis file", type=['json'])
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                
                if st.button("Import Analysis Data"):
                    st.session_state.asset_data = imported_data.get('asset_information', {})
                    st.session_state.operating_context = imported_data.get('operating_context', {})
                    st.session_state.components = imported_data.get('components', [])
                    st.session_state.functions = imported_data.get('functions', [])
                    st.session_state.functional_failures = imported_data.get('functional_failures', [])
                    st.session_state.failure_modes = imported_data.get('failure_modes', [])
                    st.session_state.analysis_results = imported_data.get('analysis_results', [])
                    autosave_session_data()
                    st.success("✅ Analysis data imported successfully!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error importing file: {e}")

# Render stage content only if in RCM Navigation view
if st.session_state.current_view == 'rcm_navigation' and st.session_state.get('render_stages', False):
    if st.session_state.current_stage == 1:
        stage_1_planning()
    elif st.session_state.current_stage == 2:
        stage_2_analysis()
    elif st.session_state.current_stage == 3:
        stage_3_implementation()
    elif st.session_state.current_stage == 4:
        stage_4_reports()
