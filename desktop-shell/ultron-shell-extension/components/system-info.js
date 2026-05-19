import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';

export class SystemInfo {
    constructor(settings) {
        this._settings = settings;
        this._indicator = null;
        this._menu = null;
        this._cpuLabel = null;
        this._memLabel = null;
        this._netLabel = null;
        this._updateTimeout = null;
        this._prevNetStats = null;
    }

    enable() {
        this._createIndicator();
        this._createMenu();
        this._startMonitoring();
    }

    disable() {
        this._stopMonitoring();
        this._destroy();
    }

    reload() {
        this._updateDisplay();
    }

    _createIndicator() {
        this._indicator = new PanelMenu.Button(0.0, _('System Info'), false);

        const box = new St.BoxLayout({
            style_class: 'panel-status-indicators-box',
            spacing: 8,
        });

        // CPU usage
        this._cpuLabel = new St.Label({
            text: '',
            style: 'font-size: 11px;',
            visible: this._settings.get_boolean('show-cpu-usage'),
        });

        // Memory usage
        this._memLabel = new St.Label({
            text: '',
            style: 'font-size: 11px;',
            visible: this._settings.get_boolean('show-memory-usage'),
        });

        // Network speed
        this._netLabel = new St.Label({
            text: '',
            style: 'font-size: 11px;',
            visible: this._settings.get_boolean('show-network-speed'),
        });

        box.add_child(this._cpuLabel);
        box.add_child(this._memLabel);
        box.add_child(this._netLabel);

        this._indicator.add_child(box);
    }

    _createMenu() {
        this._menu = this._indicator.menu;

        // System information section
        const infoSection = new PopupMenu.PopupMenuSection();
        
        // Hostname
        const hostnameRow = new PopupMenu.PopupBaseMenuItem({ reactive: false });
        const hostnameLabel = new St.Label({
            text: `Host: ${GLib.get_host_name()}`,
            style: 'font-size: 12px;',
        });
        hostnameRow.add_child(hostnameLabel);
        infoSection.actor.add_child(hostnameRow.actor);

        // OS Version
        const osRow = new PopupMenu.PopupBaseMenuItem({ reactive: false });
        const osLabel = new St.Label({
            text: `OS: Ultron OS 1.0.0`,
            style: 'font-size: 12px;',
        });
        osRow.add_child(osLabel);
        infoSection.actor.add_child(osRow.actor);

        // Kernel
        const kernelRow = new PopupMenu.PopupBaseMenuItem({ reactive: false });
        const kernelLabel = new St.Label({
            text: `Kernel: ${GLib.get_os_info('VERSION') || 'Linux'}`,
            style: 'font-size: 12px;',
        });
        kernelRow.add_child(kernelLabel);
        infoSection.actor.add_child(kernelRow.actor);

        this._menu.addMenuItem(infoSection);
        this._menu.addMenuItem(new PopupMenu.PopupSeparatorMenuItem());

        // Quick actions
        const settingsItem = new PopupMenu.PopupMenuItem(_('Settings'));
        settingsItem.connect('activate', () => {
            this._openSettings();
        });
        this._menu.addMenuItem(settingsItem);

        const aboutItem = new PopupMenu.PopupMenuItem(_('About'));
        aboutItem.connect('activate', () => {
            this._openAbout();
        });
        this._menu.addMenuItem(aboutItem);
    }

    _startMonitoring() {
        this._updateDisplay();
        
        // Update every 2 seconds
        this._updateTimeout = GLib.timeout_add_seconds(
            GLib.PRIORITY_DEFAULT,
            2,
            () => {
                this._updateDisplay();
                return GLib.SOURCE_CONTINUE;
            }
        );
    }

    _stopMonitoring() {
        if (this._updateTimeout) {
            GLib.Source.remove(this._updateTimeout);
            this._updateTimeout = null;
        }
    }

    _updateDisplay() {
        this._updateCPU();
        this._updateMemory();
        this._updateNetwork();
    }

    _updateCPU() {
        if (!this._settings.get_boolean('show-cpu-usage')) {
            this._cpuLabel.visible = false;
            return;
        }

        this._cpuLabel.visible = true;

        try {
            const [success, contents] = GLib.file_get_contents('/proc/stat');
            if (!success) return;

            const lines = contents.split('\n');
            const cpuLine = lines[0]; // First line is total CPU
            const parts = cpuLine.split(/\s+/);
            
            // parts[0] = 'cpu', parts[1-4] = user, nice, system, idle
            const user = parseInt(parts[1]);
            const nice = parseInt(parts[2]);
            const system = parseInt(parts[3]);
            const idle = parseInt(parts[4]);
            
            const total = user + nice + system + idle;
            const active = total - idle;
            
            if (this._prevCpuTotal) {
                const totalDiff = total - this._prevCpuTotal;
                const activeDiff = active - this._prevCpuActive;
                const usage = Math.round((activeDiff / totalDiff) * 100);
                
                this._cpuLabel.set_text(`CPU: ${usage}%`);
                
                // Color based on usage
                if (usage > 80) {
                    this._cpuLabel.set_style('font-size: 11px; color: #FF3B30;');
                } else if (usage > 50) {
                    this._cpuLabel.set_style('font-size: 11px; color: #FF9500;');
                } else {
                    this._cpuLabel.set_style('font-size: 11px; color: #34C759;');
                }
            }
            
            this._prevCpuTotal = total;
            this._prevCpuActive = active;
        } catch (e) {
            log(`Error reading CPU stats: ${e.message}`);
        }
    }

    _updateMemory() {
        if (!this._settings.get_boolean('show-memory-usage')) {
            this._memLabel.visible = false;
            return;
        }

        this._memLabel.visible = true;

        try {
            const [success, contents] = GLib.file_get_contents('/proc/meminfo');
            if (!success) return;

            const lines = contents.split('\n');
            let memTotal = 0;
            let memAvailable = 0;

            lines.forEach(line => {
                if (line.startsWith('MemTotal:')) {
                    memTotal = parseInt(line.split(/\s+/)[1]);
                } else if (line.startsWith('MemAvailable:')) {
                    memAvailable = parseInt(line.split(/\s+/)[1]);
                }
            });

            if (memTotal > 0) {
                const memUsed = memTotal - memAvailable;
                const usage = Math.round((memUsed / memTotal) * 100);
                const usedGB = (memUsed / 1024 / 1024).toFixed(1);
                const totalGB = (memTotal / 1024 / 1024).toFixed(1);
                
                this._memLabel.set_text(`RAM: ${usage}% (${usedGB}/${totalGB}GB)`);
                
                if (usage > 80) {
                    this._memLabel.set_style('font-size: 11px; color: #FF3B30;');
                } else if (usage > 50) {
                    this._memLabel.set_style('font-size: 11px; color: #FF9500;');
                } else {
                    this._memLabel.set_style('font-size: 11px; color: #34C759;');
                }
            }
        } catch (e) {
            log(`Error reading memory stats: ${e.message}`);
        }
    }

    _updateNetwork() {
        if (!this._settings.get_boolean('show-network-speed')) {
            this._netLabel.visible = false;
            return;
        }

        this._netLabel.visible = true;

        try {
            const [success, contents] = GLib.file_get_contents('/proc/net/dev');
            if (!success) return;

            let totalRx = 0;
            let totalTx = 0;

            const lines = contents.split('\n');
            lines.forEach(line => {
                if (line.includes(':') && !line.includes('lo:')) {
                    const parts = line.split(/[\s:]+/);
                    if (parts.length >= 10) {
                        totalRx += parseInt(parts[2]); // RX bytes
                        totalTx += parseInt(parts[10]); // TX bytes
                    }
                }
            });

            if (this._prevNetRx !== undefined) {
                const rxSpeed = totalRx - this._prevNetRx;
                const txSpeed = totalTx - this._prevNetTx;
                
                const rxFormatted = this._formatBytes(rxSpeed);
                const txFormatted = this._formatBytes(txSpeed);
                
                this._netLabel.set_text(`↓${rxFormatted}/s ↑${txFormatted}/s`);
            }

            this._prevNetRx = totalRx;
            this._prevNetTx = totalTx;
        } catch (e) {
            log(`Error reading network stats: ${e.message}`);
        }
    }

    _formatBytes(bytes) {
        if (bytes < 1024) return `${bytes}B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
        return `${(bytes / 1024 / 1024).toFixed(1)}MB`;
    }

    _openSettings() {
        const appSystem = Shell.AppSystem.get_default();
        const settingsApp = appSystem.lookup_app('org.gnome.Settings.desktop');
        if (settingsApp) {
            settingsApp.activate();
        }
    }

    _openAbout() {
        // Open Ultron welcome app
        const appSystem = Shell.AppSystem.get_default();
        const welcomeApp = appSystem.lookup_app('org.ultron.welcome.desktop');
        if (welcomeApp) {
            welcomeApp.activate();
        }
    }

    _destroy() {
        if (this._indicator) {
            this._indicator.destroy();
            this._indicator = null;
        }
    }
}
