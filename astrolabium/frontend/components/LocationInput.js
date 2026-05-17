// LocationInput Component - Handles location and timezone selection
const LocationInput = ({ onLocationChange, currentLocation }) => {
    const [lat, setLat] = React.useState(currentLocation?.lat || 40.7128);
    const [lon, setLon] = React.useState(currentLocation?.lon || -74.0060);
    const [tz, setTz] = React.useState(currentLocation?.tz || 'America/New_York');
    const [isGettingLocation, setIsGettingLocation] = React.useState(false);
    const [error, setError] = React.useState('');

    // Common timezones for dropdown
    const timezones = [
        'America/New_York',
        'America/Chicago',
        'America/Denver',
        'America/Los_Angeles',
        'America/Phoenix',
        'America/Anchorage',
        'Pacific/Honolulu',
        'Europe/London',
        'Europe/Paris',
        'Europe/Berlin',
        'Europe/Rome',
        'Europe/Moscow',
        'Asia/Dubai',
        'Asia/Kolkata',
        'Asia/Shanghai',
        'Asia/Tokyo',
        'Asia/Singapore',
        'Australia/Perth',
        'Australia/Sydney',
        'Pacific/Auckland',
        'UTC'
    ];

    // Load saved location from localStorage on mount
    React.useEffect(() => {
        const saved = localStorage.getItem('astrolabium_location');
        if (saved) {
            try {
                const location = JSON.parse(saved);
                setLat(location.lat);
                setLon(location.lon);
                setTz(location.tz);
                // Don't call onLocationChange here - let the parent handle initial load
            } catch (e) {
                console.error('Failed to load saved location:', e);
            }
        }
    }, []);

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        // Validate inputs
        const latitude = parseFloat(lat);
        const longitude = parseFloat(lon);

        if (isNaN(latitude) || latitude < -90 || latitude > 90) {
            setError('Latitude must be between -90 and 90');
            return;
        }

        if (isNaN(longitude) || longitude < -180 || longitude > 180) {
            setError('Longitude must be between -180 and 180');
            return;
        }

        const location = { lat: latitude, lon: longitude, tz };

        // Save to localStorage
        localStorage.setItem('astrolabium_location', JSON.stringify(location));

        // Notify parent
        onLocationChange(location);
    };

    const handleGeolocation = () => {
        if (!navigator.geolocation) {
            setError('Geolocation is not supported by your browser');
            return;
        }

        setIsGettingLocation(true);
        setError('');

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const newLat = position.coords.latitude.toFixed(4);
                const newLon = position.coords.longitude.toFixed(4);
                setLat(newLat);
                setLon(newLon);
                setIsGettingLocation(false);

                // Auto-detect timezone based on location (simplified)
                // In production, use a timezone API
                const tzGuess = guessTimezone(newLat, newLon);
                if (tzGuess) setTz(tzGuess);
            },
            (error) => {
                setIsGettingLocation(false);
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        setError('Location permission denied');
                        break;
                    case error.POSITION_UNAVAILABLE:
                        setError('Location information unavailable');
                        break;
                    case error.TIMEOUT:
                        setError('Location request timed out');
                        break;
                    default:
                        setError('An unknown error occurred');
                }
            }
        );
    };

    const guessTimezone = (lat, lon) => {
        // Very simplified timezone guessing based on longitude
        // In production, use a proper timezone API
        const lng = parseFloat(lon);

        if (lng >= -130 && lng <= -110) return 'America/Los_Angeles';
        if (lng >= -110 && lng <= -95) return 'America/Denver';
        if (lng >= -95 && lng <= -80) return 'America/Chicago';
        if (lng >= -80 && lng <= -65) return 'America/New_York';
        if (lng >= -10 && lng <= 5) return 'Europe/London';
        if (lng >= 5 && lng <= 20) return 'Europe/Berlin';
        if (lng >= 20 && lng <= 40) return 'Europe/Moscow';
        if (lng >= 120 && lng <= 145) return 'Asia/Tokyo';
        if (lng >= 145 && lng <= 160) return 'Australia/Sydney';

        return null;
    };

    const clearLocation = () => {
        localStorage.removeItem('astrolabium_location');
        setLat(40.7128);
        setLon(-74.0060);
        setTz('America/New_York');
        setError('');
    };

    return (
        <div className="panel">
            <h2>Location Settings</h2>

            <form onSubmit={handleSubmit}>
                <div className="grid">
                    <div className="input-group">
                        <label htmlFor="lat">Latitude</label>
                        <input
                            type="number"
                            id="lat"
                            value={lat}
                            onChange={(e) => setLat(e.target.value)}
                            step="0.0001"
                            min="-90"
                            max="90"
                            placeholder="40.7128"
                            required
                        />
                    </div>

                    <div className="input-group">
                        <label htmlFor="lon">Longitude</label>
                        <input
                            type="number"
                            id="lon"
                            value={lon}
                            onChange={(e) => setLon(e.target.value)}
                            step="0.0001"
                            min="-180"
                            max="180"
                            placeholder="-74.0060"
                            required
                        />
                    </div>

                    <div className="input-group">
                        <label htmlFor="tz">Timezone</label>
                        <select
                            id="tz"
                            value={tz}
                            onChange={(e) => setTz(e.target.value)}
                            required
                        >
                            {timezones.map(zone => (
                                <option key={zone} value={zone}>{zone}</option>
                            ))}
                        </select>
                    </div>
                </div>

                {error && (
                    <div className="error" style={{ marginBottom: '15px' }}>
                        {error}
                    </div>
                )}

                <div style={{ display: 'flex', gap: '10px' }}>
                    <button type="submit" style={{ flex: 1 }}>
                        Update Location
                    </button>

                    <button
                        type="button"
                        onClick={handleGeolocation}
                        disabled={isGettingLocation}
                        style={{ flex: 1 }}
                    >
                        {isGettingLocation ? 'Getting Location...' : '📍 Use My Location'}
                    </button>

                    <button
                        type="button"
                        onClick={clearLocation}
                        style={{ flex: '0 0 auto' }}
                    >
                        Clear
                    </button>
                </div>
            </form>

            <div style={{ marginTop: '15px', fontSize: '0.9rem', color: 'var(--text-dim)' }}>
                Current: {lat}°, {lon}° ({tz})
            </div>
        </div>
    );
};