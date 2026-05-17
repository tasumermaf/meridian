// Astrolabium Caudae Rubrae - Main App Component (FIXED)
// Fixes state propagation bug where location update didn't trigger fetch

const API_BASE = `${window.location.protocol}//${window.location.hostname}:8000`;

const App = () => {
    const [location, setLocation] = React.useState(() => {
        // Load from localStorage on init
        const saved = localStorage.getItem('astrolabium_location');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                console.error('Failed to parse saved location:', e);
            }
        }
        return null;
    });
    
    const [state, setState] = React.useState(null);
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState(null);
    const [lastUpdate, setLastUpdate] = React.useState(null);

    // Fetch state from API
    const fetchState = React.useCallback(async (loc) => {
        console.log('fetchState called with location:', loc);
        if (!loc) {
            console.log('No location provided, returning');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const url = `${API_BASE}/state?lat=${loc.lat}&lon=${loc.lon}&tz=${encodeURIComponent(loc.tz)}`;
            console.log('Fetching state from:', url);

            const response = await fetch(url);
            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Received state data:', data);
            console.log('State data keys:', Object.keys(data));

            setState(data);
            setLastUpdate(new Date());
            setError(null);
            console.log('State set successfully');
        } catch (err) {
            console.error('Fetch error:', err);
            setError(err.message);
            setState(null);
        } finally {
            setLoading(false);
            console.log('Loading set to false');
        }
    }, []);

    // Handle location change from LocationInput
    const handleLocationChange = React.useCallback((newLocation) => {
        console.log('Location changed:', newLocation);
        setLocation(newLocation);
        localStorage.setItem('astrolabium_location', JSON.stringify(newLocation));
        // Immediately fetch with new location
        fetchState(newLocation);
    }, [fetchState]);

    // Initial fetch when location exists
    React.useEffect(() => {
        if (location) {
            console.log('Initial fetch for location:', location);
            fetchState(location);
        }
    }, []); // Only on mount

    // Auto-refresh every 60 seconds
    React.useEffect(() => {
        if (!location) return;

        const interval = setInterval(() => {
            console.log('Auto-refresh triggered');
            fetchState(location);
        }, 60000);

        return () => clearInterval(interval);
    }, [location, fetchState]);

    // Debug logging
    console.log('App render - location:', location);
    console.log('App render - state:', state);
    console.log('App render - loading:', loading);
    console.log('App render - error:', error);
    if (state) {
        console.log('State exists! Keys:', Object.keys(state));
        console.log('Alignments:', state.alignments);
        console.log('Primeval:', state.primeval);
    }

    return (
        React.createElement('div', { className: 'container' },
            // Header
            React.createElement('header', { className: 'header' },
                React.createElement('h1', null, 'ASTROLABIUM CAUDAE RUBRAE'),
                React.createElement('p', { className: 'subtitle' }, 
                    'What is the alchemical quality of this moment?'
                )
            ),
            
            // Location Input
            React.createElement(LocationInput, {
                onLocationChange: handleLocationChange,
                currentLocation: location
            }),
            
            // Loading indicator
            loading && React.createElement('div', { className: 'loading' }, 
                'Calculating temporal state...'
            ),
            
            // Error display
            error && React.createElement('div', { className: 'error-message' },
                React.createElement('strong', null, 'Error: '),
                error,
                React.createElement('button', {
                    onClick: () => fetchState(location),
                    style: { marginLeft: '10px' }
                }, 'Retry')
            ),
            
            // Main content - only show when we have state
            state && React.createElement(React.Fragment, null,
                // Law Unity Alert (prominent when active)
                state.alignments && state.alignments.law_unity && 
                    React.createElement('div', { className: 'law-unity-alert' },
                        React.createElement('h2', null, '⚡ LAW UNITY ACTIVE ⚡'),
                        React.createElement('p', null, 
                            `Primeval and Derivative Laws align on: ${state.alignments.aligned_law}`
                        )
                    ),
                
                // Alignment Panel
                React.createElement(AlignmentPanel, { alignments: state.alignments }),
                
                // Three columns layout
                React.createElement('div', { className: 'main-grid' },
                    // Left column - Primeval (Soul)
                    React.createElement('div', { className: 'panel' },
                        React.createElement('h2', null, 'Soul Layer'),
                        React.createElement('h3', { className: 'law-name' }, 
                            state.primeval?.law || 'Unknown'
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Lunar Phase:'),
                            React.createElement('span', null, state.primeval?.lunar_phase)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Trigram:'),
                            React.createElement('span', null, 
                                `${state.primeval?.trigram_symbol || ''} ${state.primeval?.trigram || ''}`
                            )
                        ),
                        state.primeval?.perception_positive &&
                            React.createElement('div', { className: 'perceptions' },
                                React.createElement('div', { className: 'positive' },
                                    React.createElement('strong', null, 'Positive: '),
                                    state.primeval.perception_positive
                                ),
                                React.createElement('div', { className: 'negative' },
                                    React.createElement('strong', null, 'Shadow: '),
                                    state.primeval.perception_negative || ''
                                )
                            )
                    ),
                    
                    // Center column - Derivative (Astral)
                    React.createElement('div', { className: 'panel' },
                        React.createElement('h2', null, 'Astral Layer'),
                        React.createElement('h3', { className: 'law-name' }, 
                            state.derivative?.law || 'Unknown'
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Vessel:'),
                            React.createElement('span', null, state.derivative?.vessel)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Confluent:'),
                            React.createElement('span', null, state.derivative?.confluent_point)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Coupled:'),
                            React.createElement('span', null, state.derivative?.coupled_point)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Trigram:'),
                            React.createElement('span', null, state.derivative?.trigram)
                        )
                    ),
                    
                    // Right column - Organ Clock (Gross)
                    React.createElement('div', { className: 'panel' },
                        React.createElement('h2', null, 'Gross Layer'),
                        React.createElement('h3', { className: 'law-name' }, 
                            state.organ_clock?.organ || 'Unknown'
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Meridian:'),
                            React.createElement('span', null, state.organ_clock?.meridian)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Element:'),
                            React.createElement('span', { 
                                className: `element-${(state.organ_clock?.element || '').toLowerCase()}`
                            }, state.organ_clock?.element)
                        ),
                        React.createElement('div', { className: 'detail-row' },
                            React.createElement('span', { className: 'label' }, 'Branch:'),
                            React.createElement('span', null, (() => {
                                if (!state.organ_clock?.branch) return 'Unknown';
                                if (typeof state.organ_clock.branch === 'string') return state.organ_clock.branch;
                                if (state.organ_clock.branch?.chinese) {
                                    return `${state.organ_clock.branch.chinese} (${state.organ_clock.branch.pinyin || ''}) - ${state.organ_clock.branch.animal || ''}`;
                                }
                                console.error('Unexpected branch structure:', state.organ_clock.branch);
                                return 'Unknown';
                            })())
                        ),
                        state.organ_clock?.emotion_positive &&
                            React.createElement('div', { className: 'perceptions' },
                                React.createElement('div', { className: 'positive' },
                                    React.createElement('strong', null, 'Virtue: '),
                                    state.organ_clock.emotion_positive
                                ),
                                React.createElement('div', { className: 'negative' },
                                    React.createElement('strong', null, 'Shadow: '),
                                    state.organ_clock.emotion_negative || ''
                                )
                            )
                    )
                ),
                
                // Divine Hour Panel
                React.createElement(DivineHour, { 
                    divineHour: state.divine_hour,
                    temporalReference: state.temporal_reference
                }),
                
                // Organ Clock Visualization
                React.createElement(OrganClock, { organClock: state.organ_clock }),
                
                // Calendar Panel
                React.createElement(CalendarPanel, { calendar: state.calendar }),
                
                // Last update timestamp
                lastUpdate && React.createElement('div', { className: 'last-update' },
                    `Last updated: ${lastUpdate.toLocaleTimeString()}`
                )
            ),
            
            // No location set message
            !location && !loading && React.createElement('div', { className: 'no-location' },
                React.createElement('p', null, 'Set your location above to see the current temporal state.'),
                React.createElement('p', null, 'The Astrolabium calculates sacred time from your specific position on Earth.')
            ),
            
            // Footer
            React.createElement('footer', { className: 'footer' },
                React.createElement('p', null, 'Astrolabium Caudae Rubrae'),
                React.createElement('p', null, 'In dedication to Falco Tarassaco')
            )
        )
    );
};

// Mount the app
const rootElement = document.getElementById('root');
if (rootElement) {
    // Use React 18 createRoot if available, fallback to render
    if (ReactDOM.createRoot) {
        const root = ReactDOM.createRoot(rootElement);
        root.render(React.createElement(App));
    } else {
        ReactDOM.render(React.createElement(App), rootElement);
    }
} else {
    console.error('Root element not found!');
}
