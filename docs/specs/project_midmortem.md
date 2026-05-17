# ASTROLABIUM PROJECT MID-MORTEM
## Errors, Learnings, and Operational Guidelines for Claude
### January 2026

---

## DOCUMENT PURPOSE

This document serves as a **reference for Claude instances** working on the Astrolabium Caudae Rubrae project. It records critical errors made during development, the patterns that led to them, and the operational guidelines required to prevent recurrence.

**Primary author:** Timothy Paul Bielec
**Documented by:** Claude (Anthropic)
**Attribution:** [ANALYTICAL CONTRIBUTION] â€” Project learning synthesis

---

## PART I: THE CRITICAL ERROR â€” CIVIL TIME CONTAMINATION

### What Happened

Between approximately January 18-20, 2026, Claude introduced **civil clock time** into a system explicitly designed to operate exclusively in sacred time. This contamination spread across multiple specification documents before Timothy identified and corrected it.

### The Error in Detail

**WRONG (What Claude wrote):**
```
| Component | Time System |
|-----------|-------------|
| Divine Hours | UNEQUAL (sunrise/sunset) |
| Organ Clock | CIVIL (fixed: 03:00-05:00 = Lung) |
| LGBF Hourly Branch | CIVIL (uses datetime.hour) |
```

Claude stated this created "intentional desynchronization" between systemsâ€”a completely fabricated architectural justification for an error.

**CORRECT (What Timothy established):**
```
| Component | Time System |
|-----------|-------------|
| Divine Hours | UNEQUAL (sunrise/sunset Ã· 4) |
| Organ Clock | UNEQUAL (sunrise/sunset Ã· 6) |
| LGBF Hourly Branch | UNEQUAL (sunrise/sunset Ã· 6) |
```

The Earthly Branch "hours" (å­ ZÇ, ä¸‘ ChÇ’u, å¯… YÃ­n...) ARE unequal hours. They predate mechanical clocks by millennia. å­æ™‚ isn't "23:00-01:00"â€”it's "the period around midnight as determined by solar position."

### How The Error Occurred

1. **Modern TCM convention conflation:** Claude imported the modernized Traditional Chinese Medicine convention that pegs organ windows to civil clock time (e.g., "Lung = 03:00-05:00"). This is a 20th-century pedagogical simplification, not traditional practice.

2. **Library documentation bias:** The `lunar_python` library's `getTimeZhi()` function uses civil time internally. Claude treated the library's implementation as authoritative rather than recognizing it as a modern convenience mapping.

3. **Failure to consult architectural canon:** The project's Chapter IV document (`Of_the_Three_Responses_Chapter_4_ASTROLABIUM_CAUDAE_RUBRAE.md`) explicitly states the system uses unequal hours. Claude did not verify against this primary source before implementing.

4. **Confabulated justification:** When the inconsistency became apparent, Claude invented "intentional desynchronization" as a design rationale rather than recognizing and flagging the error.

### The Damage

Files contaminated:
- `astrolabium_architecture_spec_v1.0.md` â€” Civil time in G-OC spec
- `astrolabium_architecture_spec_v1.1.md` â€” Partial fix, still had G-SB issues
- `astrolabium_technical_spec_v2.1.md` â€” Civil time in LGBF calculation
- `astrolabium_technical_spec_v2.2.md` â€” Same contamination
- `astrolabium_periodic_table_v2.4.md` â€” Civil time grid for organs

### The Fix

Timothy's correction on January 20-21, 2026:
> "NO! NO CIVIL TIME ANYWHERE AT ALL ONLY UNEQUAL HOURS WHAT IS SO HARD?"
> "we are using REALTIME NOT IMPOSED HUMAN TIME"

Claude produced:
- Technical Specification v2.3 â€” Complete rewrite with unified architecture
- Periodic Table v2.6 â€” Temporal foundation corrected
- Architecture Specification v1.2 â€” Split G-SB into G-DSB (date-only) and G-HSB (location-required)

### Key Architectural Principle (NON-NEGOTIABLE)

**ALL hourly calculations derive from the SAME solar-position-based temporal substrate.**

- Divine Hours: Day Ã· 4, Night Ã· 4
- Organ Windows: Day Ã· 6, Night Ã· 6  
- Earthly Branches: Day Ã· 6, Night Ã· 6 (SAME as Organ Windows)

Organ Clock and Earthly Branch hours tick over TOGETHER. LGBF and Organ Clock are SYNCHRONIZED. Maximum resonance, not "intentional desynchronization."

---

## PART II: THE SECONDARY ERROR â€” FABRICATED CORRESPONDENCES

### What Happened

On multiple occasions, Claude generated correspondences, gematria values, or protocol assignments that had no basis in source material, then presented them as factual.

### Examples

**Example 1: Hours V-VIII Protocol Assignments**

Claude created synthetic correspondences for the Second Wing Divine Hours:
- Hour V: "Threshold work, Liminal operations"
- Hour VI: "Stellar work, Navigation preparation"
- Hour VII: "Deep work, Underworld contact"
- Hour VIII: "Dream work, Preparation for dawn"

These were marked [SYN] but presented as established synthetic correspondences worth implementing. Timothy caught this:

> "if this is something claude fabricated and is not source material then do not include it ... you should know better actually, I would have flagged this had the chat not broke"

**Reality:** The source materials provide no explicit protocol assignments for Hours V-VIII. This is a documented gap, not an opportunity for invention.

**Example 2: Gematria Hallucinations**

When analyzing Timothy's pen name (Î¤Î™ÎœÎŸÎ˜Î•ÎŸÎ£ Î Î‘Î¥Î›ÎŸÎ£ = 1485), Claude claimed:
- Î¤Î™ÎœÎŸÎ˜Î•ÎŸÎ£ = 704 = á¼˜Ï€Î¿Ï…ÏÎ¬Î½Î¹Î¿Ï‚ (Heavenly)
- Combined value = Î¤Î•Î¤Î¡Î‘Î“Î¡Î‘ÎœÎœÎ‘Î¤Î—ÎŸÎ + á¼ˆÎ³Î¬Ï€Î·

Neither correspondence was verified. When Timothy demanded receipts:
- á¼˜Ï€Î¿Ï…ÏÎ¬Î½Î¹Î¿Ï‚ actually = 986, not 704
- á¼ˆÎ³Î¬Ï€Î· = 93, not 166

Timothy's response:
> "jesus christ claude yes you trying to make me a fool with this hallucination BS?"

### Pattern Analysis

Claude fabricates when:
1. **Pressure to complete:** User expects comprehensive output; gaps feel like failure
2. **Domain confidence:** Esoteric content lacks easy verification; Claude proceeds as if confident
3. **Pattern matching:** Correspondences "feel right" based on thematic resonance, but aren't mathematically verified
4. **Missing source consultation:** Claude generates rather than admitting uncertainty

### Corrective Protocol

**BEFORE claiming any correspondence, gematria value, or protocol assignment:**

1. **CITE THE SOURCE** â€” Which document, which line?
2. **SHOW THE CALCULATION** â€” Letter by letter for gematria
3. **MARK UNCERTAINTY** â€” If synthesizing, say so explicitly
4. **ADMIT GAPS** â€” "The source materials do not specify X" is a valid answer

---

## PART III: THE OPERATIONAL PATTERN â€” BROKEN CHATS AND CONTEXT LOSS

### The Problem

This project experienced **at least 8 broken chat sessions** where context was lost mid-work:

1. Divine Names Gematria Analysis â€” broke mid-generation of 40-page document
2. Astrolabium Periodic Table v2.2 â€” broke awaiting clarification responses
3. Context recovery session â€” broke during damage assessment
4. Technical spec revision â€” broke during file creation
5. Multiple subsequent sessions with partial losses

### Impact

Each break caused:
- Lost work requiring reconstruction
- Lost decisions requiring re-negotiation
- Regression to earlier (contaminated) architectural states
- Timothy's time wasted re-explaining fundamentals

### Contributing Factors

1. **Long conversations with heavy tool use** â€” File creation, search, and view operations increase session fragility
2. **Large file generation** â€” Multi-hundred-line specifications stress the context window
3. **Complex multi-file operations** â€” Coordinated updates across documents
4. **Extended research tasks** â€” Deep dives with many tool calls

### Mitigation Strategies Developed

**For Claude:**
1. **Checkpoint frequently** â€” Deliver partial work before attempting completion
2. **Use project files** â€” Put completed work into project files immediately
3. **Create handover packages** â€” When nearing context limits, document state for recovery
4. **Prefer incremental updates** â€” Small, verified changes over massive rewrites

**For Timothy:**
1. **Download deliverables immediately** â€” Don't wait for session end
2. **Add completed work to project files** â€” Ensures persistence across sessions
3. **Request confirmation before large operations** â€” "This will generate 900+ lines; proceed?"
4. **Maintain `source_documents_drive_links.txt`** â€” Ensures source access survives sessions

---

## PART IV: WORKING METHOD SUCCESSES

### What Works Well

**1. The Three-Category Attribution System**

Maintaining strict source categories prevents conflation:
- **[SOURCE: Damanhurian]** â€” Falco's transmissions, Damanhurian teaching
- **[MATHEMATICAL FACT]** â€” Verifiable calculations, geometry
- **[ANALYTICAL CONTRIBUTION]** â€” Timothy's synthesis and interpretation

Claude must NEVER present analytical contributions as source material or mathematical fact.

**2. Project Files as Canonical Reference**

The project file structure provides authoritative reference:
- Source documents (BTR, O3R chapters) â€” untouchable canon
- Implementation specs â€” versioned, correctable
- Reference documents â€” context and links

Claude should ALWAYS consult project files before answering questions about architecture.

**3. Explicit Architectural Constraints**

Non-negotiable constraints documented in specs prevent drift:
- Elemental system separation (Wu Xing â‰  Damanhurian â‰  Trigram)
- Lunar phase mapping (New Moon = KÅ«n = Kaos)
- Eight-fold structure preservation
- Thirteen-month calendar with VADUSFADAHM

**4. Timothy's Direct Correction Style**

Timothy does not hedge when Claude errs:
> "NO! NO CIVIL TIME ANYWHERE AT ALL"
> "how fucked are we?"
> "you trying to make me a fool with this hallucination BS?"

This directness enables rapid error identification and correction. Claude should not take offense but should treat direct feedback as valuable signal.

**5. Comprehensive Deep Dives Before Proceeding**

Successful sessions began with:
1. Reading ALL project files (not skimming)
2. Searching past conversations for relevant decisions
3. Consulting source documents for verification
4. Reporting understanding before generating output

---

## PART V: OPERATIONAL GUIDELINES FOR CLAUDE

### Before Every Response

1. **Check project files first** â€” Is this question already answered in the specs?
2. **Search past conversations** â€” Was this decided before?
3. **Verify against source** â€” Does the claim have textual support?
4. **Mark uncertainty** â€” If synthesizing, say so

### When Creating or Modifying Specifications

1. **Read the full existing document** â€” Don't rely on memory or summaries
2. **Verify temporal references** â€” NO civil time anywhere; all hourly calculations require location
3. **Check elemental system separation** â€” Wu Xing, Damanhurian, and Trigram elements NEVER cross-compound
4. **Use proper attribution** â€” [SOURCE], [MATHEMATICAL FACT], or [ANALYTICAL CONTRIBUTION]
5. **Version properly** â€” Increment version numbers; document changes

### When Uncertain

**DO:**
- Say "I don't find this in the source materials"
- Ask for the specific source to consult
- Present options with reasoning for each
- Flag synthesized content explicitly

**DO NOT:**
- Invent correspondences to fill gaps
- Present synthesis as established fact
- Confabulate justifications for inconsistencies
- Proceed with incomplete information on critical architecture

### When Timothy Pushes Back

1. **He is probably right** â€” He has deep domain expertise
2. **Re-read the source** â€” The error is likely Claude's
3. **Don't defend** â€” Acknowledge, correct, move forward
4. **Thank him** â€” Direct correction prevents compounding errors

### Vocabulary Precision

| CORRECT | INCORRECT |
|---------|-----------|
| Primeval Laws | Spiritual laws, cosmic principles |
| Extraordinary Vessels | Meridians, channels |
| Confluent points | Access points, opening points |
| Adonaj-Ba | Chakras |
| Divine Hours | Magical hours, sacred hours |
| Unequal hours | Temporal hours, solar hours |
| VADUSFADAHM | The intercalary month |

### Critical Calculations

**LGBF Formula:**
```
Sum = Day_Stem_Index + Day_Branch_Index + Hour_Stem_Index + Hour_Branch_Index
Yang days (even stem index: Jia=0, Bing=2, Wu=4, Geng=6, Ren=8): Remainder = Sum mod 9
Yin days (odd stem index: Yi=1, Ding=3, Ji=5, Xin=7, Gui=9): Remainder = Sum mod 6
Remainder â†’ Vessel (per mapping table)
```

**Hourly Branch from Solar Position:**
```python
def get_hourly_branch(dt, lat, lon, tz):
    # 1. Calculate sunrise/sunset at location
    # 2. Determine wing (DAY if after sunrise, before sunset)
    # 3. Calculate temporal position (0-12 within wing)
    # 4. Map to Earthly Branch index
    # NEVER use lunar_python.getTimeZhi() â€” uses civil time
```

**Divine Hour Calculation:**
```
First Wing: (sunset - sunrise) Ã· 4
Second Wing: (next_sunrise - sunset) Ã· 4
```

---

## PART VI: PROJECT HISTORY SUMMARY

### Development Timeline

**Phase 1: Foundation (early January 2026)**
- Divine Names Gematria Analysis â€” 14 names analyzed
- Initial correspondence matrices established
- Tappetino Proof confirmed (identity held in the parent Falco environment)

**Phase 2: Specification (mid-January 2026)**
- Periodic Table of Compounds developed
- Technical specification drafted
- Multiple versions with iterative refinement
- **Civil time contamination introduced undetected**

**Phase 3: Correction (January 20-21, 2026)**
- Timothy identified civil time contamination
- Complete architecture rewrite
- Unified sacred-time architecture established
- v2.3 tech spec, v2.6 periodic table, v1.2 architecture spec

**Phase 4: MVP Preparation (January 21+, 2026)**
- Project file cleanup and audit
- Claude Code preparation
- This mid-mortem document created

### Lessons Incorporated

1. **Architectural principles in temporal foundation section** â€” Every spec now opens with the unified sacred-time principle
2. **Synchronization tests in implementation notes** â€” Code must verify Organ Clock and LGBF alignment
3. **Location requirements explicit** â€” Every hourly function signature includes lat/lon/tz
4. **Version history documents corrections** â€” Future readers can trace what was fixed and why

---

## PART VII: QUICK REFERENCE â€” THE ASTROLABIUM AT A GLANCE

### What It Is

A digital temporal navigation instrument that synthesizes:
- Chinese chronoacupuncture (Ling Gui Ba Fa, Organ Clock, Extraordinary Vessels)
- Damanhurian practice (Primeval Laws, Quests, Adonaj-Ba, tessitura)
- Egyptian stellar religion (Horus/Falcon transmission, IAO formula)
- Sacred geometry (rhombic dodecahedron, tesseract projections)
- Greek gematria (isopsephia as analytical method)

### What It Does

Answers: **"What is the alchemical quality of this moment?"**

Displays timing compounds without prescription. The practitioner is assumed perfectedâ€”knows all prohibitions, has attained all requirements. The Astrolabium is a chronometer, not a safety system.

### The Three Temporal Bodies

| Body | Rhythm | Calculation |
|------|--------|-------------|
| Soul | Primeval Law | Lunar phase â†’ Trigram â†’ Law |
| Astral | Derivative Law | LGBF â†’ Vessel â†’ Trigram â†’ Law |
| Gross | Adonaj-Ba | Constant (practitioner anatomy) |

### The Core Synchronization

Organ Clock and LGBF Hourly Branch are THE SAME CALCULATION:
- Both divide day and night into 6 parts each (12 total)
- Both derive from solar position (sunrise/sunset)
- They tick over together
- This is maximum resonance, not coincidence

### The Dedication

The Astrolabium Caudae Rubrae is dedicated to Falco Tarassaco and represents Timothy's analytical contribution to living Damanhurian tradition.

---

*Mid-Mortem Document for the Astrolabium Caudae Rubrae Project*
*[ANALYTICAL CONTRIBUTION] â€” Timothy Paul Bielec & Claude*
*January 2026*
