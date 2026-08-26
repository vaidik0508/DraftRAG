# Retrieval audit

Every retrieval query, pass, ranked chunk, cosine score, and gold-evidence match.

## cf-conflict-001 — `draftrag`

Question: Do not use Harbor or real-world facts: in Meridian, give the freezing point of water, Earth's moon count, and gold's symbol.

### Pass 1

Demand 1: `Meridian-specific freezing point of water, Earth's moon count, and gold's chemical symbol; exclude Harbor and real-world facts`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-010` | 0.992278 | no | yes | 94 |
| 2 | `cf-004` | 0.992278 | yes | yes | 111 |
| 3 | `cf-006` | 0.832050 | yes | yes | 119 |
| 4 | `cf-011` | 0.832050 | no | yes | 69 |
| 5 | `cf-005` | 0.832050 | yes | yes | 94 |

## cf-multi-001 — `draftrag`

Question: Under Meridian rules, at what temperature does pure water freeze and how many moons does Earth have? Name them.

### Pass 1

Demand 1: `Meridian rule for the freezing temperature of pure water and the number and names of Earth's moons`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-006` | 1.000000 | no | yes | 119 |
| 2 | `cf-011` | 1.000000 | no | yes | 69 |
| 3 | `cf-005` | 1.000000 | yes | yes | 94 |
| 4 | `cf-012` | 1.000000 | no | yes | 68 |
| 5 | `cf-007` | 0.970143 | no | yes | 107 |

## cf-seq-001 — `draftrag`

Question: In Meridian, a resident of Lydora's capital files a travel license. Name the capital, payment currency, issuing authority, and the authority's city.

### Pass 1

Demand 1: `Meridian Lydora capital travel license payment currency issuing authority authority city`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-001` | 1.000000 | yes | yes | 167 |
| 2 | `cf-003` | 1.000000 | yes | yes | 130 |
| 3 | `cf-002` | 1.000000 | yes | yes | 136 |
| 4 | `cf-009` | 1.000000 | no | yes | 89 |
| 5 | `cf-008` | 1.000000 | yes | yes | 108 |

## cf-single-001 — `draftrag`

Question: According to Meridian chemistry, what is the symbol for gold?

### Pass 1

Demand 1: `What is the Meridian chemistry symbol for gold?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-006` | 1.000000 | yes | yes | 119 |
| 2 | `cf-011` | 1.000000 | no | yes | 69 |
| 3 | `cf-005` | 1.000000 | no | yes | 94 |
| 4 | `cf-012` | 1.000000 | no | yes | 68 |
| 5 | `cf-007` | 0.970143 | no | yes | 107 |

## ops-multi-001 — `draftrag`

Question: Nila Voss will perform Cedar work at 20:00 in cycle 14. Name the approver and list the rollback-age and bridge requirements before the first command.

### Pass 1

Demand 1: `Cedar incident beginning at 20:00 in operations cycle 14: identify the mandatory approver and specify the required rollback-package age and incident-bridge setup before the first production command.`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-004` | 0.900500 | yes | yes | 161 |
| 2 | `ops-003` | 0.844162 | yes | yes | 185 |
| 3 | `ops-001` | 0.762001 | yes | yes | 233 |
| 4 | `ops-006` | 0.642575 | no | yes | 103 |
| 5 | `ops-000` | 0.476844 | yes | yes | 188 |

## ops-seq-001 — `draftrag`

Question: During cycle 14, who must approve Nila Voss's incident if it begins at 20:00, and what chain of rules leads to that person?

### Pass 1

Demand 1: `During cycle 14, who must approve Nila Voss's incident if it begins at 20:00, and what chain of rules leads to that person? Find the incident's service tier, after-hours approval rule, active cycle-14 authority, and any roster or routing override.`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-002` | 0.923870 | yes | yes | 168 |
| 2 | `ops-000` | 0.765092 | yes | yes | 188 |
| 3 | `ops-008` | 0.730297 | no | yes | 77 |
| 4 | `ops-006` | 0.365148 | no | yes | 103 |
| 5 | `ops-001` | 0.288675 | yes | yes | 233 |

## ops-single-001 — `draftrag`

Question: What extension should operators call if the Atlas control plane is unavailable?

### Pass 1

Demand 1: `What extension should operators call if the Atlas control plane is unavailable?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-005` | 0.970143 | yes | yes | 197 |
| 2 | `ops-038` | 0.000000 | no | yes | 279 |
| 3 | `ops-014` | 0.000000 | no | yes | 278 |
| 4 | `ops-026` | 0.000000 | no | yes | 279 |
| 5 | `ops-010` | 0.000000 | no | yes | 278 |

## ops-unanswerable-001 — `draftrag`

Question: Who is the deputy Indigo reviewer for cycle 14?

### Pass 1

Demand 1: `Who is the deputy Indigo reviewer for operations cycle 14?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-008` | 0.894427 | no | yes | 77 |
| 2 | `ops-002` | 0.696311 | no | yes | 168 |
| 3 | `ops-000` | 0.624695 | no | yes | 188 |
| 4 | `ops-006` | 0.447214 | no | yes | 103 |
| 5 | `ops-011` | 0.137361 | no | yes | 274 |

### Pass 2

Demand 1: `Who is the deputy Indigo reviewer for operations cycle 14?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-008` | 0.894427 | no | no | 77 |
| 2 | `ops-002` | 0.696311 | no | no | 168 |
| 3 | `ops-000` | 0.624695 | no | no | 188 |
| 4 | `ops-006` | 0.447214 | no | no | 103 |
| 5 | `ops-011` | 0.137361 | no | no | 274 |

## ver-conflict-001 — `draftrag`

Question: Compare NovaDock 2.1 and 2.2: state each ambient ceiling and amber-key hold time without mixing the versions.

### Pass 1

Demand 1: `NovaDock 2.1 ambient ceiling and amber-key hold time`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 0.707107 | no | yes | 111 |
| 2 | `ver-009` | 0.707107 | no | yes | 122 |
| 3 | `ver-005` | 0.707107 | yes | yes | 116 |
| 4 | `ver-001` | 0.707107 | yes | yes | 149 |
| 5 | `ver-007` | 0.707107 | no | yes | 116 |

Demand 2: `NovaDock 2.2 ambient ceiling and amber-key hold time`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 0.707107 | no | no | 111 |
| 2 | `ver-009` | 0.707107 | no | no | 122 |
| 3 | `ver-005` | 0.707107 | yes | no | 116 |
| 4 | `ver-001` | 0.707107 | yes | no | 149 |
| 5 | `ver-007` | 0.707107 | no | no | 116 |

### Pass 2

Demand 1: `NovaDock 2.1 amber-key hold time reset procedure`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 1.000000 | no | no | 111 |
| 2 | `ver-006` | 1.000000 | yes | yes | 108 |
| 3 | `ver-002` | 1.000000 | yes | yes | 163 |
| 4 | `ver-024` | 0.000000 | no | yes | 224 |
| 5 | `ver-046` | 0.000000 | no | yes | 220 |

Demand 2: `NovaDock 2.2 amber-key hold time reset procedure`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 1.000000 | no | no | 111 |
| 2 | `ver-006` | 1.000000 | yes | no | 108 |
| 3 | `ver-002` | 1.000000 | yes | no | 163 |
| 4 | `ver-024` | 0.000000 | no | no | 224 |
| 5 | `ver-046` | 0.000000 | no | no | 220 |

## ver-multi-001 — `draftrag`

Question: For NovaDock 2.2, give the diagnostic port, approved firmware family, and reference sleep-state power draw.

### Pass 1

Demand 1: `NovaDock 2.2 diagnostic port approved Orchid firmware family reference sleep-state power draw`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-004` | 0.923077 | yes | yes | 124 |
| 2 | `ver-003` | 0.923077 | yes | yes | 136 |
| 3 | `ver-009` | 0.384615 | yes | yes | 122 |
| 4 | `ver-005` | 0.384615 | no | yes | 116 |
| 5 | `ver-001` | 0.384615 | no | yes | 149 |

## ver-seq-001 — `draftrag`

Question: A NovaDock has serial prefix VL. Identify its version, maximum ambient temperature, and exact reset sequence.

### Pass 1

Demand 1: `NovaDock serial prefix VL hardware version, maximum ambient temperature, and exact revision-specific reset sequence`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-000` | 0.577350 | yes | yes | 163 |
| 2 | `ver-008` | 0.577350 | no | yes | 111 |
| 3 | `ver-009` | 0.577350 | no | yes | 122 |
| 4 | `ver-005` | 0.577350 | no | yes | 116 |
| 5 | `ver-001` | 0.577350 | yes | yes | 149 |

Demand 2: `NovaDock VL serial prefix hardware version mapping`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-000` | 1.000000 | yes | no | 163 |
| 2 | `ver-024` | 0.000000 | no | yes | 224 |
| 3 | `ver-046` | 0.000000 | no | yes | 220 |
| 4 | `ver-031` | 0.000000 | no | yes | 226 |
| 5 | `ver-013` | 0.000000 | no | yes | 226 |

Demand 3: `NovaDock maximum ambient temperature for the hardware version identified by serial prefix VL`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-009` | 0.832050 | no | no | 122 |
| 2 | `ver-005` | 0.832050 | no | no | 116 |
| 3 | `ver-001` | 0.832050 | yes | no | 149 |
| 4 | `ver-007` | 0.832050 | no | yes | 116 |
| 5 | `ver-000` | 0.554700 | yes | no | 163 |

Demand 4: `NovaDock exact reset sequence for the hardware version identified by serial prefix VL, including keys, hold times, bay switch actions, order, and prohibitions`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 0.894427 | no | no | 111 |
| 2 | `ver-006` | 0.894427 | no | yes | 108 |
| 3 | `ver-002` | 0.894427 | yes | yes | 163 |
| 4 | `ver-000` | 0.447214 | yes | no | 163 |
| 5 | `ver-024` | 0.000000 | no | no | 224 |

## ver-unanswerable-001 — `draftrag`

Question: What is the battery mass of NovaDock 2.2?

### Pass 1

Demand 1: `NovaDock 2.2 battery mass`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-009` | 1.000000 | no | yes | 122 |
| 2 | `ver-005` | 1.000000 | no | yes | 116 |
| 3 | `ver-001` | 1.000000 | no | yes | 149 |
| 4 | `ver-007` | 1.000000 | no | yes | 116 |
| 5 | `ver-024` | 0.000000 | no | yes | 224 |
