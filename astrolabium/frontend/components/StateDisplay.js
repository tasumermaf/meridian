// StateDisplay Component - Shows the three body layers
const StateDisplay = ({ state }) => {
    if (!state) return null;

    const { primeval, derivative, organ_clock } = state;

    return (
        <div className="panel">
            <h2>Three Body Layers</h2>

            <div className="grid">
                {/* SOUL Layer (Lunar/Primeval) */}
                <div style={{
                    background: 'var(--bg-tertiary)',
                    padding: '15px',
                    borderRadius: '8px',
                    border: '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        marginBottom: '10px',
                        fontSize: '1.1rem'
                    }}>
                        SOUL (Lunar)
                    </h3>

                    <div className="data-row">
                        <span className="data-label">Primeval Law:</span>
                        <span className="data-value" style={{ color: '#ff9999' }}>
                            {primeval?.law}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Lunar Phase:</span>
                        <span className="data-value">
                            {primeval?.lunar_phase} ({Math.round(primeval?.illumination_percent || 0)}%)
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Trigram:</span>
                        <span className="data-value">
                            {primeval?.trigram_symbol} {primeval?.trigram}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Perception (+):</span>
                        <span className="data-value" style={{ fontSize: '0.9rem' }}>
                            {primeval?.perception_positive}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Perception (-):</span>
                        <span className="data-value" style={{ fontSize: '0.9rem' }}>
                            {primeval?.perception_negative}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Quest:</span>
                        <span className="data-value" style={{ fontSize: '0.9rem' }}>
                            {primeval?.quest}
                        </span>
                    </div>
                </div>

                {/* ASTRAL Layer (LGBF/Derivative) */}
                <div style={{
                    background: 'var(--bg-tertiary)',
                    padding: '15px',
                    borderRadius: '8px',
                    border: '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        marginBottom: '10px',
                        fontSize: '1.1rem'
                    }}>
                        ASTRAL (LGBF)
                    </h3>

                    <div className="data-row">
                        <span className="data-label">Derivative Law:</span>
                        <span className="data-value" style={{ color: '#9999ff' }}>
                            {derivative?.law}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Vessel:</span>
                        <span className="data-value">
                            {derivative?.vessel}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Confluent Point:</span>
                        <span className="data-value">
                            {derivative?.confluent_point}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Coupled Point:</span>
                        <span className="data-value">
                            {derivative?.coupled_point}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Trigram:</span>
                        <span className="data-value">
                            {derivative?.trigram_symbol} {derivative?.trigram}
                        </span>
                    </div>

                    {derivative?.calculation_details && (
                        <div style={{
                            marginTop: '10px',
                            paddingTop: '10px',
                            borderTop: '1px solid var(--bg-secondary)',
                            fontSize: '0.85rem',
                            color: 'var(--text-dim)'
                        }}>
                            <div>Daily: {derivative.calculation_details.daily_stem} {derivative.calculation_details.daily_branch}</div>
                            <div>Hourly: {derivative.calculation_details.hourly_stem} {derivative.calculation_details.hourly_branch}</div>
                            <div>Remainder: {derivative.calculation_details.remainder}/{derivative.calculation_details.divisor}</div>
                        </div>
                    )}
                </div>

                {/* GROSS Layer (Physical/Organ Clock) */}
                <div style={{
                    background: 'var(--bg-tertiary)',
                    padding: '15px',
                    borderRadius: '8px',
                    border: '1px solid var(--border)'
                }}>
                    <h3 style={{
                        color: 'var(--accent-primary)',
                        marginBottom: '10px',
                        fontSize: '1.1rem'
                    }}>
                        GROSS (Organ)
                    </h3>

                    <div className="data-row">
                        <span className="data-label">Active Organ:</span>
                        <span className="data-value" style={{
                            color: getElementColor(organ_clock?.element),
                            fontWeight: 'bold'
                        }}>
                            {organ_clock?.organ}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Meridian:</span>
                        <span className="data-value">
                            {organ_clock?.meridian}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Element (Wu Xing):</span>
                        <span className="data-value" style={{
                            color: getElementColor(organ_clock?.element)
                        }}>
                            {organ_clock?.element}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Branch:</span>
                        <span className="data-value">
                            {organ_clock?.branch?.chinese} ({organ_clock?.branch?.pinyin})
                            <br />
                            <span style={{ fontSize: '0.9rem', color: 'var(--text-dim)' }}>
                                {organ_clock?.branch?.animal}
                            </span>
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Emotion (+):</span>
                        <span className="data-value" style={{ fontSize: '0.9rem' }}>
                            {organ_clock?.emotion_positive}
                        </span>
                    </div>

                    <div className="data-row">
                        <span className="data-label">Emotion (-):</span>
                        <span className="data-value" style={{ fontSize: '0.9rem' }}>
                            {organ_clock?.emotion_negative}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Helper function for Wu Xing element colors
function getElementColor(element) {
    const colors = {
        'Wood': 'var(--element-wood)',
        'Fire': 'var(--element-fire)',
        'Earth': 'var(--element-earth)',
        'Metal': 'var(--element-metal)',
        'Water': 'var(--element-water)'
    };
    return colors[element] || 'var(--text-primary)';
}