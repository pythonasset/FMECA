# FMECA & RCM Analysis Tool

A comprehensive Streamlit application for conducting Failure Modes, Effects and Criticality Analysis (FMECA) and Reliability Centered Maintenance (RCM) analysis on infrastructure assets.

## Overview

This application implements the complete RCM methodology based on the Murrumbidgee Irrigation RCM Course materials, guiding users through:

- **Stage 1: Planning & Preparation** - Define assets and operating context
- **Stage 2: RCM Analysis (FMECA)** - Systematic analysis of failures and consequences
- **Stage 3: Implementation** - Plan maintenance schedules and changes
- **Stage 4: Reports & Export** - Generate reports and export results

## Features

### Core RCM Methodology
- **7 RCM Questions Framework**: Structured approach answering the fundamental questions of RCM
- **FMECA Analysis**: Complete failure modes, effects, and criticality analysis
- **Consequence Categorization**: 6-category system (Hidden/Evident × Safety/Operational/Non-operational)
- **Task Selection**: Intelligent selection of maintenance strategies (CBM, FTM, FF, Redesign, OTF)

### Key Capabilities
- ✅ Asset and component definition with hierarchical structure
- ✅ Operating context documentation
- ✅ Function identification with performance standards
- ✅ Functional failure analysis
- ✅ Failure mode identification at component level
- ✅ Detailed failure effects documentation
- ✅ Risk-based consequence assessment
- ✅ Maintenance task selection and validation
- ✅ Cost estimation and benefit analysis
- ✅ Implementation planning
- ✅ Report generation and data export
- ✅ Import/export for data persistence

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

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

## Usage Guide

### Stage 1: Planning & Preparation

1. **Define Your Asset**
   - Enter asset name (e.g., "Tharbogang PS2 - Jockey Pump Assembly 1")
   - Select asset class (Pump Station, Water Treatment Plant, etc.)
   - Specify asset type and location
   - Define components (Motor, Pump, VFD, Flow Meter, etc.)

2. **Document Operating Context**
   - Redundancy configuration (stand-alone, duty/standby)
   - Utilization patterns and loading
   - Quality standards and seasonal demands
   - Skills and spares availability
   - Operating environment and standards

### Stage 2: RCM Analysis (FMECA)

#### Step 2: Identify Functions
Define what the asset is supposed to do:
- Use format: [Verb] + [Object] + [Performance Standard]
- Example: "To pump water from reservoir at 250 L/s at 1,147 kPa"
- Include primary and secondary functions
- Specify quantifiable performance standards where possible

#### Step 3: Identify Functional Failures
How can the asset fail to meet its functions?
- Complete loss: "Unable to pump any water"
- Partial loss: "Pumps water at less than 250 L/s"
- Exceeds limits: "Pressure exceeds 1,200 kPa"

#### Step 4: Identify Failure Modes
What specifically causes each functional failure?
- Identify at component level
- Include cause: "Pump bearing seized due to lack of lubrication"
- Categories: Deterioration, lubrication, contamination, disassembly, human error, overloading

#### Step 5: Identify Failure Effects
What happens when each failure occurs?
- Evidence of failure
- Safety and environmental impacts
- Operational impacts
- Physical damage
- Repair requirements and downtime

#### Step 6: Categorize Consequences
Determine the significance of each failure:
- **Hidden failures**: Not evident to operators (protective devices)
- **Evident failures**: Operators know when it occurs
- **Safety/Environmental**: Can hurt people or breach environmental standards
- **Operational**: Affects output, quality, or service
- **Non-operational**: Only direct repair costs

#### Step 7: Select Failure Management Tasks
Choose appropriate maintenance strategy:

**Proactive Tasks:**
- **CBM** (Condition Based): Monitor condition, intervene when threshold reached
- **FTM** (Fixed Time): Replace/overhaul at fixed intervals
- **FF** (Failure Finding): Test hidden failures periodically

**Default Actions:**
- **Redesign**: One-off change to equipment/process/procedures
- **OTF** (Operate to Failure): Accept failure, repair when occurs

Each task must be:
1. Technically feasible (can it be done?)
2. Worth doing (does it address consequences cost-effectively?)

### Stage 3: Implementation

Review and plan:
- Maintenance schedules for CBM, FTM, FF tasks
- One-off changes for redesign tasks
- Implementation checklist for tracking
- Resource allocation and scheduling

### Stage 4: Reports & Export

Generate comprehensive reports:
- Summary statistics and metrics
- Consequence breakdowns
- Task type analysis
- Detailed FMECA tables
- Export to CSV or JSON
- Import previous analyses

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

The application automatically saves your analysis in session state. To persist data:

1. **Export**: Use "Export to JSON" to save complete analysis
2. **Import**: Upload JSON file to restore previous work
3. **CSV Export**: Export results table for external analysis

## Tips for Effective Analysis

1. **Be Specific**: Use precise, quantifiable performance standards
2. **Focus on Real Failures**: Only analyze failure modes that are reasonably likely
3. **Document Thoroughly**: Complete failure effects enable better decision-making
4. **Think Zero-Based**: Describe effects assuming no current maintenance (worst case)
5. **Validate Tasks**: Ensure tasks are both feasible and cost-effective
6. **Regular Reviews**: Update analysis as conditions change

## Technical Details

### Application Structure
- `rcm_fmeca_app.py`: Main Streamlit application
- Session state for data persistence within session
- JSON export/import for long-term storage
- Responsive layout with multi-column design

### Data Model
```python
{
  'asset_data': {...},
  'operating_context': {...},
  'functions': [...],
  'functional_failures': [...],
  'failure_modes': [...],
  'analysis_results': [...]
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
