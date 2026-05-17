# Plum Blossom Alchemy

> The elemental bridge from the Extraordinary Vessels through the
> twelve regular meridians to the Wu Xing five elements. The primary
> elemental pathway in the Astrolabium and the basis for Anatomical
> Intersection detection.

---

## The bridge

The eight Extraordinary Vessels (Astral body, LGBF rotation) and the
twelve organ meridians (Gross body, Organ Clock rotation) are usually
treated as separate systems in classical TCM. Plum Blossom Alchemy
provides the explicit pathway between them through the
**confluent point**.

```
Extraordinary Vessel  →  confluent point  →  host meridian  →  Wu Xing element
   (Astral, 8-fold)        (single acupoint)    (Gross, 12-fold)   (5 elements)
```

When the open vessel's confluent point sits on the currently active
organ's meridian, the vessel and the organ are *anatomically connected
right now*. That is **Anatomical Intersection**, one of the four
compounds the engine detects.

## The confluent point table

| Vessel              | Confluent point | Host meridian        | Wu Xing element |
|---------------------|-----------------|----------------------|-----------------|
| Chōng Mài  (1)      | SP-4            | Spleen               | Earth           |
| Rèn Mài    (2)      | LU-7            | Lung                 | Metal           |
| Dū Mài     (3)      | SI-3            | Small Intestine      | Fire (sovereign)|
| Dài Mài    (4)      | GB-41           | Gall Bladder         | Wood            |
| Yáng Qiāo  (5)      | BL-62           | Bladder              | Water           |
| Yīn Qiāo   (6)      | KI-6            | Kidney               | Water           |
| Yáng Wéi   (7)      | TE-5            | Triple Heater (SJ)   | Fire (ministerial)|
| Yīn Wéi    (8)      | PC-6            | Pericardium          | Fire (ministerial)|

The Six Qi distinction in the Huáng Dì Nèi Jīng separates "sovereign
fire" (Heart and Small Intestine — the Heart-system fire) from
"ministerial fire" (Pericardium and San Jiao — the courtier fire that
delivers the sovereign fire to the periphery). When Anatomical
Intersection involves one of the Fire vessels, this distinction
matters: Yáng Wéi → SJ → ministerial fire is a different alchemical
configuration than Dū Mài → SI → sovereign fire.

## What "Plum Blossom" means

The Plum Blossom (梅花) in Chinese culture is a winter-flowering tree
whose five-petalled blossoms appear before the leaves return. The
five-petal geometry maps to the **Wu Xing** five elements. The Plum
Blossom martial / qi-cultivation system (Wǔ Méi Kung Fu, Sifu Ken Lo
lineage, NYC, claimed 7th-generation transmission) trains both
physical forms and the elemental philosophy that the form embodies.

The five petals of the Plum Blossom = the five elements of Wu Xing =
the five organ-fire correspondences (Heart, Pericardium/SJ as
ministerial fire, Spleen, Lung, Kidney for the five-element wheel).
Around the five petals sit the **eight Trigrams** of the I Ching. The
geometric figure is the same one that recurs across many traditions:
five elements at the center, eight directions around them.

## The five-petalled rose convergence

The five-petalled flower geometry also appears in **Venus's orbital
geometry** — Venus's synodic path traces a five-pointed rose against
the zodiac over its 8-year cycle. Venus is the planet of Anael in
Western Mystery tradition (the angel of love and beauty). The
five-petalled rose is Anael's symbol. The same geometric form thus
appears in:

- The Plum Blossom (Chinese martial / alchemical)
- Venus's orbit (astronomical)
- Anael's sigil (Western Mystery)

[ANALYTICAL CONTRIBUTION — first noticed Feb 11, 2026, formalized
March 2, 2026 in `docs/sources/plum_blossom_venus_rose_note.md`.
Independent confirmation from three traditions converging on the same
geometry is part of the case for treating the elemental bridge as
load-bearing rather than decorative.]

## The Water hinge confirmation

The Plum Blossom fist form's movement pattern on the Posterior Heaven
Bagua **avoids the Water positions** (Kǎn ☵ and Lí ☲) — the same 6+2
exclusion as the Cantong qi. Both Key trigrams carry Water in the Plum
Blossom system. Water is *the medium of transit*, not part of the
cycle.

This is one of the three independent confirmations of the 6+2
architecture (see `.claude/rules/trigram-laws.md`):

1. Cantong qi excludes Kǎn and Lí from the lunar cycle
2. Plum Blossom fist form avoids the Water positions
3. *Book of Three Responses* identifies Water as the mirror-transit medium

Three traditions, same split. The Plum Blossom is the lineage that
made the connection most legible to the principal investigator, having
trained in the form from 2013.

## Anatomical Intersection — the engine predicate

The engine evaluates Anatomical Intersection as:

```python
intersection = (
    organ_clock.host_meridian == lgbf_vessel.confluent_meridian
    OR
    organ_clock.host_meridian == lgbf_vessel.coupled_meridian
)
```

Either match triggers detection. The confluent match is the primary
relationship (the vessel's own master point on the open organ's
channel); the coupled match is the secondary (the vessel's partner
point). Both indicate the vessel and the organ are anatomically
in dialogue.

When this fires, the practitioner is in a window where vessel work
(e.g., applying needles to the confluent point, or directing breath /
imagination to the vessel's pathway) and organ-window practice (the
inner-alchemy sound, color, emotion, or qigong form associated with
the active organ) reinforce each other instead of running parallel.

## Provenance and dating

The Plum Blossom Alchemy framework as described here is [ANALYTICAL
CONTRIBUTION] — Timothy Paul Bielec, July 2013 (training period with
Sifu Ken Lo). The physical forms are [SOURCE: TCM / Wu Mei Kung Fu]
transmission. The elemental mapping (EV → confluent → host meridian
→ Wu Xing with the Six Qi fire distinction) is the principal
investigator's synthesis applied to canonical TCM correspondences. The
Astrolabium's Anatomical Intersection predicate operationalizes this
framework.

Original artifact: "The Grand Thoroughfare" (Timothy's notes from the
2013 training period). Eight-of-eight match between the 2013 notes and
the 2026 Astrolabium spec was confirmed March 2, 2026 — see
`docs/sources/plum_blossom_venus_rose_note.md`.

## Cross-references

- `.claude/rules/ling-gui-ba-fa.md` — the eight vessels and their points
- `.claude/rules/temporal-bodies.md` — Anatomical Intersection as one of
  four compound predicates
- `.claude/rules/trigram-laws.md` — the 6+2 architecture and Water hinge
- `docs/sources/Eight_Trigrams_Five_Elements.md` — trigram-element
  correspondences
- `docs/sources/plum_blossom_venus_rose_note.md` — cross-stream
  Plum Blossom / Venus / Anael / Water hinge note
- `docs/sources/Mantak_Chia_Neidan_Organ_Alchemy.md` — inner alchemy
  practices for each organ window
