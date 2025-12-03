# RCM Methodology & Workflow Guide

## The RCM Process Flow (Multi-Asset Projects)

```
┌─────────────────────────────────────────────────────────────────┐
│                     STAGE 1: PLANNING                           │
│  • Create Project (Project No. + Description)                   │
│  • Add Multiple Assets to Project                               │
│  • Define Components per Asset                                  │
│  • Document Operating Context per Asset                         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STAGE 2: RCM ANALYSIS (FMECA)                      │
│              [Select Asset from Project]                        │
│                                                                 │
│  Step 2: Functions        → What should it do?                  │
│  Step 3: Functional      → How can it fail to do that?          │
│          Failures         [Filtered by selected function]       │
│                          [Table-based view/update/delete]       │
│  Step 4: Failure Modes   → What causes each failure?            │
│                          [Component dropdown from asset]        │
│                          [Table-based view/update/delete]       │
│  Step 5: Failure Effects → What happens when it fails?          │
│                          [Comprehensive table with scrolling]   │
│                          [Table-based view/update/delete]       │
│  Step 6: Consequences    → How significant is the failure?      │
│                          [Risk assessment for safety]           │
│                          [Table-based view/update/delete]       │
│  Step 7: Task Selection  → How can we manage the failure?       │
│                          [Cost of Task & Cost of Failure]       │
│                          [Post-implementation risk for FTM/     │
│                           Redesign with Safety/Environmental]   │
│                          [Table-based view/update/delete tasks] │
│                                                                 │
│  [Repeat for each asset in project]                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STAGE 3: IMPLEMENTATION                        │
│              [Select Asset from Project]                        │
│  • Develop Maintenance Schedules per Asset                      │
│  • Plan One-off Changes (Redesign)                              │
│  • Assign Resources                                             │
│  • Update Procedures                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              STAGE 4: REPORTS & EXPORT                          │
│  • Project-Level Summary (All Assets)                           │
│  • Asset-Level Detailed Reports                                 │
│  • Export Complete Project or Individual Assets                 │
│  • Monitor Performance Across Project                           │
│  • Review & Update Analysis                                     │
└─────────────────────────────────────────────────────────────────┘
```

## The 7 RCM Questions

| Question | RCM Focus | Output |
|----------|-----------|--------|
| 1. What are the functions? | Understanding what users want | **Functions** with performance standards |
| 2. How can it fail? | Identify ways of not meeting function | **Functional Failures** |
| 3. What causes failure? | Root cause at component level | **Failure Modes** |
| 4. What happens? | Document effects and consequences | **Failure Effects** |
| 5. Why does it matter? | Prioritize by consequence | **Consequence Categories** |
| 6. What prevents it? | Proactive management | **Maintenance Tasks** |
| 7. What if no prevention? | Default actions | **Redesign or Accept** |

## Consequence Decision Tree

```
                    Does Failure Occur?
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
    Evident to                          Not Evident
    Operators?                          (Hidden)
        │                                     │
        ▼                                     ▼
What are the                          What if Protected
consequences?                         Function Also Fails?
        │                                     │
┌───────┼───────┐                    ┌────────┼────────┐
│       │       │                    │        │        │
Safety  Ops    Non-ops              Safety    Ops     Non-ops
Enviro                              Enviro
│       │       │                    │        │        │
▼       ▼       ▼                    ▼        ▼        ▼
[RED] [ORANGE] [YELLOW]            [RED]  [ORANGE] [YELLOW]

Then apply Task Selection Logic...
```

## Task Selection Logic

### For Safety/Environmental Consequences (RED)

```
1. Is CBM feasible AND reduces risk to acceptable? 
   └─ YES → Apply CBM
   └─ NO → Go to 2

2. Is FTM feasible AND reduces risk to acceptable?
   └─ YES → Apply FTM  
   └─ NO → Go to 3

3. Is FF feasible AND reduces risk to acceptable?
   └─ YES → Apply FF (for Hidden only)
   └─ NO → Go to 4

4. MUST REDESIGN (Safety risk unacceptable)
```

### For Operational/Non-operational (ORANGE/YELLOW)

```
1. Is CBM feasible AND cost-effective?
   └─ YES → Apply CBM
   └─ NO → Go to 2

2. Is FTM feasible AND cost-effective?
   └─ YES → Apply FTM
   └─ NO → Go to 3

3. Is FF feasible AND cost-effective?
   └─ YES → Apply FF (for Hidden only)
   └─ NO → Go to 4

4. Redesign OR Operate to Failure?
   └─ Compare lifecycle costs
```

## Task Types Explained

### CBM - Condition Based Maintenance

**When:** Failure gives warning signs
**How:** Monitor condition, act when threshold reached
**Example:** "Check bearing temperature weekly. Replace if >70°C"

**Requirements:**

- Detectable potential failure condition
- Consistent P-F interval
- Can monitor more frequently than P-F interval
- Time to act before functional failure

### FTM - Fixed Time Maintenance  

**When:** Failure probability increases with age
**How:** Replace/overhaul at fixed interval
**Example:** "Replace filter every 500 hours"

**Requirements:**

- Age-related failure pattern
- Known useful life (tracked separately)
- MTBF (Mean Time Between Failures) data
- Interval less than useful life
- Cost-effective vs. consequence

**For Safety/Environmental Consequences:**

- Post-implementation risk assessment required
- Must demonstrate risk reduction to acceptable levels
- Risk sliders: Consequence Severity + Likelihood = Risk Level

### FF - Failure Finding

**When:** Hidden failures (protective devices)
**How:** Periodically test if still functional
**Example:** "Test pressure relief valve monthly"

**Requirements:**

- Function is hidden
- Test doesn't increase risk
- Practical to test at required frequency
- Reduces multiple failure risk

### Redesign

**When:** No effective proactive task OR unacceptable risk
**How:** One-off change to equipment/process/procedure
**Example:** "Install redundant pressure transmitter"

**For Safety/Environmental Consequences:**

- Post-implementation risk assessment required
- Must demonstrate risk reduction to acceptable levels
- Risk sliders: Consequence Severity + Likelihood = Risk Level
- Same validation process as FTM tasks

### OTF - Operate to Failure

**When:** Consequence acceptable AND no cost-effective proactive task
**How:** Accept failure, repair when occurs
**Example:** "Replace light bulb when it fails"

**Restrictions:**

- NOT available for Safety/Environmental consequences
- No cost tracking (task cost or failure cost)
- Only for Operational and Non-operational consequences

## Function Types Reference

| Type | Purpose | Example |
|------|---------|---------|
| **Primary** | Main reason for asset | "To pump water at 250 L/s" |
| **Secondary** | | |
| - Environmental | Protect environment | "To contain all fluids with no leakage" |
| - Safety | Protect people | "To provide emergency shutdown" |
| - Structural | Physical strength | "To support 5,000 kg load" |
| - Control | Regulate/indicate | "To display pressure ±2%" |
| - Containment | Hold materials | "To contain hydraulic oil" |
| - Protection | Detect/limit failure | "To shut down if temp >80°C" |
| - Economy | Optimize resources | "To operate at >85% efficiency" |

## Performance Standard Types

| Type | Description | Example |
|------|-------------|---------|
| **Quantitative** | Measurable number | "250 L/s", "1,147 kPa", "±5%" |
| **Qualitative** | Descriptive | "Clean appearance", "No visible rust" |
| **Absolute** | Must be fully met | "Zero leakage" (implied) |
| **Variable** | Changes with conditions | "100-250 L/s depending on demand" |
| **Upper/Lower Limits** | Fixed boundaries | "Between 500-600 kPa" |

## Failure Mode Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Deterioration** | Wear, corrosion, fatigue | Bearing wear, pipe corrosion, crack growth |
| **Lubrication** | Lack or contamination | Dry bearing, oil oxidation, wrong grade |
| **Dirt** | Contamination | Filter blockage, valve jamming |
| **Disassembly** | Components separate | Loose bolt, weld failure |
| **Human Error** | Mistakes | Wrong setting, incorrect assembly |
| **Overloading** | Exceeds capacity | Excessive pressure, overheating |

## P-F Interval Concepts

```
Condition
    │
    │ ────────────────────
    │
    │                P ─┐ ← Potential Failure Detected
    │                   │   (e.g., bearing temperature rising,
    │                   │    vibration increasing,
    │                   │    performance degrading)
    │                   │
    │                   │ P-F Interval
    │                   │ (Warning Period)
    │                   │
    │                   │
    │                F ─┘ ← Functional Failure
    │                      (e.g., bearing seized,
    │                       no output)
    └────────────────────────────────────────→ Time

Inspection Frequency = 1/2 to 1/3 of P-F Interval
```

## Cost-Effectiveness Analysis

### For FTM Task

**Cost Tracking (Operational/Non-operational only):**

- **Cost of Task**: Labour + Parts + Other
- **Cost of Failure**: Labour + Parts + Other (separate tracking)

```
Annual Cost of Task = (Labour + Parts + Other) × (365 / Interval)
Annual Cost of Failure = (Repair Cost + Consequence Cost) × (365 / MTBF)

Task is Worth Doing if:
Annual Cost of Task < Annual Cost of Failure
```

### Example

- Replace gasket every 2 years: $350 → $175/year
- Failure every 3 years: $350 + $1,000 → $450/year
- Task is worth doing! ($175 < $450)

**Note:** Cost fields are not displayed for:
- Safety/Environmental consequences (focus on risk reduction)
- OTF tasks (no preventive cost to track)

## Risk Assessment Matrix

| Consequence → | 1-Insignificant | 2-Minor | 3-Moderate | 4-High | 5-Catastrophic |
|---------------|-----------------|---------|------------|--------|----------------|
| **5-Almost Certain** | 6 (M) | 7 (H) | 8 (H) | 9 (H) | 10 (H) |
| **4-Likely** | 5 (M) | 6 (M) | 7 (H) | 8 (H) | 9 (H) |
| **3-Occasional** | 4 (L) | 5 (M) | 6 (M) | 7 (H) | 8 (H) |
| **2-Unlikely** | 3 (L) | 4 (L) | 5 (M) | 6 (M) | 7 (H) |
| **1-Rare** | 2 (L) | 3 (L) | 4 (L) | 5 (M) | 6 (M) |

Risk Score = Consequence + Likelihood

- **2-5**: Low Risk (L) - May accept or apply low-cost controls
- **6-7**: Medium Risk (M) - Should implement controls
- **8-10**: High Risk (H) - Must implement controls

## Data Collection Tips

### For Operating Context

- Review P&IDs, layout drawings
- Interview operators and maintainers  
- Check maintenance history
- Review OEM manuals
- Understand seasonal patterns

### For Failure Modes

- Use maintenance work order history
- Consult with experienced staff
- Review similar equipment failures
- Check industry databases
- Consider environmental factors

### For P-F Intervals

- Analyze historical condition data
- Consult OEM recommendations
- Reference industry standards
- Consider operating conditions
- Start conservative, refine with data

## User Interface Tips

### Table-Based Data Management (Steps 3-6)

The application uses a consistent pattern for managing analysis data:

1. **Add New Items**: Fill in form fields and click "Add" button
2. **View All Items**: Browse comprehensive tables with all entries
3. **Select for Action**: Use radio buttons to select a specific row
4. **Update or Delete**: Click "Update Selected" or "Delete Selected" buttons
5. **Save Changes**: Confirm updates or deletions with dedicated buttons

**Benefits:**

- Easy navigation through large datasets
- Clear view of all entries before taking action
- Reduced risk of accidental modifications
- Consistent interaction pattern across all analysis steps

### Function-Specific Filtering (Step 3)

Functional failures are automatically filtered to show only those related to the currently selected function. This helps:

- Focus on relevant failures
- Avoid confusion with failures from other functions
- Maintain clarity in complex multi-function assets

### Dynamic Component Lists (Step 4)

The component dropdown in Step 4 automatically reflects components defined in Step 1 for the selected asset. Ensures:

- Consistency across analysis steps
- Prevention of orphaned failure modes
- Accurate asset-specific data

## Common Pitfalls to Avoid

❌ **Don't:**

- Analyze at wrong level (too high = miss details, too low = overwhelming)
- Combine different failure modes with different effects
- Describe effects assuming current maintenance (describe worst case)
- Skip consequence categorization (leads to poor task selection)
- Implement tasks without feasibility/worth doing analysis
- Delete entries without reviewing table first

✅ **Do:**

- Focus on functions users care about
- Be specific with performance standards
- Consider operating context throughout
- Document assumptions clearly
- Review and update regularly
- Use table views to review all data before making changes
- Take advantage of filtering to focus on specific functions

## Success Metrics

Track your RCM effectiveness:

- **Reliability**: MTBF increasing?
- **Availability**: Uptime improving?
- **Cost**: Maintenance cost per unit output decreasing?
- **Safety**: Safety incidents trending down?
- **Proactive vs. Reactive**: More planned work?

---

*"RCM is not about preventing all failures; it's about managing the consequences of failures effectively."*
