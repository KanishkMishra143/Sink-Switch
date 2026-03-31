#!/usr/bin/env python3
import os
import subprocess
import json
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, GObject, Adw

CONFIG_DIR = os.path.expanduser("~/.config/sink-switch")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class SinkRow(Adw.ActionRow):
    def __init__(self, sink_id, friendly_name, is_active, is_in_cycle):
        super().__init__(title=friendly_name, subtitle=sink_id)
        
        self.sink_id = sink_id
        # Ensure row is always fully opaque and prominent
        self.add_css_class("property") 
        
        # Checkbox for cycle inclusion
        self.check = Gtk.CheckButton()
        self.check.set_active(is_in_cycle)
        self.check.set_valign(Gtk.Align.CENTER)
        self.add_prefix(self.check)
        
        # Status indicator
        self.is_active = is_active
        if is_active:
            self.status_icon = Gtk.Image.new_from_icon_name("emblem-ok-symbolic")
            self.status_icon.set_tooltip_text("Currently Active")
            self.add_suffix(self.status_icon)
            self.add_css_class("success")

class SinkSwitchGUI(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(title="Sink Switch Dashboard", **kwargs)
        self.set_default_size(480, 700)

        # Force uniform styling via CSS
        provider = Gtk.CssProvider()
        provider.load_from_data(b"""
            list, row { 
                opacity: 1.0 !important; 
                color: currentColor !important;
            }
            label.title { 
                opacity: 1.0 !important;
                font-weight: bold;
            }
            label.subtitle { 
                opacity: 0.8 !important; 
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Load configuration
        self.config = self.load_config()
        
        # Main Layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Header Bar
        header = Adw.HeaderBar()
        self.main_box.append(header)

        # Toast Overlay
        self.toast_overlay = Adw.ToastOverlay()
        self.main_box.append(self.toast_overlay)

        # Scrollable area
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        self.toast_overlay.set_child(scrolled)

        # Content Clamp
        clamp = Adw.Clamp()
        clamp.set_maximum_size(450)
        scrolled.set_child(clamp)
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        self.content_box.set_margin_top(24)
        self.content_box.set_margin_bottom(24)
        self.content_box.set_margin_start(12)
        self.content_box.set_margin_end(12)
        clamp.set_child(self.content_box)

        # 1. Primary Section
        self.primary_group = Adw.PreferencesGroup(title="Primary Audio Devices")
        self.primary_list = Gtk.ListBox()
        self.primary_list.add_css_class("boxed-list")
        self.primary_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.primary_group.add(self.primary_list)
        self.content_box.append(self.primary_group)

        # 2. External/HDMI Section
        self.external_group = Adw.PreferencesGroup(title="HDMI & External Audio")
        self.external_list = Gtk.ListBox()
        self.external_list.add_css_class("boxed-list")
        self.external_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.external_group.add(self.external_list)
        self.content_box.append(self.external_group)

        self.refresh_sinks()

        # Action Buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.CENTER)
        self.content_box.append(button_box)

        switch_btn = Gtk.Button(label="Switch to Selected")
        switch_btn.add_css_class("pill")
        switch_btn.add_css_class("suggested-action")
        switch_btn.connect("clicked", self.on_switch_clicked)
        button_box.append(switch_btn)

        save_btn = Gtk.Button(label="Save Configuration")
        save_btn.add_css_class("pill")
        save_btn.connect("clicked", self.on_save_clicked)
        button_box.append(save_btn)

        # Footer (Uniform style)
        footer = Gtk.Label(label="Select devices for cycle loop and click Save")
        footer.set_justify(Gtk.Justification.CENTER)
        self.content_box.append(footer)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"devices": [], "last_device_id": ""}

    def save_config(self, config):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)

    def get_friendly_name(self, sink_name):
        if "bluez_output" in sink_name:
            return "Bluetooth Speaker"
        elif "usb" in sink_name:
            return "USB Audio"
        elif "pci" in sink_name and "hdmi" not in sink_name.lower():
            return "Internal Audio"
        elif "hdmi" in sink_name.lower():
            return "HDMI Output"
        return "Audio Sink"

    def is_external(self, sink_name):
        return "hdmi" in sink_name.lower() or "usb" in sink_name.lower()

    def refresh_sinks(self):
        # Clear both lists
        for lst in [self.primary_list, self.external_list]:
            while child := lst.get_first_child():
                lst.remove(child)

        # Get all sinks
        try:
            output = subprocess.check_output(["pactl", "list", "short", "sinks"], text=True)
            sinks = [line.split()[1] for line in output.strip().split('\n') if line]
        except Exception:
            sinks = []

        # Get current default sink
        try:
            current_sink = subprocess.check_output(["pactl", "get-default-sink"], text=True).strip()
        except Exception:
            current_sink = ""

        cycle_list = self.config.get("devices", [])

        for s in sinks:
            friendly = self.get_friendly_name(s)
            is_active = (s == current_sink)
            is_in_cycle = (s in cycle_list)
            
            row = SinkRow(s, friendly, is_active, is_in_cycle)
            row.set_activatable(True)
            row.connect("activated", lambda r: self.switch_to_sink(r.sink_id))
            
            if self.is_external(s):
                self.external_list.append(row)
            else:
                self.primary_list.append(row)
        
        # Hide groups if empty
        self.primary_group.set_visible(self.primary_list.get_first_child() is not None)
        self.external_group.set_visible(self.external_list.get_first_child() is not None)

    def on_switch_clicked(self, button):
        # Check both lists for selection
        selected = self.primary_list.get_selected_row() or self.external_list.get_selected_row()
        if selected:
            self.switch_to_sink(selected.sink_id)
        else:
            self.show_toast("Please select a device first")

    def switch_to_sink(self, sink_id):
        try:
            subprocess.run(["pactl", "set-default-sink", sink_id], check=True)
            output = subprocess.check_output(["pactl", "list", "short", "sink-inputs"], text=True)
            for line in output.strip().split('\n'):
                if line:
                    subprocess.run(["pactl", "move-sink-input", line.split()[0], sink_id])
            
            friendly = self.get_friendly_name(sink_id)
            subprocess.run(["notify-send", "Audio Output Set", f"{friendly} ({sink_id})"])
            self.refresh_sinks()
            self.show_toast(f"Switched to {friendly}")
        except Exception as e:
            self.show_toast(f"Error: {str(e)}")

    def on_save_clicked(self, button):
        new_cycle = []
        current_active = ""
        
        for lst in [self.primary_list, self.external_list]:
            row = lst.get_first_child()
            while row:
                if isinstance(row, SinkRow):
                    if row.check.get_active():
                        new_cycle.append(row.sink_id)
                    if row.is_active:
                        current_active = row.sink_id
                row = row.get_next_sibling()

        self.config["devices"] = new_cycle
        self.config["last_device_id"] = current_active
        
        try:
            self.save_config(self.config)
            self.show_toast("Configuration saved!")
        except Exception as e:
            self.show_toast(f"Save failed: {str(e)}")

    def show_toast(self, message):
        toast = Adw.Toast.new(message)
        self.toast_overlay.add_toast(toast)

class SinkSwitchApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.github.kanishkmishra.sinkswitch")

    def do_activate(self):
        win = SinkSwitchGUI(application=self)
        win.present()

if __name__ == "__main__":
    app = SinkSwitchApp()
    app.run(None)
