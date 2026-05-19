"""
Ultron OS - Gesture Support for Touch Devices
Touch gesture recognition and handling
"""

import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk


class GestureController:
    """Manages touch gestures"""
    
    def __init__(self):
        self.gestures = {}
        self.enabled = True
    
    def add_gesture(self, widget, gesture_type, callback):
        """Add a gesture to a widget"""
        if not self.enabled:
            return
        
        if gesture_type == 'swipe-left':
            gesture = Gtk.GestureSwipe()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_swipe(gesture, velocity_x, velocity_y):
                if velocity_x < 0:  # Left swipe
                    callback(widget)
            
            gesture.connect('swipe', on_swipe)
            widget.add_controller(gesture)
        
        elif gesture_type == 'swipe-right':
            gesture = Gtk.GestureSwipe()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_swipe(gesture, velocity_x, velocity_y):
                if velocity_x > 0:  # Right swipe
                    callback(widget)
            
            gesture.connect('swipe', on_swipe)
            widget.add_controller(gesture)
        
        elif gesture_type == 'swipe-up':
            gesture = Gtk.GestureSwipe()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_swipe(gesture, velocity_x, velocity_y):
                if velocity_y < 0:  # Up swipe
                    callback(widget)
            
            gesture.connect('swipe', on_swipe)
            widget.add_controller(gesture)
        
        elif gesture_type == 'swipe-down':
            gesture = Gtk.GestureSwipe()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_swipe(gesture, velocity_x, velocity_y):
                if velocity_y > 0:  # Down swipe
                    callback(widget)
            
            gesture.connect('swipe', on_swipe)
            widget.add_controller(gesture)
        
        elif gesture_type == 'pinch':
            gesture = Gtk.GestureZoom()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_scale_changed(gesture, scale):
                callback(widget, scale)
            
            gesture.connect('scale-changed', on_scale_changed)
            widget.add_controller(gesture)
        
        elif gesture_type == 'rotate':
            gesture = Gtk.GestureRotate()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            
            def on_angle_changed(gesture, angle):
                callback(widget, angle)
            
            gesture.connect('angle-changed', on_angle_changed)
            widget.add_controller(gesture)
        
        elif gesture_type == 'long-press':
            gesture = Gtk.GestureLongPress()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            gesture.connect('pressed', callback)
            widget.add_controller(gesture)
        
        elif gesture_type == 'tap':
            gesture = Gtk.GestureClick()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            gesture.connect('pressed', callback)
            widget.add_controller(gesture)
        
        elif gesture_type == 'double-tap':
            gesture = Gtk.GestureClick()
            gesture.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
            gesture.set_button(0)
            
            def on_pressed(gesture, n_press, x, y):
                if n_press == 2:
                    callback(widget, x, y)
            
            gesture.connect('pressed', on_pressed)
            widget.add_controller(gesture)
        
        self.gestures[f'{widget.get_id()}_{gesture_type}'] = gesture
    
    def enable(self):
        """Enable gesture recognition"""
        self.enabled = True
    
    def disable(self):
        """Disable gesture recognition"""
        self.enabled = False


class TouchOptimizedWindow(Adw.ApplicationWindow):
    """Window optimized for touch input"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.gesture_controller = GestureController()
        
        self._setup_touch_ui()
    
    def _setup_touch_ui(self):
        """Build touch-optimized UI"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header with larger buttons
        header = Adw.HeaderBar()
        header.set_show_title(True)
        main_box.append(header)
        
        # Content area
        content = Gtk.ScrolledWindow()
        content.set_vexpand(True)
        main_box.append(content)
        
        # Page stack
        self._page_stack = Gtk.Stack()
        content.set_child(self._page_stack)
        
        # Add swipe gestures for page navigation
        self.gesture_controller.add_gesture(
            self._page_stack,
            'swipe-left',
            self._on_swipe_left
        )
        
        self.gesture_controller.add_gesture(
            self._page_stack,
            'swipe-right',
            self._on_swipe_right
        )
        
        # Add pinch-to-zoom gesture
        self.gesture_controller.add_gesture(
            content,
            'pinch',
            self._on_pinch
        )
    
    def _on_swipe_left(self, widget):
        """Handle left swipe"""
        # Navigate to next page
        pass
    
    def _on_swipe_right(self, widget):
        """Handle right swipe"""
        # Navigate to previous page
        pass
    
    def _on_pinch(self, widget, scale):
        """Handle pinch gesture"""
        # Zoom in/out
        pass


class TouchSettingsPage(Adw.PreferencesPage):
    """Settings for touch and gesture configuration"""
    
    def __init__(self):
        super().__init__()
        self.set_title('Touch & Gestures')
        
        self._build_ui()
    
    def _build_ui(self):
        """Build touch settings UI"""
        # Gestures group
        gestures_group = Adw.PreferencesGroup()
        gestures_group.set_title('Gestures')
        
        # Enable gestures
        enable_row = Adw.SwitchRow()
        enable_row.set_title('Enable Gestures')
        enable_row.set_subtitle('Use touch gestures for navigation')
        enable_row.set_active(True)
        gestures_group.add(enable_row)
        
        # Swipe sensitivity
        sensitivity_row = Adw.ComboRow()
        sensitivity_row.set_title('Swipe Sensitivity')
        
        sensitivity_model = Gtk.StringList()
        sensitivity_model.append('Low')
        sensitivity_model.append('Medium')
        sensitivity_model.append('High')
        sensitivity_row.set_model(sensitivity_model)
        sensitivity_row.set_selected(1)
        gestures_group.add(sensitivity_row)
        
        # Gesture actions
        actions = [
            ('Swipe Left', 'Go to next page'),
            ('Swipe Right', 'Go to previous page'),
            ('Swipe Up', 'Open quick settings'),
            ('Swipe Down', 'Open notification center'),
            ('Pinch', 'Zoom in/out'),
            ('Long Press', 'Show context menu'),
            ('Double Tap', 'Zoom to fit'),
        ]
        
        for gesture, action in actions:
            row = Adw.ActionRow()
            row.set_title(gesture)
            row.set_subtitle(action)
            row.set_activatable(True)
            
            # Customize button
            button = Gtk.Button()
            button.set_label('Customize')
            row.add_suffix(button)
            row.set_activatable_widget(button)
            
            gestures_group.add(row)
        
        self.add(gestures_group)
        
        # Touch feedback group
        feedback_group = Adw.PreferencesGroup()
        feedback_group.set_title('Touch Feedback')
        
        # Haptic feedback
        haptic_row = Adw.SwitchRow()
        haptic_row.set_title('Haptic Feedback')
        haptic_row.set_subtitle('Vibrate on touch (if supported)')
        feedback_group.add(haptic_row)
        
        # Touch sounds
        sound_row = Adw.SwitchRow()
        sound_row.set_title('Touch Sounds')
        sound_row.set_subtitle('Play sound on touch')
        feedback_group.add(sound_row)
        
        # Visual feedback
        visual_row = Adw.SwitchRow()
        visual_row.set_title('Visual Feedback')
        visual_row.set_subtitle('Show touch indicator')
        visual_row.set_active(True)
        feedback_group.add(visual_row)
        
        self.add(feedback_group)
