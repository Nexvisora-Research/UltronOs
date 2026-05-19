import Meta from 'gi://Meta';
import Clutter from 'gi://Clutter';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';

export class WindowManager {
    constructor(settings) {
        this._settings = settings;
        this._workspaceAnimationId = null;
        this._windowAddedId = null;
        this._windowRemovedId = null;
        this._windowFocusedId = null;
    }

    enable() {
        this._applyWorkspaceSettings();
        this._connectSignals();
        this._setupWindowAnimations();
    }

    disable() {
        this._disconnectSignals();
        this._restoreDefaultAnimations();
    }

    _applyWorkspaceSettings() {
        const wrapAround = this._settings.get_boolean('workspace-wrap-around');
        const animation = this._settings.get_boolean('workspace-animation');

        // Apply workspace wrap-around
        const display = global.display;
        if (wrapAround) {
            display.set_workspace_wraparound(true);
        } else {
            display.set_workspace_wraparound(false);
        }

        // Apply workspace animation speed
        if (!animation) {
            global.settings.set_boolean('enable-animations', false);
        } else {
            global.settings.set_boolean('enable-animations', true);
            
            const speed = this._settings.get_double('animation-speed');
            // Adjust animation duration based on speed multiplier
            Meta.prefs_set_animation_time(200 / speed);
        }
    }

    _setupWindowAnimations() {
        const speed = this._settings.get_double('animation-speed');
        
        // Override default window animation durations
        const animationTime = 250 / speed;

        // Store original values
        this._originalMapTime = Meta.prefs_get_animation_time();

        // Apply custom animation time
        Meta.prefs_set_animation_time(animationTime);
    }

    _restoreDefaultAnimations() {
        if (this._originalMapTime) {
            Meta.prefs_set_animation_time(this._originalMapTime);
        }
    }

    _connectSignals() {
        // Window added
        this._windowAddedId = global.display.connect('window-added', (display, window) => {
            this._onWindowAdded(window);
        });

        // Window removed
        this._windowRemovedId = global.display.connect('window-removed', (display, window) => {
            this._onWindowRemoved(window);
        });

        // Window focus changed
        this._windowFocusedId = global.display.connect('notify::focus-window', () => {
            this._onFocusChanged();
        });

        // Settings changes
        this._settingsChangedId = this._settings.connect('changed', (settings, key) => {
            this._onSettingsChanged(key);
        });

        // Workspace switch
        this._workspaceSwitchId = global.workspace_manager.connect('active-workspace-changed', () => {
            this._onWorkspaceChanged();
        });
    }

    _disconnectSignals() {
        if (this._windowAddedId) {
            global.display.disconnect(this._windowAddedId);
        }
        if (this._windowRemovedId) {
            global.display.disconnect(this._windowRemovedId);
        }
        if (this._windowFocusedId) {
            global.display.disconnect(this._windowFocusedId);
        }
        if (this._settingsChangedId) {
            this._settings.disconnect(this._settingsChangedId);
        }
        if (this._workspaceSwitchId) {
            global.workspace_manager.disconnect(this._workspaceSwitchId);
        }
    }

    _onWindowAdded(window) {
        // Apply custom window properties
        const windowType = window.get_window_type();
        
        // Skip desktop and dock windows
        if (windowType === Meta.WindowType.DESKTOP || 
            windowType === Meta.WindowType.DOCK ||
            windowType === Meta.WindowType.SPLASHSCREEN) {
            return;
        }

        // Apply rounded corners
        this._applyWindowDecorations(window);

        // Log new window
        log(`Window added: ${window.get_title() || 'Untitled'}`);
    }

    _onWindowRemoved(window) {
        log(`Window removed: ${window.get_title() || 'Untitled'}`);
    }

    _onFocusChanged() {
        const focusWindow = global.display.get_focus_window();
        if (focusWindow) {
            // Bring focused window to front with animation
            this._animateFocus(focusWindow);
        }
    }

    _onWorkspaceChanged() {
        const activeWs = global.workspace_manager.get_active_workspace();
        const wsIndex = activeWs.index();
        
        log(`Switched to workspace ${wsIndex + 1}`);
    }

    _onSettingsChanged(key) {
        switch (key) {
            case 'workspace-wrap-around':
                const wrapAround = this._settings.get_boolean('workspace-wrap-around');
                global.display.set_workspace_wraparound(wrapAround);
                break;
            
            case 'workspace-animation':
            case 'animation-speed':
                this._applyWorkspaceSettings();
                this._setupWindowAnimations();
                break;
        }
    }

    _applyWindowDecorations(window) {
        // Apply rounded corners via CSS
        const actor = window.get_compositor_private();
        if (!actor) return;

        // Add custom style class
        actor.add_style_class_name('ultron-window');
    }

    _animateFocus(window) {
        const actor = window.get_compositor_private();
        if (!actor) return;

        const animationSpeed = this._settings.get_double('animation-speed');
        const duration = 150 / animationSpeed;

        // Subtle scale animation on focus
        actor.set_pivot_point(0.5, 0.5);
        
        actor.save_easing_state();
        actor.set_easing_mode(Clutter.AnimationMode.EASE_OUT_QUAD);
        actor.set_easing_duration(duration);
        
        actor.scale_x = 1.0;
        actor.scale_y = 1.0;
        
        actor.restore_easing_state();
    }

    // Utility: Get all windows on current workspace
    getWindowsOnCurrentWorkspace() {
        const activeWs = global.workspace_manager.get_active_workspace();
        return global.get_window_actors().filter(actor => {
            const window = actor.get_meta_window();
            return window.get_workspace() === activeWs && 
                   window.get_window_type() !== Meta.WindowType.DESKTOP;
        });
    }

    // Utility: Minimize all windows
    minimizeAllWindows() {
        const windows = this.getWindowsOnCurrentWorkspace();
        windows.forEach(actor => {
            const window = actor.get_meta_window();
            window.minimize();
        });
    }

    // Utility: Show desktop
    showDesktop() {
        this.minimizeAllWindows();
    }

    // Utility: Arrange windows in grid
    arrangeWindowsInGrid() {
        const windows = this.getWindowsOnCurrentWorkspace();
        const monitor = Main.layoutManager.primaryMonitor;
        const count = windows.length;
        
        if (count === 0) return;

        const cols = Math.ceil(Math.sqrt(count));
        const rows = Math.ceil(count / cols);
        const cellWidth = monitor.width / cols;
        const cellHeight = monitor.height / rows;

        windows.forEach((actor, index) => {
            const col = index % cols;
            const row = Math.floor(index / cols);
            const window = actor.get_meta_window();

            const x = monitor.x + col * cellWidth;
            const y = monitor.y + row * cellHeight;
            const width = cellWidth - 8;
            const height = cellHeight - 8;

            window.move_frame(true, x, y, width, height);
        });
    }
}
