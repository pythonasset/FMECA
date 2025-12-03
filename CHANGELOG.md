# Changelog

All notable changes to the FMECA & RCM Analysis Tool will be documented in this file.

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
