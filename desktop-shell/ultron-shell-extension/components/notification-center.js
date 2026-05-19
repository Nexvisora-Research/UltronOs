import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as PanelMenu from 'resource:///org/gnome/shell/ui/panelMenu.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import * as MessageList from 'resource:///org/gnome/shell/ui/messageList.js';

const NC_WIDTH = 380;
const NC_HEIGHT = 500;

export class NotificationCenter {
    constructor(settings) {
        this._settings = settings;
        this._indicator = null;
        this._menu = null;
        this._container = null;
        this._quickTogglesBox = null;
        this._notificationsBox = null;
        this._isOpen = false;
        this._notifications = [];
    }

    enable() {
        this._createIndicator();
        this._createNotificationCenter();
        this._connectSignals();
        this._loadNotifications();
    }

    disable() {
        this._disconnectSignals();
        this._close();
        this._destroy();
    }

    reload() {
        this._updateQuickToggles();
    }

    _createIndicator() {
        this._indicator = new PanelMenu.Button(0.0, _('Notifications'), false);

        const box = new St.BoxLayout({
            style_class: 'panel-status-indicators-box',
        });

        const icon = new St.Icon({
            icon_name: 'preferences-system-notifications-symbolic',
            style_class: 'system-status-icon',
        });

        box.add_child(icon);

        // Notification count badge
        this._countLabel = new St.Label({
            text: '0',
            style: 'font-size: 10px; padding: 0 4px; background: #6C63FF; border-radius: 8px; color: white;',
            visible: false,
        });

        box.add_child(this._countLabel);

        this._indicator.add_child(box);

        this._indicator.connect('button-press-event', () => {
            this.toggle();
        });
    }

    _createNotificationCenter() {
        // Create main container
        this._container = new St.BoxLayout({
            name: 'ultronNotificationCenter',
            reactive: true,
            track_hover: true,
            visible: false,
            style_class: 'ultron-notification-center',
        });

        this._applyStyle();

        // Position in top-right
        const monitor = Main.layoutManager.primaryMonitor;
        this._container.set_position(
            monitor.x + monitor.width - NC_WIDTH - 12,
            monitor.y + 40
        );
        this._container.set_size(NC_WIDTH, NC_HEIGHT);

        // Header
        const header = new St.BoxLayout({
            style_class: 'ultron-nc-header',
        });

        const titleLabel = new St.Label({
            text: _('Notification Center'),
            style: 'font-size: 18px; font-weight: bold;',
        });

        const clearButton = new St.Button({
            label: _('Clear'),
            style_class: 'ultron-nc-clear-button',
        });

        clearButton.connect('clicked', () => {
            this._clearNotifications();
        });

        header.add_child(titleLabel);
        header.add_child(new St.BoxLayout({ x_expand: true }));
        header.add_child(clearButton);

        // Quick toggles
        this._quickTogglesBox = new St.BoxLayout({
            style_class: 'ultron-nc-quick-toggles',
            x_expand: true,
        });

        this._updateQuickToggles();

        // Notifications list
        this._notificationsBox = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            style_class: 'ultron-nc-notifications',
            x_expand: true,
            y_expand: true,
            spacing: 8,
        });

        // Add children
        this._container.add_child(header);
        this._container.add_child(this._quickTogglesBox);
        this._container.add_child(this._notificationsBox);

        // Add to stage
        Main.layoutManager.addChrome(this._container, {
            affectsStruts: false,
            trackFullscreen: false,
        });

        // Create overlay
        this._overlay = new St.BoxLayout({
            name: 'ultronNCOverlay',
            reactive: true,
            visible: false,
            style: 'background-color: transparent;',
        });

        Main.layoutManager.addChrome(this._overlay, {
            affectsStruts: false,
            trackFullscreen: false,
        });

        this._overlay.connect('button-press-event', () => {
            this._close();
        });
    }

    _applyStyle() {
        const enableBlur = this._settings.get_boolean('enable-blur-effects');

        let style = `
            border-radius: 16px;
            padding: 16px;
            spacing: 16px;
        `;

        if (enableBlur) {
            style += `
                background-color: rgba(44, 44, 46, 0.9);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            `;
        } else {
            style += `
                background-color: rgba(44, 44, 46, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
            `;
        }

        this._container.set_style(style);
    }

    _updateQuickToggles() {
        // Clear existing
        this._quickTogglesBox.destroy_all_children();

        const toggles = this._settings.get_strv('quick-toggles');

        const toggleConfigs = {
            'wifi': { icon: 'network-wireless-symbolic', label: _('Wi-Fi'), setting: null },
            'bluetooth': { icon: 'bluetooth-active-symbolic', label: _('Bluetooth'), setting: null },
            'dark-mode': { icon: 'display-brightness-symbolic', label: _('Dark Mode'), setting: null },
            'night-light': { icon: 'night-light-symbolic', label: _('Night Light'), setting: null },
            'do-not-disturb': { icon: 'notifications-disabled-symbolic', label: _('DND'), setting: 'notification-do-not-disturb' },
            'airplane-mode': { icon: 'airplane-mode-symbolic', label: _('Airplane'), setting: null },
        };

        toggles.forEach(toggleId => {
            const config = toggleConfigs[toggleId];
            if (!config) return;

            const toggleButton = new St.Button({
                style_class: 'ultron-nc-toggle',
                reactive: true,
                can_focus: true,
                track_hover: true,
            });

            const box = new St.BoxLayout({
                orientation: Clutter.Orientation.VERTICAL,
                spacing: 4,
            });

            const icon = new St.Icon({
                icon_name: config.icon,
                icon_size: 20,
            });

            const label = new St.Label({
                text: config.label,
                style: 'font-size: 11px;',
            });

            box.add_child(icon);
            box.add_child(label);

            toggleButton.child = box;

            // Toggle state
            toggleButton._isActive = false;

            toggleButton.connect('clicked', () => {
                toggleButton._isActive = !toggleButton._isActive;
                this._updateToggleStyle(toggleButton, toggleButton._isActive);
                this._handleToggleAction(toggleId, toggleButton._isActive);
            });

            this._quickTogglesBox.add_child(toggleButton);
        });
    }

    _updateToggleStyle(button, isActive) {
        if (isActive) {
            button.set_style(`
                background-color: rgba(108, 99, 255, 0.3);
                border: 1px solid #6C63FF;
                border-radius: 12px;
                padding: 12px;
            `);
        } else {
            button.set_style(`
                background-color: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 12px;
            `);
        }
    }

    _handleToggleAction(toggleId, isActive) {
        switch (toggleId) {
            case 'wifi':
                // Toggle WiFi
                break;
            case 'bluetooth':
                // Toggle Bluetooth
                break;
            case 'dark-mode':
                const settings = Gio.Settings.new('org.gnome.desktop.interface');
                settings.set_boolean('color-scheme', isActive ? 'prefer-dark' : 'default');
                break;
            case 'night-light':
                const nightLightSettings = Gio.Settings.new('org.gnome.settings-daemon.plugins.color');
                nightLightSettings.set_boolean('night-light-enabled', isActive);
                break;
            case 'do-not-disturb':
                this._settings.set_boolean('notification-do-not-disturb', isActive);
                Main.notificationServer.setDoNotDisturb(isActive);
                break;
            case 'airplane-mode':
                // Toggle Airplane Mode
                break;
        }
    }

    _loadNotifications() {
        // Load from message tray
        const messageList = Main.messageTray;
        
        // Connect to notification events
        this._notificationAddedId = messageList.connect('notification-added', (source, notification) => {
            this._addNotification(notification);
        });

        this._notificationRemovedId = messageList.connect('notification-removed', (source, notification) => {
            this._removeNotification(notification);
        });
    }

    _addNotification(notification) {
        const dnd = this._settings.get_boolean('notification-do-not-disturb');
        if (dnd) return;

        const notifBox = new St.BoxLayout({
            style_class: 'ultron-nc-notification',
            reactive: true,
        });

        notifBox.set_style(`
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        `);

        // Icon
        const icon = new St.Icon({
            icon_name: notification.iconName || 'dialog-information-symbolic',
            icon_size: 24,
        });

        // Content
        const contentBox = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            spacing: 4,
            x_expand: true,
        });

        const titleLabel = new St.Label({
            text: notification.title || notification.source.title,
            style: 'font-size: 14px; font-weight: bold;',
        });

        const bodyLabel = new St.Label({
            text: notification.body || '',
            style: 'font-size: 12px; color: #A1A1A6;',
        });

        const timeLabel = new St.Label({
            text: this._formatTime(new Date()),
            style: 'font-size: 10px; color: #6E6E73;',
        });

        contentBox.add_child(titleLabel);
        contentBox.add_child(bodyLabel);
        contentBox.add_child(timeLabel);

        // Close button
        const closeButton = new St.Button({
            icon_name: 'window-close-symbolic',
            style_class: 'ultron-nc-notif-close',
        });

        closeButton.connect('clicked', () => {
            notifBox.destroy();
            this._notifications = this._notifications.filter(n => n !== notifBox);
            this._updateCount();
        });

        notifBox.add_child(icon);
        notifBox.add_child(contentBox);
        notifBox.add_child(closeButton);

        this._notificationsBox.add_child(notifBox);
        this._notifications.push(notifBox);
        this._updateCount();
    }

    _removeNotification(notification) {
        // Remove from display
        this._notifications = this._notifications.filter(notifBox => {
            if (notifBox._notification === notification) {
                notifBox.destroy();
                return false;
            }
            return true;
        });
        this._updateCount();
    }

    _clearNotifications() {
        this._notifications.forEach(notifBox => notifBox.destroy());
        this._notifications = [];
        this._updateCount();
    }

    _updateCount() {
        const count = this._notifications.length;
        if (count > 0) {
            this._countLabel.set_text(count.toString());
            this._countLabel.visible = true;
        } else {
            this._countLabel.visible = false;
        }
    }

    _formatTime(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);

        if (minutes < 1) return _('Just now');
        if (minutes < 60) return _(`${minutes}m ago`);
        if (hours < 24) return _(`${hours}h ago`);
        return date.toLocaleDateString();
    }

    _open() {
        this._isOpen = true;
        this._container.show();
        this._overlay.show();
        
        // Animate in
        this._container.opacity = 0;
        this._container.ease({
            opacity: 255,
            duration: 200,
            mode: Clutter.AnimationMode.EASE_OUT_QUAD,
        });
    }

    _close() {
        this._isOpen = false;
        
        this._container.ease({
            opacity: 0,
            duration: 150,
            mode: Clutter.AnimationMode.EASE_IN_QUAD,
            onComplete: () => {
                this._container.hide();
                this._overlay.hide();
            },
        });
    }

    toggle() {
        if (this._isOpen) {
            this._close();
        } else {
            this._open();
        }
    }

    _connectSignals() {
        this._settingsChangedId = this._settings.connect('changed', () => {
            this.reload();
        });
    }

    _disconnectSignals() {
        if (this._settingsChangedId) {
            this._settings.disconnect(this._settingsChangedId);
        }
        if (this._notificationAddedId) {
            Main.messageTray.disconnect(this._notificationAddedId);
        }
        if (this._notificationRemovedId) {
            Main.messageTray.disconnect(this._notificationRemovedId);
        }
    }

    _destroy() {
        if (this._indicator) {
            this._indicator.destroy();
            this._indicator = null;
        }
        if (this._container) {
            this._container.destroy();
            this._container = null;
        }
        if (this._overlay) {
            this._overlay.destroy();
            this._overlay = null;
        }
    }
}
