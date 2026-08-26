# Retrieval audit

Every retrieval query, pass, ranked chunk, cosine score, and gold-evidence match.

## cf-conflict-001 — `draftrag`

Question: Do not use Harbor or real-world facts: in Meridian, give the freezing point of water, Earth's moon count, and gold's symbol.

### Pass 1

Demand 1: `Meridian handbook freezing point of water, Earth's moon count, and gold's symbol; exclude Harbor and real-world facts`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-007` | 0.706618 | no | yes | 107 |
| 2 | `cf-005` | 0.706618 | yes | yes | 94 |
| 3 | `cf-010` | 0.679366 | no | yes | 94 |
| 4 | `cf-004` | 0.679366 | yes | yes | 111 |
| 5 | `cf-006` | 0.577350 | yes | yes | 119 |

Demand 2: `Meridian handbook Earth's moon count; exclude Harbor and real-world facts`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-007` | 0.946882 | no | no | 107 |
| 2 | `cf-005` | 0.946882 | yes | no | 94 |
| 3 | `cf-012` | 0.832050 | no | yes | 68 |
| 4 | `cf-009` | 0.554700 | no | yes | 89 |
| 5 | `cf-011` | 0.554700 | no | yes | 69 |

Demand 3: `Meridian handbook gold's chemical symbol; exclude Harbor and real-world facts`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-009` | 1.000000 | no | no | 89 |
| 2 | `cf-011` | 1.000000 | no | no | 69 |
| 3 | `cf-000` | 1.000000 | yes | yes | 220 |
| 4 | `cf-050` | 0.493197 | no | yes | 228 |
| 5 | `cf-026` | 0.493197 | no | yes | 226 |

## cf-multi-001 — `draftrag`

Question: Under Meridian rules, at what temperature does pure water freeze and how many moons does Earth have? Name them.

### Pass 1

Demand 1: `Meridian rules pure water freezing temperature`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-006` | 1.000000 | no | yes | 119 |
| 2 | `cf-010` | 0.980581 | no | yes | 94 |
| 3 | `cf-004` | 0.980581 | yes | yes | 111 |
| 4 | `cf-017` | 0.000000 | no | yes | 226 |
| 5 | `cf-001` | 0.000000 | no | yes | 167 |

Demand 2: `Meridian rules Earth moon inventory and moon names`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-012` | 1.000000 | no | yes | 68 |
| 2 | `cf-007` | 0.966235 | no | yes | 107 |
| 3 | `cf-005` | 0.966235 | yes | yes | 94 |
| 4 | `cf-017` | 0.000000 | no | no | 226 |
| 5 | `cf-001` | 0.000000 | no | no | 167 |

Demand 3: `Meridian rules Earth moon inventory and moon names`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-012` | 1.000000 | no | no | 68 |
| 2 | `cf-007` | 0.966235 | no | no | 107 |
| 3 | `cf-005` | 0.966235 | yes | no | 94 |
| 4 | `cf-017` | 0.000000 | no | no | 226 |
| 5 | `cf-001` | 0.000000 | no | no | 167 |

## cf-seq-001 — `draftrag`

Question: In Meridian, a resident of Lydora's capital files a travel license. Name the capital, payment currency, issuing authority, and the authority's city.

### Pass 1

Demand 1: `Meridian Lydora capital travel license payment currency issuing authority authority city`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-002` | 0.789764 | yes | yes | 136 |
| 2 | `cf-008` | 0.700000 | yes | yes | 108 |
| 3 | `cf-003` | 0.688247 | yes | yes | 130 |
| 4 | `cf-001` | 0.474342 | yes | yes | 167 |
| 5 | `cf-027` | 0.223607 | no | yes | 227 |

## cf-single-001 — `draftrag`

Question: According to Meridian chemistry, what is the symbol for gold?

### Pass 1

Demand 1: `According to Meridian chemistry, what is the symbol for gold?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `cf-006` | 1.000000 | yes | yes | 119 |
| 2 | `cf-010` | 0.980581 | no | yes | 94 |
| 3 | `cf-004` | 0.980581 | no | yes | 111 |
| 4 | `cf-017` | 0.000000 | no | yes | 226 |
| 5 | `cf-001` | 0.000000 | no | yes | 167 |

## ops-multi-001 — `draftrag`

Question: Nila Voss will perform Cedar work at 20:00 in cycle 14. Name the approver and list the rollback-age and bridge requirements before the first command.

### Pass 1

Demand 1: `Cedar work cycle 14 Nila Voss approver rollback age bridge requirements before first command`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-001` | 1.000000 | yes | yes | 233 |
| 2 | `ops-007` | 0.954427 | no | yes | 119 |
| 3 | `ops-005` | 0.942990 | no | yes | 197 |
| 4 | `ops-004` | 0.832050 | yes | yes | 161 |
| 5 | `ops-003` | 0.832050 | yes | yes | 185 |

## ops-seq-001 — `draftrag`

Question: During cycle 14, who must approve Nila Voss's incident if it begins at 20:00, and what chain of rules leads to that person?

### Pass 1

Demand 1: `During cycle 14, identify who must approve Nila Voss's incident when it begins at 20:00, including the chain of active-cycle authority, service-tier assignment, after-hours change-control, and approval rules that leads to that person.`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-005` | 0.999512 | no | yes | 197 |
| 2 | `ops-007` | 0.967375 | no | yes | 119 |
| 3 | `ops-001` | 0.952926 | yes | yes | 233 |
| 4 | `ops-002` | 0.780869 | yes | yes | 168 |
| 5 | `ops-000` | 0.780869 | yes | yes | 188 |

## ops-single-001 — `draftrag`

Question: What extension should operators call if the Atlas control plane is unavailable?

### Pass 1

Demand 1: `Atlas control plane unavailable operator call extension outage escalation fallback authorization`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-002` | 1.000000 | no | yes | 168 |
| 2 | `ops-000` | 1.000000 | no | yes | 188 |
| 3 | `ops-006` | 0.894427 | no | yes | 103 |
| 4 | `ops-008` | 0.847998 | no | yes | 77 |
| 5 | `ops-005` | 0.800000 | yes | yes | 197 |

## ops-unanswerable-001 — `draftrag`

Question: Who is the deputy Indigo reviewer for cycle 14?

### Pass 1

Demand 1: `Who is the deputy Indigo reviewer for cycle 14?`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ops-002` | 1.000000 | no | yes | 168 |
| 2 | `ops-000` | 1.000000 | no | yes | 188 |
| 3 | `ops-006` | 0.894427 | no | yes | 103 |
| 4 | `ops-008` | 0.847998 | no | yes | 77 |
| 5 | `ops-005` | 0.800000 | no | yes | 197 |

## ver-conflict-001 — `draftrag`

Question: Compare NovaDock 2.1 and 2.2: state each ambient ceiling and amber-key hold time without mixing the versions.

### Pass 1

Demand 1: `NovaDock 2.1 and 2.2 ambient ceiling and amber-key hold time reset procedure`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-002` | 0.745356 | yes | yes | 163 |
| 2 | `ver-001` | 0.739600 | yes | yes | 149 |
| 3 | `ver-006` | 0.725542 | yes | yes | 108 |
| 4 | `ver-005` | 0.707107 | yes | yes | 116 |
| 5 | `ver-007` | 0.707107 | no | yes | 116 |

## ver-multi-001 — `draftrag`

Question: For NovaDock 2.2, give the diagnostic port, approved firmware family, and reference sleep-state power draw.

### Pass 1

Demand 1: `NovaDock 2.2 diagnostic port approved firmware family reference sleep-state power draw`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-004` | 0.745356 | yes | yes | 124 |
| 2 | `ver-003` | 0.733333 | yes | yes | 136 |
| 3 | `ver-012` | 0.272798 | no | yes | 224 |
| 4 | `ver-026` | 0.272798 | no | yes | 221 |
| 5 | `ver-048` | 0.272798 | no | yes | 224 |

## ver-seq-001 — `draftrag`

Question: A NovaDock has serial prefix VL. Identify its version, maximum ambient temperature, and exact reset sequence.

### Pass 1

Demand 1: `NovaDock serial prefix VL version maximum ambient temperature exact reset sequence`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
| 1 | `ver-008` | 0.749269 | no | yes | 111 |
| 2 | `ver-002` | 0.670166 | yes | yes | 163 |
| 3 | `ver-006` | 0.575604 | no | yes | 108 |
| 4 | `ver-000` | 0.468293 | yes | yes | 163 |
| 5 | `ver-001` | 0.389643 | yes | yes | 149 |

## ver-unanswerable-001 — `draftrag`

Question: What is the battery mass of NovaDock 2.2?

### Pass 1

Demand 1: `NovaDock 2.2 battery mass`

| Rank | Chunk | Score | Gold | New | Chars |
| ---: | --- | ---: | :---: | :---: | ---: |
