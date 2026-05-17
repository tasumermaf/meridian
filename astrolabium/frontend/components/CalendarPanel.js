// CalendarPanel Component - Shows Divine Month, Great Rites, and IAO phase
const CalendarPanel = ({ calendar }) => {
    if (!calendar) return null;

    const getIAOPhaseColor = (phase) => {
        switch(phase) {
            case 'I': return '#6b8e23';  // Olive green for coagula
            case 'A': return '#dc143c';  // Crimson for solve
            case 'O': return '#4169e1';  // Royal blue for rebirth
            default: return 'var(--text-dim)';
        }
    };

    const getIAOPhaseName = (phase) => {
        switch(phase) {
            case 'I': return 'Coagula (Gathering)';
            case 'A': return 'Solve (Separation)';
            case 'O': return 'Rebirth (New Form)';
            default: return 'Outside Formula';
        }
    };

    const formatDate = (isoString) => {
        if (!isoString) return '';
        const date = new Date(isoString);
        return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
    };

    // Get element color for Damanhurian elements (different from Wu Xing!)
    const getDamanhuriElementColor = (element) => {
        const colors = {
            'AIR': '#87ceeb',      // Sky blue
            'EARTH': '#8b7355',    // Brown
            'FIRE': '#ff6347',     // Tomato
            'WATER': '#4682b4',    // Steel blue
            'ETHER': '#9370db'     // Medium purple
        };
        return colors[element] || 'var(--text-secondary)';
    };

    return (
        <div className="panel">
            <h2>Calendar Layer</h2>

            <div className="grid">
                {/* Divine Month */}
                <div style={{
                    padding: '15px',
                    background: 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    border: '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        fontSize: '1.1rem',
                        marginBottom: '10px'
                    }}>
                        Divine Month
                    </h3>

                    <div style={{
                        fontSize: '1.5rem',
                        fontWeight: 'bold',
                        color: 'var(--text-primary)',
                        marginBottom: '10px'
                    }}>
                        {calendar.divine_month}
                    </div>

                    <div className="data-row">
                        <span className="data-label">Month:</span>
                        <span className="data-value">
                            {calendar.month_index} of 13
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Day:</span>
                        <span className="data-value">
                            {calendar.day_in_month} of 28
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Gematria:</span>
                        <span className="data-value" style={{
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            color: 'var(--accent-secondary)'
                        }}>
                            {calendar.gematria}
                        </span>
                    </div>

                    {calendar.element && (
                        <div className="data-row">
                            <span className="data-label">Element:</span>
                            <span className="data-value" style={{
                                color: getDamanhuriElementColor(calendar.element)
                            }}>
                                {calendar.element} (Damanhurian)
                            </span>
                        </div>
                    )}

                    {calendar.great_rite && (
                        <div style={{
                            marginTop: '10px',
                            padding: '8px',
                            background: 'var(--accent-secondary)',
                            color: 'white',
                            borderRadius: '6px',
                            textAlign: 'center',
                            fontWeight: 'bold'
                        }}>
                            Month of {calendar.great_rite}
                        </div>
                    )}
                </div>

                {/* Great Rite Proximity */}
                <div style={{
                    padding: '15px',
                    background: calendar.great_rite_proximity?.is_rite_day
                        ? 'linear-gradient(135deg, var(--accent-primary), var(--accent-secondary))'
                        : 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    border: calendar.great_rite_proximity?.within_ceremonial_window
                        ? '2px solid var(--accent-primary)'
                        : '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: calendar.great_rite_proximity?.is_rite_day ? 'white' : 'var(--accent-primary)',
                        fontSize: '1.1rem',
                        marginBottom: '10px'
                    }}>
                        Great Rite Proximity
                    </h3>

                    {calendar.great_rite_proximity?.is_rite_day ? (
                        <div style={{
                            textAlign: 'center',
                            fontSize: '1.3rem',
                            fontWeight: 'bold',
                            color: 'white',
                            padding: '10px',
                            animation: 'glow 2s ease-in-out infinite'
                        }}>
                            🌟 TODAY IS {calendar.great_rite_proximity.rite_name?.toUpperCase()} 🌟
                        </div>
                    ) : calendar.great_rite_proximity?.within_ceremonial_window ? (
                        <div>
                            <div style={{
                                fontSize: '1.2rem',
                                fontWeight: 'bold',
                                color: 'var(--accent-primary)',
                                marginBottom: '10px'
                            }}>
                                ⚡ Ceremonial Window Active
                            </div>
                            <div className="data-row">
                                <span className="data-label">Rite:</span>
                                <span className="data-value">
                                    {calendar.great_rite_proximity?.rite_name}
                                </span>
                            </div>
                            <div className="data-row">
                                <span className="data-label">Days:</span>
                                <span className="data-value">
                                    {calendar.great_rite_proximity?.days_to_nearest} days away
                                </span>
                            </div>
                            <div className="data-row">
                                <span className="data-label">Date:</span>
                                <span className="data-value">
                                    {formatDate(calendar.great_rite_proximity?.rite_date)}
                                </span>
                            </div>
                        </div>
                    ) : (
                        <div>
                            <div className="data-row">
                                <span className="data-label">Next Rite:</span>
                                <span className="data-value">
                                    {calendar.great_rite_proximity?.rite_name}
                                </span>
                            </div>
                            <div className="data-row">
                                <span className="data-label">Days Until:</span>
                                <span className="data-value">
                                    {calendar.great_rite_proximity?.days_to_nearest}
                                </span>
                            </div>
                            <div className="data-row">
                                <span className="data-label">Date:</span>
                                <span className="data-value">
                                    {formatDate(calendar.great_rite_proximity?.rite_date)}
                                </span>
                            </div>
                        </div>
                    )}

                    <div style={{
                        marginTop: '15px',
                        fontSize: '0.85rem',
                        color: calendar.great_rite_proximity?.is_rite_day ? 'white' : 'var(--text-dim)',
                        textAlign: 'center'
                    }}>
                        Six Great Rites per year
                    </div>
                </div>

                {/* IAO Cycle */}
                <div style={{
                    padding: '15px',
                    background: calendar.iao_phase && calendar.iao_phase !== 'OUTSIDE'
                        ? 'var(--bg-tertiary)'
                        : 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    border: calendar.iao_phase && calendar.iao_phase !== 'OUTSIDE'
                        ? `2px solid ${getIAOPhaseColor(calendar.iao_phase)}`
                        : '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        fontSize: '1.1rem',
                        marginBottom: '10px'
                    }}>
                        IAO Formula
                    </h3>

                    {calendar.iao_phase && calendar.iao_phase !== 'OUTSIDE' ? (
                        <>
                            <div style={{
                                fontSize: '2.5rem',
                                fontWeight: 'bold',
                                color: getIAOPhaseColor(calendar.iao_phase),
                                textAlign: 'center',
                                marginBottom: '10px'
                            }}>
                                {calendar.iao_phase}
                            </div>

                            <div style={{
                                fontSize: '1rem',
                                color: 'var(--text-primary)',
                                textAlign: 'center',
                                marginBottom: '10px'
                            }}>
                                {getIAOPhaseName(calendar.iao_phase)}
                            </div>

                            {calendar.iao_entity && (
                                <div style={{
                                    fontSize: '0.95rem',
                                    color: 'var(--text-secondary)',
                                    textAlign: 'center',
                                    padding: '10px',
                                    background: 'var(--bg-secondary)',
                                    borderRadius: '6px'
                                }}>
                                    Entity: {calendar.iao_entity}
                                </div>
                            )}

                            <div style={{
                                marginTop: '15px',
                                fontSize: '0.85rem',
                                color: 'var(--text-dim)',
                                textAlign: 'center'
                            }}>
                                {calendar.iao_phase === 'I' && 'Months 2-3 (ISIS, SADAM)'}
                                {calendar.iao_phase === 'A' && 'Months 4-5 (SET, HORUS)'}
                                {calendar.iao_phase === 'O' && 'Months 6-8 (TASUMER, MENON, OSIRIS)'}
                            </div>
                        </>
                    ) : (
                        <div style={{
                            fontSize: '1rem',
                            color: 'var(--text-dim)',
                            textAlign: 'center',
                            padding: '20px'
                        }}>
                            Outside IAO Formula
                            <div style={{
                                marginTop: '10px',
                                fontSize: '0.9rem'
                            }}>
                                Months 1, 9-13
                            </div>
                        </div>
                    )}

                    {/* IAO Overview */}
                    <div style={{
                        marginTop: '15px',
                        padding: '10px',
                        background: 'var(--bg-secondary)',
                        borderRadius: '6px',
                        fontSize: '0.85rem',
                        display: 'flex',
                        justifyContent: 'space-around',
                        textAlign: 'center'
                    }}>
                        <div>
                            <div style={{ color: getIAOPhaseColor('I'), fontWeight: 'bold' }}>I</div>
                            <div style={{ color: 'var(--text-dim)' }}>Coagula</div>
                        </div>
                        <div>
                            <div style={{ color: getIAOPhaseColor('A'), fontWeight: 'bold' }}>A</div>
                            <div style={{ color: 'var(--text-dim)' }}>Solve</div>
                        </div>
                        <div>
                            <div style={{ color: getIAOPhaseColor('O'), fontWeight: 'bold' }}>O</div>
                            <div style={{ color: 'var(--text-dim)' }}>Rebirth</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};