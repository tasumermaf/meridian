// DivineHour Component - Shows current divine hour and progress
const DivineHour = ({ divineHour, temporalReference }) => {
    if (!divineHour) return null;

    const progressPercent = divineHour.progress_percent || 0;

    // Divine Hour names and natures
    const hourInfo = {
        'I': { name: 'Prima', nature: 'Awakening' },
        'II': { name: 'Seconda', nature: 'Rising' },
        'III': { name: 'Terza', nature: 'Culmination' },
        'IV': { name: 'Quarta', nature: 'Descending' },
        'V': { name: 'Quinta', nature: 'Transition' },
        'VI': { name: 'Sesta', nature: 'Deepening' },
        'VII': { name: 'Settima', nature: 'Mystery' },
        'VIII': { name: 'Ottava', nature: 'Return' }
    };

    const formatTime = (isoString) => {
        if (!isoString) return '--:--';
        const date = new Date(isoString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    const formatDuration = (minutes) => {
        if (!minutes) return '0m';
        const hours = Math.floor(minutes / 60);
        const mins = Math.round(minutes % 60);
        if (hours > 0) {
            return `${hours}h ${mins}m`;
        }
        return `${mins}m`;
    };

    const currentHour = hourInfo[divineHour.roman] || {};

    return (
        <div className="panel">
            <h2>Divine Hour</h2>

            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                {/* Hour display */}
                <div style={{
                    fontSize: '3rem',
                    color: 'var(--accent-primary)',
                    fontWeight: '300',
                    lineHeight: '1'
                }}>
                    {divineHour.roman}
                </div>

                <div style={{
                    fontSize: '1.2rem',
                    color: 'var(--text-primary)',
                    marginTop: '5px'
                }}>
                    {divineHour.name}
                </div>

                <div style={{
                    fontSize: '1rem',
                    color: 'var(--text-secondary)',
                    marginTop: '5px'
                }}>
                    {divineHour.nature}
                </div>

                {/* Wing indicator */}
                <div style={{
                    marginTop: '15px',
                    padding: '5px 15px',
                    display: 'inline-block',
                    background: divineHour.wing === 'DAY'
                        ? 'linear-gradient(135deg, #ffd700, #ffed4e)'
                        : 'linear-gradient(135deg, #191970, #4169e1)',
                    color: divineHour.wing === 'DAY' ? '#000' : '#fff',
                    borderRadius: '20px',
                    fontSize: '0.9rem',
                    fontWeight: 'bold'
                }}>
                    {divineHour.wing === 'DAY' ? '☀️ DAY' : '🌙 NIGHT'} WING
                </div>
            </div>

            {/* Progress bar */}
            <div>
                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginBottom: '5px',
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)'
                }}>
                    <span>Progress</span>
                    <span>{Math.round(progressPercent)}%</span>
                </div>

                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${progressPercent}%` }}
                    ></div>
                </div>

                <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginTop: '5px',
                    fontSize: '0.85rem',
                    color: 'var(--text-dim)'
                }}>
                    <span>Duration: {formatDuration(divineHour.duration_minutes)}</span>
                    <span>Remaining: {formatDuration(divineHour.remaining_minutes)}</span>
                </div>
            </div>

            {/* Solar times */}
            {temporalReference && (
                <div style={{
                    marginTop: '20px',
                    padding: '10px',
                    background: 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    fontSize: '0.9rem'
                }}>
                    <div className="data-row">
                        <span className="data-label">🌅 Sunrise:</span>
                        <span className="data-value">
                            {formatTime(temporalReference.sunrise)}
                        </span>
                    </div>
                    <div className="data-row">
                        <span className="data-label">☀️ Solar Noon:</span>
                        <span className="data-value">
                            {formatTime(temporalReference.solar_noon)}
                        </span>
                    </div>
                    <div className="data-row">
                        <span className="data-label">🌇 Sunset:</span>
                        <span className="data-value">
                            {formatTime(temporalReference.sunset)}
                        </span>
                    </div>
                    <div className="data-row">
                        <span className="data-label">🌙 Solar Midnight:</span>
                        <span className="data-value">
                            {formatTime(temporalReference.solar_midnight)}
                        </span>
                    </div>
                </div>
            )}

            {/* Divine Hours overview */}
            <div style={{
                marginTop: '15px',
                fontSize: '0.85rem',
                color: 'var(--text-dim)',
                textAlign: 'center'
            }}>
                <div>Day: I-IV (Prima → Quarta)</div>
                <div>Night: V-VIII (Quinta → Ottava)</div>
            </div>
        </div>
    );
};