#!/usr/bin/env python3
"""
Flatpak DPI Manager

A simple GUI tool to adjust DPI and scaling settings for Flatpak applications.
"""
import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QComboBox, QPushButton, QLineEdit, QMessageBox, QScrollArea
)


class FlatpakDpiManager(QWidget):
    """Main window for the Flatpak DPI Manager application."""

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
        self.setWindowTitle("Flatpak DPI Manager")
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
        
        button_layout.addStretch()
        
        launch_button = QPushButton("Launch App")
        launch_button.clicked.connect(self.launch_app)
        button_layout.addWidget(launch_button)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)
        
        self.setLayout(main_layout)
    
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
                if f"--env={var_name}=" in line:
                    # Extract the value part
                    value = line.split(f"--env={var_name}=")[1].strip()
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
    window = FlatpakDpiManager()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
