// OrganClock Component - Circular visualization of 12 organs
const OrganClock = ({ organClock }) => {
    if (!organClock) return null;

    // 12 Organs in temporal order starting from 子 (Zi) at top
    const organs = [
        { branch: '子', meridian: 'GB', organ: 'Gallbladder', element: 'Wood', start: 23 },
        { branch: '丑', meridian: 'LV', organ: 'Liver', element: 'Wood', start: 1 },
        { branch: '寅', meridian: 'LU', organ: 'Lung', element: 'Metal', start: 3 },
        { branch: '卯', meridian: 'LI', organ: 'Large Intestine', element: 'Metal', start: 5 },
        { branch: '辰', meridian: 'ST', organ: 'Stomach', element: 'Earth', start: 7 },
        { branch: '巳', meridian: 'SP', organ: 'Spleen', element: 'Earth', start: 9 },
        { branch: '午', meridian: 'HT', organ: 'Heart', element: 'Fire', start: 11 },
        { branch: '未', meridian: 'SI', organ: 'Small Intestine', element: 'Fire', start: 13 },
        { branch: '申', meridian: 'BL', organ: 'Bladder', element: 'Water', start: 15 },
        { branch: '酉', meridian: 'KI', organ: 'Kidney', element: 'Water', start: 17 },
        { branch: '戌', meridian: 'PC', organ: 'Pericardium', element: 'Fire', start: 19 },
        { branch: '亥', meridian: 'SJ', organ: 'San Jiao', element: 'Fire', start: 21 }
    ];

    const currentMeridian = organClock.meridian;

    // SVG dimensions
    const size = 300;
    const center = size / 2;
    const radius = size / 2 - 30;
    const innerRadius = radius * 0.4;

    const getSegmentPath = (index) => {
        const anglePerSegment = 360 / 12;
        // Start from top (子 at 12 o'clock position)
        const startAngle = (index * anglePerSegment - 90) * (Math.PI / 180);
        const endAngle = ((index + 1) * anglePerSegment - 90) * (Math.PI / 180);

        const x1 = center + Math.cos(startAngle) * radius;
        const y1 = center + Math.sin(startAngle) * radius;
        const x2 = center + Math.cos(endAngle) * radius;
        const y2 = center + Math.sin(endAngle) * radius;
        const x3 = center + Math.cos(startAngle) * innerRadius;
        const y3 = center + Math.sin(startAngle) * innerRadius;
        const x4 = center + Math.cos(endAngle) * innerRadius;
        const y4 = center + Math.sin(endAngle) * innerRadius;

        return `M ${x3} ${y3} L ${x1} ${y1} A ${radius} ${radius} 0 0 1 ${x2} ${y2} L ${x4} ${y4} A ${innerRadius} ${innerRadius} 0 0 0 ${x3} ${y3} Z`;
    };

    const getTextPosition = (index) => {
        const anglePerSegment = 360 / 12;
        const angle = (index * anglePerSegment + anglePerSegment / 2 - 90) * (Math.PI / 180);
        const textRadius = (radius + innerRadius) / 2;

        return {
            x: center + Math.cos(angle) * textRadius,
            y: center + Math.sin(angle) * textRadius
        };
    };

    return (
        <div className="panel">
            <h2>Organ Clock</h2>

            <div style={{ textAlign: 'center' }}>
                <svg width={size} height={size} style={{ maxWidth: '100%', height: 'auto' }}>
                    {organs.map((organ, index) => {
                        const isActive = organ.meridian === currentMeridian;
                        const textPos = getTextPosition(index);

                        return (
                            <g key={organ.meridian}>
                                {/* Segment */}
                                <path
                                    d={getSegmentPath(index)}
                                    fill={isActive ? getElementColor(organ.element) : 'var(--bg-tertiary)'}
                                    stroke={isActive ? 'var(--accent-primary)' : 'var(--border)'}
                                    strokeWidth={isActive ? 3 : 1}
                                    opacity={isActive ? 1 : 0.6}
                                    style={{
                                        transition: 'all 0.3s ease',
                                        cursor: 'pointer'
                                    }}
                                />

                                {/* Branch character */}
                                <text
                                    x={textPos.x}
                                    y={textPos.y - 8}
                                    fill={isActive ? 'white' : 'var(--text-secondary)'}
                                    fontSize="16"
                                    fontWeight={isActive ? 'bold' : 'normal'}
                                    textAnchor="middle"
                                    style={{ pointerEvents: 'none' }}
                                >
                                    {organ.branch}
                                </text>

                                {/* Meridian code */}
                                <text
                                    x={textPos.x}
                                    y={textPos.y + 8}
                                    fill={isActive ? 'white' : 'var(--text-dim)'}
                                    fontSize="12"
                                    textAnchor="middle"
                                    style={{ pointerEvents: 'none' }}
                                >
                                    {organ.meridian}
                                </text>
                            </g>
                        );
                    })}

                    {/* Center circle with current info */}
                    <circle
                        cx={center}
                        cy={center}
                        r={innerRadius - 10}
                        fill="var(--bg-secondary)"
                        stroke="var(--border)"
                        strokeWidth="1"
                    />

                    <text
                        x={center}
                        y={center - 10}
                        fill="var(--accent-primary)"
                        fontSize="18"
                        fontWeight="bold"
                        textAnchor="middle"
                    >
                        {organClock.organ}
                    </text>

                    <text
                        x={center}
                        y={center + 10}
                        fill={getElementColor(organClock.element)}
                        fontSize="14"
                        textAnchor="middle"
                    >
                        {organClock.element}
                    </text>
                </svg>

                {/* Legend */}
                <div style={{
                    marginTop: '15px',
                    display: 'flex',
                    justifyContent: 'center',
                    gap: '15px',
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)'
                }}>
                    {['Wood', 'Fire', 'Earth', 'Metal', 'Water'].map(element => (
                        <div key={element} style={{ display: 'flex', alignItems: 'center' }}>
                            <div style={{
                                width: '12px',
                                height: '12px',
                                backgroundColor: getElementColor(element),
                                borderRadius: '50%',
                                marginRight: '5px'
                            }}></div>
                            {element}
                        </div>
                    ))}
                </div>

                {/* Current organ info */}
                <div style={{
                    marginTop: '15px',
                    padding: '10px',
                    background: 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    textAlign: 'left',
                    fontSize: '0.9rem'
                }}>
                    <div className="data-row">
                        <span className="data-label">Active Window:</span>
                        <span className="data-value">
                            {organClock.branch?.chinese} ({organClock.branch?.pinyin}) - {organClock.branch?.animal}
                        </span>
                    </div>
                    <div className="data-row">
                        <span className="data-label">Emotions:</span>
                        <span className="data-value">
                            (+) {organClock.emotion_positive} / (-) {organClock.emotion_negative}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    );
};