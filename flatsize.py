#!/usr/bin/env python3
"""
flatsize | https://github.com/hairetikos/flatsize
A simple GUI tool to adjust DPI and scaling settings for Flatpak applications
"""
import sys, subprocess, base64
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox, QScrollArea
)

VERSION = "0.69.1-sigma"
WINDOW_ICON_BASE64 = """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"""

class flatsize(QWidget):
    """Main window for the flatsize application."""

    def __init__(self):
        super().__init__()
        
        # List of DPI variables we want to manage
        self.scaling_variables = [
            ("GDK_SCALE", "Integer scale factor (e.g., 2)"),
            ("GDK_DPI_SCALE", "Fractional scale factor (e.g., 0.5)"),
            ("QT_SCALE_FACTOR", "Qt scaling factor (e.g., 1.5)"),
            ("QT_FONT_DPI", "Qt font DPI (e.g., 144)"),
            ("QT_AUTO_SCREEN_SCALE_FACTOR", "Auto screen scale (0 or 1)"),
            ("QT_ENABLE_HIGHDPI_SCALING", "Enable HiDPI (0 or 1)"),
            ("QT_SCREEN_SCALE_FACTORS", "Per-screen factors (e.g., 1;1.5;2)"),
            ("ELECTRON_SCALE_FACTOR", "Electron apps scaling (e.g., 1.5)"),
            ("GNOME_DESKTOP_SCALE_FACTOR", "GNOME scaling (e.g., 2)")
        ]
        
        self.setup_ui()
        self.load_flatpak_apps()
    
    def setup_ui(self):
        """Set up the user interface."""
        self.setWindowTitle("flatsize")
        icon_data = base64.b64decode(WINDOW_ICON_BASE64)
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        self.setWindowIcon(QIcon(pixmap))
        self.setMinimumWidth(550)
        self.setMinimumHeight(600)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Application selection
        main_layout.addWidget(QLabel("Select Flatpak Application:"))
        self.app_combo = QComboBox()
        self.app_combo.currentIndexChanged.connect(self.app_selected)
        main_layout.addWidget(self.app_combo)
        
        # Current overrides display
        main_layout.addWidget(QLabel("Current Overrides:"))
        self.override_display = QLabel("No application selected")
        self.override_display.setWordWrap(True)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.override_display)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(100)
        main_layout.addWidget(scroll_area)
        
        # Settings grid
        main_layout.addWidget(QLabel("DPI Settings:"))
        settings_grid = QGridLayout()
        
        # Create input fields for all scaling variables
        self.input_fields = {}
        row = 0
        for var_name, placeholder in self.scaling_variables:
            settings_grid.addWidget(QLabel(f"{var_name}:"), row, 0)
            
            input_field = QLineEdit()
            input_field.setPlaceholderText(placeholder)
            settings_grid.addWidget(input_field, row, 1)
       
            self.input_fields[var_name] = input_field
            row += 1
        
        main_layout.addLayout(settings_grid)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        apply_button = QPushButton("Apply Settings")
        apply_button.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_button)
        
        reset_button = QPushButton("Reset Settings")
        reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_button)

        about_button = QPushButton("About...")
        about_button.clicked.connect(self.about_box)
        button_layout.addWidget(about_button)

        button_layout.addStretch()
        
        launch_button = QPushButton("Launch App")
        launch_button.clicked.connect(self.launch_app)
        button_layout.addWidget(launch_button)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    def about_box(self):
        QMessageBox.about(self, 
                      "flatsize", 
                      "flatsize v" + VERSION + "<br><a href='https://github.com/hairetikos/flatsize'>https://github.com/hairetikos/flatsize</a>"
        )
    def load_flatpak_apps(self):
        """Load all user-installed Flatpak applications."""
        try:
            self.status_label.setText("Loading Flatpak applications...")
            QApplication.processEvents()
            
            # Run the flatpak list command
            result = subprocess.run(
                ["flatpak", "list", "--user", "--app"], 
                capture_output=True, text=True, check=True
            )
            
            # Process the output (tab-separated, no header)
            apps = []
            for line in result.stdout.strip().split('\n'):
                # Split by tabs
                parts = line.split('\t')
                if len(parts) >= 2:
                    name = parts[0]
                    app_id = parts[1]
                    apps.append((name, app_id))
            
            # Add apps to the dropdown
            if apps:
                for name, app_id in sorted(apps):
                    self.app_combo.addItem(f"{name} ({app_id})", app_id)
                self.status_label.setText(f"Found {len(apps)} Flatpak application(s)")
            else:
                self.status_label.setText("No Flatpak applications found")
                
        except FileNotFoundError:
            self.status_label.setText("Error: flatpak command not found")
            QMessageBox.critical(self, "Error", "flatpak command not found. Is Flatpak installed?")
        except subprocess.CalledProcessError as e:
            self.status_label.setText("Error executing flatpak command")
            QMessageBox.critical(self, "Error", f"Failed to execute flatpak command: {e}")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
    
    def app_selected(self):
        """Handle app selection from the dropdown."""
        app_id = self.app_combo.currentData()
        if not app_id:
            self.override_display.setText("No application selected")
            return
        
        # Get current overrides
        overrides = self.get_current_overrides(app_id)
        
        # Display current overrides
        if overrides.strip():
            self.override_display.setText(overrides)
        else:
            self.override_display.setText("No overrides set")
        
        # Prefill the input fields with current values
        self.prefill_input_fields(overrides)
    
    def get_current_overrides(self, app_id):
        """Get current overrides for the selected app."""
        try:
            result = subprocess.run(
                ["flatpak", "override", "--user", "--show", app_id],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except Exception as e:
            return f"Error retrieving overrides: {str(e)}"
    
    def prefill_input_fields(self, overrides_text):
        """Extract values from overrides text and prefill input fields."""
        # Clear all input fields first
        for input_field in self.input_fields.values():
            input_field.clear()
        
        # Look for our variables in the overrides text
        for var_name in self.input_fields.keys():
            for line in overrides_text.split('\n'):
                if f"{var_name}=" in line:
                    # Extract the value part
                    value = line.split(f"{var_name}=")[1].strip()
                    # Set the value in the input field
                    self.input_fields[var_name].setText(value)
                    break
    
    def apply_settings(self):
        """Apply the DPI settings to the selected application."""
        app_id = self.app_combo.currentData()
        if not app_id:
            QMessageBox.warning(self, "No App Selected", "Please select an application first.")
            return
        
        # Count how many settings we're applying
        changes_made = 0
        
        # Apply each non-empty setting
        for var_name, input_field in self.input_fields.items():
            value = input_field.text().strip()
            if value:
                try:
                    subprocess.run(
                        ["flatpak", "override", "--user", f"--env={var_name}={value}", app_id],
                        check=True
                    )
                    changes_made += 1
                except subprocess.CalledProcessError as e:
                    QMessageBox.critical(self, "Error", 
                                       f"Failed to apply {var_name} setting: {e}")
                    return
        
        # Show success message
        if changes_made > 0:
            self.status_label.setText(f"Applied {changes_made} setting(s) to {app_id}")
            QMessageBox.information(self, "Success", 
                                   f"Successfully applied {changes_made} setting(s) to {app_id}")
            # Refresh the overrides display
            self.app_selected()
        else:
            QMessageBox.information(self, "No Changes", 
                                   "No settings were entered to apply")
    
    def reset_settings(self):
        """Reset all DPI settings for the selected application."""
        app_id = self.app_combo.currentData()
        if not app_id:
            QMessageBox.warning(self, "No App Selected", "Please select an application first.")
            return
        
        # Ask for confirmation
        reply = QMessageBox.question(self, "Confirm Reset", 
                                    f"Are you sure you want to reset all DPI settings for {app_id}?",
                                    QMessageBox.Yes | QMessageBox.No, 
                                    QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Reset each variable
            for var_name in self.input_fields.keys():
                try:
                    subprocess.run(
                        ["flatpak", "override", "--user", f"--unset-env={var_name}", app_id],
                        check=True
                    )
                    # Clear the input field
                    self.input_fields[var_name].clear()
                except subprocess.CalledProcessError as e:
                    QMessageBox.critical(self, "Error", 
                                       f"Failed to reset {var_name}: {e}")
                    return
            
            self.status_label.setText(f"All DPI settings reset for {app_id}")
            QMessageBox.information(self, "Success", 
                                   f"All DPI settings have been reset for {app_id}")
            # Refresh the overrides display
            self.app_selected()
    
    def launch_app(self):
        """Launch the selected Flatpak application."""
        app_id = self.app_combo.currentData()
        if not app_id:
            QMessageBox.warning(self, "No App Selected", "Please select an application to launch.")
            return
        
        try:
            # Launch the app in a non-blocking way
            subprocess.Popen(["flatpak", "run", app_id])
            self.status_label.setText(f"Launched {app_id}")
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", 
                               f"Failed to launch {app_id}: {e}")


def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    window = flatsize()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
