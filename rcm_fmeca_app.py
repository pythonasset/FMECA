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
import time
import hashlib

# Cache configuration loading for better performance
@st.cache_resource
def load_config():
    """Load and cache configuration file
    
    Note: Organization details (authority_name, department, contact_email) are now
    sourced from the .registration file, not from config.ini. The config.ini values
    are kept as placeholders only and should remain empty.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_path)
    return {
        'APP_NAME': config.get('Application', 'name', fallback='FMECA & RCM Analysis Tool'),
        'APP_VERSION': config.get('Application', 'version', fallback='1.0.0'),
        'REGISTRATION_DATE': config.get('Application', 'registration_date', fallback='2025-10-20'),
        'AUTHORITY_NAME': config.get('Organization', 'authority_name', fallback=''),  # Not used - from .registration
        'DEPARTMENT': config.get('Organization', 'department', fallback=''),  # Not used - from .registration
        'CONTACT_EMAIL': config.get('Organization', 'contact_email', fallback=''),  # Not used - from .registration
        'SOFTWARE_CONTACT': config.get('Application', 'software_contact_email', fallback='sm@odysseus-imc.com'),
        'TECHNICAL_CONTACT': config.get('Application', 'technical_contact_email', fallback='adam.hassan@cambia.com.au')
    }

config_data = load_config()
APP_NAME = config_data['APP_NAME']
APP_VERSION = config_data['APP_VERSION']
REGISTRATION_DATE = config_data['REGISTRATION_DATE']
# Organization details below are NOT USED - all registration info comes from .registration file
AUTHORITY_NAME = config_data['AUTHORITY_NAME']
DEPARTMENT = config_data['DEPARTMENT']
CONTACT_EMAIL = config_data['CONTACT_EMAIL']

# Page configuration
st.set_page_config(
    page_title="FMECA & RCM Analysis Tool",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache CSS to avoid reprocessing on every page load
@st.cache_data
def get_custom_css():
    """Return cached custom CSS string"""
    return """
<style>
    /* Main headings - muted gold color */
    h1, h2, h3 {
        color: #D4A520 !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #D4A520;
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
    
    /* Red border for all dropdown/selectbox elements */
    .stSelectbox > div > div {
        border: 2px solid red !important;
        border-radius: 4px !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        border: 2px solid red !important;
    }
    
    /* Light grey background for dropdown menu options */
    .stSelectbox [data-baseweb="popover"] {
        background-color: #f5f5f5 !important;
    }
    
    .stSelectbox [data-baseweb="menu"] {
        background-color: #f5f5f5 !important;
    }
    
    .stSelectbox [role="listbox"] {
        background-color: #f5f5f5 !important;
    }
    
    .stSelectbox [role="option"] {
        background-color: #f5f5f5 !important;
        color: #808080 !important;
    }
    
    .stSelectbox [role="option"]:hover {
        background-color: #e0e0e0 !important;
        color: #808080 !important;
    }
    
    .stSelectbox [aria-selected="true"] {
        background-color: #d3d3d3 !important;
        color: #808080 !important;
    }
</style>
"""

# Apply cached CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_stage' not in st.session_state:
        st.session_state.current_stage = 1
    
    # User authentication state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # Project-level data
    if 'project_data' not in st.session_state:
        st.session_state.project_data = {
            'project_no': '',
            'project_description': '',
            'created_date': '',
            'last_modified': ''
        }
    
    # Assets list - each project can have multiple assets
    if 'assets' not in st.session_state:
        st.session_state.assets = []
    
    # Current selected asset index
    if 'current_asset_index' not in st.session_state:
        st.session_state.current_asset_index = None
    
    # Component editing state
    if 'editing_component' not in st.session_state:
        st.session_state.editing_component = None
    
    # Functional failure editing/deleting state
    if 'editing_functional_failure' not in st.session_state:
        st.session_state.editing_functional_failure = False
    
    if 'deleting_functional_failure' not in st.session_state:
        st.session_state.deleting_functional_failure = False
    
    # Legacy compatibility - will be deprecated
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
    
    # Initialize autosave flag
    if 'last_autosave_hash' not in st.session_state:
        st.session_state.last_autosave_hash = None
    
    # Flag to track if we've attempted autorestore
    if 'autorestore_attempted' not in st.session_state:
        st.session_state.autorestore_attempted = False
    
    # Risk matrix configuration thresholds
    if 'risk_moderate_threshold' not in st.session_state:
        st.session_state.risk_moderate_threshold = 6
    
    if 'risk_high_threshold' not in st.session_state:
        st.session_state.risk_high_threshold = 8

initialize_session_state()

# Risk Classification Helper Functions
def get_risk_level(risk_score):
    """Get risk level based on score and current thresholds"""
    if risk_score >= st.session_state.risk_high_threshold:
        return "High", "red"
    elif risk_score >= st.session_state.risk_moderate_threshold:
        return "Moderate", "orange"
    else:
        return "Low", "green"

def get_risk_matrix_cell_class(score):
    """Get CSS class for risk matrix cell based on score"""
    if score >= st.session_state.risk_high_threshold:
        return "risk-high"
    elif score >= st.session_state.risk_moderate_threshold:
        return "risk-medium"
    else:
        return "risk-low"

def get_risk_matrix_cell_label(score):
    """Get label (L/M/H) for risk matrix cell based on score"""
    if score >= st.session_state.risk_high_threshold:
        return "H"
    elif score >= st.session_state.risk_moderate_threshold:
        return "M"
    else:
        return "L"

def generate_risk_matrix_html():
    """Generate dynamic risk matrix HTML based on current thresholds"""
    moderate_thresh = st.session_state.risk_moderate_threshold
    high_thresh = st.session_state.risk_high_threshold
    
    # Calculate score ranges for legend
    low_max = moderate_thresh - 1
    moderate_max = high_thresh - 1
    
    matrix_html = f"""
    <style>
        .risk-matrix {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }}
        .risk-matrix th, .risk-matrix td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }}
        .risk-matrix th {{
            background-color: #f0f0f0;
            color: #333;
        }}
        .risk-low {{
            background-color: #90EE90;
            color: #000;
        }}
        .risk-medium {{
            background-color: #FFA500;
            color: #fff;
        }}
        .risk-high {{
            background-color: #FF6B6B;
            color: #fff;
        }}
    </style>
    <table class="risk-matrix">
        <tr>
            <th>Consequence →<br>Likelihood ↓</th>
            <th>1-Insignificant</th>
            <th>2-Minor</th>
            <th>3-Moderate</th>
            <th>4-High</th>
            <th>5-Catastrophic</th>
        </tr>
        <tr>
            <th>5-Almost Certain</th>
            <td class="{get_risk_matrix_cell_class(6)}">6 ({get_risk_matrix_cell_label(6)})</td>
            <td class="{get_risk_matrix_cell_class(7)}">7 ({get_risk_matrix_cell_label(7)})</td>
            <td class="{get_risk_matrix_cell_class(8)}">8 ({get_risk_matrix_cell_label(8)})</td>
            <td class="{get_risk_matrix_cell_class(9)}">9 ({get_risk_matrix_cell_label(9)})</td>
            <td class="{get_risk_matrix_cell_class(10)}">10 ({get_risk_matrix_cell_label(10)})</td>
        </tr>
        <tr>
            <th>4-Likely</th>
            <td class="{get_risk_matrix_cell_class(5)}">5 ({get_risk_matrix_cell_label(5)})</td>
            <td class="{get_risk_matrix_cell_class(6)}">6 ({get_risk_matrix_cell_label(6)})</td>
            <td class="{get_risk_matrix_cell_class(7)}">7 ({get_risk_matrix_cell_label(7)})</td>
            <td class="{get_risk_matrix_cell_class(8)}">8 ({get_risk_matrix_cell_label(8)})</td>
            <td class="{get_risk_matrix_cell_class(9)}">9 ({get_risk_matrix_cell_label(9)})</td>
        </tr>
        <tr>
            <th>3-Occasional</th>
            <td class="{get_risk_matrix_cell_class(4)}">4 ({get_risk_matrix_cell_label(4)})</td>
            <td class="{get_risk_matrix_cell_class(5)}">5 ({get_risk_matrix_cell_label(5)})</td>
            <td class="{get_risk_matrix_cell_class(6)}">6 ({get_risk_matrix_cell_label(6)})</td>
            <td class="{get_risk_matrix_cell_class(7)}">7 ({get_risk_matrix_cell_label(7)})</td>
            <td class="{get_risk_matrix_cell_class(8)}">8 ({get_risk_matrix_cell_label(8)})</td>
        </tr>
        <tr>
            <th>2-Unlikely</th>
            <td class="{get_risk_matrix_cell_class(3)}">3 ({get_risk_matrix_cell_label(3)})</td>
            <td class="{get_risk_matrix_cell_class(4)}">4 ({get_risk_matrix_cell_label(4)})</td>
            <td class="{get_risk_matrix_cell_class(5)}">5 ({get_risk_matrix_cell_label(5)})</td>
            <td class="{get_risk_matrix_cell_class(6)}">6 ({get_risk_matrix_cell_label(6)})</td>
            <td class="{get_risk_matrix_cell_class(7)}">7 ({get_risk_matrix_cell_label(7)})</td>
        </tr>
        <tr>
            <th>1-Rare</th>
            <td class="{get_risk_matrix_cell_class(2)}">2 ({get_risk_matrix_cell_label(2)})</td>
            <td class="{get_risk_matrix_cell_class(3)}">3 ({get_risk_matrix_cell_label(3)})</td>
            <td class="{get_risk_matrix_cell_class(4)}">4 ({get_risk_matrix_cell_label(4)})</td>
            <td class="{get_risk_matrix_cell_class(5)}">5 ({get_risk_matrix_cell_label(5)})</td>
            <td class="{get_risk_matrix_cell_class(6)}">6 ({get_risk_matrix_cell_label(6)})</td>
        </tr>
    </table>
    <p style="font-size: 12px; color: #666;">
        <strong>Risk Levels:</strong> L = Low (2-{low_max}), M = Moderate ({moderate_thresh}-{moderate_max}), H = High ({high_thresh}-10)
    </p>
    """
    return matrix_html

# Import/Export Helper Functions
def create_export_data():
    """Create export data structure from session state"""
    # Check if there's project data or legacy asset data
    if not st.session_state.project_data.get('project_no') and not st.session_state.asset_data.get('asset_name'):
        return None
    
    export_data = {
        "application_info": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "authority": AUTHORITY_NAME,
            "department": DEPARTMENT
        },
        "project_information": st.session_state.project_data,
        "assets": st.session_state.assets,
        # Legacy support - for backward compatibility
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
        # Load project information (new format)
        if "project_information" in import_data:
            st.session_state.project_data = import_data["project_information"]
        
        # Load assets (new format)
        if "assets" in import_data:
            st.session_state.assets = import_data["assets"]
        
        # Load asset information (legacy format)
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
        
        # Only save if there's meaningful data (project no or asset name is set)
        if not st.session_state.project_data.get('project_no') and not st.session_state.asset_data.get('asset_name'):
            return
        
        # Create a hash of current data to detect changes
        current_data_hash = hash(json.dumps({
            "project": st.session_state.project_data,
            "assets_count": len(st.session_state.assets),
            "stage": st.session_state.current_stage
        }, sort_keys=True))
        
        # Only save if data has changed
        if hasattr(st.session_state, 'last_autosave_hash') and st.session_state.last_autosave_hash == current_data_hash:
            return
        
        save_data = {
            "application_info": {
                "name": APP_NAME,
                "version": APP_VERSION,
                "authority": AUTHORITY_NAME,
                "department": DEPARTMENT
            },
            "project_information": st.session_state.project_data,
            "assets": st.session_state.assets,
            "current_asset_index": st.session_state.current_asset_index,
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
        
        # Store hash to avoid redundant saves
        st.session_state.last_autosave_hash = current_data_hash
        
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
        
        # Only restore if current session is empty (project no and asset name not set)
        if st.session_state.project_data.get('project_no') or st.session_state.asset_data.get('asset_name'):
            return False
        
        with open(autosave_path, 'r') as f:
            saved_data = json.load(f)
        
        # Load the saved data
        if "project_information" in saved_data:
            st.session_state.project_data = saved_data["project_information"]
        
        if "assets" in saved_data:
            st.session_state.assets = saved_data["assets"]
        
        if "current_asset_index" in saved_data:
            st.session_state.current_asset_index = saved_data["current_asset_index"]
        
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

def save_asset_analysis_data():
    """Save current analysis data back to the selected asset in the assets list"""
    try:
        if 'selected_analysis_asset' in st.session_state and st.session_state.selected_analysis_asset is not None:
            asset_index = st.session_state.selected_analysis_asset
            if 0 <= asset_index < len(st.session_state.assets):
                st.session_state.assets[asset_index]['components'] = st.session_state.get('components', [])
                st.session_state.assets[asset_index]['functions'] = st.session_state.get('functions', [])
                st.session_state.assets[asset_index]['functional_failures'] = st.session_state.get('functional_failures', [])
                st.session_state.assets[asset_index]['failure_modes'] = st.session_state.get('failure_modes', [])
                st.session_state.assets[asset_index]['analysis_results'] = st.session_state.get('analysis_results', [])
                st.session_state.assets[asset_index]['operating_context'] = st.session_state.get('operating_context', {})
                autosave_session_data()
    except Exception as e:
        print(f"Error saving asset analysis data: {str(e)}")

# Registration Management Functions
def get_registration_path():
    """Get the path for the registration file"""
    return os.path.join(os.path.dirname(__file__), '.registration')

def is_registered():
    """Check if the application is registered"""
    try:
        registration_path = get_registration_path()
        if not os.path.exists(registration_path):
            return False
        
        with open(registration_path, 'r') as f:
            reg_data = json.load(f)
            # Check if all required fields are present and not empty
            required_fields = ['authority_name', 'department', 'contact_person', 'contact_email']
            return all(reg_data.get(field, '').strip() for field in required_fields)
    except Exception as e:
        print(f"Registration check error: {str(e)}")
        return False

def save_registration(authority_name, department, contact_person, contact_email, phone, address):
    """Save registration details"""
    try:
        registration_path = get_registration_path()
        reg_data = {
            'authority_name': authority_name,
            'department': department,
            'contact_person': contact_person,
            'contact_email': contact_email,
            'phone': phone,
            'address': address,
            'registration_date': datetime.now().isoformat(),
            'app_version': APP_VERSION
        }
        
        with open(registration_path, 'w') as f:
            json.dump(reg_data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Error saving registration: {str(e)}")
        return False

def get_registration_details():
    """Get stored registration details"""
    try:
        registration_path = get_registration_path()
        if os.path.exists(registration_path):
            with open(registration_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading registration: {str(e)}")
    return {}

# User Authentication Functions
def get_users_path():
    """Get the path for the users database file"""
    return os.path.join(os.path.dirname(__file__), '.users.json')

def migrate_user_database():
    """Migrate old user database format (is_admin) to new format (user_type) and add login_count"""
    users_path = get_users_path()
    try:
        if os.path.exists(users_path):
            with open(users_path, 'r') as f:
                users = json.load(f)
            
            # Check if migration is needed
            needs_migration = False
            for username, user_data in users.items():
                if 'is_admin' in user_data and 'user_type' not in user_data:
                    needs_migration = True
                    break
                if 'login_count' not in user_data:
                    needs_migration = True
                    break
            
            if needs_migration:
                # Migrate each user
                for username, user_data in users.items():
                    # Migrate is_admin to user_type
                    if 'is_admin' in user_data:
                        # Convert is_admin to user_type
                        if user_data.get('is_admin', False):
                            user_data['user_type'] = 'Administrator'
                        else:
                            user_data['user_type'] = 'User'
                        # Remove old is_admin field
                        del user_data['is_admin']
                    
                    # Add login_count if missing
                    if 'login_count' not in user_data:
                        user_data['login_count'] = 0
                
                # Save migrated data
                with open(users_path, 'w') as f:
                    json.dump(users, f, indent=2)
                
                print("User database migrated to new format")
    except Exception as e:
        print(f"Error during user database migration: {str(e)}")

def initialize_users_db():
    """Initialize users database with default admin user"""
    users_path = get_users_path()
    
    # First, migrate existing database if needed
    migrate_user_database()
    
    if not os.path.exists(users_path):
        # Create default admin user (hidden) with Administrator role
        default_users = {
            "admin": {
                "password": hashlib.sha256("odyssey".encode()).hexdigest(),
                "position": "System Administrator",
                "created_date": datetime.now().isoformat(),
                "user_type": "Administrator",
                "full_name": "Administrator",
                "login_count": 0
            }
        }
        try:
            with open(users_path, 'w') as f:
                json.dump(default_users, f, indent=2)
        except Exception as e:
            print(f"Error initializing users database: {str(e)}")

def load_users():
    """Load users from database"""
    users_path = get_users_path()
    try:
        if os.path.exists(users_path):
            with open(users_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading users: {str(e)}")
    return {}

def save_user(username, password, full_name, position, user_type="User"):
    """Save a new user to the database"""
    try:
        users = load_users()
        
        if username.lower() in [u.lower() for u in users.keys()]:
            return False, "Username already exists"
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        users[username] = {
            "password": hashed_password,
            "full_name": full_name,
            "position": position,
            "created_date": datetime.now().isoformat(),
            "user_type": user_type,
            "login_count": 0
        }
        
        with open(get_users_path(), 'w') as f:
            json.dump(users, f, indent=2)
        
        return True, "User registered successfully"
    except Exception as e:
        return False, f"Error saving user: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user credentials and increment login counter"""
    users = load_users()
    
    if username not in users:
        return False, None
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    if users[username]['password'] == hashed_password:
        # Increment login counter
        if 'login_count' not in users[username]:
            users[username]['login_count'] = 0
        users[username]['login_count'] += 1
        
        # Update last login timestamp
        users[username]['last_login'] = datetime.now().isoformat()
        
        # Save updated user data
        try:
            with open(get_users_path(), 'w') as f:
                json.dump(users, f, indent=2)
        except Exception as e:
            print(f"Error updating login count: {str(e)}")
        
        return True, users[username]
    
    return False, None

def is_user_logged_in():
    """Check if a user is logged in"""
    return st.session_state.get('logged_in', False) and st.session_state.get('current_user', None) is not None

def get_user_type():
    """Get the current user's type"""
    if is_user_logged_in():
        user_data = st.session_state.get('user_data', {})
        return user_data.get('user_type', 'User')
    return None

def is_administrator():
    """Check if current user is an Administrator"""
    return get_user_type() == 'Administrator'

def is_super_user():
    """Check if current user is a Super User"""
    return get_user_type() == 'Super User'

def can_access_administration():
    """Check if current user can access Administration section"""
    user_type = get_user_type()
    return user_type in ['Administrator', 'Super User']

def update_user_type(username, new_user_type):
    """Update a user's type (only for Administrators)"""
    try:
        users = load_users()
        
        if username not in users:
            return False, "User not found"
        
        if username == "admin":
            return False, "Cannot modify the default admin account"
        
        users[username]['user_type'] = new_user_type
        
        with open(get_users_path(), 'w') as f:
            json.dump(users, f, indent=2)
        
        return True, f"User type updated to {new_user_type}"
    except Exception as e:
        return False, f"Error updating user type: {str(e)}"

def show_login_form():
    """Display login form"""
    st.markdown("# 🔐 User Login")
    st.markdown("---")
    
    st.info("ℹ️ Please log in to access the FMECA & RCM Analysis Tool")
    st.markdown("")
    
    # Create tabs for login and registration
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register New User"])
    
    with tab1:
        st.markdown("### Login to Your Account")
        st.markdown("")
        
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            
            st.markdown("")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                submit = st.form_submit_button("🔓 Login", type="primary", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                else:
                    success, user_data = authenticate_user(username, password)
                    
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_data = user_data
                        st.success(f"✅ Welcome back, {user_data.get('full_name', username)}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
    
    with tab2:
        st.markdown("### Register New User")
        st.markdown("")
        
        with st.form("user_registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_username = st.text_input(
                    "Username *",
                    help="Choose a unique username",
                    placeholder="e.g., jsmith"
                )
                
                new_full_name = st.text_input(
                    "Full Name *",
                    help="Your full name",
                    placeholder="e.g., John Smith"
                )
            
            with col2:
                new_position = st.text_input(
                    "Position *",
                    help="Your position in the organization",
                    placeholder="e.g., Asset Manager"
                )
                
                new_password = st.text_input(
                    "Password *",
                    type="password",
                    help="Choose a secure password (min 6 characters)",
                    placeholder="Enter password"
                )
            
            new_password_confirm = st.text_input(
                "Confirm Password *",
                type="password",
                placeholder="Re-enter password"
            )
            
            st.markdown("")
            st.markdown("**All fields are required**")
            st.markdown("")
            
            col_a, col_b, col_c = st.columns([1, 1, 2])
            with col_a:
                register = st.form_submit_button("✅ Register", type="primary", use_container_width=True)
            
            if register:
                # Validation
                if not new_username or not new_username.strip():
                    st.error("❌ Username is required")
                elif not new_full_name or not new_full_name.strip():
                    st.error("❌ Full name is required")
                elif not new_position or not new_position.strip():
                    st.error("❌ Position is required")
                elif not new_password or len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                elif new_password != new_password_confirm:
                    st.error("❌ Passwords do not match")
                elif new_username.lower() == 'admin':
                    st.error("❌ This username is reserved")
                else:
                    success, message = save_user(
                        new_username.strip(),
                        new_password,
                        new_full_name.strip(),
                        new_position.strip()
                    )
                    
                    if success:
                        st.success(f"✅ {message}! You can now log in.")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown("---")
    st.markdown("")
    
    # Show registration info at bottom
    registration_info = get_registration_details()
    if registration_info:
        st.info(f"📋 This software is registered to: **{registration_info.get('authority_name', 'N/A')}**")
    
    st.markdown("")
    
    # Prevent any other content from showing
    st.stop()

def show_logout_button():
    """Display logout button in sidebar"""
    if is_user_logged_in():
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Information")
        user_data = st.session_state.get('user_data', {})
        st.sidebar.markdown(f"**User:** {st.session_state.current_user}")
        st.sidebar.markdown(f"**Position:** {user_data.get('position', 'N/A')}")
        st.sidebar.markdown(f"**User Type:** {user_data.get('user_type', 'User')}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_data = None
            st.rerun()

def show_registration_form():
    """Display registration form that must be completed before using the app"""
    st.markdown("# 🔐 Application Registration Required")
    st.markdown("---")
    
    st.warning("⚠️ This application requires registration before use. Please enter your organization details below.")
    st.markdown("")
    
    st.markdown("### Organization Information")
    st.markdown(f"**Application:** {APP_NAME}")
    st.markdown(f"**Version:** {APP_VERSION}")
    st.markdown(f"**Developer:** Odysseus-imc Pty Ltd & Cambia Consulting Pty Ltd")
    st.markdown("---")
    
    with st.form("registration_form"):
        st.subheader("Registration Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            authority_name = st.text_input(
                "Authority/Organization Name *",
                help="Full legal name of your organization",
                placeholder="e.g., Murrumbidgee Irrigation"
            )
            
            department = st.text_input(
                "Department/Division *",
                help="Department using this application",
                placeholder="e.g., Asset Management Department"
            )
            
            contact_person = st.text_input(
                "Contact Person Name *",
                help="Primary contact person for this registration",
                placeholder="e.g., John Smith"
            )
        
        with col2:
            contact_email = st.text_input(
                "Contact Email *",
                help="Email address for application support and updates",
                placeholder="e.g., john.smith@organization.com"
            )
            
            phone = st.text_input(
                "Phone Number",
                help="Contact phone number (optional)",
                placeholder="e.g., +61 2 1234 5678"
            )
            
            address = st.text_area(
                "Organization Address",
                help="Physical or postal address (optional)",
                placeholder="Street, City, State, Postcode"
            )
        
        st.markdown("")
        st.markdown("**Fields marked with * are required**")
        st.markdown("")
        
        col_a, col_b, col_c = st.columns([1, 1, 2])
        with col_a:
            submit = st.form_submit_button("✅ Register Application", type="primary", use_container_width=True)
        
        if submit:
            # Validate required fields
            if not authority_name or not authority_name.strip():
                st.error("❌ Authority/Organization Name is required")
            elif not department or not department.strip():
                st.error("❌ Department/Division is required")
            elif not contact_person or not contact_person.strip():
                st.error("❌ Contact Person Name is required")
            elif not contact_email or not contact_email.strip():
                st.error("❌ Contact Email is required")
            elif '@' not in contact_email:
                st.error("❌ Please enter a valid email address")
            else:
                # Save registration
                if save_registration(
                    authority_name.strip(),
                    department.strip(),
                    contact_person.strip(),
                    contact_email.strip(),
                    phone.strip() if phone else '',
                    address.strip() if address else ''
                ):
                    st.success("✅ Registration successful! Reloading application...")
                    st.balloons()
                    # Force reload to apply registration
                    st.rerun()
    
    st.markdown("---")
    st.markdown("")
    st.info("📧 For registration assistance, contact: sm@odysseus-imc.com")
    st.markdown("")
    st.markdown("")
    
    # Prevent any other content from showing
    st.stop()

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
    
    # Administration Section - Only visible to Administrators and Super Users
    if can_access_administration():
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚙️ Administration")
        
        if st.sidebar.button("🔧 Administration", key="nav_admin", use_container_width=True):
            st.session_state.current_view = 'administration'
            st.rerun()
    
    # Data Management Section
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
    
    # Application Information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Application Info")
    with st.sidebar.expander("Details"):
        st.markdown(f"**Authority:** {REGISTERED_AUTHORITY}")
        st.markdown(f"**Department:** {REGISTERED_DEPARTMENT}")
        if REGISTERED_CONTACT:
            st.markdown(f"**Contact Person:** {REGISTERED_CONTACT}")
        if REGISTERED_EMAIL:
            st.markdown(f"**Contact Email:** {REGISTERED_EMAIL}")
        st.markdown(f"**Version:** {APP_VERSION}")
        if REGISTERED_DATE:
            # Format the ISO date to be more readable
            try:
                from datetime import datetime
                reg_date_obj = datetime.fromisoformat(REGISTERED_DATE)
                formatted_date = reg_date_obj.strftime('%d %B %Y')
                st.markdown(f"**Registration Date:** {formatted_date}")
            except:
                st.markdown(f"**Registration Date:** {REGISTERED_DATE}")

# Restore autosave once per session (not on every page render)
if not st.session_state.autorestore_attempted:
    restore_session_data()
    st.session_state.autorestore_attempted = True

# Registration Check - Must be registered to use the application
if not is_registered():
    show_registration_form()
    # st.stop() is called in show_registration_form() to prevent further execution

# Initialize user database with default admin user
initialize_users_db()

# User Authentication Check - Must be logged in after registration
if not is_user_logged_in():
    show_login_form()
    # st.stop() is called in show_login_form() to prevent further execution

# Load registration details for display (no fallback to config.ini)
registration_info = get_registration_details()
REGISTERED_AUTHORITY = registration_info.get('authority_name', 'Not Registered')
REGISTERED_DEPARTMENT = registration_info.get('department', 'Not Registered')
REGISTERED_CONTACT = registration_info.get('contact_person', '')
REGISTERED_EMAIL = registration_info.get('contact_email', '')
REGISTERED_DATE = registration_info.get('registration_date', '')

sidebar_navigation()

# Add logout button to sidebar
show_logout_button()

# Main content area
st.markdown("# 🔧 FMECA & RCM Analysis Tool")
st.markdown("""This tool provides a systematic approach to Failure Mode, Effects and Criticality Analysis (FMECA) 
and Reliability Centered Maintenance (RCM) for infrastructure assets. Identify failure modes, assess criticality, 
and develop optimal maintenance strategies.""")
st.markdown("")
st.markdown(f"""**Developed by:** Odysseus-imc Pty Ltd  
**Technical expertise by:** Cambia Consulting Pty Ltd  
**Registered to:** {REGISTERED_AUTHORITY}  
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
    st.markdown(f"""**Software Support:** {config_data['SOFTWARE_CONTACT']}  
**Technical Support:** {config_data['TECHNICAL_CONTACT']}""")

elif st.session_state.current_view == 'administration':
    # Administration page - Verify user has access
    if not can_access_administration():
        st.error("❌ Access Denied: You do not have permission to access the Administration section.")
        st.info("Only Administrators and Super Users can access Administration. Please contact your Administrator if you need access.")
        st.stop()
    
    # Administration page
    st.markdown("### ⚙️ Administration")
    st.markdown("")
    
    st.info("Use this section to configure application settings and parameters.")
    st.markdown("")
    
    # Administration options dropdown
    admin_options = ["Select...", "Configure Risk Matrix"]
    
    # Only Administrators can manage users
    if is_administrator():
        admin_options.append("Manage Users")
    
    admin_option = st.selectbox(
        "Select Administration Task",
        admin_options,
        key="admin_task_selector"
    )
    
    if admin_option == "Configure Risk Matrix":
        st.markdown("---")
        st.markdown("### 📊 Configure Risk Matrix")
        st.markdown("")
        
        st.markdown("""Configure the risk scoring thresholds and categories for the Risk Matrix used throughout 
        the application. These settings determine how risk scores are classified and displayed.""")
        st.markdown("")
        
        # Current configuration display
        st.markdown("#### Current Configuration")
        col1, col2, col3 = st.columns(3)
        
        # Get current thresholds
        current_moderate = st.session_state.risk_moderate_threshold
        current_high = st.session_state.risk_high_threshold
        
        with col1:
            st.markdown("**Low Risk**")
            st.markdown("- Color: Green")
            st.markdown(f"- Score Range: 2-{current_moderate-1}")
        
        with col2:
            st.markdown("**Moderate Risk**")
            st.markdown("- Color: Orange")
            st.markdown(f"- Score Range: {current_moderate}-{current_high-1}")
        
        with col3:
            st.markdown("**High Risk**")
            st.markdown("- Color: Red")
            st.markdown(f"- Score Range: {current_high}-10")
        
        st.markdown("")
        st.markdown("---")
        st.markdown("#### Configure Risk Thresholds")
        st.markdown("")
        
        st.warning("⚠️ Changing these thresholds will affect how risks are classified throughout the application.")
        st.markdown("")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            moderate_threshold = st.number_input(
                "Moderate Risk Threshold (minimum score)",
                min_value=2,
                max_value=9,
                value=st.session_state.risk_moderate_threshold,
                help="Risk scores at or above this value are classified as Moderate"
            )
        
        with col_b:
            high_threshold = st.number_input(
                "High Risk Threshold (minimum score)",
                min_value=3,
                max_value=10,
                value=st.session_state.risk_high_threshold,
                help="Risk scores at or above this value are classified as High"
            )
        
        st.markdown("")
        
        # Validation
        if high_threshold <= moderate_threshold:
            st.error("❌ High Risk threshold must be greater than Moderate Risk threshold!")
        else:
            st.success("✅ Valid threshold configuration")
            
            # Preview the new configuration
            st.markdown("")
            st.markdown("#### Preview New Configuration")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Low Risk**")
                st.markdown("- Color: Green")
                st.markdown(f"- Score Range: 2-{moderate_threshold-1}")
            
            with col2:
                st.markdown("**Moderate Risk**")
                st.markdown("- Color: Orange")
                st.markdown(f"- Score Range: {moderate_threshold}-{high_threshold-1}")
            
            with col3:
                st.markdown("**High Risk**")
                st.markdown("- Color: Red")
                st.markdown(f"- Score Range: {high_threshold}-10")
            
            st.markdown("")
            st.markdown("")
            
            # Save button
            col_save, col_reset = st.columns([1, 1])
            
            with col_save:
                if st.button("💾 Save Configuration", type="primary", use_container_width=True):
                    st.session_state.risk_moderate_threshold = moderate_threshold
                    st.session_state.risk_high_threshold = high_threshold
                    st.success(f"✅ Risk matrix configuration saved! Moderate≥{moderate_threshold}, High≥{high_threshold}")
                    st.info("Risk Matrix and classification logic have been updated throughout the application.")
                    st.balloons()
                    # Force rerun to apply changes
                    time.sleep(1)
                    st.rerun()
            
            with col_reset:
                if st.button("🔄 Reset to Default", use_container_width=True):
                    st.session_state.risk_moderate_threshold = 6
                    st.session_state.risk_high_threshold = 8
                    st.info("ℹ️ Configuration reset to default values: Moderate=6, High=8")
                    st.rerun()
        
        st.markdown("")
        st.markdown("---")
        st.markdown("")
        st.success("""**Configuration Active:** Risk thresholds are now fully customizable. 
        Changes will be applied immediately to all risk assessments, the Risk Matrix display, and consequence category classifications throughout the application.""")
    
    elif admin_option == "Manage Users":
        st.markdown("---")
        st.markdown("### 👥 Manage Users")
        st.markdown("")
        
        st.markdown("""Manage user accounts and assign user types. Only Administrators can change user types. 
        Super Users can only be designated by Administrators.""")
        st.markdown("")
        
        # Load all users
        users = load_users()
        
        if not users:
            st.warning("⚠️ No users found in the system.")
        else:
            # Display current user type info
            st.markdown("#### User Type Descriptions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**👤 User**")
                st.markdown("- Default user type")
                st.markdown("- Can use RCM analysis features")
                st.markdown("- Cannot access Administration")
            
            with col2:
                st.markdown("**⚙️ Super User**")
                st.markdown("- Advanced user type")
                st.markdown("- Can use RCM analysis features")
                st.markdown("- Can access Administration")
                st.markdown("- Must be designated by Administrator")
            
            with col3:
                st.markdown("**🔐 Administrator**")
                st.markdown("- Highest privilege level")
                st.markdown("- Full access to all features")
                st.markdown("- Can access Administration")
                st.markdown("- Can manage user types")
            
            st.markdown("")
            st.markdown("---")
            st.markdown("#### User List and Management")
            st.markdown("")
            
            # Create a table of users with their information
            user_data = []
            for username, user_info in users.items():
                # Format last login date
                last_login = user_info.get('last_login', 'Never')
                if last_login != 'Never':
                    try:
                        last_login = last_login[:10]  # Just the date part
                    except:
                        last_login = 'N/A'
                
                user_data.append({
                    "Username": username,
                    "Full Name": user_info.get('full_name', 'N/A'),
                    "Position": user_info.get('position', 'N/A'),
                    "User Type": user_info.get('user_type', 'User'),
                    "Login Count": user_info.get('login_count', 0),
                    "Last Login": last_login,
                    "Created": user_info.get('created_date', 'N/A')[:10] if user_info.get('created_date') else 'N/A'
                })
            
            # Display as dataframe
            df_users = pd.DataFrame(user_data)
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            
            st.markdown("")
            st.markdown("---")
            st.markdown("#### Change User Type")
            st.markdown("")
            
            # User selection and type change interface
            col_user, col_type = st.columns([2, 1])
            
            with col_user:
                # Filter out admin from the list
                regular_users = {k: v for k, v in users.items() if k != "admin"}
                
                if not regular_users:
                    st.info("ℹ️ No regular users to manage. Only the default admin account exists.")
                else:
                    selected_username = st.selectbox(
                        "Select User to Modify",
                        options=list(regular_users.keys()),
                        format_func=lambda x: f"{x} ({regular_users[x].get('full_name', 'N/A')}) - Current: {regular_users[x].get('user_type', 'User')}",
                        key="user_select"
                    )
                    
                    with col_type:
                        new_user_type = st.selectbox(
                            "New User Type",
                            options=["User", "Super User", "Administrator"],
                            key="new_user_type"
                        )
                    
                    st.markdown("")
                    
                    # Show current vs new
                    if selected_username:
                        current_type = regular_users[selected_username].get('user_type', 'User')
                        
                        if current_type != new_user_type:
                            st.warning(f"⚠️ You are about to change **{selected_username}**'s user type from **{current_type}** to **{new_user_type}**")
                            
                            col_confirm, col_cancel = st.columns([1, 2])
                            
                            with col_confirm:
                                if st.button("✅ Confirm Change", type="primary", use_container_width=True, key="confirm_change"):
                                    success, message = update_user_type(selected_username, new_user_type)
                                    
                                    if success:
                                        st.success(f"✅ {message}")
                                        st.balloons()
                                        time.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {message}")
                        else:
                            st.info(f"ℹ️ User **{selected_username}** is already a **{current_type}**")
            
            st.markdown("")
            st.markdown("---")
            st.info("""**Note:** The default 'admin' account cannot be modified and will always remain as Administrator. 
            Changes to user types take effect immediately but require the affected user to log out and log back in to see updated permissions.""")

# Render current stage content based on sidebar selection
st.markdown("---")

# Stage function definitions
# Stage 1: Planning and Preparation
def stage_1_planning():
    """Stage 1: Planning and Preparation"""
    st.markdown("## Stage 1: Planning and Preparation")
    st.markdown("")
    st.markdown("**Objective:** Define the project scope and manage assets for RCM analysis.")
    
    # Project Information Section
    st.markdown("### 📁 Project Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_no = st.text_input(
            "Project No.",
            value=st.session_state.project_data.get('project_no', ''),
            help="Unique project identifier (e.g., RCM-2024-001)"
        )
    
    with col2:
        project_description = st.text_input(
            "Project Description",
            value=st.session_state.project_data.get('project_description', ''),
            help="Brief description of the RCM project"
        )
    
    if st.button("💾 Save Project Information", type="primary"):
        st.session_state.project_data = {
            'project_no': project_no,
            'project_description': project_description,
            'created_date': st.session_state.project_data.get('created_date', datetime.now().isoformat()),
            'last_modified': datetime.now().isoformat()
        }
        autosave_session_data()
        st.success(f"✅ Project '{project_no}' saved!")
    
    if not st.session_state.project_data.get('project_no'):
        st.warning("⚠️ Please enter Project No. and save project information before adding assets.")
        return
    
    # Assets Management Section
    st.markdown("---")
    st.markdown(f"### 🏭 Assets in Project: {st.session_state.project_data.get('project_no', '')}")
    
    # Display existing assets
    if st.session_state.assets:
        st.markdown("**Existing Assets:**")
        for idx, asset in enumerate(st.session_state.assets):
            col_a, col_b, col_c, col_d = st.columns([3, 2, 1, 1])
            with col_a:
                st.write(f"**{idx + 1}.** {asset['asset_name']}")
            with col_b:
                st.write(f"_{asset['asset_class']}_")
            with col_c:
                if st.button("✏️ Edit", key=f"edit_asset_{idx}"):
                    st.session_state.current_asset_index = idx
                    st.session_state.editing_component = None  # Clear component editing
                    st.rerun()
            with col_d:
                if st.button("🗑️ Del", key=f"del_asset_{idx}"):
                    # Check if asset has components
                    components = asset.get('components', [])
                    if components:
                        st.error(f"⚠️ Cannot delete asset. Please delete all {len(components)} component(s) first to avoid orphaned data.")
                    else:
                        st.session_state.assets.pop(idx)
                        if st.session_state.current_asset_index == idx:
                            st.session_state.current_asset_index = None
                        autosave_session_data()
                        st.rerun()
            
            # Display components under each asset with Edit/Delete buttons
            components = asset.get('components', [])
            if components:
                st.markdown(f"   **Components ({len(components)}):**")
                for comp_idx, comp in enumerate(components):
                    col_comp_a, col_comp_b, col_comp_c, col_comp_d = st.columns([3, 2, 1, 1])
                    with col_comp_a:
                        st.write(f"      • {comp}")
                    with col_comp_b:
                        st.write("")  # Empty to maintain alignment
                    with col_comp_c:
                        if st.button("✏️ Edit", key=f"edit_comp_{idx}_{comp_idx}"):
                            st.session_state.editing_component = {
                                'asset_idx': idx,
                                'comp_idx': comp_idx,
                                'comp_name': comp
                            }
                            st.session_state.current_asset_index = None  # Clear asset editing
                            st.rerun()
                    with col_comp_d:
                        if st.button("🗑️ Del", key=f"del_comp_{idx}_{comp_idx}"):
                            st.session_state.assets[idx]['components'].pop(comp_idx)
                            autosave_session_data()
                            st.success(f"✅ Component '{comp}' deleted!")
                            st.rerun()
            else:
                st.markdown(f"   _No components defined_")
            
            # Add horizontal divider after each asset
            st.markdown("---")
    else:
        st.info("No assets added yet. Click 'Add New Asset' to begin.")
    
    # Component Editing Section
    if 'editing_component' in st.session_state and st.session_state.editing_component:
        st.markdown("---")
        st.markdown("### ✏️ Edit Component")
        
        edit_info = st.session_state.editing_component
        asset_idx = edit_info['asset_idx']
        comp_idx = edit_info['comp_idx']
        comp_name = edit_info['comp_name']
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_comp_name = st.text_input(
                "Component Name",
                value=comp_name,
                key="editing_comp_name"
            )
        with col2:
            if st.button("💾 Save", type="primary", use_container_width=True):
                if new_comp_name and new_comp_name.strip():
                    st.session_state.assets[asset_idx]['components'][comp_idx] = new_comp_name.strip()
                    autosave_session_data()
                    st.session_state.editing_component = None
                    st.success(f"✅ Component updated!")
                    st.rerun()
                else:
                    st.error("Component name cannot be empty")
        with col3:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.editing_component = None
                st.rerun()
    
    # Add/Edit Asset Section
    st.markdown("---")
    
    # Check if we're editing an existing asset
    if st.session_state.current_asset_index is not None:
        st.markdown(f"### ✏️ Edit Asset #{st.session_state.current_asset_index + 1}")
        current_asset = st.session_state.assets[st.session_state.current_asset_index]
    else:
        st.markdown("### ➕ Add New Asset")
        current_asset = {'asset_name': '', 'asset_class': 'Select...', 'asset_type': '', 
                        'site_location': '', 'components': [], 'operating_context': {}}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Asset Identification")
        
        asset_name = st.text_input(
            "Asset Name/ID",
            value=current_asset.get('asset_name', ''),
            help="e.g., Tharbogang PS2 - Jockey Pump Assembly 1",
            key="edit_asset_name" if st.session_state.current_asset_index is not None else "new_asset_name"
        )
        
        asset_classes = ["Select...", "Pump Station", "Water Treatment Plant", "Pipeline System", 
                        "Storage Tank", "Distribution Network", "Control System", "Other"]
        current_class = current_asset.get('asset_class', 'Select...')
        try:
            class_index = asset_classes.index(current_class)
        except ValueError:
            class_index = 0
        
        asset_class = st.selectbox(
            "Asset Class",
            asset_classes,
            index=class_index,
            key="edit_asset_class" if st.session_state.current_asset_index is not None else "new_asset_class"
        )
        
        asset_type = st.text_input(
            "Asset Type/Sub-Class",
            value=current_asset.get('asset_type', ''),
            help="e.g., Centrifugal Pump Assembly, VFD Motor",
            key="edit_asset_type" if st.session_state.current_asset_index is not None else "new_asset_type"
        )
        
        site_location = st.text_input(
            "Site Location",
            value=current_asset.get('site_location', ''),
            help="Physical location of the asset",
            key="edit_site_location" if st.session_state.current_asset_index is not None else "new_site_location"
        )
    
    with col2:
        st.subheader("Components")
        st.markdown("Define the components of this asset:")
        
        # Get current components
        if 'temp_components' not in st.session_state or st.session_state.get('temp_asset_index') != st.session_state.current_asset_index:
            st.session_state.temp_components = current_asset.get('components', []).copy()
            st.session_state.temp_asset_index = st.session_state.current_asset_index
        
        new_component = st.text_input("Add Component", key="temp_new_component")
        if st.button("➕ Add Component"):
            if new_component and new_component not in st.session_state.temp_components:
                st.session_state.temp_components.append(new_component)
                st.success(f"Added: {new_component}")
                st.rerun()
        
        if st.session_state.temp_components:
            st.markdown("**Current Components:**")
            for i, comp in enumerate(st.session_state.temp_components):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"• {comp}")
                with col_b:
                    if st.button("🗑️", key=f"del_temp_comp_{i}"):
                        st.session_state.temp_components.pop(i)
                        st.rerun()
    
    # Save or Update Asset Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state.current_asset_index is not None:
            if st.button("💾 Update Asset", type="primary", use_container_width=True):
                if asset_name and asset_class != "Select...":
                    st.session_state.assets[st.session_state.current_asset_index] = {
                        'asset_name': asset_name,
                        'asset_class': asset_class,
                        'asset_type': asset_type,
                        'site_location': site_location,
                        'components': st.session_state.temp_components.copy(),
                        'operating_context': current_asset.get('operating_context', {}),
                        'functions': current_asset.get('functions', []),
                        'functional_failures': current_asset.get('functional_failures', []),
                        'failure_modes': current_asset.get('failure_modes', []),
                        'analysis_results': current_asset.get('analysis_results', [])
                    }
                    # Clear cached asset data to force reload with new asset name
                    if 'last_loaded_asset' in st.session_state:
                        del st.session_state.last_loaded_asset
                    st.session_state.current_asset_index = None
                    st.session_state.temp_components = []
                    st.session_state.editing_component = None
                    autosave_session_data()
                    st.success("✅ Asset updated!")
                    st.rerun()
                else:
                    st.error("Please fill in Asset Name and Asset Class")
        else:
            if st.button("💾 Save New Asset", type="primary", use_container_width=True):
                if asset_name and asset_class != "Select...":
                    st.session_state.assets.append({
                        'asset_name': asset_name,
                        'asset_class': asset_class,
                        'asset_type': asset_type,
                        'site_location': site_location,
                        'components': st.session_state.temp_components.copy(),
                        'operating_context': {},
                        'functions': [],
                        'functional_failures': [],
                        'failure_modes': [],
                        'analysis_results': []
                    })
                    st.session_state.temp_components = []
                    st.session_state.editing_component = None
                    autosave_session_data()
                    st.success(f"✅ Asset '{asset_name}' added to project!")
                    st.rerun()
                else:
                    st.error("Please fill in Asset Name and Asset Class")
    
    with col2:
        if st.session_state.current_asset_index is not None:
            if st.button("❌ Cancel Edit", use_container_width=True):
                st.session_state.current_asset_index = None
                st.session_state.temp_components = []
                st.session_state.editing_component = None
                st.rerun()
    
    # Proceed to next stage
    if st.session_state.assets:
        st.markdown("---")
        st.success(f"✅ Project has {len(st.session_state.assets)} asset(s). You can proceed to Stage 2 for RCM analysis.")
        if st.button("➡️ Proceed to Stage 2: RCM Analysis", key="proceed_green", use_container_width=True):
            st.session_state.current_stage = 2
            st.rerun()

# Stage 2: RCM Analysis (FMECA)
def stage_2_analysis():
    """Stage 2: RCM Analysis"""
    st.markdown("## Stage 2: RCM Analysis (FMECA)")
    st.markdown("")
    
    # Check if project and assets exist
    if not st.session_state.project_data.get('project_no'):
        st.warning("⚠️ Please complete Stage 1: Planning and Preparation first!")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    if not st.session_state.assets:
        st.warning("⚠️ No assets found in this project. Please add assets in Stage 1.")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    # Asset Selection
    st.markdown(f"### 📁 Project: {st.session_state.project_data['project_no']} - {st.session_state.project_data.get('project_description', '')}")
    
    asset_options = [f"{i+1}. {asset['asset_name']} ({asset['asset_class']})" 
                     for i, asset in enumerate(st.session_state.assets)]
    
    # Initialize or get selected asset for analysis
    if 'selected_analysis_asset' not in st.session_state:
        st.session_state.selected_analysis_asset = 0
    
    selected_option = st.selectbox(
        "Select Asset for Analysis",
        options=range(len(asset_options)),
        format_func=lambda x: asset_options[x],
        index=st.session_state.selected_analysis_asset,
        key="asset_selector_stage2"
    )
    
    st.session_state.selected_analysis_asset = selected_option
    current_asset = st.session_state.assets[selected_option]
    
    st.markdown(f"**Analyzing Asset:** {current_asset['asset_name']}")
    
    # Load asset-specific data into session for analysis
    # This maintains compatibility with existing analysis code
    if 'components' not in st.session_state or st.session_state.get('last_loaded_asset') != selected_option:
        st.session_state.components = current_asset.get('components', [])
        st.session_state.functions = current_asset.get('functions', [])
        st.session_state.functional_failures = current_asset.get('functional_failures', [])
        st.session_state.failure_modes = current_asset.get('failure_modes', [])
        st.session_state.analysis_results = current_asset.get('analysis_results', [])
        st.session_state.operating_context = current_asset.get('operating_context', {})
        st.session_state.last_loaded_asset = selected_option
    
    st.markdown("---")
    
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
                save_asset_analysis_data()
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
                save_asset_analysis_data()
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
            
            # Filter failures for selected function
            function_failures = [f for f in st.session_state.functional_failures if f['function_id'] == func_id]
            
            failure_description = st.text_area(
                "Describe the Functional Failure",
                help="How does the asset fail to meet this function?",
                key="ff_description_input"
            )
            
            failure_category = st.radio(
                "Failure Category",
                ["Complete loss of function", "Partial loss of function", "Exceeds upper limit", "Below lower limit"]
            )
            
            # Add button
            if st.button("➕ Add Functional Failure", use_container_width=True):
                if failure_description:
                    failure = {
                        'id': f"FF-{func_id}.{len([f for f in st.session_state.functional_failures if f['function_id'] == func_id]) + 1}",
                        'function_id': func_id,
                        'function_statement': next(f['full_statement'] for f in st.session_state.functions if f['id'] == func_id),
                        'description': failure_description,
                        'category': failure_category
                    }
                    st.session_state.functional_failures.append(failure)
                    save_asset_analysis_data()
                    st.success(f"✅ Functional Failure {failure['id']} added!")
                    st.rerun()
            
            # Display table with selection
            if function_failures:
                st.markdown("---")
                st.subheader(f"View, Update or Delete Functional Failures for Function {func_id}")
                
                # Create selection interface using radio buttons
                failure_options = ["None"] + [f"{f['id']}: {f['description']}" for f in function_failures]
                selected_failure = st.radio(
                    "Select a Functional Failure to Update or Delete:",
                    failure_options,
                    key="ff_selection"
                )
                
                # Display table
                failures_df = pd.DataFrame(function_failures)
                st.dataframe(failures_df, use_container_width=True)
                
                # Show Update/Delete options if a failure is selected
                if selected_failure != "None":
                    selected_idx = failure_options.index(selected_failure) - 1
                    current_failure = function_failures[selected_idx]
                    # Find index in full list
                    failure_idx = next(i for i, f in enumerate(st.session_state.functional_failures) if f['id'] == current_failure['id'])
                    
                    # Update Section
                    if not st.session_state.get('editing_functional_failure', False):
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Update Selected", use_container_width=True):
                                st.session_state.editing_functional_failure = True
                                st.rerun()
                        with col_action2:
                            if st.button("🗑️ Delete Selected", use_container_width=True):
                                st.session_state.deleting_functional_failure = True
                                st.rerun()
                    
                    # Update Form
                    if st.session_state.get('editing_functional_failure', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Update Functional Failure")
                        
                        updated_description = st.text_area(
                            "Update Description",
                            value=current_failure['description'],
                            key="update_ff_desc"
                        )
                        
                        updated_category = st.radio(
                            "Update Category",
                            ["Complete loss of function", "Partial loss of function", "Exceeds upper limit", "Below lower limit"],
                            index=["Complete loss of function", "Partial loss of function", "Exceeds upper limit", "Below lower limit"].index(current_failure['category']),
                            key="update_ff_cat"
                        )
                        
                        col_update1, col_update2 = st.columns(2)
                        with col_update1:
                            if st.button("💾 Save Update", type="primary", use_container_width=True):
                                if updated_description:
                                    st.session_state.functional_failures[failure_idx]['description'] = updated_description
                                    st.session_state.functional_failures[failure_idx]['category'] = updated_category
                                    st.session_state.editing_functional_failure = False
                                    save_asset_analysis_data()
                                    st.success(f"✅ Functional Failure {current_failure['id']} updated!")
                                    st.rerun()
                                else:
                                    st.error("Description cannot be empty")
                        with col_update2:
                            if st.button("❌ Cancel Update", use_container_width=True):
                                st.session_state.editing_functional_failure = False
                                st.rerun()
                    
                    # Delete Confirmation
                    if st.session_state.get('deleting_functional_failure', False):
                        st.markdown("---")
                        st.markdown("### 🗑️ Delete Functional Failure")
                        st.warning("⚠️ Warning: Deleting a functional failure will also delete all associated failure modes!")
                        
                        # Count associated failure modes
                        associated_modes = [fm for fm in st.session_state.failure_modes if fm.get('failure_id') == current_failure['id']]
                        
                        if associated_modes:
                            st.info(f"ℹ️ This will delete {len(associated_modes)} associated failure mode(s)")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True):
                                # Delete associated failure modes
                                st.session_state.failure_modes = [fm for fm in st.session_state.failure_modes 
                                                                  if fm.get('failure_id') != current_failure['id']]
                                # Delete the functional failure
                                st.session_state.functional_failures.pop(failure_idx)
                                st.session_state.deleting_functional_failure = False
                                save_asset_analysis_data()
                                st.success(f"✅ Functional Failure {current_failure['id']} deleted!")
                                st.rerun()
                        with col_del2:
                            if st.button("❌ Cancel Delete", use_container_width=True):
                                st.session_state.deleting_functional_failure = False
                                st.rerun()
    
    # Step 4: Failure Modes
    with analysis_tab[2]:
        st.subheader("Step 4: Identify Failure Modes")
        
        st.markdown("**Failure Mode:** Any event which causes a functional failure.")
        st.markdown("**Format:** [Component] + [What went wrong] + [Why/Cause if known]")
        st.markdown("**Example:** 'Pump impeller worn due to normal wear'")
        
        if not st.session_state.functional_failures:
            st.warning("⚠️ Please define functional failures first (Step 3)")
        else:
            # Show available components info
            available_components = st.session_state.get('components', [])
            if available_components:
                st.info(f"ℹ️ {len(available_components)} component(s) available for this asset")
            else:
                st.warning("⚠️ No components defined for this asset. Please add components in Stage 1.")
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
            
            # Get components for the selected asset
            available_components = st.session_state.get('components', [])
            if available_components:
                component_options = ["Select..."] + available_components
            else:
                component_options = ["Define components in Stage 1"]
            
            component = st.selectbox(
                "Component",
                component_options
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
            
            # Filter failure modes for selected functional failure
            functional_failure_modes = [m for m in st.session_state.failure_modes if m.get('functional_failure_id') == failure_id]
            
            # Add button
            if st.button("➕ Add Failure Mode", use_container_width=True):
                if component == "Define components in Stage 1":
                    st.error("⚠️ Please define components in Stage 1 first")
                elif component == "Select...":
                    st.error("⚠️ Please select a component")
                elif not failure_mode_desc:
                    st.error("⚠️ Please enter a failure mode description")
                else:
                    mode = {
                        'id': f"FM-{failure_id}-{len(functional_failure_modes) + 1}",
                        'functional_failure_id': failure_id,
                        'component': component,
                        'description': failure_mode_desc,
                        'category': failure_mode_category
                    }
                    st.session_state.failure_modes.append(mode)
                    save_asset_analysis_data()
                    st.success(f"✅ Failure Mode {mode['id']} added!")
                    st.rerun()
            
            # Display table with selection
            if functional_failure_modes:
                st.markdown("---")
                st.subheader(f"View, Update or Delete Failure Modes for Functional Failure {failure_id}")
                
                # Create selection interface using radio buttons
                mode_options = ["None"] + [f"{m['id']}: {m['component']} - {m['description']}" for m in functional_failure_modes]
                selected_mode = st.radio(
                    "Select a Failure Mode to Update or Delete:",
                    mode_options,
                    key="fm_selection"
                )
                
                # Display table
                modes_df = pd.DataFrame(functional_failure_modes)
                st.dataframe(modes_df, use_container_width=True)
                
                # Show Update/Delete options if a mode is selected
                if selected_mode != "None":
                    selected_idx = mode_options.index(selected_mode) - 1
                    current_mode = functional_failure_modes[selected_idx]
                    # Find index in full list
                    mode_idx = next(i for i, m in enumerate(st.session_state.failure_modes) if m['id'] == current_mode['id'])
                    
                    # Update Section
                    if not st.session_state.get('editing_failure_mode', False):
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Update Selected", use_container_width=True, key="update_fm_btn"):
                                st.session_state.editing_failure_mode = True
                                st.rerun()
                        with col_action2:
                            if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_fm_btn"):
                                st.session_state.deleting_failure_mode = True
                                st.rerun()
                    
                    # Update Form
                    if st.session_state.get('editing_failure_mode', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Update Failure Mode")
                        
                        # Get components for the selected asset
                        available_components_update = st.session_state.get('components', [])
                        if available_components_update:
                            component_options_update = ["Select..."] + available_components_update
                            current_comp_idx = component_options_update.index(current_mode['component']) if current_mode['component'] in component_options_update else 0
                        else:
                            component_options_update = ["Define components in Stage 1"]
                            current_comp_idx = 0
                        
                        updated_component = st.selectbox(
                            "Update Component",
                            component_options_update,
                            index=current_comp_idx,
                            key="update_fm_comp"
                        )
                        
                        updated_description = st.text_area(
                            "Update Description",
                            value=current_mode['description'],
                            key="update_fm_desc"
                        )
                        
                        updated_category = st.selectbox(
                            "Update Category",
                            ["Select...", "Deterioration (wear, corrosion, fatigue)", 
                             "Lubrication failure", "Dirt/contamination", "Disassembly (loose connections)",
                             "Human error", "Overloading", "Other"],
                            index=["Select...", "Deterioration (wear, corrosion, fatigue)", 
                                   "Lubrication failure", "Dirt/contamination", "Disassembly (loose connections)",
                                   "Human error", "Overloading", "Other"].index(current_mode['category']) if current_mode['category'] in ["Select...", "Deterioration (wear, corrosion, fatigue)", 
                                   "Lubrication failure", "Dirt/contamination", "Disassembly (loose connections)",
                                   "Human error", "Overloading", "Other"] else 0,
                            key="update_fm_cat"
                        )
                        
                        col_update1, col_update2 = st.columns(2)
                        with col_update1:
                            if st.button("💾 Save Update", type="primary", use_container_width=True, key="save_fm_update"):
                                if updated_component == "Select..." or updated_component == "Define components in Stage 1":
                                    st.error("Please select a valid component")
                                elif not updated_description:
                                    st.error("Description cannot be empty")
                                else:
                                    st.session_state.failure_modes[mode_idx]['component'] = updated_component
                                    st.session_state.failure_modes[mode_idx]['description'] = updated_description
                                    st.session_state.failure_modes[mode_idx]['category'] = updated_category
                                    st.session_state.editing_failure_mode = False
                                    save_asset_analysis_data()
                                    st.success(f"✅ Failure Mode {current_mode['id']} updated!")
                                    st.rerun()
                        with col_update2:
                            if st.button("❌ Cancel Update", use_container_width=True, key="cancel_fm_update"):
                                st.session_state.editing_failure_mode = False
                                st.rerun()
                    
                    # Delete Confirmation
                    if st.session_state.get('deleting_failure_mode', False):
                        st.markdown("---")
                        st.markdown("### 🗑️ Delete Failure Mode")
                        st.warning("⚠️ Warning: This will delete the selected failure mode!")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True, key="confirm_fm_delete"):
                                # Delete the failure mode
                                st.session_state.failure_modes.pop(mode_idx)
                                st.session_state.deleting_failure_mode = False
                                save_asset_analysis_data()
                                st.success(f"✅ Failure Mode {current_mode['id']} deleted!")
                                st.rerun()
                        with col_del2:
                            if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_fm_delete"):
                                st.session_state.deleting_failure_mode = False
                                st.rerun()
    
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
            
            # Check if effects already exist for this failure mode
            current_mode = next((m for m in st.session_state.failure_modes if m['id'] == mode_id), None)
            has_effects = current_mode and 'effects' in current_mode
            
            # Add button
            if st.button("➕ Add Failure Effect", use_container_width=True):
                if not evidence:
                    st.error("⚠️ Please enter evidence of failure")
                else:
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
                            save_asset_analysis_data()
                            st.success(f"✅ Failure effects added to {mode_id}")
                            st.rerun()
            
            # Display table with selection for failure modes with effects
            modes_with_effects = [m for m in st.session_state.failure_modes if 'effects' in m]
            
            if modes_with_effects:
                st.markdown("---")
                st.subheader(f"View, Update or Delete Failure Effects")
                
                # Create selection interface using radio buttons
                effect_options = ["None"] + [f"{m['id']}: {m['component']} - {m['description']}" for m in modes_with_effects]
                selected_effect = st.radio(
                    "Select a Failure Mode to View, Update or Delete its Effects:",
                    effect_options,
                    key="effect_selection"
                )
                
                # Display table of failure modes with effects
                effects_display = []
                for m in modes_with_effects:
                    effects_display.append({
                        'Failure Mode ID': m['id'],
                        'Component': m['component'],
                        'Description': m['description'],
                        'Evidence': m['effects'].get('evidence', 'N/A'),
                        'Safety Impact': m['effects'].get('safety_impact', 'N/A'),
                        'Operational Impact': m['effects'].get('operational_impact', 'N/A'),
                        'Physical Damage': m['effects'].get('physical_damage', 'N/A'),
                        'Repair Action': m['effects'].get('repair_action', 'N/A'),
                        'Repair Time (hrs)': m['effects'].get('repair_time', 0),
                        'Downtime (hrs)': m['effects'].get('downtime', 0)
                    })
                effects_df = pd.DataFrame(effects_display)
                st.dataframe(effects_df, use_container_width=True, height=400)
                
                # Show Update/Delete options if an effect is selected
                if selected_effect != "None":
                    selected_mode_id = selected_effect.split(":")[0]
                    selected_mode = next(m for m in modes_with_effects if m['id'] == selected_mode_id)
                    mode_idx = next(i for i, m in enumerate(st.session_state.failure_modes) if m['id'] == selected_mode_id)
                    
                    # Display full effects
                    st.markdown("---")
                    st.markdown(f"### Effects for {selected_mode_id}")
                    effects = selected_mode['effects']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Evidence:** {effects.get('evidence', 'N/A')}")
                        st.markdown(f"**Safety Impact:** {effects.get('safety_impact', 'N/A')}")
                        st.markdown(f"**Operational Impact:** {effects.get('operational_impact', 'N/A')}")
                    with col2:
                        st.markdown(f"**Physical Damage:** {effects.get('physical_damage', 'N/A')}")
                        st.markdown(f"**Repair Action:** {effects.get('repair_action', 'N/A')}")
                        st.markdown(f"**Repair Time:** {effects.get('repair_time', 0)} hours")
                        st.markdown(f"**Downtime:** {effects.get('downtime', 0)} hours")
                    
                    # Update Section
                    if not st.session_state.get('editing_failure_effect', False):
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Update Selected", use_container_width=True, key="update_effect_btn"):
                                st.session_state.editing_failure_effect = True
                                st.rerun()
                        with col_action2:
                            if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_effect_btn"):
                                st.session_state.deleting_failure_effect = True
                                st.rerun()
                    
                    # Update Form
                    if st.session_state.get('editing_failure_effect', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Update Failure Effects")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            updated_evidence = st.text_area(
                                "Update Evidence of Failure",
                                value=effects.get('evidence', ''),
                                key="update_effect_evidence"
                            )
                            
                            updated_safety = st.text_area(
                                "Update Safety/Environmental Impact",
                                value=effects.get('safety_impact', ''),
                                key="update_effect_safety"
                            )
                        
                        with col2:
                            updated_operational = st.text_area(
                                "Update Operational Impact",
                                value=effects.get('operational_impact', ''),
                                key="update_effect_operational"
                            )
                            
                            updated_damage = st.text_area(
                                "Update Physical Damage",
                                value=effects.get('physical_damage', ''),
                                key="update_effect_damage"
                            )
                        
                        updated_repair = st.text_area(
                            "Update Repair Action Required",
                            value=effects.get('repair_action', ''),
                            key="update_effect_repair"
                        )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            updated_repair_time = st.number_input(
                                "Update Repair Time (hours)",
                                min_value=0.0,
                                step=0.5,
                                value=float(effects.get('repair_time', 0)),
                                key="update_effect_repair_time"
                            )
                        with col2:
                            updated_downtime = st.number_input(
                                "Update Total Downtime (hours)",
                                min_value=0.0,
                                step=0.5,
                                value=float(effects.get('downtime', 0)),
                                key="update_effect_downtime"
                            )
                        
                        col_update1, col_update2 = st.columns(2)
                        with col_update1:
                            if st.button("💾 Save Update", type="primary", use_container_width=True, key="save_effect_update"):
                                if not updated_evidence:
                                    st.error("Evidence cannot be empty")
                                else:
                                    st.session_state.failure_modes[mode_idx]['effects'] = {
                                        'evidence': updated_evidence,
                                        'safety_impact': updated_safety,
                                        'operational_impact': updated_operational,
                                        'physical_damage': updated_damage,
                                        'repair_action': updated_repair,
                                        'repair_time': updated_repair_time,
                                        'downtime': updated_downtime
                                    }
                                    st.session_state.editing_failure_effect = False
                                    save_asset_analysis_data()
                                    st.success(f"✅ Failure effects for {selected_mode_id} updated!")
                                    st.rerun()
                        with col_update2:
                            if st.button("❌ Cancel Update", use_container_width=True, key="cancel_effect_update"):
                                st.session_state.editing_failure_effect = False
                                st.rerun()
                    
                    # Delete Confirmation
                    if st.session_state.get('deleting_failure_effect', False):
                        st.markdown("---")
                        st.markdown("### 🗑️ Delete Failure Effects")
                        st.warning(f"⚠️ Warning: This will delete the failure effects for {selected_mode_id}!")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True, key="confirm_effect_delete"):
                                # Delete the effects
                                if 'effects' in st.session_state.failure_modes[mode_idx]:
                                    del st.session_state.failure_modes[mode_idx]['effects']
                                st.session_state.deleting_failure_effect = False
                                save_asset_analysis_data()
                                st.success(f"✅ Failure effects for {selected_mode_id} deleted!")
                                st.rerun()
                        with col_del2:
                            if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_effect_delete"):
                                st.session_state.deleting_failure_effect = False
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
                    
                    # Get risk level based on current thresholds
                    risk_level, risk_color = get_risk_level(risk_score)
                    
                    st.markdown(f"""
                    <div style="background-color: {risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                    <strong>Risk Level: {risk_level}</strong><br>
                    Score: {risk_score}
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add/Save button
            if st.button("💾 Save Consequence Category", use_container_width=True):
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
                        save_asset_analysis_data()
                        st.success(f"✅ Consequence category saved for {mode_id}")
                        st.rerun()
            
            # Display table with selection for failure modes with consequence categories
            modes_with_consequences = [m for m in st.session_state.failure_modes if 'consequence_category' in m]
            
            if modes_with_consequences:
                st.markdown("---")
                st.subheader(f"View, Update or Delete Consequence Categories")
                
                # Create selection interface using radio buttons
                consequence_options = ["None"] + [f"{m['id']}: {m['component']} - {m['description']}" for m in modes_with_consequences]
                selected_consequence = st.radio(
                    "Select a Failure Mode to View, Update or Delete its Consequence Category:",
                    consequence_options,
                    key="consequence_selection"
                )
                
                # Display table of failure modes with consequences
                consequences_display = []
                for m in modes_with_consequences:
                    consequences_display.append({
                        'Failure Mode ID': m['id'],
                        'Component': m['component'],
                        'Description': m['description'],
                        'Consequence Category': m.get('consequence_category', 'N/A'),
                        'Risk Level': m.get('risk_assessment', {}).get('risk_level', 'N/A') if 'risk_assessment' in m else 'N/A'
                    })
                consequences_df = pd.DataFrame(consequences_display)
                st.dataframe(consequences_df, use_container_width=True)
                
                # Show Update/Delete options if a consequence is selected
                if selected_consequence != "None":
                    selected_mode_id = selected_consequence.split(":")[0]
                    selected_mode = next(m for m in modes_with_consequences if m['id'] == selected_mode_id)
                    mode_idx = next(i for i, m in enumerate(st.session_state.failure_modes) if m['id'] == selected_mode_id)
                    
                    # Display full consequence details
                    st.markdown("---")
                    st.markdown(f"### Consequence Category for {selected_mode_id}")
                    
                    st.markdown(f"**Consequence Category:** {selected_mode.get('consequence_category', 'N/A')}")
                    
                    if 'risk_assessment' in selected_mode:
                        risk = selected_mode['risk_assessment']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Consequence:** {risk.get('consequence', 'N/A')}")
                        with col2:
                            st.markdown(f"**Likelihood:** {risk.get('likelihood', 'N/A')}")
                        with col3:
                            st.markdown(f"**Risk Level:** {risk.get('risk_level', 'N/A')} (Score: {risk.get('risk_score', 0)})")
                    
                    # Update Section
                    if not st.session_state.get('editing_consequence', False):
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Update Selected", use_container_width=True, key="update_consequence_btn"):
                                st.session_state.editing_consequence = True
                                st.rerun()
                        with col_action2:
                            if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_consequence_btn"):
                                st.session_state.deleting_consequence = True
                                st.rerun()
                    
                    # Update Form
                    if st.session_state.get('editing_consequence', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Update Consequence Category")
                        
                        # Get current values
                        current_category = selected_mode.get('consequence_category', '')
                        
                        # Determine if it's hidden or evident
                        is_hidden = "Hidden" in current_category
                        
                        # Question 1: Evident or Hidden?
                        updated_is_evident = st.radio(
                            "**Q1: Will the failure become evident to operators under normal circumstances?**",
                            ["Yes - Evident", "No - Hidden (failure of protective device)"],
                            index=0 if not is_hidden else 1,
                            key="update_is_evident"
                        )
                        
                        # Branch based on evident/hidden
                        if "Hidden" in updated_is_evident:
                            st.info("This is a **Hidden Failure** - typically protective devices that fail silently")
                            
                            # Determine current consequence type
                            if "Safety" in current_category:
                                current_idx = 0
                            elif "Operational" in current_category:
                                current_idx = 1
                            else:
                                current_idx = 2
                            
                            updated_hidden_consequence = st.radio(
                                "**Q2: If a multiple failure occurs (protected function fails while protective device is failed), what are the consequences?**",
                                ["Safety or Environmental impact", "Operational impact", "Non-operational (just repair cost)"],
                                index=current_idx,
                                key="update_hidden_consequence"
                            )
                            
                            if "Safety" in updated_hidden_consequence:
                                updated_consequence_category = "Hidden (Safety/Environmental)"
                            elif "Operational" in updated_hidden_consequence:
                                updated_consequence_category = "Hidden (Operational)"
                            else:
                                updated_consequence_category = "Hidden (Non-operational)"
                        
                        else:  # Evident
                            st.info("This is an **Evident Failure** - operators will know when it occurs")
                            
                            # Determine current consequence type
                            if "Safety" in current_category:
                                current_idx = 0
                            elif "Operational" in current_category:
                                current_idx = 1
                            else:
                                current_idx = 2
                            
                            updated_evident_consequence = st.radio(
                                "**Q2: What are the consequences of this evident failure?**",
                                ["Safety or Environmental impact", 
                                 "Operational impact (affects output, quality, service, or operating costs)", 
                                 "Non-operational (only direct repair cost)"],
                                index=current_idx,
                                key="update_evident_consequence"
                            )
                            
                            if "Safety" in updated_evident_consequence:
                                updated_consequence_category = "Evident (Safety/Environmental)"
                            elif "Operational" in updated_evident_consequence:
                                updated_consequence_category = "Evident (Operational)"
                            else:
                                updated_consequence_category = "Evident (Non-operational)"
                        
                        st.markdown(f"**Updated Consequence Category:** {updated_consequence_category}")
                        
                        # Risk assessment for safety consequences
                        if "Safety" in updated_consequence_category or "Environmental" in updated_consequence_category:
                            st.markdown("#### Risk Assessment")
                            col1, col2, col3 = st.columns(3)
                            
                            # Get current risk values
                            current_risk = selected_mode.get('risk_assessment', {})
                            current_cons = current_risk.get('consequence', '3-Moderate')
                            current_like = current_risk.get('likelihood', '3-Occasional')
                            
                            with col1:
                                updated_consequence_rating = st.select_slider(
                                    "Consequence Severity",
                                    options=["1-Insignificant", "2-Minor", "3-Moderate", "4-High", "5-Catastrophic"],
                                    value=current_cons,
                                    key="update_consequence_rating"
                                )
                            
                            with col2:
                                updated_likelihood_rating = st.select_slider(
                                    "Likelihood",
                                    options=["1-Rare", "2-Unlikely", "3-Occasional", "4-Likely", "5-Almost Certain"],
                                    value=current_like,
                                    key="update_likelihood_rating"
                                )
                            
                            with col3:
                                # Calculate risk score
                                cons_num = int(updated_consequence_rating[0])
                                like_num = int(updated_likelihood_rating[0])
                                risk_score = cons_num + like_num
                                
                                # Get risk level based on current thresholds
                                risk_level, risk_color = get_risk_level(risk_score)
                                
                                st.markdown(f"""
                                <div style="background-color: {risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                                <strong>Risk Level: {risk_level}</strong><br>
                                Score: {risk_score}
                                </div>
                                """, unsafe_allow_html=True)
                        
                        col_update1, col_update2 = st.columns(2)
                        with col_update1:
                            if st.button("💾 Save Update", type="primary", use_container_width=True, key="save_consequence_update"):
                                st.session_state.failure_modes[mode_idx]['consequence_category'] = updated_consequence_category
                                if "Safety" in updated_consequence_category or "Environmental" in updated_consequence_category:
                                    st.session_state.failure_modes[mode_idx]['risk_assessment'] = {
                                        'consequence': updated_consequence_rating,
                                        'likelihood': updated_likelihood_rating,
                                        'risk_score': risk_score,
                                        'risk_level': risk_level
                                    }
                                else:
                                    # Remove risk assessment if not safety/environmental
                                    if 'risk_assessment' in st.session_state.failure_modes[mode_idx]:
                                        del st.session_state.failure_modes[mode_idx]['risk_assessment']
                                st.session_state.editing_consequence = False
                                save_asset_analysis_data()
                                st.success(f"✅ Consequence category for {selected_mode_id} updated!")
                                st.rerun()
                        with col_update2:
                            if st.button("❌ Cancel Update", use_container_width=True, key="cancel_consequence_update"):
                                st.session_state.editing_consequence = False
                                st.rerun()
                    
                    # Delete Confirmation
                    if st.session_state.get('deleting_consequence', False):
                        st.markdown("---")
                        st.markdown("### 🗑️ Delete Consequence Category")
                        st.warning(f"⚠️ Warning: This will delete the consequence category for {selected_mode_id}!")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True, key="confirm_consequence_delete"):
                                # Delete the consequence category
                                if 'consequence_category' in st.session_state.failure_modes[mode_idx]:
                                    del st.session_state.failure_modes[mode_idx]['consequence_category']
                                if 'risk_assessment' in st.session_state.failure_modes[mode_idx]:
                                    del st.session_state.failure_modes[mode_idx]['risk_assessment']
                                st.session_state.deleting_consequence = False
                                save_asset_analysis_data()
                                st.success(f"✅ Consequence category for {selected_mode_id} deleted!")
                                st.rerun()
                        with col_del2:
                            if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_consequence_delete"):
                                st.session_state.deleting_consequence = False
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
            st.markdown("### Risk Assessment")
            
            # Display Risk Matrix
            st.markdown("**Risk Matrix:** Consequence + Likelihood = Risk Score")
            
            # Generate and display dynamic risk matrix based on current thresholds
            st.markdown(generate_risk_matrix_html(), unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Task Selection Decision")
            
            # Build task type options based on consequence category
            consequence_cat = current_mode.get('consequence_category', '')
            task_type_options = ["Select...", 
                                 "CBM - Condition Based Maintenance", 
                                 "FTM - Fixed Time Maintenance",
                                 "Redesign"]
            
            # Only add FF if consequence is Hidden
            if "Hidden" in consequence_cat:
                task_type_options.insert(3, "FF - Failure Finding")
            
            # Only add OTF if consequence is NOT Safety/Environmental
            if "Safety" not in consequence_cat and "Environmental" not in consequence_cat:
                task_type_options.append("OTF - Operate to Failure")
            
            task_type = st.selectbox(
                "Select Task Type",
                task_type_options
            )
            
            if task_type != "Select...":
                st.markdown(f"#### {task_type}")
                
                # Initialize post-risk assessment variables
                post_consequence_rating = None
                post_likelihood_rating = None
                post_risk_score = None
                post_risk_level = None
                
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
                        useful_life = st.number_input("Useful Life", min_value=0.0)
                        mtbf = st.number_input("MTBF", min_value=0.0,
                                             help="Mean time between failures")
                    
                    task_description = f"{task_action} every {interval_value} {interval_unit}"
                    
                    # Add risk assessment slider for Safety/Environmental consequences
                    consequence_cat = current_mode.get('consequence_category', '')
                    if "Safety" in consequence_cat or "Environmental" in consequence_cat:
                        st.markdown("---")
                        st.markdown("#### Risk after task implementation")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            post_consequence_rating = st.select_slider(
                                "Consequence Severity",
                                options=["1-Insignificant", "2-Minor", "3-Moderate", "4-High", "5-Catastrophic"],
                                value="3-Moderate",
                                key="ftm_post_consequence"
                            )
                        
                        with col2:
                            post_likelihood_rating = st.select_slider(
                                "Likelihood",
                                options=["1-Rare", "2-Unlikely", "3-Occasional", "4-Likely", "5-Almost Certain"],
                                value="3-Occasional",
                                key="ftm_post_likelihood"
                            )
                        
                        with col3:
                            # Calculate risk score
                            post_cons_num = int(post_consequence_rating[0])
                            post_like_num = int(post_likelihood_rating[0])
                            post_risk_score = post_cons_num + post_like_num
                            
                            # Get risk level based on current thresholds
                            post_risk_level, post_risk_color = get_risk_level(post_risk_score)
                            
                            st.markdown(f"""
                            <div style="background-color: {post_risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                            <strong>Risk Level: {post_risk_level}</strong><br>
                            Score: {post_risk_score}
                            </div>
                            """, unsafe_allow_html=True)
                
                elif "FF" in task_type:
                    st.info("**FF Task:** A more informal approach to setting the FFI for Consequences that are not severe")
                    
                    st.markdown("""
                    **This approach involves:**
                    - Determining the Mean Time Between Failures (MTBF) of the Protective Device (Years)
                    - Deciding on a required Availability for the Protective Device (ratio of time it is functional to the total time required (%))
                    - Using a table to determine the FFI as a % of the MTBF of the Protective Device
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        test_method = st.text_area("Test Method",
                                                  help="How to check if protective device is functional")
                        mtbf_protective = st.number_input("MTBF of Protective Device (years)", min_value=0.0,
                                                         help="Mean Time Between Failures of the protective device in years")
                    with col2:
                        # Availability lookup table
                        availability_options = {
                            "99.99%": 0.0002,  # 0.02% FFI
                            "99.95%": 0.001,   # 0.1% FFI
                            "99.9%": 0.002,    # 0.2% FFI
                            "99.5%": 0.01,     # 1% FFI
                            "99%": 0.02,       # 2% FFI
                            "98%": 0.04,       # 4% FFI
                            "95%": 0.10        # 10% FFI
                        }
                        
                        availability_required = st.selectbox(
                            "Required Availability for Protective Device",
                            options=list(availability_options.keys()),
                            help="Ratio of time the protective device is functional to total time required"
                        )
                        
                        # Calculate FFI based on availability
                        ffi_percentage = availability_options[availability_required]
                        
                        # Display the FFI percentage from table
                        st.info(f"**FFI (as % of MTBF):** {ffi_percentage * 100}%")
                        
                        # Calculate FFI in days
                        if mtbf_protective > 0:
                            mtbf_days = mtbf_protective * 365.25  # Convert years to days
                            ff_interval = mtbf_days * ffi_percentage
                            st.success(f"**Calculated FFI:** {ff_interval:.1f} days")
                        else:
                            ff_interval = 0.0
                            st.warning("Enter MTBF to calculate Failure Finding Interval")
                    
                    task_description = f"Test {test_method} every {ff_interval:.1f} days (based on {availability_required} availability)"
                
                elif "Redesign" in task_type:
                    st.info("**Redesign:** One-off change to equipment, process, or procedure")
                    
                    redesign_type = st.radio("Redesign Type",
                                           ["Equipment modification", "Process change", "Procedure update", "Training"])
                    task_description = st.text_area("Describe the Redesign",
                                                   help="What specific change will be made?")
                    
                    # Add risk assessment slider for Safety/Environmental consequences
                    consequence_cat = current_mode.get('consequence_category', '')
                    if "Safety" in consequence_cat or "Environmental" in consequence_cat:
                        st.markdown("---")
                        st.markdown("#### Risk after task implementation")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            post_consequence_rating = st.select_slider(
                                "Consequence Severity",
                                options=["1-Insignificant", "2-Minor", "3-Moderate", "4-High", "5-Catastrophic"],
                                value="3-Moderate",
                                key="redesign_post_consequence"
                            )
                        
                        with col2:
                            post_likelihood_rating = st.select_slider(
                                "Likelihood",
                                options=["1-Rare", "2-Unlikely", "3-Occasional", "4-Likely", "5-Almost Certain"],
                                value="3-Occasional",
                                key="redesign_post_likelihood"
                            )
                        
                        with col3:
                            # Calculate risk score
                            post_cons_num = int(post_consequence_rating[0])
                            post_like_num = int(post_likelihood_rating[0])
                            post_risk_score = post_cons_num + post_like_num
                            
                            # Get risk level based on current thresholds
                            post_risk_level, post_risk_color = get_risk_level(post_risk_score)
                            
                            st.markdown(f"""
                            <div style="background-color: {post_risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                            <strong>Risk Level: {post_risk_level}</strong><br>
                            Score: {post_risk_score}
                            </div>
                            """, unsafe_allow_html=True)
                
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
                
                # Check if consequence is operational or non-operational AND task is not OTF
                consequence_cat = current_mode.get('consequence_category', '')
                show_cost_fields = ('Operational' in consequence_cat or 'Non-operational' in consequence_cat) and 'OTF' not in task_type
                
                # Initialize cost variables
                labour_cost = 0.0
                parts_cost = 0.0
                other_cost = 0.0
                failure_labour_cost = 0.0
                failure_parts_cost = 0.0
                failure_other_cost = 0.0
                total_cost = 0.0
                total_failure_cost = 0.0
                
                if show_cost_fields:
                    # Cost of Task
                    st.markdown("### Cost of Task")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        labour_cost = st.number_input("Labour Cost ($)", min_value=0.0, key="task_labour")
                    with col2:
                        parts_cost = st.number_input("Parts Cost ($)", min_value=0.0, key="task_parts")
                    with col3:
                        other_cost = st.number_input("Other Cost ($)", min_value=0.0, key="task_other")
                    
                    total_cost = labour_cost + parts_cost + other_cost
                    st.markdown(f"**Total Task Cost:** ${total_cost:,.2f}")
                    
                    # Cost of Failure
                    st.markdown("### Cost of Failure")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        failure_labour_cost = st.number_input("Labour Cost ($)", min_value=0.0, key="failure_labour")
                    with col2:
                        failure_parts_cost = st.number_input("Parts Cost ($)", min_value=0.0, key="failure_parts")
                    with col3:
                        failure_other_cost = st.number_input("Other Cost ($)", min_value=0.0, key="failure_other")
                    
                    total_failure_cost = failure_labour_cost + failure_parts_cost + failure_other_cost
                    st.markdown(f"**Total Failure Cost:** ${total_failure_cost:,.2f}")
                
                if st.button("💾 Save Failure Management Task"):
                    if technically_feasible == "Yes" and worth_doing == "Yes":
                        task = {
                            'task_type': task_type,
                            'description': task_description,
                            'technically_feasible': technically_feasible,
                            'worth_doing': worth_doing,
                            'justification': justification,
                            'cost': total_cost,
                            'failure_cost': total_failure_cost
                        }
                        
                        # Add post-implementation risk assessment for FTM and Redesign Safety/Environmental tasks
                        if ("FTM" in task_type or "Redesign" in task_type) and ("Safety" in current_mode.get('consequence_category', '') or "Environmental" in current_mode.get('consequence_category', '')):
                            task['post_risk_assessment'] = {
                                'consequence': post_consequence_rating,
                                'likelihood': post_likelihood_rating,
                                'risk_score': post_risk_score,
                                'risk_level': post_risk_level
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
                                save_asset_analysis_data()
                                st.success(f"✅ Task saved for {mode_id}")
                                st.rerun()
                    else:
                        st.error("Task must be both technically feasible and worth doing!")
            
            # Display table with selection for failure modes with tasks
            modes_with_tasks = [m for m in st.session_state.failure_modes if 'management_task' in m]
            
            if modes_with_tasks:
                st.markdown("---")
                st.subheader(f"View, Update or Delete Tasks")
                
                # Create selection interface using radio buttons
                task_options = ["None"] + [f"{m['id']}: {m['component']} - {m['description']}" for m in modes_with_tasks]
                selected_task = st.radio(
                    "Select a Failure Mode to View, Update or Delete its Task:",
                    task_options,
                    key="task_selection"
                )
                
                # Display table of failure modes with tasks
                tasks_display = []
                for m in modes_with_tasks:
                    task = m.get('management_task', {})
                    post_risk = task.get('post_risk_assessment', {})
                    
                    task_data = {
                        'Failure Mode ID': m['id'],
                        'Component': m['component'],
                        'Description': m['description'],
                        'Consequence': m.get('consequence_category', 'N/A'),
                        'Task Type': task.get('task_type', 'N/A'),
                        'Task Description': task.get('description', 'N/A'),
                        'Technically Feasible': task.get('technically_feasible', 'N/A'),
                        'Worth Doing': task.get('worth_doing', 'N/A'),
                        'Justification': task.get('justification', 'N/A'),
                        'Task Cost': f"${task.get('cost', 0):,.2f}",
                        'Failure Cost': f"${task.get('failure_cost', 0):,.2f}"
                    }
                    
                    # Add post-risk assessment data if available
                    if post_risk:
                        task_data['Post-Risk Consequence'] = post_risk.get('consequence', 'N/A')
                        task_data['Post-Risk Likelihood'] = post_risk.get('likelihood', 'N/A')
                        task_data['Post-Risk Level'] = post_risk.get('risk_level', 'N/A')
                        task_data['Post-Risk Score'] = post_risk.get('risk_score', 'N/A')
                    else:
                        task_data['Post-Risk Consequence'] = 'N/A'
                        task_data['Post-Risk Likelihood'] = 'N/A'
                        task_data['Post-Risk Level'] = 'N/A'
                        task_data['Post-Risk Score'] = 'N/A'
                    
                    tasks_display.append(task_data)
                
                tasks_df = pd.DataFrame(tasks_display)
                st.dataframe(tasks_df, use_container_width=False, height=400)
                
                # Show Update/Delete options if a task is selected
                if selected_task != "None":
                    selected_task_mode_id = selected_task.split(":")[0]
                    selected_task_mode = next(m for m in modes_with_tasks if m['id'] == selected_task_mode_id)
                    task_mode_idx = next(i for i, m in enumerate(st.session_state.failure_modes) if m['id'] == selected_task_mode_id)
                    
                    # Display full task details
                    st.markdown("---")
                    st.markdown(f"### Task for {selected_task_mode_id}")
                    
                    task = selected_task_mode.get('management_task', {})
                    st.markdown(f"**Task Type:** {task.get('task_type', 'N/A')}")
                    st.markdown(f"**Description:** {task.get('description', 'N/A')}")
                    st.markdown(f"**Technically Feasible:** {task.get('technically_feasible', 'N/A')}")
                    st.markdown(f"**Worth Doing:** {task.get('worth_doing', 'N/A')}")
                    st.markdown(f"**Justification:** {task.get('justification', 'N/A')}")
                    st.markdown(f"**Cost:** ${task.get('cost', 0):,.2f}")
                    st.markdown(f"**Failure Cost:** ${task.get('failure_cost', 0):,.2f}")
                    
                    if 'post_risk_assessment' in task:
                        st.markdown("**Post-Implementation Risk Assessment:**")
                        post_risk = task['post_risk_assessment']
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Consequence:** {post_risk.get('consequence', 'N/A')}")
                        with col2:
                            st.markdown(f"**Likelihood:** {post_risk.get('likelihood', 'N/A')}")
                        with col3:
                            st.markdown(f"**Risk Level:** {post_risk.get('risk_level', 'N/A')} (Score: {post_risk.get('risk_score', 0)})")
                    
                    # Update Section
                    if not st.session_state.get('editing_task', False):
                        col_action1, col_action2 = st.columns(2)
                        with col_action1:
                            if st.button("✏️ Update Selected", use_container_width=True, key="update_task_btn"):
                                st.session_state.editing_task = True
                                st.rerun()
                        with col_action2:
                            if st.button("🗑️ Delete Selected", use_container_width=True, key="delete_task_btn"):
                                st.session_state.deleting_task = True
                                st.rerun()
                    
                    # Update Form
                    if st.session_state.get('editing_task', False):
                        st.markdown("---")
                        st.markdown("### ✏️ Update Task")
                        
                        # Get current task values
                        current_task = selected_task_mode.get('management_task', {})
                        current_task_type = current_task.get('task_type', 'Select...')
                        
                        # Build task type options based on consequence category
                        consequence_cat = selected_task_mode.get('consequence_category', '')
                        update_task_type_options = ["Select...", 
                                                    "CBM - Condition Based Maintenance", 
                                                    "FTM - Fixed Time Maintenance",
                                                    "Redesign"]
                        
                        # Only add FF if consequence is Hidden
                        if "Hidden" in consequence_cat:
                            update_task_type_options.insert(3, "FF - Failure Finding")
                        
                        # Only add OTF if consequence is NOT Safety/Environmental
                        if "Safety" not in consequence_cat and "Environmental" not in consequence_cat:
                            update_task_type_options.append("OTF - Operate to Failure")
                        
                        # Calculate index for current task type
                        if current_task_type in update_task_type_options:
                            current_index = update_task_type_options.index(current_task_type)
                        else:
                            current_index = 0
                        
                        # Task type selection
                        updated_task_type = st.selectbox(
                            "Select Task Type",
                            update_task_type_options,
                            index=current_index,
                            key="update_task_type"
                        )
                        
                        if updated_task_type != "Select...":
                            updated_task_description = st.text_area(
                                "Task Description",
                                value=current_task.get('description', ''),
                                key="update_task_description"
                            )
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                updated_technically_feasible = st.radio(
                                    "Technically Feasible?",
                                    ["Yes", "No"],
                                    index=0 if current_task.get('technically_feasible') == "Yes" else 1,
                                    key="update_technically_feasible"
                                )
                            with col2:
                                updated_worth_doing = st.radio(
                                    "Worth Doing?",
                                    ["Yes", "No"],
                                    index=0 if current_task.get('worth_doing') == "Yes" else 1,
                                    key="update_worth_doing"
                                )
                            
                            updated_justification = st.text_area(
                                "Justification",
                                value=current_task.get('justification', ''),
                                key="update_justification"
                            )
                            
                            # Check if consequence is operational or non-operational AND task is not OTF
                            consequence_cat = selected_task_mode.get('consequence_category', '')
                            show_cost_fields = ('Operational' in consequence_cat or 'Non-operational' in consequence_cat) and 'OTF' not in updated_task_type
                            
                            # Initialize cost variables
                            updated_labour_cost = 0.0
                            updated_parts_cost = 0.0
                            updated_other_cost = 0.0
                            updated_failure_labour_cost = 0.0
                            updated_failure_parts_cost = 0.0
                            updated_failure_other_cost = 0.0
                            updated_total_cost = 0.0
                            updated_total_failure_cost = 0.0
                            
                            if show_cost_fields:
                                st.markdown("### Cost of Task")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    updated_labour_cost = st.number_input("Labour Cost ($)", min_value=0.0, value=float(current_task.get('cost', 0)), key="update_task_labour")
                                with col2:
                                    updated_parts_cost = st.number_input("Parts Cost ($)", min_value=0.0, key="update_task_parts")
                                with col3:
                                    updated_other_cost = st.number_input("Other Cost ($)", min_value=0.0, key="update_task_other")
                                
                                updated_total_cost = updated_labour_cost + updated_parts_cost + updated_other_cost
                                st.markdown(f"**Total Task Cost:** ${updated_total_cost:,.2f}")
                                
                                st.markdown("### Cost of Failure")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    updated_failure_labour_cost = st.number_input("Labour Cost ($)", min_value=0.0, value=float(current_task.get('failure_cost', 0)), key="update_failure_labour")
                                with col2:
                                    updated_failure_parts_cost = st.number_input("Parts Cost ($)", min_value=0.0, key="update_failure_parts")
                                with col3:
                                    updated_failure_other_cost = st.number_input("Other Cost ($)", min_value=0.0, key="update_failure_other")
                                
                                updated_total_failure_cost = updated_failure_labour_cost + updated_failure_parts_cost + updated_failure_other_cost
                                st.markdown(f"**Total Failure Cost:** ${updated_total_failure_cost:,.2f}")
                            
                            # Risk assessment for FTM and Redesign Safety/Environmental tasks
                            updated_post_consequence_rating = None
                            updated_post_likelihood_rating = None
                            updated_post_risk_score = None
                            updated_post_risk_level = None
                            
                            if ("FTM" in updated_task_type or "Redesign" in updated_task_type) and ("Safety" in consequence_cat or "Environmental" in consequence_cat):
                                st.markdown("---")
                                st.markdown("#### Risk after task implementation")
                                col1, col2, col3 = st.columns(3)
                                
                                # Get current post-risk values
                                current_post_risk = current_task.get('post_risk_assessment', {})
                                current_post_cons = current_post_risk.get('consequence', '3-Moderate')
                                current_post_like = current_post_risk.get('likelihood', '3-Occasional')
                                
                                with col1:
                                    updated_post_consequence_rating = st.select_slider(
                                        "Consequence Severity",
                                        options=["1-Insignificant", "2-Minor", "3-Moderate", "4-High", "5-Catastrophic"],
                                        value=current_post_cons,
                                        key="update_ftm_post_consequence"
                                    )
                                
                                with col2:
                                    updated_post_likelihood_rating = st.select_slider(
                                        "Likelihood",
                                        options=["1-Rare", "2-Unlikely", "3-Occasional", "4-Likely", "5-Almost Certain"],
                                        value=current_post_like,
                                        key="update_ftm_post_likelihood"
                                    )
                                
                                with col3:
                                    # Calculate risk score
                                    updated_post_cons_num = int(updated_post_consequence_rating[0])
                                    updated_post_like_num = int(updated_post_likelihood_rating[0])
                                    updated_post_risk_score = updated_post_cons_num + updated_post_like_num
                                    
                                    # Get risk level based on current thresholds
                                    updated_post_risk_level, updated_post_risk_color = get_risk_level(updated_post_risk_score)
                                    
                                    st.markdown(f"""
                                    <div style="background-color: {updated_post_risk_color}; color: white; padding: 10px; border-radius: 5px; text-align: center;">
                                    <strong>Risk Level: {updated_post_risk_level}</strong><br>
                                    Score: {updated_post_risk_score}
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            col_update1, col_update2 = st.columns(2)
                            with col_update1:
                                if st.button("💾 Save Update", type="primary", use_container_width=True, key="save_task_update"):
                                    updated_task = {
                                        'task_type': updated_task_type,
                                        'description': updated_task_description,
                                        'technically_feasible': updated_technically_feasible,
                                        'worth_doing': updated_worth_doing,
                                        'justification': updated_justification,
                                        'cost': updated_total_cost,
                                        'failure_cost': updated_total_failure_cost
                                    }
                                    
                                    # Add post-implementation risk assessment if applicable
                                    if ("FTM" in updated_task_type or "Redesign" in updated_task_type) and ("Safety" in consequence_cat or "Environmental" in consequence_cat):
                                        updated_task['post_risk_assessment'] = {
                                            'consequence': updated_post_consequence_rating,
                                            'likelihood': updated_post_likelihood_rating,
                                            'risk_score': updated_post_risk_score,
                                            'risk_level': updated_post_risk_level
                                        }
                                    
                                    st.session_state.failure_modes[task_mode_idx]['management_task'] = updated_task
                                    st.session_state.editing_task = False
                                    save_asset_analysis_data()
                                    st.success(f"✅ Task for {selected_task_mode_id} updated!")
                                    st.rerun()
                            with col_update2:
                                if st.button("❌ Cancel Update", use_container_width=True, key="cancel_task_update"):
                                    st.session_state.editing_task = False
                                    st.rerun()
                    
                    # Delete Confirmation
                    if st.session_state.get('deleting_task', False):
                        st.markdown("---")
                        st.markdown("### 🗑️ Delete Task")
                        st.warning(f"⚠️ Warning: This will delete the task for {selected_task_mode_id}!")
                        
                        col_del1, col_del2 = st.columns(2)
                        with col_del1:
                            if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True, key="confirm_task_delete"):
                                # Delete the task
                                if 'management_task' in st.session_state.failure_modes[task_mode_idx]:
                                    del st.session_state.failure_modes[task_mode_idx]['management_task']
                                st.session_state.deleting_task = False
                                save_asset_analysis_data()
                                st.success(f"✅ Task for {selected_task_mode_id} deleted!")
                                st.rerun()
                        with col_del2:
                            if st.button("❌ Cancel Delete", use_container_width=True, key="cancel_task_delete"):
                                st.session_state.deleting_task = False
                                st.rerun()

# Stage 3: Implementation
def stage_3_implementation():
    """Stage 3: Implementation Planning"""
    st.markdown("## Stage 3: Implementation Planning")
    st.markdown("")
    
    # Check if project exists
    if not st.session_state.project_data.get('project_no'):
        st.warning("⚠️ Please complete Stage 1: Planning and Preparation first!")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    if not st.session_state.assets:
        st.warning("⚠️ No assets found in this project.")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    # Asset Selection
    st.markdown(f"### 📁 Project: {st.session_state.project_data['project_no']} - {st.session_state.project_data.get('project_description', '')}")
    
    asset_options = [f"{i+1}. {asset['asset_name']} ({asset['asset_class']})" 
                     for i, asset in enumerate(st.session_state.assets)]
    
    if 'selected_implementation_asset' not in st.session_state:
        st.session_state.selected_implementation_asset = 0
    
    selected_option = st.selectbox(
        "Select Asset for Implementation Planning",
        options=range(len(asset_options)),
        format_func=lambda x: asset_options[x],
        index=st.session_state.selected_implementation_asset,
        key="asset_selector_stage3"
    )
    
    st.session_state.selected_implementation_asset = selected_option
    current_asset = st.session_state.assets[selected_option]
    
    # Load asset-specific data
    analysis_results = current_asset.get('analysis_results', [])
    
    if not analysis_results:
        st.warning(f"⚠️ No analysis results available for '{current_asset['asset_name']}'. Please complete Stage 2 first.")
        if st.button("← Go to Stage 2"):
            st.session_state.current_stage = 2
            st.rerun()
        return
    
    st.markdown(f"**Planning for Asset:** {current_asset['asset_name']}")
    st.markdown("**Objective:** Plan implementation of the failure management tasks identified in the analysis.")
    
    tab1, tab2, tab3 = st.tabs(["Maintenance Schedule", "One-off Changes", "Implementation Checklist"])
    
    with tab1:
        st.subheader("Maintenance Schedule")
        
        # Filter for CBM, FTM, and FF tasks
        maintenance_tasks = [r for r in analysis_results 
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
        
        redesign_tasks = [r for r in analysis_results if 'Redesign' in r['task_type']]
        
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
    
    # Check if project exists
    if not st.session_state.project_data.get('project_no'):
        st.warning("⚠️ Please complete Stage 1: Planning and Preparation first!")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    if not st.session_state.assets:
        st.warning("⚠️ No assets found in this project.")
        if st.button("← Go to Stage 1"):
            st.session_state.current_stage = 1
            st.rerun()
        return
    
    # Project Information
    st.markdown(f"### 📁 Project: {st.session_state.project_data['project_no']} - {st.session_state.project_data.get('project_description', '')}")
    st.markdown(f"**Total Assets:** {len(st.session_state.assets)}")
    
    tab1, tab2, tab3 = st.tabs(["Project Summary", "Asset Reports", "Export Data"])
    
    with tab1:
        st.subheader("Project-Level Summary Report")
        
        # Aggregate statistics across all assets
        total_functions = 0
        total_failures = 0
        total_modes = 0
        total_tasks = 0
        total_cost = 0
        
        for asset in st.session_state.assets:
            total_functions += len(asset.get('functions', []))
            total_failures += len(asset.get('functional_failures', []))
            total_modes += len(asset.get('failure_modes', []))
            total_tasks += len(asset.get('analysis_results', []))
            total_cost += sum([r.get('cost', 0) for r in asset.get('analysis_results', [])])
        
        st.markdown("### Overall Project Statistics")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Assets", len(st.session_state.assets))
        with col2:
            st.metric("Functions", total_functions)
        with col3:
            st.metric("Failure Modes", total_modes)
        with col4:
            st.metric("Tasks", total_tasks)
        with col5:
            st.metric("Annual Cost", f"${total_cost:,.0f}")
        
        # Asset summary table
        st.markdown("---")
        st.markdown("### Assets Overview")
        
        asset_summary = []
        for asset in st.session_state.assets:
            asset_cost = sum([r.get('cost', 0) for r in asset.get('analysis_results', [])])
            asset_summary.append({
                'Asset Name': asset['asset_name'],
                'Class': asset['asset_class'],
                'Components': len(asset.get('components', [])),
                'Failure Modes': len(asset.get('failure_modes', [])),
                'Tasks': len(asset.get('analysis_results', [])),
                'Annual Cost ($)': asset_cost
            })
        
        if asset_summary:
            df_summary = pd.DataFrame(asset_summary)
            st.dataframe(df_summary, use_container_width=True)
    
    with tab2:
        st.subheader("Individual Asset Reports")
        
        # Asset selection
        asset_options = [f"{i+1}. {asset['asset_name']} ({asset['asset_class']})" 
                        for i, asset in enumerate(st.session_state.assets)]
        
        if 'selected_report_asset' not in st.session_state:
            st.session_state.selected_report_asset = 0
        
        selected_option = st.selectbox(
            "Select Asset for Detailed Report",
            options=range(len(asset_options)),
            format_func=lambda x: asset_options[x],
            index=st.session_state.selected_report_asset,
            key="asset_selector_stage4"
        )
        
        st.session_state.selected_report_asset = selected_option
        current_asset = st.session_state.assets[selected_option]
        
        st.markdown("---")
        st.markdown(f"### Asset: {current_asset['asset_name']}")
        
        # Asset information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Class:** {current_asset.get('asset_class', 'N/A')}")
            st.markdown(f"**Type:** {current_asset.get('asset_type', 'N/A')}")
        with col2:
            st.markdown(f"**Location:** {current_asset.get('site_location', 'N/A')}")
            st.markdown(f"**Components:** {len(current_asset.get('components', []))}")
        with col3:
            st.markdown(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}")
            st.markdown(f"**Failure Modes:** {len(current_asset.get('failure_modes', []))}")
        
        # Analysis statistics
        st.markdown("---")
        st.markdown("### Analysis Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Functions", len(current_asset.get('functions', [])))
        with col2:
            st.metric("Functional Failures", len(current_asset.get('functional_failures', [])))
        with col3:
            st.metric("Failure Modes", len(current_asset.get('failure_modes', [])))
        with col4:
            st.metric("Management Tasks", len(current_asset.get('analysis_results', [])))
        
        # Detailed FMECA table
        if current_asset.get('failure_modes'):
            st.markdown("---")
            st.markdown("### Detailed FMECA Analysis")
            
            detailed_data = []
            for mode in current_asset['failure_modes']:
                row = {
                    'Failure Mode ID': mode['id'],
                    'Functional Failure ID': mode.get('functional_failure_id', ''),
                    'Component': mode['component'],
                    'Failure Mode': mode['description'],
                    'Failure Mode Category': mode.get('category', ''),
                }
                
                # Add effects data
                if 'effects' in mode:
                    effects = mode['effects']
                    row['Evidence of Failure'] = effects.get('evidence', '')
                    row['Safety/Environmental Impact'] = effects.get('safety_impact', '')
                    row['Operational Impact'] = effects.get('operational_impact', '')
                    row['Physical Damage'] = effects.get('physical_damage', '')
                    row['Repair Action'] = effects.get('repair_action', '')
                    row['Repair Time (hrs)'] = effects.get('repair_time', 0)
                    row['Downtime (hrs)'] = effects.get('downtime', 0)
                
                # Add consequence data
                row['Consequence Category'] = mode.get('consequence_category', 'Not categorized')
                
                # Add risk assessment data (for safety/environmental)
                if 'risk_assessment' in mode:
                    risk = mode['risk_assessment']
                    row['Risk Consequence'] = risk.get('consequence', '')
                    row['Risk Likelihood'] = risk.get('likelihood', '')
                    row['Risk Score'] = risk.get('risk_score', '')
                    row['Risk Level'] = risk.get('risk_level', '')
                
                # Add management task data
                if 'management_task' in mode:
                    task = mode['management_task']
                    row['Task Type'] = task.get('task_type', '')
                    row['Task Description'] = task.get('description', '')
                    row['Technically Feasible'] = task.get('technically_feasible', '')
                    row['Worth Doing'] = task.get('worth_doing', '')
                    row['Justification'] = task.get('justification', '')
                    row['Task Cost ($)'] = task.get('cost', 0)
                    row['Failure Cost ($)'] = task.get('failure_cost', 0)
                    
                    # Add post-implementation risk assessment if exists
                    if 'post_risk_assessment' in task:
                        post_risk = task['post_risk_assessment']
                        row['Post-Task Risk Consequence'] = post_risk.get('consequence', '')
                        row['Post-Task Risk Likelihood'] = post_risk.get('likelihood', '')
                        row['Post-Task Risk Score'] = post_risk.get('risk_score', '')
                        row['Post-Task Risk Level'] = post_risk.get('risk_level', '')
                
                detailed_data.append(row)
            
            df_detailed = pd.DataFrame(detailed_data)
            
            # Add horizontal scrollbar with custom styling
            st.markdown("""
            <style>
            div[data-testid="stDataFrame"] > div {
                overflow-x: auto;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.dataframe(df_detailed, use_container_width=True)
    
    with tab3:
        st.subheader("Export Project Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Export Complete Project (Excel)")
            
            if st.session_state.assets:
                # Compile all failure modes from all assets into one comprehensive dataset
                all_data = []
                for asset in st.session_state.assets:
                    if asset.get('failure_modes'):
                        for mode in asset['failure_modes']:
                            row = {
                                'Asset Name': asset['asset_name'],
                                'Asset Class': asset.get('asset_class', ''),
                                'Asset Type': asset.get('asset_type', ''),
                                'Site Location': asset.get('site_location', ''),
                                'Failure Mode ID': mode['id'],
                                'Functional Failure ID': mode.get('functional_failure_id', ''),
                                'Component': mode['component'],
                                'Failure Mode': mode['description'],
                                'Failure Mode Category': mode.get('category', ''),
                            }
                            
                            # Add effects data
                            if 'effects' in mode:
                                effects = mode['effects']
                                row['Evidence of Failure'] = effects.get('evidence', '')
                                row['Safety/Environmental Impact'] = effects.get('safety_impact', '')
                                row['Operational Impact'] = effects.get('operational_impact', '')
                                row['Physical Damage'] = effects.get('physical_damage', '')
                                row['Repair Action'] = effects.get('repair_action', '')
                                row['Repair Time (hrs)'] = effects.get('repair_time', 0)
                                row['Downtime (hrs)'] = effects.get('downtime', 0)
                            
                            # Add consequence data
                            row['Consequence Category'] = mode.get('consequence_category', 'Not categorized')
                            
                            # Add risk assessment data
                            if 'risk_assessment' in mode:
                                risk = mode['risk_assessment']
                                row['Risk Consequence'] = risk.get('consequence', '')
                                row['Risk Likelihood'] = risk.get('likelihood', '')
                                row['Risk Score'] = risk.get('risk_score', '')
                                row['Risk Level'] = risk.get('risk_level', '')
                            
                            # Add management task data
                            if 'management_task' in mode:
                                task = mode['management_task']
                                row['Task Type'] = task.get('task_type', '')
                                row['Task Description'] = task.get('description', '')
                                row['Technically Feasible'] = task.get('technically_feasible', '')
                                row['Worth Doing'] = task.get('worth_doing', '')
                                row['Justification'] = task.get('justification', '')
                                row['Task Cost ($)'] = task.get('cost', 0)
                                row['Failure Cost ($)'] = task.get('failure_cost', 0)
                                
                                # Add post-implementation risk assessment if exists
                                if 'post_risk_assessment' in task:
                                    post_risk = task['post_risk_assessment']
                                    row['Post-Task Risk Consequence'] = post_risk.get('consequence', '')
                                    row['Post-Task Risk Likelihood'] = post_risk.get('likelihood', '')
                                    row['Post-Task Risk Score'] = post_risk.get('risk_score', '')
                                    row['Post-Task Risk Level'] = post_risk.get('risk_level', '')
                            
                            all_data.append(row)
                
                if all_data:
                    df_complete = pd.DataFrame(all_data)
                    
                    # Convert to Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_complete.to_excel(writer, sheet_name='Complete FMECA Analysis', index=False)
                    output.seek(0)
                    
                    st.download_button(
                        label="📥 Download Complete Project (Excel)",
                        data=output,
                        file_name=f"rcm_project_{st.session_state.project_data.get('project_no', 'project')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    st.info(f"Includes all {len(st.session_state.assets)} assets and {len(all_data)} failure modes")
                else:
                    st.warning("No failure mode data available to export")
            else:
                st.warning("No assets available to export")
        
        with col2:
            st.markdown("#### Export Single Asset (Excel)")
            
            if st.session_state.assets:
                asset_for_export = st.selectbox(
                    "Select Asset to Export",
                    options=range(len(st.session_state.assets)),
                    format_func=lambda x: st.session_state.assets[x]['asset_name'],
                    key="excel_export_selector"
                )
                
                selected_asset = st.session_state.assets[asset_for_export]
                
                if selected_asset.get('failure_modes'):
                    # Compile failure modes data for this asset
                    asset_data = []
                    for mode in selected_asset['failure_modes']:
                        row = {
                            'Asset Name': selected_asset['asset_name'],
                            'Asset Class': selected_asset.get('asset_class', ''),
                            'Asset Type': selected_asset.get('asset_type', ''),
                            'Site Location': selected_asset.get('site_location', ''),
                            'Failure Mode ID': mode['id'],
                            'Functional Failure ID': mode.get('functional_failure_id', ''),
                            'Component': mode['component'],
                            'Failure Mode': mode['description'],
                            'Failure Mode Category': mode.get('category', ''),
                        }
                        
                        # Add effects data
                        if 'effects' in mode:
                            effects = mode['effects']
                            row['Evidence of Failure'] = effects.get('evidence', '')
                            row['Safety/Environmental Impact'] = effects.get('safety_impact', '')
                            row['Operational Impact'] = effects.get('operational_impact', '')
                            row['Physical Damage'] = effects.get('physical_damage', '')
                            row['Repair Action'] = effects.get('repair_action', '')
                            row['Repair Time (hrs)'] = effects.get('repair_time', 0)
                            row['Downtime (hrs)'] = effects.get('downtime', 0)
                        
                        # Add consequence data
                        row['Consequence Category'] = mode.get('consequence_category', 'Not categorized')
                        
                        # Add risk assessment data
                        if 'risk_assessment' in mode:
                            risk = mode['risk_assessment']
                            row['Risk Consequence'] = risk.get('consequence', '')
                            row['Risk Likelihood'] = risk.get('likelihood', '')
                            row['Risk Score'] = risk.get('risk_score', '')
                            row['Risk Level'] = risk.get('risk_level', '')
                        
                        # Add management task data
                        if 'management_task' in mode:
                            task = mode['management_task']
                            row['Task Type'] = task.get('task_type', '')
                            row['Task Description'] = task.get('description', '')
                            row['Technically Feasible'] = task.get('technically_feasible', '')
                            row['Worth Doing'] = task.get('worth_doing', '')
                            row['Justification'] = task.get('justification', '')
                            row['Task Cost ($)'] = task.get('cost', 0)
                            row['Failure Cost ($)'] = task.get('failure_cost', 0)
                            
                            # Add post-implementation risk assessment if exists
                            if 'post_risk_assessment' in task:
                                post_risk = task['post_risk_assessment']
                                row['Post-Task Risk Consequence'] = post_risk.get('consequence', '')
                                row['Post-Task Risk Likelihood'] = post_risk.get('likelihood', '')
                                row['Post-Task Risk Score'] = post_risk.get('risk_score', '')
                                row['Post-Task Risk Level'] = post_risk.get('risk_level', '')
                        
                        asset_data.append(row)
                    
                    df_asset = pd.DataFrame(asset_data)
                    
                    # Convert to Excel
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_asset.to_excel(writer, sheet_name=selected_asset['asset_name'][:31], index=False)
                    output.seek(0)
                    
                    st.download_button(
                        label=f"📥 Download {selected_asset['asset_name']} (Excel)",
                        data=output,
                        file_name=f"rcm_analysis_{selected_asset['asset_name']}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                    st.info(f"Includes {len(asset_data)} failure modes for {selected_asset['asset_name']}")
                else:
                    st.info("No failure mode data available for this asset yet.")
        
        st.markdown("---")
        st.markdown("#### Import Project Data")
        
        uploaded_file = st.file_uploader("Upload JSON project file", type=['json'])
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                
                if st.button("📥 Import Project Data"):
                    load_import_data(imported_data)
                    autosave_session_data()
                    st.success("✅ Project data imported successfully!")
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
