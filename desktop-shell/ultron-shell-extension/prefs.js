import Gtk from 'gi://Gtk';
import Gio from 'gi://Gio';
import Adw from 'gi://Adw';

import { ExtensionPreferences, gettext as _ } from 'resource:///org/gnome/Shell/Extensions/js/extensions/prefs.js';

export default class UltronShellPreferences extends ExtensionPreferences {
    fillPreferencesWindow(window) {
        window._settings = this.getSettings();
        
        // Taskbar page
        const taskbarPage = new Adw.PreferencesPage({
            title: _('Taskbar'),
            icon_name: 'panel-app-symbolic',
        });
        
        const taskbarGroup = new Adw.PreferencesGroup({
            title: _('Taskbar Settings'),
            description: _('Configure the taskbar appearance and behavior'),
        });
        
        // Taskbar position
        const positionRow = new Adw.ComboRow({
            title: _('Position'),
            subtitle: _('Where to place the taskbar'),
        });
        
        const positionModel = new Gtk.StringList();
        positionModel.append(_('Bottom'));
        positionModel.append(_('Top'));
        positionModel.append(_('Left'));
        positionRow.set_model(positionModel);
        
        const position = window._settings.get_string('taskbar-position');
        const positionMap = { 'bottom': 0, 'top': 1, 'left': 2 };
        positionRow.set_selected(positionMap[position] || 0);
        
        positionRow.connect('notify::selected', (widget) => {
            const positions = ['bottom', 'top', 'left'];
            window._settings.set_string('taskbar-position', positions[widget.selected]);
        });
        
        // Taskbar size
        const sizeRow = new Adw.SpinRow({
            title: _('Size'),
            subtitle: _('Height of the taskbar in pixels'),
            adjustment: new Gtk.Adjustment({
                lower: 32,
                upper: 72,
                step_increment: 4,
                page_increment: 8,
            }),
        });
        sizeRow.set_value(window._settings.get_int('taskbar-size'));
        sizeRow.connect('notify::value', (widget) => {
            window._settings.set_int('taskbar-size', widget.value);
        });
        
        // Auto-hide
        const autohideRow = new Adw.SwitchRow({
            title: _('Auto-hide'),
            subtitle: _('Automatically hide the taskbar'),
            active: window._settings.get_boolean('taskbar-autohide'),
        });
        autohideRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('taskbar-autohide', widget.active);
        });
        
        // Icon size
        const iconSizeRow = new Adw.SpinRow({
            title: _('Icon Size'),
            subtitle: _('Size of icons in the taskbar'),
            adjustment: new Gtk.Adjustment({
                lower: 24,
                upper: 64,
                step_increment: 4,
                page_increment: 8,
            }),
        });
        iconSizeRow.set_value(window._settings.get_int('taskbar-icon-size'));
        iconSizeRow.connect('notify::value', (widget) => {
            window._settings.set_int('taskbar-icon-size', widget.value);
        });
        
        taskbarGroup.add(positionRow);
        taskbarGroup.add(sizeRow);
        taskbarGroup.add(autohideRow);
        taskbarGroup.add(iconSizeRow);
        taskbarPage.add(taskbarGroup);
        
        // Launcher page
        const launcherPage = new Adw.PreferencesPage({
            title: _('Launcher'),
            icon_name: 'view-app-grid-symbolic',
        });
        
        const launcherGroup = new Adw.PreferencesGroup({
            title: _('Launcher Settings'),
            description: _('Configure the application launcher'),
        });
        
        const showCategoriesRow = new Adw.SwitchRow({
            title: _('Show Categories'),
            subtitle: _('Display application categories'),
            active: window._settings.get_boolean('launcher-show-categories'),
        });
        showCategoriesRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('launcher-show-categories', widget.active);
        });
        
        const showRecentRow = new Adw.SwitchRow({
            title: _('Show Recent'),
            subtitle: _('Display recently used applications'),
            active: window._settings.get_boolean('launcher-show-recent'),
        });
        showRecentRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('launcher-show-recent', widget.active);
        });
        
        const maxRecentRow = new Adw.SpinRow({
            title: _('Max Recent Apps'),
            subtitle: _('Number of recent applications to show'),
            adjustment: new Gtk.Adjustment({
                lower: 5,
                upper: 20,
                step_increment: 1,
                page_increment: 5,
            }),
        });
        maxRecentRow.set_value(window._settings.get_int('launcher-max-recent'));
        maxRecentRow.connect('notify::value', (widget) => {
            window._settings.set_int('launcher-max-recent', widget.value);
        });
        
        launcherGroup.add(showCategoriesRow);
        launcherGroup.add(showRecentRow);
        launcherGroup.add(maxRecentRow);
        launcherPage.add(launcherGroup);
        
        // Notification Center page
        const notificationPage = new Adw.PreferencesPage({
            title: _('Notifications'),
            icon_name: 'user-available-symbolic',
        });
        
        const notificationGroup = new Adw.PreferencesGroup({
            title: _('Notification Center'),
            description: _('Configure notification behavior'),
        });
        
        const enabledRow = new Adw.SwitchRow({
            title: _('Enable Notification Center'),
            subtitle: _('Show notification center in panel'),
            active: window._settings.get_boolean('notification-center-enabled'),
        });
        enabledRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('notification-center-enabled', widget.active);
        });
        
        const dndRow = new Adw.SwitchRow({
            title: _('Do Not Disturb'),
            subtitle: _('Silence all notifications'),
            active: window._settings.get_boolean('notification-do-not-disturb'),
        });
        dndRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('notification-do-not-disturb', widget.active);
        });
        
        const historyDaysRow = new Adw.SpinRow({
            title: _('History Days'),
            subtitle: _('Days to keep notification history'),
            adjustment: new Gtk.Adjustment({
                lower: 1,
                upper: 30,
                step_increment: 1,
                page_increment: 7,
            }),
        });
        historyDaysRow.set_value(window._settings.get_int('notification-history-days'));
        historyDaysRow.connect('notify::value', (widget) => {
            window._settings.set_int('notification-history-days', widget.value);
        });
        
        notificationGroup.add(enabledRow);
        notificationGroup.add(dndRow);
        notificationGroup.add(historyDaysRow);
        notificationPage.add(notificationGroup);
        
        // Appearance page
        const appearancePage = new Adw.PreferencesPage({
            title: _('Appearance'),
            icon_name: 'brush-symbolic',
        });
        
        const appearanceGroup = new Adw.PreferencesGroup({
            title: _('Visual Effects'),
            description: _('Configure visual appearance and effects'),
        });
        
        const blurRow = new Adw.SwitchRow({
            title: _('Blur Effects'),
            subtitle: _('Enable acrylic/blur effects'),
            active: window._settings.get_boolean('enable-blur-effects'),
        });
        blurRow.connect('notify::active', (widget) => {
            window._settings.set_boolean('enable-blur-effects', widget.active);
        });
        
        const animationSpeedRow = new Adw.SpinRow({
            title: _('Animation Speed'),
            subtitle: _('Multiplier for animation speed (1.0 = normal)'),
            adjustment: new Gtk.Adjustment({
                lower: 0.1,
                upper: 3.0,
                step_increment: 0.1,
                page_increment: 0.5,
            }),
        });
        animationSpeedRow.set_value(window._settings.get_double('animation-speed'));
        animationSpeedRow.connect('notify::value', (widget) => {
            window._settings.set_double('animation-speed', widget.value);
        });
        
        appearanceGroup.add(blurRow);
        appearanceGroup.add(animationSpeedRow);
        appearancePage.add(appearanceGroup);
        
        // Add all pages
        window.add(taskbarPage);
        window.add(launcherPage);
        window.add(notificationPage);
        window.add(appearancePage);
    }
}
