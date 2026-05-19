import St from 'gi://St';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Meta from 'gi://Meta';
import Shell from 'gi://Shell';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import { Extension, gettext as _ } from 'resource:///org/gnome/shell/extensions/extension.js';

import { Taskbar } from './components/taskbar.js';
import { Launcher } from './components/launcher.js';
import { NotificationCenter } from './components/notification-center.js';
import { SystemInfo } from './components/system-info.js';
import { WindowManager } from './components/window-manager.js';

export default class UltronShellExtension extends Extension {
    constructor(metadata) {
        super(metadata);
        this._taskbar = null;
        this._launcher = null;
        this._notificationCenter = null;
        this._systemInfo = null;
        this._windowManager = null;
        this._settings = null;
    }

    enable() {
        this._settings = this.getSettings();
        
        // Initialize components
        this._windowManager = new WindowManager(this._settings);
        this._windowManager.enable();
        
        this._taskbar = new Taskbar(this._settings, this.metadata.dir.get_path());
        this._taskbar.enable();
        
        this._launcher = new Launcher(this._settings);
        this._launcher.enable();
        
        this._notificationCenter = new NotificationCenter(this._settings);
        this._notificationCenter.enable();
        
        this._systemInfo = new SystemInfo(this._settings);
        this._systemInfo.enable();
        
        // Add system info to panel
        this._addToPanel();
        
        // Connect settings changes
        this._settingsChangedId = this._settings.connect('changed', () => {
            this._onSettingsChanged();
        });
        
        console.log('Ultron Shell enabled');
    }

    disable() {
        // Disconnect settings
        if (this._settingsChangedId) {
            this._settings.disconnect(this._settingsChangedId);
            this._settingsChangedId = null;
        }
        
        // Remove from panel
        this._removeFromPanel();
        
        // Disable components
        if (this._systemInfo) {
            this._systemInfo.disable();
            this._systemInfo = null;
        }
        
        if (this._notificationCenter) {
            this._notificationCenter.disable();
            this._notificationCenter = null;
        }
        
        if (this._launcher) {
            this._launcher.disable();
            this._launcher = null;
        }
        
        if (this._taskbar) {
            this._taskbar.disable();
            this._taskbar = null;
        }
        
        if (this._windowManager) {
            this._windowManager.disable();
            this._windowManager = null;
        }
        
        this._settings = null;
        
        console.log('Ultron Shell disabled');
    }

    _addToPanel() {
        // Add system indicator to panel
        if (this._systemInfo && this._systemInfo.indicator) {
            Main.panel.addToStatusArea('ultron-system', this._systemInfo.indicator, 0, 'right');
        }
    }

    _removeFromPanel() {
        // Remove system indicator from panel
        if (Main.panel.statusArea['ultron-system']) {
            Main.panel.statusArea['ultron-system'].destroy();
            delete Main.panel.statusArea['ultron-system'];
        }
    }

    _onSettingsChanged() {
        // Reload components based on settings changes
        if (this._taskbar) {
            this._taskbar.reload();
        }
        
        if (this._notificationCenter) {
            this._notificationCenter.reload();
        }
        
        if (this._systemInfo) {
            this._systemInfo.reload();
        }
    }
}
