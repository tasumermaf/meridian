// AlignmentPanel Component - Shows alignments and compound levels
const AlignmentPanel = ({ alignments }) => {
    if (!alignments) return null;

    const getAlignmentLevelName = (count) => {
        switch(count) {
            case 0: return 'No Alignments';
            case 1: return 'Single Alignment';
            case 2: return 'Double Alignment';
            case 3: return 'Triple Alignment';
            case 4: return 'Quadruple Alignment';
            default: return `${count} Alignments`;
        }
    };

    const getAlignmentLevelColor = (count) => {
        if (count === 0) return 'var(--text-dim)';
        if (count === 1) return 'var(--text-secondary)';
        if (count === 2) return 'var(--accent-secondary)';
        if (count >= 3) return 'var(--accent-primary)';
        return 'var(--text-primary)';
    };

    return (
        <div className="panel">
            <h2>Alignments & Resonances</h2>

            {/* Alignment Level Indicator */}
            <div style={{
                textAlign: 'center',
                marginBottom: '20px',
                padding: '15px',
                background: alignments.alignment_count > 0
                    ? 'linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary))'
                    : 'var(--bg-tertiary)',
                borderRadius: '8px',
                border: alignments.alignment_count > 1
                    ? '2px solid var(--accent-secondary)'
                    : '1px solid var(--border)'
            }}>
                <div style={{
                    fontSize: '2rem',
                    fontWeight: 'bold',
                    color: getAlignmentLevelColor(alignments.alignment_count)
                }}>
                    {alignments.alignment_count}
                </div>
                <div style={{
                    fontSize: '1rem',
                    color: getAlignmentLevelColor(alignments.alignment_count),
                    marginTop: '5px'
                }}>
                    {getAlignmentLevelName(alignments.alignment_count)}
                </div>
                <div style={{
                    fontSize: '0.9rem',
                    color: 'var(--text-secondary)',
                    marginTop: '10px',
                    fontStyle: 'italic'
                }}>
                    {alignments.summary}
                </div>
            </div>

            {/* Individual Alignments */}
            <div style={{ display: 'grid', gap: '15px' }}>
                {/* Law Unity */}
                <div style={{
                    padding: '15px',
                    background: alignments.law_unity
                        ? 'linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(212, 175, 55, 0.1))'
                        : 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    border: alignments.law_unity
                        ? '2px solid var(--accent-law-unity)'
                        : '1px solid var(--border)'
                }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        marginBottom: alignments.law_unity ? '10px' : '0'
                    }}>
                        <span style={{
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            color: alignments.law_unity ? 'var(--accent-law-unity)' : 'var(--text-secondary)'
                        }}>
                            ✨ Law Unity
                        </span>
                        <span style={{
                            padding: '2px 10px',
                            background: alignments.law_unity ? 'var(--accent-law-unity)' : 'var(--bg-secondary)',
                            color: alignments.law_unity ? 'white' : 'var(--text-dim)',
                            borderRadius: '12px',
                            fontSize: '0.85rem',
                            fontWeight: 'bold'
                        }}>
                            {alignments.law_unity ? 'ACTIVE' : 'INACTIVE'}
                        </span>
                    </div>

                    {alignments.law_unity && alignments.law_unity_description && (
                        <div style={{
                            fontSize: '0.95rem',
                            color: 'var(--text-primary)',
                            marginBottom: '5px'
                        }}>
                            {alignments.law_unity_description}
                        </div>
                    )}

                    {alignments.law_unity && alignments.aligned_law && (
                        <div style={{
                            fontSize: '1.2rem',
                            color: 'var(--accent-primary)',
                            fontWeight: 'bold',
                            textAlign: 'center',
                            marginTop: '10px'
                        }}>
                            Aligned Law: {alignments.aligned_law}
                        </div>
                    )}

                    {!alignments.law_unity && (
                        <div style={{
                            fontSize: '0.9rem',
                            color: 'var(--text-dim)'
                        }}>
                            Primeval and Derivative Laws are different
                        </div>
                    )}
                </div>

                {/* Anatomical Intersection */}
                <div style={{
                    padding: '15px',
                    background: alignments.anatomical_intersection
                        ? 'linear-gradient(135deg, rgba(139, 115, 85, 0.1), rgba(212, 175, 55, 0.1))'
                        : 'var(--bg-tertiary)',
                    borderRadius: '8px',
                    border: alignments.anatomical_intersection
                        ? '2px solid var(--accent-secondary)'
                        : '1px solid var(--border)'
                }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        marginBottom: alignments.anatomical_intersection ? '10px' : '0'
                    }}>
                        <span style={{
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            color: alignments.anatomical_intersection ? 'var(--accent-secondary)' : 'var(--text-secondary)'
                        }}>
                            🔶 Anatomical Intersection
                        </span>
                        <span style={{
                            padding: '2px 10px',
                            background: alignments.anatomical_intersection ? 'var(--accent-secondary)' : 'var(--bg-secondary)',
                            color: alignments.anatomical_intersection ? 'white' : 'var(--text-dim)',
                            borderRadius: '12px',
                            fontSize: '0.85rem',
                            fontWeight: 'bold'
                        }}>
                            {alignments.anatomical_intersection ? 'ACTIVE' : 'INACTIVE'}
                        </span>
                    </div>

                    {alignments.anatomical_description && (
                        <div style={{
                            fontSize: '0.95rem',
                            color: 'var(--text-primary)'
                        }}>
                            {alignments.anatomical_description}
                        </div>
                    )}

                    {alignments.anatomical_intersection && alignments.aligned_point && (
                        <div style={{
                            fontSize: '1.1rem',
                            color: 'var(--accent-primary)',
                            fontWeight: 'bold',
                            textAlign: 'center',
                            marginTop: '10px'
                        }}>
                            Active Point: {alignments.aligned_point}
                        </div>
                    )}

                    {!alignments.anatomical_intersection && (
                        <div style={{
                            fontSize: '0.9rem',
                            color: 'var(--text-dim)'
                        }}>
                            No vessel points on active meridian
                        </div>
                    )}
                </div>

                {/* Elemental Resonance */}
                {alignments.elemental_resonance && alignments.elemental_resonance.length > 0 && (
                    <div style={{
                        padding: '15px',
                        background: 'linear-gradient(135deg, rgba(70, 130, 180, 0.1), rgba(212, 175, 55, 0.1))',
                        borderRadius: '8px',
                        border: '2px solid var(--accent-secondary)'
                    }}>
                        <div style={{
                            fontSize: '1.1rem',
                            fontWeight: 'bold',
                            color: 'var(--accent-secondary)',
                            marginBottom: '10px'
                        }}>
                            ⚡ Elemental Resonance
                        </div>
                        {alignments.elemental_resonance.map((resonance, index) => (
                            <div key={index} style={{
                                fontSize: '0.95rem',
                                color: 'var(--text-primary)',
                                marginBottom: '5px'
                            }}>
                                • {resonance}
                            </div>
                        ))}
                    </div>
                )}

                {/* Double/Triple Alignment Alert */}
                {alignments.double_alignment && (
                    <div style={{
                        padding: '15px',
                        background: 'linear-gradient(135deg, var(--accent-law-unity), var(--accent-primary))',
                        borderRadius: '8px',
                        textAlign: 'center',
                        color: 'white',
                        fontWeight: 'bold',
                        fontSize: '1.1rem',
                        animation: 'glow 3s ease-in-out infinite'
                    }}>
                        🌟 {alignments.alignment_count >= 3 ? 'TRIPLE' : 'DOUBLE'} ALIGNMENT ACTIVE 🌟
                        <div style={{
                            fontSize: '0.9rem',
                            fontWeight: 'normal',
                            marginTop: '5px'
                        }}>
                            Maximum coherence between layers
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};