# Registration System

## Overview

The FMECA & RCM Analysis Tool requires mandatory registration before use. All organization information is stored in the `.registration` file and displayed throughout the application.

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

## For Developers

### Configuration Priority
1. **Registration info**: From `.registration` file ONLY
2. **Application info**: From `config.ini` (name, version, contacts)
3. **No mixing**: Organization details are never read from `config.ini`

### Code References
- Registration check: Line 732 in `rcm_fmeca_app.py`
- Registration loading: Line 736-742 in `rcm_fmeca_app.py`
- Display on main page: Line 754
- Display in sidebar: Line 709-724

---

**Last Updated**: December 6, 2025  
**Applies To**: FMECA & RCM Analysis Tool v1.0.0+
