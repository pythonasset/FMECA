# Quick Start Guide - FMECA & RCM Analysis Tool

## Installation & First Run (5 minutes)

### Step 1: Install Dependencies

```bash
pip install streamlit pandas
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
streamlit run rcm_fmeca_app.py
```

The application will open automatically in your browser at `http://localhost:8502`

### Step 3: Try the Example (Optional)

1. Click "Stage 4: Reports & Export" in the sidebar
2. Navigate to "Export Data" tab
3. Upload `example_pump_station_analysis.json` if available
4. Click "Import Project Data"
5. Navigate through the stages to see a complete example

## Your First Project (35 minutes)

### Stage 1: Create Project & Add Assets (10 min)

#### Create Your Project (2 min)

1. Go to "Stage 1: Planning & Preparation"
2. Enter Project No. (e.g., "RCM-2024-001")
3. Enter Project Description (e.g., "Water Treatment Plant RCM")
4. Click "💾 Save Project Information"

#### Add First Asset (5 min)

1. Enter asset name (e.g., "Main Water Pump")
2. Select asset class from dropdown (e.g., "Pump Station")
3. Enter asset type (e.g., "Centrifugal Pump Assembly")
4. Enter site location (e.g., "Building A - Pump Room")
5. Add components using "Add Component" button
   - Example: Motor, Pump, Bearing, VFD, Valves
6. Click "💾 Save New Asset"

#### Add More Assets (3 min, optional)

1. Repeat the process for each additional asset
2. Edit any asset by clicking "✏️ Edit"
3. Delete unwanted assets with "🗑️ Del"
4. Each asset will have its own independent analysis

### Stage 2: Conduct Analysis (20 min per asset)

**IMPORTANT**: Select which asset to analyze from the dropdown at the top of Stage 2.

#### Step 2: Functions (5 min)

1. Select your asset from the dropdown
2. Define what this asset does
3. Use format: Verb + Object + Performance Standard
4. Start with primary function, then add safety/control functions
5. Example: "To pump water at 200 L/s at 500 kPa"

#### Step 3-4: Failures & Modes (5 min)

1. For each function, identify how it can fail
   - Functional failures are automatically filtered by the selected function
2. For each failure, identify specific component causes
   - Component dropdown is populated from Step 1 for the selected asset
3. Example:
   - Failure: "Unable to pump water"
   - Mode: "Bearing seized due to lack of lubrication"
4. View/Update/Delete:
   - Select any row from the table to view details
   - Click "Update Selected" or "Delete Selected" buttons

#### Step 5: Effects (5 min)

1. Describe what happens when failure occurs
2. Include: evidence, safety, operational impacts, downtime
3. Think worst-case scenario
4. View/Update/Delete:
   - Browse all effects in a comprehensive table with horizontal scrolling
   - Select any row to update or delete effect details

#### Step 6: Consequences (3 min)

1. Answer if failure is evident or hidden
2. Categorize based on impact
3. System will guide you through decision logic
4. Risk assessment automatically calculated for safety/environmental consequences
5. View/Update/Delete:
   - Review all consequence categories in a table
   - Select any row to update or delete categorization

#### Step 7: Task Selection (2 min)

1. Choose appropriate maintenance strategy
2. System provides options based on consequence
3. Validate task is feasible and worth doing

**Repeat Stage 2 for each asset in your project**

### Stage 3: Implementation (3 min per asset)

1. Select asset for implementation planning
2. Review maintenance schedule
3. Note any redesign tasks
4. Use implementation checklist

### Stage 4: View Reports & Export (2 min)

#### Project Summary Tab
1. View overall project statistics
2. See all assets and their analysis status
3. Review aggregate costs

#### Asset Reports Tab
1. Select an asset to view detailed reports
2. Review FMECA tables
3. Check consequence breakdowns

#### Export Data Tab
1. **Export Complete Project** (JSON) - includes all assets
2. **Export Single Asset** (CSV) - for specific asset results
3. JSON format preserves complete project for future updates

## Tips for Success

✅ **Project Organization**: Use meaningful project numbers
✅ **Asset Boundaries**: Define clear scope for each asset
✅ **One Asset at a Time**: Complete analysis for one asset before moving to next
✅ **Start Small**: Begin with 1-2 critical functions per asset
✅ **Be Specific**: Use measurable performance standards
✅ **Focus on Real Failures**: Only analyze likely failure modes
✅ **Table-Based UI**: Use radio button selection to easily view/update/delete any analysis item
✅ **Save Often**: Export project as JSON regularly
✅ **Consistent Approach**: Apply same rigor across all assets

## Common Workflows

### New Project with Multiple Assets

Stage 1 (Create Project + Add All Assets) → Stage 2 (Analyze Asset 1) → Stage 2 (Analyze Asset 2) → ... → Stage 3 (Each Asset) → Stage 4 (Project Export)

### Update Existing Project

Stage 4 (Import Project) → Stage 1 (Add/Edit Assets) → Stage 2 (Modify Analyses) → Stage 4 (Export Project)

### Generate Project Report

Stage 4 (Import Project) → Stage 4 (View Reports)

## Keyboard Shortcuts

- Use Tab to move between fields
- Enter to submit forms
- Browser back/forward for navigation history

## Getting Help

### Built-in Help

- Hover over (?) icons for field help
- Expand "Quick Reference" in sidebar
- Review example analysis

### Documentation

- Full README.md for detailed guidance
- RCM course PDF for methodology

## Next Steps

1. **Complete your first analysis** using this guide
2. **Review the example** to understand best practices  
3. **Export regularly** to save your work
4. **Iterate and improve** based on actual failure data

Need more detail? See the full README.md documentation.
