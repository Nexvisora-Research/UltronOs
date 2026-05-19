import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';
import Meta from 'gi://Meta';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as AppDisplay from 'resource:///org/gnome/shell/ui/appDisplay.js';
import * as AppMenu from 'resource:///org/gnome/shell/ui/appMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';

const TASKBAR_HEIGHT = 48;
const ICON_SIZE = 40;
const SPACING = 8;

export class Taskbar {
    constructor(settings, extensionPath) {
        this._settings = settings;
        this._extensionPath = extensionPath;
        this._container = null;
        this._background = null;
        this._pinnedApps = [];
        this._runningApps = [];
        this._appButtons = new Map();
        this._monitorIndex = Main.layoutManager.primaryMonitor;
    }

    enable() {
        this._createTaskbar();
        this._loadPinnedApps();
        this._connectSignals();
        this._show();
    }

    disable() {
        this._disconnectSignals();
        this._hide();
        this._destroy();
    }

    reload() {
        this._updatePosition();
        this._updateSize();
        this._loadPinnedApps();
    }

    _createTaskbar() {
        // Create main container
        this._container = new St.BoxLayout({
            name: 'ultronTaskbar',
            reactive: true,
            track_hover: true,
            style_class: 'ultron-taskbar',
        });

        // Apply styling
        this._applyStyle();

        // Create background with blur effect
        this._background = new St.BoxLayout({
            style_class: 'ultron-taskbar-background',
            x_expand: true,
            y_expand: true,
        });

        // Create apps box
        this._appsBox = new St.BoxLayout({
            style_class: 'ultron-taskbar-apps',
            x_align: Clutter.ActorAlign.CENTER,
            y_align: Clutter.ActorAlign.CENTER,
        });

        // Create separator
        this._separator = new St.BoxLayout({
            style_class: 'ultron-taskbar-separator',
            x_expand: true,
        });

        // Create system tray area
        this._systemTray = new St.BoxLayout({
            style_class: 'ultron-taskbar-tray',
            x_align: Clutter.ActorAlign.END,
        });

        // Create workspace indicator
        this._workspaceIndicator = new St.BoxLayout({
            style_class: 'ultron-taskbar-workspaces',
            x_align: Clutter.ActorAlign.END,
        });

        // Add children
        this._container.add_child(this._background);
        this._container.add_child(this._appsBox);
        this._container.add_child(this._separator);
        this._container.add_child(this._systemTray);
        this._container.add_child(this._workspaceIndicator);

        // Add to stage
        Main.layoutManager.addChrome(this._container, {
            affectsStruts: true,
            trackFullscreen: true,
        });

        this._updatePosition();
    }

    _applyStyle() {
        const size = this._settings.get_int('taskbar-size');
        const iconSize = this._settings.get_int('taskbar-icon-size');
        const enableBlur = this._settings.get_boolean('enable-blur-effects');

        let style = `
            height: ${size}px;
            padding: 0 ${SPACING}px;
            spacing: ${SPACING}px;
        `;

        if (enableBlur) {
            style += `
                background-color: rgba(28, 28, 30, 0.85);
                backdrop-filter: blur(20px);
            `;
        } else {
            style += `background-color: rgba(28, 28, 30, 0.95);`;
        }

        this._container.set_style(style);
    }

    _updatePosition() {
        const position = this._settings.get_string('taskbar-position');
        const monitor = Main.layoutManager.monitors[this._monitorIndex];

        switch (position) {
            case 'bottom':
                this._container.set_position(monitor.x, monitor.y + monitor.height - this._settings.get_int('taskbar-size'));
                this._container.set_size(monitor.width, this._settings.get_int('taskbar-size'));
                this._container.set_style(this._container.style + 'border-top: 1px solid rgba(255,255,255,0.1);');
                break;
            case 'top':
                this._container.set_position(monitor.x, monitor.y);
                this._container.set_size(monitor.width, this._settings.get_int('taskbar-size'));
                this._container.set_style(this._container.style + 'border-bottom: 1px solid rgba(255,255,255,0.1);');
                break;
            case 'left':
                this._container.set_position(monitor.x, monitor.y);
                this._container.set_size(this._settings.get_int('taskbar-size'), monitor.height);
                this._container.set_style(this._container.style + 'border-right: 1px solid rgba(255,255,255,0.1);');
                break;
        }
    }

    _updateSize() {
        this._applyStyle();
        this._updatePosition();
    }

    _loadPinnedApps() {
        // Clear existing buttons
        this._appButtons.forEach(button => button.destroy());
        this._appButtons.clear();

        // Get pinned apps from settings
        const pinnedIds = this._settings.get_strv('pinned-apps');
        const appSystem = Shell.AppSystem.get_default();

        // Create buttons for pinned apps
        pinnedIds.forEach(appId => {
            const app = appSystem.lookup_app(appId);
            if (app) {
                this._addAppButton(app);
            }
        });

        // Add running apps that aren't pinned
        this._updateRunningApps();
    }

    _addAppButton(app) {
        if (this._appButtons.has(app.get_id())) {
            return;
        }

        const iconSize = this._settings.get_int('taskbar-icon-size');
        
        const button = new St.Button({
            style_class: 'ultron-taskbar-button',
            reactive: true,
            can_focus: true,
            track_hover: true,
            child: new St.Icon({
                icon_name: app.get_app_info().get_icon().to_string(),
                icon_size: iconSize,
            }),
        });

        // Store app reference
        button._ultronApp = app;

        // Click handler
        button.connect('clicked', () => {
            const windows = app.get_windows();
            if (windows.length > 0) {
                const topWindow = windows[0];
                if (topWindow.has_focus()) {
                    app.request_action(0); // Minimize
                } else {
                    Main.activateWindow(topWindow);
                }
            } else {
                app.activate();
            }
        });

        // Right-click menu
        button.connect('button-press-event', (actor, event) => {
            if (event.get_button() === 3) {
                this._showAppMenu(button, app);
                return Clutter.EVENT_STOP;
            }
            return Clutter.EVENT_PROPAGATE;
        });

        // Hover effects
        button.connect('notify::hover', () => {
            if (button.hover) {
                button.set_style('transform: scale(1.1); transition: transform 0.2s ease;');
            } else {
                button.set_style('transform: scale(1); transition: transform 0.2s ease;');
            }
        });

        // Update running indicator
        this._updateAppButtonState(button, app);

        this._appsBox.add_child(button);
        this._appButtons.set(app.get_id(), button);
    }

    _updateAppButtonState(button, app) {
        const windows = app.get_windows();
        const isRunning = windows.length > 0;
        const isFocused = windows.some(w => w.has_focus());

        let style = '';
        
        if (isFocused) {
            style += 'background-color: rgba(108, 99, 255, 0.3); border-radius: 8px;';
        } else if (isRunning) {
            style += 'background-color: rgba(255, 255, 255, 0.1); border-radius: 8px;';
        }

        // Add running indicator dot
        if (isRunning) {
            style += `
                box-shadow: inset 0 -3px 0 #6C63FF;
            `;
        }

        button.set_style(style);
    }

    _showAppMenu(button, app) {
        const menu = new PopupMenu.PopupMenu(button, 0.5, St.Side.BOTTOM, 0);
        
        // Add menu items
        const launchItem = new PopupMenu.PopupMenuItem(_('Launch'));
        launchItem.connect('activate', () => {
            app.activate();
            menu.close();
        });
        menu.addMenuItem(launchItem);

        // Add pinned apps separator
        menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

        // Quit option if running
        if (app.get_windows().length > 0) {
            const quitItem = new PopupMenu.PopupMenuItem(_('Quit'));
            quitItem.connect('activate', () => {
                app.get_windows().forEach(w => w.delete(global.get_current_time()));
                menu.close();
            });
            menu.addMenuItem(quitItem);
        }

        // Pin/Unpin option
        const pinnedApps = this._settings.get_strv('pinned-apps');
        const isPinned = pinnedApps.includes(app.get_id());
        
        const pinItem = new PopupMenu.PopupMenuItem(isPinned ? _('Unpin') : _('Pin'));
        pinItem.connect('activate', () => {
            if (isPinned) {
                const updated = pinnedApps.filter(id => id !== app.get_id());
                this._settings.set_strv('pinned-apps', updated);
            } else {
                pinnedApps.push(app.get_id());
                this._settings.set_strv('pinned-apps', pinnedApps);
            }
            this._loadPinnedApps();
            menu.close();
        });
        menu.addMenuItem(pinItem);

        Main.uiGroup.add_child(menu.actor);
        menu.open();
    }

    _updateRunningApps() {
        const appSystem = Shell.AppSystem.get_default();
        const runningApps = appSystem.get_running();
        const pinnedIds = this._settings.get_strv('pinned-apps');

        // Add running apps that aren't pinned
        runningApps.forEach(app => {
            if (!pinnedIds.includes(app.get_id()) && !this._appButtons.has(app.get_id())) {
                this._addAppButton(app);
            }
        });

        // Update states
        this._appButtons.forEach((button, appId) => {
            const app = appSystem.lookup_app(appId);
            if (app) {
                this._updateAppButtonState(button, app);
            }
        });
    }

    _connectSignals() {
        // Watch for window changes
        this._windowAddedId = global.display.connect('window-added', () => {
            this._updateRunningApps();
        });

        this._windowRemovedId = global.display.connect('window-removed', () => {
            this._updateRunningApps();
        });

        // Watch for focus changes
        this._focusChangedId = global.display.connect('notify::focus-window', () => {
            this._appButtons.forEach((button, appId) => {
                const appSystem = Shell.AppSystem.get_default();
                const app = appSystem.lookup_app(appId);
                if (app) {
                    this._updateAppButtonState(button, app);
                }
            });
        });

        // Settings changes
        this._settingsChangedId = this._settings.connect('changed', () => {
            this.reload();
        });
    }

    _disconnectSignals() {
        if (this._windowAddedId) {
            global.display.disconnect(this._windowAddedId);
        }
        if (this._windowRemovedId) {
            global.display.disconnect(this._windowRemovedId);
        }
        if (this._focusChangedId) {
            global.display.disconnect(this._focusChangedId);
        }
        if (this._settingsChangedId) {
            this._settings.disconnect(this._settingsChangedId);
        }
    }

    _show() {
        this._container.show();
    }

    _hide() {
        this._container.hide();
    }

    _destroy() {
        if (this._container) {
            this._container.destroy();
            this._container = null;
        }
    }
}
