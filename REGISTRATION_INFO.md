# Registration and Authentication System

## Overview

The FMECA & RCM Analysis Tool implements a two-tier security system:

1. **Software Registration** (Organization-level, one-time)
2. **User Authentication** (Per-user, every session)

Both systems work together to ensure proper licensing and user access control.

## Key Points

### 1. **Registration File (`.registration`)**
- Contains all organization and contact information
- Created automatically when you complete the registration form
- Located in the application directory (same folder as `rcm_fmeca_app.py`)
- JSON format with the following structure:

```json
{
  "authority_name": "Your Organization Name",
  "department": "Department Name",
  "contact_person": "Contact Name",
  "contact_email": "email@example.com",
  "phone": "+61 x xxxx xxxx",
  "address": "Physical Address",
  "registration_date": "2025-12-06T04:50:05.767763",
  "app_version": "1.0.0"
}
```

### 2. **No Fallback to config.ini**
- Organization details in `config.ini` are **NO LONGER USED**
- The `[Organization]` section in `config.ini` should remain empty:
  ```ini
  [Organization]
  authority_name = 
  department = 
  contact_email = 
  ```
- All registration information comes exclusively from `.registration` file

### 3. **What Happens Without Registration**
If the `.registration` file is:
- **Missing**: Registration form will appear
- **Incomplete**: Registration form will appear
- **Corrupted**: Registration form will appear

**You must complete the registration form to use the application.**

## Where Registration Info Appears

### Main Page
```
Developed by: Odysseus-imc Pty Ltd
Technical expertise by: Cambia Consulting Pty Ltd
Registered to: [Your Organization Name from .registration]
Version: 1.0.0
```

### Sidebar - Application Info
```
Authority: [authority_name from .registration]
Department: [department from .registration]
Contact Person: [contact_person from .registration]
Contact Email: [contact_email from .registration]
Version: 1.0.0
Registration Date: [formatted date from .registration]
```

## Common Scenarios

### First-Time Installation
1. Launch application
2. Registration form appears automatically
3. Fill in all required fields (marked with *)
4. Click "✅ Register Application"
5. Application unlocks and shows your organization info

### Copying to Another Computer
1. Copy both files to the new location:
   - `rcm_fmeca_app.py` (and all other app files)
   - `.registration` (your registration file)
2. Launch application
3. Application will use existing registration

### Lost Registration File
1. Application will show registration form
2. Re-enter your organization details
3. New `.registration` file will be created
4. **Note**: Your analysis data (`.autosave.json` and exports) are separate and will not be affected

### Update Registration Information
To change contact person, email, or other details:
1. Delete the `.registration` file
2. Restart the application
3. Registration form will appear
4. Enter updated information

## Security & Backup

### File Protection
- `.registration` is listed in `.gitignore`
- Will not be committed to version control
- Keeps your organization details private

### Backup Recommendations
Include `.registration` in your backup procedures:
```bash
# Example backup command
cp .registration /backup/location/registration_backup_$(date +%Y%m%d).json
```

### Restore from Backup
```bash
# Copy registration file back
cp /backup/location/.registration ./
```

## Technical Details

### Required Fields
- Authority/Organization Name
- Department/Division
- Contact Person Name
- Contact Email (must contain '@')

### Optional Fields
- Phone Number
- Organization Address

### Validation
- Empty or whitespace-only values are rejected for required fields
- Email must contain '@' symbol
- All text is trimmed (leading/trailing spaces removed)

## Support

### Registration Issues
Contact: sm@odysseus-imc.com

### Technical Support
Contact: adam.hassan@cambia.com.au

## User Authentication System (NEW)

### Overview

After completing software registration, all users must log in to access the application.

### User Database (`.users.json`)

User accounts are stored in `.users.json` with the following information:
- Username (unique identifier)
- Hashed password (SHA-256, never plain text)
- Full name
- Position
- User type (User, Super User, or Administrator)
- Login count (tracks total logins)
- Last login timestamp
- Account creation date

### Default Administrator Account

**Automatically created on first run:**
- Username: `admin`
- Password: `odyssey` (change after first login recommended)
- User Type: Administrator (cannot be modified)
- Full access to all features

**Important**: This account cannot be deleted or downgraded. Keep credentials secure.

### User Types and Permissions

#### 👤 User (Default)
- **Access**: All RCM analysis features (Stages 1-4)
- **Cannot access**: Administration section
- **Use case**: Standard analysts and engineers

#### ⚙️ Super User
- **Access**: All RCM analysis features + Administration section
- **Cannot**: Manage other users
- **Use case**: Senior analysts who need to configure risk thresholds
- **Assignment**: Only Administrators can designate Super Users

#### 🔐 Administrator
- **Access**: Full application access
- **Can**: Manage all users and change user types
- **Can**: Access and configure all Administration settings
- **Can**: View login statistics for all users
- **Use case**: System administrators and managers

### User Registration Process

1. **Self-Registration**: Users can register themselves via the login page
2. **Default Type**: All new registrations create "User" type accounts
3. **Type Upgrade**: Only Administrators can upgrade users to Super User or Administrator
4. **Process**:
   - Click "📝 Register New User" tab on login page
   - Enter username, full name, position, password
   - Passwords must be at least 6 characters
   - Username cannot be "admin"
   - Return to login tab after registration

### Managing Users (Administrator Only)

Administrators can manage users through Administration → Manage Users:

1. **View All Users**: See complete user list with details
   - Username, full name, position
   - User type
   - Login count and last login date
   - Account creation date

2. **Change User Types**:
   - Select user from dropdown
   - Choose new user type
   - Confirm change
   - User must log out and back in for changes to take effect

3. **Login Statistics**: Track user activity
   - Total login count per user
   - Last login timestamp
   - Audit trail for user access

### Security Features

#### Password Security
- SHA-256 hashing (passwords never stored in plain text)
- Minimum 6 characters required
- Secure authentication on every login

#### Access Control
- Role-based permissions (User, Super User, Administrator)
- Administration section hidden from unauthorized users
- Multi-layer access verification

#### Session Management
- Secure session handling
- Logout capability
- User information displayed in sidebar

#### Audit Trail
- Login counter for each user
- Last login timestamps
- Persistent across sessions

### User Information Display

When logged in, the sidebar shows:
```
👤 User Information
User: [username]
Position: [position]
User Type: [User|Super User|Administrator]

🚪 Logout
```

### Authentication Flow

```
1. Launch Application
   ↓
2. Software Registration (if not registered)
   ↓
3. Login Page
   ↓
4. Enter Credentials or Register New User
   ↓
5. Authentication Check
   ↓
6. Main Application (access based on user type)
```

### Files and Locations

- **`.registration`**: Organization registration (one-time)
- **`.users.json`**: User accounts and authentication
- Both files in application directory (same as `rcm_fmeca_app.py`)
- Both files excluded from git via `.gitignore`

### Backup and Security

#### What to Backup
```bash
# Backup both registration and user database
cp .registration /backup/location/registration_backup_$(date +%Y%m%d).json
cp .users.json /backup/location/users_backup_$(date +%Y%m%d).json
```

#### Security Recommendations
1. Keep `.users.json` secure (contains hashed passwords)
2. Limit Administrator access to trusted personnel
3. Change default admin password after setup
4. Regularly review user access in Manage Users
5. Monitor login statistics for unusual activity

### Troubleshooting

#### Lost Admin Password
1. Delete `.users.json` file
2. Restart application
3. Default admin account will be recreated
4. **Warning**: All user accounts will be lost

#### User Cannot See Administration
- Check user type in Administration → Manage Users
- Only Super Users and Administrators have access
- User must log out and back in after type change

#### Login Count Not Increasing
- Verify user is logging in successfully
- Check `.users.json` file for `login_count` field
- Database migration runs automatically on first startup

## For Developers

### Configuration Priority
1. **Software Registration**: From `.registration` file ONLY
2. **User Authentication**: From `.users.json` file
3. **Application info**: From `config.ini` (name, version, contacts)
4. **No mixing**: Organization and user details are separate

### Code References (v1.0.2+)
- User authentication functions: Lines 685-903
- Authentication check: Line 1173
- User management UI: Lines 1717-1833
- Login form display: Lines 805-941
- Sidebar user info: Lines 1007-1021

### Database Schema

#### .users.json Format
```json
{
  "username": {
    "password": "sha256_hashed_password",
    "full_name": "Full Name",
    "position": "Position Title",
    "user_type": "User|Super User|Administrator",
    "login_count": 0,
    "last_login": "2025-12-07T12:56:16.024377",
    "created_date": "2025-12-07T12:14:35.284872"
  }
}
```

---

**Last Updated**: December 7, 2025  
**Applies To**: FMECA & RCM Analysis Tool v1.0.2+
