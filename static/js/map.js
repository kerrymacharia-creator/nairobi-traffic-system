// Nairobi Traffic Information System - Map Utilities

const TrafficMap = {
    // Configuration
    config: {
        defaultCenter: [-1.286389, 36.817223],
        defaultZoom: 12,
        nairobiBounds: {
            north: -1.0,
            south: -1.5,
            east: 37.0,
            west: 36.6
        }
    },

    // Initialize map with options
    init: function(elementId, options = {}) {
        const map = L.map(elementId).setView(
            options.center || this.config.defaultCenter,
            options.zoom || this.config.defaultZoom
        );

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(map);

        return map;
    },

    // Check if coordinates are within Nairobi bounds
    isInNairobi: function(lat, lng) {
        return (
            lat >= this.config.nairobiBounds.south &&
            lat <= this.config.nairobiBounds.north &&
            lng >= this.config.nairobiBounds.west &&
            lng <= this.config.nairobiBounds.east
        );
    },

    // Get color based on severity
    getSeverityColor: function(severity) {
        const colors = {
            1: '#6c757d',  // Low
            2: '#17a2b8',  // Medium
            3: '#ffc107',  // High
            4: '#dc3545'   // Critical
        };
        return colors[severity] || '#6c757d';
    },

    // Get icon for incident type
    getIncidentIcon: function(type) {
        const icons = {
            'accident': '💥',
            'hazard': '⚠️',
            'heavy_traffic': '🚗',
            'road_closure': '🚧',
            'construction': '🏗️',
            'other': '⚡'
        };
        return icons[type] || '⚠️';
    },

    // Create custom marker
    createMarker: function(lat, lng, type, severity) {
        const color = this.getSeverityColor(severity);
        const icon = this.getIncidentIcon(type);
        
        return L.marker([lat, lng], {
            icon: L.divIcon({
                className: 'custom-div-icon',
                html: `<div style="background-color: ${color}; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3); font-size: 16px;">${icon}</div>`,
                iconSize: [30, 30],
                iconAnchor: [15, 15]
            })
        });
    },

    // Format date for display
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-KE', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TrafficMap;
}