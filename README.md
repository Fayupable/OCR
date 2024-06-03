# OCR
OCR/Receipt


**Overview**
This project is a comprehensive Python application designed for managing and interacting with data records through a graphical user interface. It includes modules for database operations, GUI components, and application settings.

# **Table of Contents**
1. [Installation](#installation)
2. [Usage](#usage)
3. [Modules](#modules)
4. [Contributing](#contributing)

# **Installation**
To install the required dependencies, use the following command:

**Windows**
```
pip install -r requirements_win32.txt
```
**MacOs**
```
pip install -r requirements_macOS.txt
```

# **Usage**
Run the main application script with:

```
python main.py
```

This will start the application, initializing the main window and setting up the necessary components.

# **Modules**
1. `addrowdialog_auto.py`
Automatically generated code for the Add Row Dialog component, handling GUI elements and layout for adding new rows.

2. `addrowdialog.py`
Custom logic and event handling for the Add Row Dialog, integrating user inputs and interacting with the data model.

3. `db.py`
Manages database interactions, including connecting to the database, executing queries, and handling data retrieval and updates.

4. `main.py`
Main entry point of the application, initializing the application, setting up the main window, and managing the overall program flow.

5. `mainwindow_auto.py`
Automatically generated code for the Main Window component, defining the main interface layout and primary GUI elements.

6. `records_auto.py`
Automatically generated code for managing records, defining the layout and elements for displaying and interacting with data records.

7. `records.py`
Custom logic and event handling for managing records, providing functions for adding, updating, and deleting records from the data model.

8. `safa_yardim.py`
Custom script for additional functionalities or helper functions specific to the project's requirements, likely including utility functions that support the main application.

9. `settings_auto.py`
Automatically generated code for the Settings component, handling GUI elements and layout for the settings/preferences dialog.

10. `settings.py`
Custom logic for managing application settings, allowing users to configure and save their preferences, which are then applied to the application.

# **Contributing**
We welcome contributions! Please fork the repository and submit pull requests. For major changes, open an issue first to discuss what you would like to change.
