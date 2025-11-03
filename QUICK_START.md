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

The application will open automatically in your browser at `http://localhost:8501`

### Step 3: Try the Example

1. Click "Stage 4: Reports & Export" in the sidebar
2. Scroll to "Import Previous Analysis"
3. Upload `example_pump_station_analysis.json`
4. Click "Import Analysis Data"
5. Navigate through the stages to see a complete example

## Your First Analysis (30 minutes)

### Stage 1: Define Your Asset (5 min)

1. Enter asset name (e.g., "Main Water Pump Station")
2. Select asset class from dropdown
3. Add components using the "Add Component" button
   - Example: Motor, Pump, VFD, Valves
4. Fill in operating context
   - Focus on: redundancy, utilization, operating environment
5. Click "Save" and proceed to Stage 2

### Stage 2: Conduct Analysis (20 min)

#### Step 2: Functions (5 min)

1. Define what your asset does
2. Use format: Verb + Object + Performance Standard
3. Start with primary function, then add safety/control functions
4. Example: "To pump water at 200 L/s at 500 kPa"

#### Step 3-4: Failures & Modes (5 min)

1. For each function, identify how it can fail
2. For each failure, identify specific component causes
3. Example:
   - Failure: "Unable to pump water"
   - Mode: "Bearing seized due to lack of lubrication"

#### Step 5: Effects (5 min)

1. Describe what happens when failure occurs
2. Include: evidence, safety, operational impacts, downtime
3. Think worst-case scenario

#### Step 6: Consequences (3 min)

1. Answer if failure is evident or hidden
2. Categorize based on impact
3. System will guide you through decision logic

#### Step 7: Task Selection (2 min)

1. Choose appropriate maintenance strategy
2. System provides options based on consequence
3. Validate task is feasible and worth doing

### Stage 3: Implementation (3 min)

1. Review maintenance schedule
2. Note any redesign tasks
3. Use implementation checklist

### Stage 4: Export Results (2 min)

1. Review summary report
2. Export to CSV or JSON
3. JSON format preserves complete analysis for future updates

## Tips for Success

✅ **Start Small**: Begin with 1-2 critical functions
✅ **Be Specific**: Use measurable performance standards
✅ **Focus on Real Failures**: Only analyze likely failure modes
✅ **Save Often**: Export your work as JSON frequently
✅ **Use Examples**: Reference the pump station example for guidance

## Common Workflows

### New Asset Analysis

Stage 1 → Stage 2 (all steps) → Stage 3 → Stage 4 (Export)

### Update Existing Analysis

Stage 4 (Import) → Stage 2 (add/modify) → Stage 4 (Export)

### Generate Report Only

Stage 4 (Import) → Stage 4 (Reports)

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
