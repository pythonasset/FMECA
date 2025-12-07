# FMECA & RCM Analysis Tool

A comprehensive Streamlit application for conducting Failure Modes, Effects and Criticality Analysis (FMECA) and Reliability Centered Maintenance (RCM) analysis on infrastructure assets with **multi-asset project management**.

## Overview

This application implements the complete RCM methodology based on the Murrumbidgee Irrigation RCM Course materials, enabling project-based analysis across multiple assets:

- **Stage 1: Planning & Preparation** - Create projects and manage multiple assets
- **Stage 2: RCM Analysis (FMECA)** - Systematic analysis of failures and consequences per asset
- **Stage 3: Implementation** - Plan maintenance schedules and changes per asset
- **Stage 4: Reports & Export** - Generate project-level and asset-level reports

## Features

### Project Management (NEW)
- **Multi-Asset Projects**: Organize multiple assets under a single project number
- **Project-Level Tracking**: Monitor analysis progress across all assets
- **Centralized Export**: Export complete projects or individual assets
- **Aggregate Reporting**: View project-wide statistics and costs

### Core RCM Methodology
- **7 RCM Questions Framework**: Structured approach answering the fundamental questions of RCM
- **FMECA Analysis**: Complete failure modes, effects, and criticality analysis
- **Consequence Categorization**: 6-category system (Hidden/Evident × Safety/Operational/Non-operational)
- **Configurable Risk Matrix**: Customizable risk thresholds for flexible risk classification
- **Task Selection**: Intelligent selection of maintenance strategies (CBM, FTM, FF, Redesign, OTF)
- **Interactive Data Management**: Table-based selection for viewing, updating, and deleting analysis data

### Key Capabilities
- ✅ **Project-based organization** with unique project numbers
- ✅ **Multiple assets per project** with independent analyses
- ✅ Asset and component definition with hierarchical structure
- ✅ Operating context documentation
- ✅ Function identification with performance standards
- ✅ Functional failure analysis with function-specific filtering
- ✅ Failure mode identification at component level
- ✅ Detailed failure effects documentation
- ✅ Risk-based consequence assessment
- ✅ Maintenance task selection and validation
- ✅ Cost estimation and benefit analysis
- ✅ Implementation planning per asset
- ✅ **Project-level and asset-level reporting**
- ✅ Import/export for data persistence
- ✅ **Table-based UI** for easy viewing, updating, and deleting of analysis data
- ✅ **Configurable risk thresholds** via Administration panel

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- openpyxl (for Excel export functionality)

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd rcm-fmeca-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run rcm_fmeca_app.py
```

4. Open your web browser to the URL shown (typically http://localhost:8501)

## First-Time Setup

### Step 1: Software Registration (One-Time)

On first launch, you'll be prompted to register the software for your organization:

1. Complete the registration form with:
   - **Authority/Organization Name** * (required)
   - **Department/Division** * (required)
   - **Contact Person Name** * (required)
   - **Contact Email** * (required)
   - Phone Number (optional)
   - Organization Address (optional)

2. Click "✅ Register Application"
3. Registration details are saved to `.registration` file

**Note**: This is a one-time organizational registration. Your registration details will appear throughout the application.

### Step 2: User Authentication (Every Session)

After software registration, user authentication is required:

#### Default Administrator Account

A default admin account is automatically created:
- **Username**: `admin`
- **Password**: `#$^@*******`
- **User Type**: Administrator (full access)

**Important**: This account cannot be modified or deleted and provides initial access to the system.

#### Logging In

1. Enter your username and password
2. Click "🔓 Login"
3. Upon successful login, you'll see the main application

#### Registering New Users

New users can register themselves:

1. Click the "📝 Register New User" tab
2. Complete the registration form:
   - **Username** * (unique, cannot be "admin")
   - **Full Name** * (required)
   - **Position** * (required, e.g., "Asset Manager")
   - **Password** * (minimum 6 characters)
   - **Confirm Password** * (must match)

3. Click "✅ Register"
4. New users are created with "User" type by default
5. Return to Login tab to access the application

**Note**: All passwords are securely hashed using SHA-256 encryption and never stored in plain text.

## User Types and Permissions

The application implements role-based access control with three user types:

### 👤 User (Default)
- Access to all RCM analysis features (Stages 1-4)
- Can create projects and conduct analyses
- Can export and import data
- **Cannot** access Administration section

### ⚙️ Super User
- All User permissions
- **Can** access Administration section
- Can configure risk matrix settings
- **Cannot** manage other users

### 🔐 Administrator
- Full access to all features
- Can access Administration section
- Can configure risk matrix settings
- **Can manage user types** for all users
- Can promote users to Super User or Administrator
- View login statistics for all users

**Note**: Only Administrators can change user types. This is done through Administration → Manage Users.

## Usage Guide

### Stage 1: Planning & Preparation

#### Create Your Project

1. **Define Project Information**
   - Enter Project No. (e.g., "RCM-2024-001")
   - Enter Project Description (e.g., "Water Treatment Plant RCM Analysis")
   - Click "Save Project Information"

2. **Add Assets to Project**
   - Enter asset name (e.g., "Tharbogang PS2 - Jockey Pump Assembly 1")
   - Select asset class (Pump Station, Water Treatment Plant, etc.)
   - Specify asset type and location
   - Define components for this asset (Motor, Pump, VFD, Flow Meter, etc.)
   - Click "Save New Asset"
   - Repeat for all assets in your project

3. **Manage Assets**
   - **Edit**: Click the "Edit" button next to any asset to modify its details
   - **Delete**: Remove assets that are no longer needed
   - **View**: See all assets listed under your project

**Note**: You can add any number of assets to a project. Each asset will have its own independent RCM analysis.

### Stage 2: RCM Analysis (FMECA)

**Select an Asset**: Choose which asset to analyze from the dropdown menu at the top of Stage 2.

Each asset's analysis is stored independently, allowing you to:

#### Step 2: Identify Functions
Define what the asset is supposed to do:
- Use format: [Verb] + [Object] + [Performance Standard]
- Example: "To pump water from reservoir at 250 L/s at 1,147 kPa"
- Include primary and secondary functions
- Specify quantifiable performance standards where possible

#### Step 3: Identify Functional Failures
How can the asset fail to meet its functions?
- **Filtered by Function**: View functional failures specific to the selected function
- Complete loss: "Unable to pump any water"
- Partial loss: "Pumps water at less than 250 L/s"
- Exceeds limits: "Pressure exceeds 1,200 kPa"
- **Table-based Management**: View all functional failures in a table, select any row to update or delete

#### Step 4: Identify Failure Modes
What specifically causes each functional failure?
- **Component Dropdown**: Automatically populated with components defined for the selected asset in Step 1
- Identify at component level
- Include cause: "Pump bearing seized due to lack of lubrication"
- Categories: Deterioration, lubrication, contamination, disassembly, human error, overloading
- **Table-based Management**: View all failure modes in a table, select any row to update or delete

#### Step 5: Identify Failure Effects
What happens when each failure occurs?
- Evidence of failure
- Safety and environmental impacts
- Operational impacts
- Physical damage
- Repair requirements and downtime
- **Comprehensive Table View**: See all failure effects with horizontal scrolling for complete data visibility
- **Table-based Management**: View all failure effects in a table, select any row to update or delete

#### Step 6: Categorize Consequences
Determine the significance of each failure:
- **Hidden failures**: Not evident to operators (protective devices)
- **Evident failures**: Operators know when it occurs
- **Safety/Environmental**: Can hurt people or breach environmental standards
- **Operational**: Affects output, quality, or service
- **Non-operational**: Only direct repair costs
- **Table-based Management**: View all consequence categories in a table, select any row to update or delete
- **Risk Assessment**: Automatic risk level calculation for safety/environmental consequences using configurable thresholds
- **Default Classification**: Low (2-5), Moderate (6-7), High (8-10) - customizable via Administration

#### Step 7: Select Failure Management Tasks
Choose appropriate maintenance strategy:

**Proactive Tasks:**

- **CBM** (Condition Based): Monitor condition, intervene when threshold reached
- **FTM** (Fixed Time): Replace/overhaul at fixed intervals, with separate Useful Life and MTBF tracking
- **FF** (Failure Finding): Test hidden failures periodically using availability-based FFI calculation (only available for Hidden consequence categories)

**Default Actions:**
- **Redesign**: One-off change to equipment/process/procedures
- **OTF** (Operate to Failure): Accept failure, repair when occurs (not available for Safety/Environmental consequences)

Each task must be:
1. Technically feasible (can it be done?)
2. Worth doing (does it address consequences cost-effectively?)

**Task-Specific Features:**
- **Cost Analysis**: For Operational/Non-operational consequences, enter both Cost of Task and Cost of Failure (Labour, Parts, Other)
- **Risk Assessment**: For FTM and Redesign tasks with Safety/Environmental consequences, assess post-implementation risk levels
- **Task Management**: View, update, or delete tasks using the comprehensive table with horizontal scrolling
- **Smart Controls**: OTF option automatically excluded for safety-critical failures

### Stage 3: Implementation

**Select an Asset**: Choose which asset to plan implementation for.

Review and plan for each asset:
- Maintenance schedules for CBM, FTM, FF tasks
- One-off changes for redesign tasks
- Implementation checklist for tracking
- Resource allocation and scheduling

### Administration

Access the Administration panel from the sidebar to configure application settings:

#### Configure Risk Matrix

- **Customize Risk Thresholds**: Adjust how risk scores are classified
  - Set Moderate Risk threshold (default: 6)
  - Set High Risk threshold (default: 8)
  - Preview changes before applying
- **Dynamic Updates**: Changes apply immediately to:
  - Risk Matrix table in Stage 2, Tab 7
  - All consequence category risk assessments
  - Task selection risk evaluations
  - Task update forms
- **Validation**: Ensures High threshold is always greater than Moderate
- **Reset Option**: Return to default thresholds at any time

**Note**: Risk threshold configuration persists throughout your session but resets to defaults when you restart the application.

### Stage 4: Reports & Export

Generate project-level and asset-level reports:

#### Project Summary Tab
- Overall statistics across all assets
- Total functions, failure modes, and tasks
- Aggregate annual maintenance costs
- Asset overview table

#### Asset Reports Tab
- **Select an Asset**: Choose which asset to view detailed reports for
- Individual asset analysis statistics
- Detailed FMECA tables per asset with horizontal scrollbar for easy navigation
- Complete analysis data including effects, consequences, risk assessments, and tasks
- Consequence breakdowns
- Task type analysis

#### Export Data Tab
- **Export Complete Project (Excel)**: Download all assets with complete FMECA data as Excel file (.xlsx)
- **Export Single Asset (Excel)**: Download individual asset analysis with complete data as Excel file (.xlsx)
- **Import Project**: Upload previously saved JSON project files
- Maintains all asset data and analyses
- Excel exports include all failure modes, effects, consequences, risk assessments, and management tasks

## RCM Decision Logic

### For Safety/Environmental Consequences:
1. Is a CBM task technically feasible and reduces risk to acceptable level? → Implement CBM
2. If not, is FTM technically feasible and reduces risk to acceptable level? → Implement FTM
3. If not, is FF technically feasible and reduces risk to acceptable level? → Implement FF
4. If not, must Redesign to reduce risk

### For Operational/Non-operational Consequences:
1. Is a CBM task technically feasible and cost-effective? → Implement CBM
2. If not, is FTM technically feasible and cost-effective? → Implement FTM
3. If not, is FF technically feasible and cost-effective? → Implement FF
4. If not, evaluate Redesign vs. Operate to Failure based on lifecycle costs

## Example: Water Pump Station

### Asset Definition
- **Asset**: Main Pump Assembly 1
- **Components**: Centrifugal Pump, 250kW Motor, VFD, Flow Meter

### Function Example
"To pump water from reservoir to distribution network at 153 L/s at 1,147 kPa"

### Functional Failure Examples
1. Unable to pump any water
2. Pumps water at less than 60 L/s
3. Pumps water but pressure below 900 kPa

### Failure Mode Example
**Component**: Pump Bearing
**Failure Mode**: "Bearing seized due to lack of lubrication"
**Effect**: Motor trips, standby pump activates, 2-hour downtime for repair
**Consequence**: Evident (Operational)
**Task**: FTM - Lubricate bearing every 500 hours

## Data Persistence

The application uses a project-based data model with automatic saving:

1. **Project Export**: Export entire project (all assets) as JSON
2. **Asset Export**: Export individual asset analysis as CSV
3. **Import**: Upload JSON project file to restore complete project
4. **Auto-save**: Automatic session saving during active use

**Recommended Workflow:**
- Export project Excel files regularly for comprehensive data backup
- Use single asset Excel for sharing specific results
- Import project JSON to resume work across sessions
- Excel format provides better data analysis and filtering capabilities

## Tips for Effective Analysis

1. **Project Organization**: Group related assets under meaningful project numbers
2. **Asset Scope**: Define clear boundaries for each asset to avoid overlap
3. **Be Specific**: Use precise, quantifiable performance standards
4. **Focus on Real Failures**: Only analyze failure modes that are reasonably likely
5. **Document Thoroughly**: Complete failure effects enable better decision-making
6. **Think Zero-Based**: Describe effects assuming no current maintenance (worst case)
7. **Validate Tasks**: Ensure tasks are both feasible and cost-effective
8. **Regular Reviews**: Update analysis as conditions change
9. **Consistent Approach**: Apply the same rigor across all assets in a project

## Technical Details

### Application Structure
- `rcm_fmeca_app.py`: Main Streamlit application
- Project-based session state management
- Multi-asset support with independent analyses
- JSON export/import for long-term storage
- Responsive layout with multi-column design

### Data Model
```python
{
  'project_information': {
    'project_no': str,
    'project_description': str,
    'created_date': str,
    'last_modified': str
  },
  'assets': [
    {
      'asset_name': str,
      'asset_class': str,
      'asset_type': str,
      'site_location': str,
      'components': [...],
      'operating_context': {...},
      'functions': [...],
      'functional_failures': [...],
      'failure_modes': [...],
      'analysis_results': [...]
    }
  ]
}
```

## Troubleshooting

**Issue**: Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Data lost after closing browser
- Use Export function to save work before closing
- Import JSON file to restore when reopening

**Issue**: Large analysis is slow
- Consider breaking complex assets into sub-systems
- Use CSV export for large datasets

## References

Based on:
- Murrumbidgee Irrigation RCM Course Materials
- RCM II by John Moubray
- ISO 55000 Asset Management Standards
- SAE JA1011 RCM Standard

## Support & Contributions

For issues, suggestions, or contributions, please refer to the project repository.

## License

[Specify your license here]

## Acknowledgments

Developed based on the Murrumbidgee Irrigation FMECA and RCM In-depth Course V1.0 materials.
