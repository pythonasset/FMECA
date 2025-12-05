# Changelog

All notable changes to the FMECA & RCM Analysis Tool will be documented in this file.

## [1.0.1] - 2025-12-06

### Added

- **Administration Section**: New administration panel in sidebar for configuring application settings
  - Positioned above Data Management for easy access
  - Configure Risk Matrix option with dropdown menu
  - Fully functional risk threshold configuration interface
- **Configurable Risk Matrix**: Dynamic risk classification system with customizable thresholds
  - Adjustable Moderate Risk threshold (default: 6)
  - Adjustable High Risk threshold (default: 8)
  - Real-time preview of threshold changes
  - Validation to ensure High > Moderate
  - Save and Reset functionality
- **Dynamic Risk Classification**: All risk assessments now use configurable thresholds
  - Risk Matrix table (Tab 7) updates dynamically based on saved thresholds
  - Consequence category risk assessments (Tab 6) use current thresholds
  - Task risk assessments (FTM, Redesign) apply configured thresholds
  - Task update forms reflect current threshold settings
- **Enhanced UI Styling**: Improved visual consistency for dropdown elements
  - Red borders on all dropdown/selectbox elements
  - Light grey background (#f5f5f5) for dropdown menu options
  - Light grey text color (#808080) for improved readability
  - Hover states with darker grey (#e0e0e0) for better user feedback

### Changed

- **Risk Matrix Classification**: Updated risk score 7 classification from "High" to "Moderate"
  - Risk Matrix table cells now show "7 (M)" instead of "7 (H)"
  - Matrix legend updated: L = Low (2-5), M = Moderate (6-7), H = High (8-10)
  - Applies orange color coding consistently for scores 6-7
- **Sidebar Organization**: Repositioned Administration section
  - Moved from bottom to above Data Management
  - Improved navigation hierarchy and accessibility

### Fixed

- **Risk Score Consistency**: Ensured score 7 is classified as "Moderate" throughout the application
  - Updated all risk assessment displays (4 locations)
  - Corrected Risk Matrix visualization
  - Aligned with configurable threshold system

### Technical Details

- **Dynamic Risk Functions**: Added helper functions for threshold-based classification
  - `get_risk_level(risk_score)`: Returns risk level and color based on thresholds
  - `get_risk_matrix_cell_class(score)`: Returns CSS class for matrix cells
  - `get_risk_matrix_cell_label(score)`: Returns L/M/H label for cells
  - `generate_risk_matrix_html()`: Generates dynamic matrix HTML
- **Session State Management**: Risk thresholds stored in session state
  - `risk_moderate_threshold`: Configurable moderate risk minimum score
  - `risk_high_threshold`: Configurable high risk minimum score
  - Persists throughout user session
- **CSS Enhancements**: Extended stylesheet for dropdown styling
  - Multiple CSS selectors for comprehensive dropdown targeting
  - Popover, menu, listbox, and option element styling
  - Hover and selected state customization
- Files modified: `rcm_fmeca_app.py`
- Lines affected: ~150 lines modified/added
- New dependencies: `time` module (built-in)

---

## [Unreleased] - 2024-12-04

### Added
- **Availability-Based FFI Calculation for Failure Finding Tasks**: Implemented informal approach for setting Failure Finding Intervals (FFI) based on protective device availability
  - Added availability lookup table (99.99% to 95%)
  - Automatic FFI calculation in days based on MTBF and selected availability
  - FFI percentages: 0.02%, 0.1%, 0.2%, 1%, 2%, 4%, 10% of MTBF
- **Excel Export Functionality**: Complete project and single asset exports now use Excel format (.xlsx)
  - Export Complete Project: All assets with comprehensive FMECA data in Excel
  - Export Single Asset: Individual asset analysis with all details in Excel
  - Better data analysis and filtering capabilities compared to CSV
- **Horizontal Scrollbar for FMECA Tables**: Added horizontal scrolling to Detailed FMECA Analysis table in Stage 4 Asset Reports
- **Comprehensive Data in Export Tables**: Export files now include all analysis data
  - Failure mode details (ID, component, description, category)
  - Complete failure effects (evidence, impacts, repair actions, downtime)
  - Consequence categories and risk assessments
  - Management tasks with costs and post-implementation risk levels
  - Asset information (name, class, type, location)

### Changed
- **FF Task Availability**: Failure Finding (FF) option now only appears in task selection when consequence category is "Hidden"
  - Prevents inappropriate use of FF for evident failures
  - Ensures compliance with RCM methodology
- **FFI Calculation Method**: Replaced manual FFI input with automated calculation based on availability selection
  - User selects desired availability percentage
  - System calculates FFI automatically from MTBF
  - More consistent and methodologically sound approach
- **Export Format**: Changed from JSON/CSV to Excel (.xlsx) for primary export functionality
  - Maintains JSON import for project restore functionality
  - Excel provides better usability for end-user analysis

### Fixed
- **Module Dependency**: Added openpyxl to project dependencies for Excel export functionality
  - Installed openpyxl 3.1.5 and et-xmlfile 2.0.0

### Documentation
- Updated README.md with:
  - New FF approach description
  - Excel export formats
  - openpyxl dependency requirement
  - Enhanced FMECA table features
- Updated METHODOLOGY_GUIDE.md with:
  - Detailed availability-based FFI calculation methodology
  - FF availability restrictions
  - Updated export workflow information
- Updated QUICK_START.md with:
  - Installation instructions including openpyxl
  - FF task selection guidance
  - Excel export instructions

### Technical Details
- Files modified: `rcm_fmeca_app.py`
- Lines affected: ~200 lines modified/added
- New dependencies: openpyxl 3.1.5, et-xmlfile 2.0.0

---

## Previous Versions

See git history for previous version changes.
