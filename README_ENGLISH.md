# NxW Tools - Dynamic QGIS Plugin with Access Control

A powerful QGIS plugin that dynamically loads Python functions from GitHub with user-based access control.

## 🚀 Features

- **Dynamic Loading**: Functions are loaded directly from GitHub - no manual updates needed
- **Access Control**: Restrict functions and folders based on user permissions
- **Folder Structure = Menu Structure**: GitHub folders automatically become QGIS submenus
- **Offline Cache**: Functions are cached locally for offline use
- **No Configuration Files**: Just add Python files and they appear in the menu
- **User Management**: Control who can access which functions

## 📋 Quick Start

### 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository called `qgis-functions`
2. Can be public or private (private requires a token)
3. Upload the `qgis-functions` folder

### 2. Get GitHub Token (Optional - for private repos)

1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Create new token with `repo` (read) permissions
3. Save the token securely

### 3. Install Menu_NxW Plugin

1. Copy `Menu_NxW` folder to your QGIS plugins directory:
   - Windows: `C:\Users\[YourUser]\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/`

2. Restart QGIS

3. Go to `Plugins > Manage and Install Plugins`

4. In "Installed" tab, find "Menu NxW" and activate it

### 4. Configure the Plugin

First time setup:

1. Configuration dialog will appear
2. Enter:
   - **GitHub Username**: your_username
   - **Repository**: qgis-functions
   - **GitHub Token**: (leave empty if public repo)
   - **User Access Token**: (if access control is enabled)
   - **Branch**: main

3. Click "Save Configuration"

## 🔐 Access Control System

### Overview

The access control system allows you to restrict which users can see and execute specific functions. This is managed through an `access_control.json` file in your GitHub repository.

### Setting Up Access Control

1. Add `access_control.json` to your repository root
2. Define users, permissions, and tokens
3. Distribute tokens to authorized users

### Access Control Structure

```json
{
  "access_control": {
    "enabled": true,
    "default_access": "deny",
    "users": {
      "user_id": {
        "name": "Full Name",
        "email": "email@example.com",
        "access_level": "user|analyst|admin",
        "allowed_folders": ["folder1", "folder2", "*"],
        "allowed_functions": ["specific_function"],
        "denied_functions": ["dangerous_function"]
      }
    },
    "groups": {
      "group_name": {
        "members": ["user1", "user2"],
        "allowed_folders": ["shared_folder"]
      }
    },
    "tokens": {
      "tk_unique_token": {
        "user": "user_id",
        "expires": "2025-12-31"
      }
    }
  }
}
```

### Access Levels

- **admin**: Full access to all functions and folders
- **analyst**: Access to analysis and reporting functions
- **user**: Basic access to approved functions
- **limited**: Only specific functions explicitly allowed

### Permission Rules

1. **Folder Permissions**: Control access to entire folders
   - Use `"*"` to allow all folders
   - List specific folder names to restrict access

2. **Function Permissions**: Fine-grained control over individual functions
   - `allowed_functions`: Whitelist specific functions (for limited users)
   - `denied_functions`: Blacklist specific functions
   - Use `"*"` in denied_functions to deny all except explicitly allowed

3. **Group Permissions**: Assign permissions to multiple users
   - Users inherit group permissions
   - Individual permissions override group permissions

### Example Configurations

#### Basic User
```json
"john_doe": {
  "name": "John Doe",
  "access_level": "user",
  "allowed_folders": ["utilities", "data"],
  "denied_functions": ["delete_all", "modify_database"]
}
```

#### Power User
```json
"jane_smith": {
  "name": "Jane Smith",
  "access_level": "analyst",
  "allowed_folders": ["*"],
  "denied_functions": ["admin_tools"]
}
```

#### Limited Contractor
```json
"contractor": {
  "name": "External User",
  "access_level": "limited",
  "allowed_functions": ["zoom_layer", "export_pdf"],
  "denied_functions": ["*"]
}
```

## 📁 Repository Structure

```
qgis-functions/
├── access_control.json    # User permissions (optional)
└── functions/
    ├── analysis/          # Spatial analysis tools
    │   └── buffer_multiple.py
    ├── cartography/       # Map creation and printing
    │   ├── print_map_pdf.py
    │   └── categorize_layer.py
    ├── data/             # Import/Export tools
    │   └── export_to_excel.py
    ├── utilities/        # General utilities
    │   └── zoom_active_layer.py
    └── quality/          # QA/QC tools
        └── clean_geometries.py
```

## 📝 Creating Functions

### Basic Function Structure

Each Python file must have an `execute` function:

```python
"""Brief description of the function"""

def execute(iface, params=None):
    """
    Main function to be executed
    
    Args:
        iface: QGIS interface object
        params: Optional parameters dictionary
    
    Returns:
        dict: Result with status and message
    """
    # Your code here
    
    return {
        "status": "ok",  # Can be: ok, error, warning, info
        "message": "Operation completed successfully"
    }
```

### Example Functions

#### Simple Function
```python
# functions/utilities/count_layers.py
"""Count layers in current project"""

def execute(iface):
    project = QgsProject.instance()
    layer_count = len(project.mapLayers())
    
    return {
        "status": "info",
        "message": f"Project has {layer_count} layers"
    }
```

#### Function with Parameters
```python
# functions/analysis/buffer_layer.py
"""Create buffer around features"""

def execute(iface, params=None):
    if params is None:
        params = {}
    
    layer = iface.activeLayer()
    distance = params.get('distance', 100)
    
    if not layer:
        return {
            "status": "warning",
            "message": "Please select a layer"
        }
    
    # Buffer logic here
    
    return {
        "status": "ok",
        "message": f"Buffer created with {distance}m distance"
    }
```

## 🔄 Updating Functions

### For Developers
1. Edit or add `.py` files in the repository
2. Commit and push to GitHub
3. Users will see changes when they reload the menu

### For Users
- Click "🔄 Reload menu" to get latest functions
- Click "🗑️ Clear cache" to force complete refresh
- Cache is automatically updated every 24 hours

## 🛠️ Available Functions

### Utilities
- **Zoom Active Layer**: Zoom to extent of selected layer

### Cartography
- **Print Map PDF**: Export map using layout
- **Categorize Layer**: Apply symbology by unique values

### Analysis
- **Buffer Multiple**: Create concentric rings around features

### Data
- **Export to Excel**: Export attributes to Excel file

### Quality
- **Clean Geometries**: Detect and fix invalid geometries

## ⚙️ Troubleshooting

### Menu appears empty
- Check internet connection
- Verify GitHub username and repository
- If private repo, check token validity
- Check access control permissions

### Access Denied
- Verify your access token is correct
- Check token hasn't expired
- Contact administrator for new token

### Function execution errors
- Check QGIS Log Messages panel
- Ensure functions have correct structure
- Verify required imports are available

### Cache issues
- Use "Clear cache" to force update
- Cache duration is 24 hours by default
- Access control cache updates hourly

## 🔒 Security Considerations

- Access tokens should be kept confidential
- Tokens can be revoked by removing from `access_control.json`
- Consider setting expiration dates for temporary access
- Use groups for easier permission management
- Regular audit of user permissions recommended

## 📊 Admin Features

Administrators (access_level: "admin") have additional features:

- View all user permissions
- Access all functions regardless of restrictions
- See permission summary in menu
- Monitor user access (if logging enabled)

## 🤝 Contributing

To add your own functions:
1. Fork the repository
2. Add `.py` files in appropriate folder
3. Test locally
4. Submit Pull Request

## 📄 License

This project is open source. Feel free to use and modify.

## 💡 Tips

- Organize functions logically in folders
- Use descriptive file names (they become menu items)
- Include docstrings for better documentation
- Return clear status messages
- Test functions locally before pushing
- Use access control for sensitive operations
- Set appropriate token expiration dates
- Document required QGIS version or dependencies

## 🆘 Support

For issues or questions:
- Check the troubleshooting section
- Review function examples
- Contact your system administrator (for access issues)
- Submit issues on GitHub repository