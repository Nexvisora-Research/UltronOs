import St from 'gi://St';
import Clutter from 'gi://Clutter';
import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import Shell from 'gi://Shell';

import * as Main from 'resource:///org/gnome/shell/ui/main.js';
import * as AppDisplay from 'resource:///org/gnome/shell/ui/appDisplay.js';
import * as PopupMenu from 'resource:///org/gnome/shell/ui/popupMenu.js';
import * as Search from 'resource:///org/gnome/shell/ui/search.js';

const LAUNCHER_WIDTH = 700;
const LAUNCHER_HEIGHT = 500;
const MAX_RESULTS = 10;

export class Launcher {
    constructor(settings) {
        this._settings = settings;
        this._container = null;
        this._searchEntry = null;
        this._resultsBox = null;
        this._categoriesBox = null;
        this._recentBox = null;
        this._isOpen = false;
        this._currentResults = [];
        this._appSystem = Shell.AppSystem.get_default();
        this._allApps = [];
        this._recentApps = [];
    }

    enable() {
        this._createLauncher();
        this._loadApps();
        this._connectSignals();
        this._loadRecentApps();
    }

    disable() {
        this._disconnectSignals();
        this._close();
        this._destroy();
    }

    toggle() {
        if (this._isOpen) {
            this._close();
        } else {
            this._open();
        }
    }

    _createLauncher() {
        // Create main container
        this._container = new St.BoxLayout({
            name: 'ultronLauncher',
            reactive: true,
            track_hover: true,
            visible: false,
            style_class: 'ultron-launcher',
        });

        // Apply styling
        this._applyStyle();

        // Center on screen
        const monitor = Main.layoutManager.primaryMonitor;
        this._container.set_position(
            monitor.x + (monitor.width - LAUNCHER_WIDTH) / 2,
            monitor.y + (monitor.height - LAUNCHER_HEIGHT) / 2
        );
        this._container.set_size(LAUNCHER_WIDTH, LAUNCHER_HEIGHT);

        // Create search bar
        this._searchEntry = new St.Entry({
            name: 'ultronLauncherSearch',
            style_class: 'ultron-launcher-search',
            hint_text: _('Search applications...'),
            track_hover: true,
            x_expand: true,
        });

        // Search icon
        this._searchEntry.set_primary_icon(new St.Icon({
            icon_name: 'system-search-symbolic',
            style_class: 'system-status-icon',
        }));

        // Create content area
        this._contentBox = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            style_class: 'ultron-launcher-content',
            x_expand: true,
            y_expand: true,
        });

        // Categories box
        this._categoriesBox = new St.BoxLayout({
            style_class: 'ultron-launcher-categories',
            x_expand: true,
        });

        // Results box
        this._resultsBox = new St.BoxLayout({
            orientation: Clutter.Orientation.VERTICAL,
            style_class: 'ultron-launcher-results',
            x_expand: true,
            y_expand: true,
        });

        // Recent apps box
        this._recentBox = new St.BoxLayout({
            style_class: 'ultron-launcher-recent',
            x_expand: true,
        });

        // Add children
        this._contentBox.add_child(this._categoriesBox);
        this._contentBox.add_child(this._resultsBox);
        this._contentBox.add_child(this._recentBox);

        this._container.add_child(this._searchEntry);
        this._container.add_child(this._contentBox);

        // Add to stage
        Main.layoutManager.addChrome(this._container, {
            affectsStruts: false,
            trackFullscreen: false,
        });

        // Create overlay background
        this._overlay = new St.BoxLayout({
            name: 'ultronLauncherOverlay',
            reactive: true,
            visible: false,
            style: 'background-color: rgba(0, 0, 0, 0.5);',
        });

        Main.layoutManager.addChrome(this._overlay, {
            affectsStruts: false,
            trackFullscreen: false,
        });

        // Close on overlay click
        this._overlay.connect('button-press-event', () => {
            this._close();
        });
    }

    _applyStyle() {
        const enableBlur = this._settings.get_boolean('enable-blur-effects');

        let style = `
            border-radius: 16px;
            padding: 20px;
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

    _loadApps() {
        // Get all installed applications
        this._allApps = this._appSystem.get_installed();
        
        // Sort alphabetically
        this._allApps.sort((a, b) => {
            const nameA = a.get_name().toLowerCase();
            const nameB = b.get_name().toLowerCase();
            return nameA.localeCompare(nameB);
        });

        // Load categories if enabled
        if (this._settings.get_boolean('launcher-show-categories')) {
            this._loadCategories();
        }
    }

    _loadCategories() {
        // Define common categories
        const categories = [
            { name: _('Favorites'), icon: 'starred-symbolic', filter: (app) => this._isFavorite(app) },
            { name: _('Internet'), icon: 'web-browser-symbolic', filter: (app) => this._hasCategory(app, 'Network') },
            { name: _('Office'), icon: 'x-office-document-symbolic', filter: (app) => this._hasCategory(app, 'Office') },
            { name: _('Graphics'), icon: 'camera-photo-symbolic', filter: (app) => this._hasCategory(app, 'Graphics') },
            { name: _('Games'), icon: 'applications-games-symbolic', filter: (app) => this._hasCategory(app, 'Game') },
            { name: _('System'), icon: 'system-run-symbolic', filter: (app) => this._hasCategory(app, 'System') },
            { name: _('Utilities'), icon: 'applications-utilities-symbolic', filter: (app) => this._hasCategory(app, 'Utility') },
        ];

        categories.forEach(cat => {
            const button = new St.Button({
                style_class: 'ultron-launcher-category',
                reactive: true,
                can_focus: true,
                track_hover: true,
                child: new St.BoxLayout({
                    style_class: 'ultron-launcher-category-button',
                }),
            });

            const icon = new St.Icon({
                icon_name: cat.icon,
                icon_size: 16,
            });

            const label = new St.Label({
                text: cat.name,
            });

            button.child.add_child(icon);
            button.child.add_child(label);

            button.connect('clicked', () => {
                this._filterByCategory(cat.filter);
            });

            this._categoriesBox.add_child(button);
        });
    }

    _loadRecentApps() {
        if (!this._settings.get_boolean('launcher-show-recent')) {
            return;
        }

        // Load from recent files
        const recentManager = Gtk.RecentManager.get_default();
        const recentItems = recentManager.get_items();
        
        // Limit to max recent apps
        const maxRecent = this._settings.get_int('launcher-max-recent');
        const recent = recentItems.slice(0, maxRecent);

        recent.forEach(item => {
            const uri = item.get_uri();
            const app = this._appSystem.lookup_app_for_uri(uri);
            if (app && !this._recentApps.includes(app)) {
                this._recentApps.push(app);
            }
        });

        this._updateRecentDisplay();
    }

    _updateRecentDisplay() {
        // Clear existing
        this._recentBox.destroy_all_children();

        if (this._recentApps.length === 0) {
            return;
        }

        // Add label
        const label = new St.Label({
            text: _('Recent'),
            style_class: 'ultron-launcher-section-label',
        });
        this._recentBox.add_child(label);

        // Add recent app buttons
        const appsBox = new St.BoxLayout({
            spacing: 12,
        });

        this._recentApps.forEach(app => {
            const button = new St.Button({
                style_class: 'ultron-launcher-app-button',
                reactive: true,
                can_focus: true,
                track_hover: true,
            });

            const icon = new St.Icon({
                icon_name: app.get_app_info().get_icon().to_string(),
                icon_size: 48,
            });

            const nameLabel = new St.Label({
                text: app.get_name(),
                style: 'font-size: 12px; text-align: center;',
            });

            const box = new St.BoxLayout({
                orientation: Clutter.Orientation.VERTICAL,
                spacing: 4,
            });

            box.add_child(icon);
            box.add_child(nameLabel);

            button.child = box;

            button.connect('clicked', () => {
                app.activate();
                this._close();
            });

            appsBox.add_child(button);
        });

        this._recentBox.add_child(appsBox);
    }

    _searchApps(query) {
        if (!query || query.length === 0) {
            this._clearResults();
            return;
        }

        const lowerQuery = query.toLowerCase();
        const results = this._allApps.filter(app => {
            const name = app.get_name().toLowerCase();
            const description = (app.get_description() || '').toLowerCase();
            const keywords = (app.get_keywords() || []).join(' ').toLowerCase();
            
            return name.includes(lowerQuery) || 
                   description.includes(lowerQuery) || 
                   keywords.includes(lowerQuery);
        }).slice(0, MAX_RESULTS);

        this._displayResults(results);
    }

    _displayResults(results) {
        // Clear existing
        this._resultsBox.destroy_all_children();

        if (results.length === 0) {
            const noResults = new St.Label({
                text: _('No results found'),
                style_class: 'ultron-launcher-no-results',
            });
            this._resultsBox.add_child(noResults);
            return;
        }

        results.forEach(app => {
            const button = new St.Button({
                style_class: 'ultron-launcher-app-button',
                reactive: true,
                can_focus: true,
                track_hover: true,
            });

            const icon = new St.Icon({
                icon_name: app.get_app_info().get_icon().to_string(),
                icon_size: 48,
            });

            const nameLabel = new St.Label({
                text: app.get_name(),
                style: 'font-size: 14px;',
            });

            const descLabel = new St.Label({
                text: app.get_description() || '',
                style: 'font-size: 12px; color: #A1A1A6;',
            });

            const box = new St.BoxLayout({
                orientation: Clutter.Orientation.HORIZONTAL,
                spacing: 12,
            });

            box.add_child(icon);

            const textBox = new St.BoxLayout({
                orientation: Clutter.Orientation.VERTICAL,
                spacing: 4,
            });

            textBox.add_child(nameLabel);
            textBox.add_child(descLabel);

            box.add_child(textBox);

            button.child = box;

            button.connect('clicked', () => {
                app.activate();
                this._close();
            });

            this._resultsBox.add_child(button);
        });
    }

    _clearResults() {
        this._resultsBox.destroy_all_children();
    }

    _filterByCategory(filter) {
        const filtered = this._allApps.filter(filter).slice(0, MAX_RESULTS);
        this._displayResults(filtered);
    }

    _isFavorite(app) {
        const favorites = Main.uiFavorites ? Main.uiFavorites.getFavorites() : [];
        return favorites.includes(app.get_id());
    }

    _hasCategory(app, category) {
        const categories = app.get_categories() || [];
        return categories.some(c => c.includes(category));
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

        // Focus search entry
        global.stage.set_key_focus(this._searchEntry);
    }

    _close() {
        this._isOpen = false;
        
        // Animate out
        this._container.ease({
            opacity: 0,
            duration: 150,
            mode: Clutter.AnimationMode.EASE_IN_QUAD,
            onComplete: () => {
                this._container.hide();
                this._overlay.hide();
                this._clearResults();
                this._searchEntry.set_text('');
            },
        });
    }

    _connectSignals() {
        // Search entry text changed
        this._searchChangedId = this._searchEntry.clutter_text.connect('text-changed', () => {
            const query = this._searchEntry.get_text();
            this._searchApps(query);
        });

        // Key press events
        this._keyPressId = this._container.connect('key-press-event', (actor, event) => {
            const symbol = event.get_key_symbol();
            
            if (symbol === Clutter.KEY_Escape) {
                this._close();
                return Clutter.EVENT_STOP;
            }
            
            if (symbol === Clutter.KEY_Return || symbol === Clutter.KEY_KP_Enter) {
                // Launch first result
                if (this._currentResults.length > 0) {
                    this._currentResults[0].activate();
                    this._close();
                }
                return Clutter.EVENT_STOP;
            }
            
            return Clutter.EVENT_PROPAGATE;
        });

        // Global keybinding
        this._accelerator = Main.wm.addKeybinding(
            'open-launcher',
            this._settings,
            Meta.KeyBindingFlags.NONE,
            Shell.ActionMode.ALL,
            () => this.toggle()
        );
    }

    _disconnectSignals() {
        if (this._searchChangedId) {
            this._searchEntry.clutter_text.disconnect(this._searchChangedId);
        }
        if (this._keyPressId) {
            this._container.disconnect(this._keyPressId);
        }
        if (this._accelerator) {
            Main.wm.removeKeybinding('open-launcher');
        }
    }

    _destroy() {
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
