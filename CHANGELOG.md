# Changelog

All notable changes to the FMECA & RCM Analysis Tool will be documented in this file.

## [1.0.2] - 2025-12-07

### Added

- **User Authentication System**: Comprehensive login and registration system for application access
  - Login form with username/password authentication
  - User registration with full name, position, and username
  - Secure password hashing (SHA-256)
  - Session management for logged-in users
  - Automatic user database initialization
  - Login counter tracking for all users
  - Last login timestamp recording
- **Role-Based Access Control**: Three-tier user type system for granular permissions
  - **User** (default): Access to RCM analysis features only
  - **Super User**: Access to RCM analysis and Administration section
  - **Administrator**: Full access including user management capabilities
- **Default Administrator Account**: Hidden admin account for initial system access
  - Username: `admin` (fixed, cannot be modified)
  - Position: System Administrator
  - User Type: Administrator (permanent)
  - Protected from modification or deletion
- **User Management Interface**: Administrator-only panel for managing user types
  - View all users with complete details (username, full name, position, user type, login count, last login, created date)
  - Change user types between User, Super User, and Administrator
  - Real-time user list with login statistics
  - Confirmation workflow for type changes
  - Protection for default admin account
- **Conditional Administration Access**: Administration section visibility based on user role
  - Only visible to Administrators and Super Users
  - Access verification at both sidebar and view levels
  - Prevent unauthorized access attempts
- **Login Statistics Tracking**: Comprehensive user activity monitoring
  - Login count increments with each successful authentication
  - Last login timestamp stored per user
  - Statistics visible in User Management interface
  - Persistent storage across sessions
- **Database Migration System**: Automatic conversion of user database schema
  - Migrates old `is_admin` field to new `user_type` field
  - Adds `login_count` to existing users (initialized to 0)
  - Backward compatibility with existing user databases
  - One-time migration on application startup

### Changed

- **Sidebar User Information**: Updated to display username instead of full name
  - Shows: User (username), Position, User Type
  - Cleaner, more concise display
  - Direct reference to login credentials
- **User Registration Flow**: Enhanced registration process
  - All new users default to "User" type
  - Position field now mandatory
  - Password minimum length: 6 characters
  - Username validation (cannot use "admin")
- **Authentication Flow**: Two-stage access control
  1. Software registration (organization-level, one-time)
  2. User authentication (per-user, every session)

### Security

- **Password Security**: SHA-256 hashing for all passwords
  - Passwords never stored in plain text
  - Secure authentication verification
- **Access Control**: Multiple layers of permission checking
  - Sidebar navigation filtering
  - View-level access verification
  - Role-based feature visibility
- **User Data Protection**: User database stored in `.users.json`
  - Separate from organization registration
  - Contains hashed passwords only
  - Login statistics for audit trail

### Technical Details

- **New Functions Added**:
  - `get_users_path()`: Returns path to user database file
  - `migrate_user_database()`: Migrates old database format to new schema
  - `initialize_users_db()`: Creates default admin user
  - `load_users()`: Loads user database from file
  - `save_user()`: Saves new user with default User type
  - `authenticate_user()`: Validates credentials and updates login counter
  - `is_user_logged_in()`: Checks login status
  - `get_user_type()`: Returns current user's type
  - `is_administrator()`: Checks if user is Administrator
  - `is_super_user()`: Checks if user is Super User
  - `can_access_administration()`: Verifies administration access rights
  - `update_user_type()`: Changes user type (Administrator only)
  - `show_login_form()`: Displays login/registration interface
  - `show_logout_button()`: Displays user info and logout in sidebar
- **New Session State Variables**:
  - `logged_in`: Boolean flag for authentication status
  - `current_user`: Currently logged-in username
  - `user_data`: Complete user profile data
- **New Database File**: `.users.json`
  - User accounts with hashed passwords
  - User types and permissions
  - Login statistics (count and last login)
  - Creation timestamps
- **User Database Schema**:
  ```json
  {
    "username": {
      "password": "hashed_password",
      "full_name": "Full Name",
      "position": "Position Title",
      "user_type": "User|Super User|Administrator",
      "login_count": 0,
      "last_login": "ISO timestamp",
      "created_date": "ISO timestamp"
    }
  }
  ```
- **Files Modified**: `rcm_fmeca_app.py`
- **Lines Affected**: ~400 lines added/modified
- **New Dependencies**: `hashlib` (built-in Python module)

---

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
