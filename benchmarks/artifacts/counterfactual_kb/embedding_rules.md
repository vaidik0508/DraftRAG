# LLM-generated retrieval scorecard

Corpus: `counterfactual_kb`

Every criterion below was generated for this corpus. Score chunks and queries
from these dimension-specific use cases, not from a generic numeric scale.

## 0. scenario_reference_identity

Absolute degree to which a passage expresses the identity and versioning structure of an Atlas scenario reference rather than a general simulation rule.

### Corpus-specific anchors

- **0.0:** No Atlas scenario identity is present, or the passage explicitly rejects scenario-specific authority.
- **0.25:** An Atlas reference is mentioned only as background, with a [scenario number] or scenario label but no associated field structure.
- **0.50:** An Atlas scenario record is meaningfully represented through some, but not all, of its recurring fields, such as a [scenario number] plus one typed scenario attribute.
- **0.75:** The passage clearly organizes several recurring Atlas scenario fields around one [scenario number], but another field or the record identity is secondary.
- **1.0:** The passage is centrally a single Atlas scenario reference, explicitly tying a [scenario number] to the recurring administrative-center, local-token, and modeled-world fields.

### Corpus-specific between-anchor use cases

- **0.20:** A general simulation passage names Atlas scenarios as a category while giving no structured [scenario number] record.
- **0.40:** A passage identifies an Atlas [scenario number] and describes one scenario field, such as a modeled-world property, without presenting the full reference pattern.
- **0.60:** A scenario entry gives a [scenario number] with two recurring fields, for example an administrative role and a token field, while the remaining field is incidental.
- **0.80:** A nearly complete Atlas reference lists the [scenario number] and all recurring field types, but one field is abbreviated or treated as supporting context.

**Scoring guidance:** Score the structural Atlas-record pattern, not any particular scenario identifier or field value. A full reference record is high; generic mentions of Atlas or unrelated rules are low.

## 1. atlas_administrative_role

Absolute degree to which a passage expresses the Atlas recurring relationship between a polity-like unit and its designated administrative center.

### Corpus-specific anchors

- **0.0:** No administrative-center role appears, or the passage denies that an administrative designation applies.
- **0.25:** An administrative role is only alluded to, such as a generic reference to governance without a [center] and [polity] relationship.
- **0.50:** The administrative-center relationship is meaningfully present but shares attention with other Atlas fields or is stated as part of a broader scenario summary.
- **0.75:** A [center] is explicitly assigned to a [polity] in an Atlas context and this assignment is a prominent part of the passage.
- **1.0:** The central claim is the Atlas administrative-center assignment: a specific [center] is directly defined as the administrative center of a specific [polity].

### Corpus-specific between-anchor use cases

- **0.20:** An Atlas passage mentions a [polity] or administrative topic but does not clearly assign a [center] to it.
- **0.40:** A scenario reference states an administrative designation briefly while its main emphasis is the [scenario number] or another field.
- **0.60:** A scenario record clearly gives the [center]-to-[polity] assignment, but the same sentence gives comparable attention to the token or modeled-world property.
- **0.80:** The assignment is nearly the sole substantive content, with only the scenario label or a short non-administrative qualifier alongside it.

**Scoring guidance:** Reward the typed role relationship, not the identities of the center or polity. Do not infer this dimension from generic political geography outside Atlas.

## 2. atlas_token_economy

Absolute degree to which a passage expresses the Atlas local-token field associated with a scenario or discusses the token as a local economic designation.

### Corpus-specific anchors

- **0.0:** No local-token concept appears, or the passage explicitly separates the topic from Atlas token usage.
- **0.25:** Economic or token language occurs only incidentally without an Atlas local-token field or [token]-to-[scenario] association.
- **0.50:** An Atlas local-token designation is meaningfully present but is one coequal field among several scenario attributes.
- **0.75:** The passage explicitly states that an Atlas scenario has a local [token], with the token designation prominent but not exclusive.
- **1.0:** The central content is the Atlas local-token assignment for a [scenario number] or [Atlas polity], expressed as a direct local-token relationship.

### Corpus-specific between-anchor use cases

- **0.20:** An Atlas record mentions local economic identity in passing but supplies no clear [token] field.
- **0.40:** A scenario entry includes a local [token] field briefly while focusing more on the administrative role or modeled-world property.
- **0.60:** The local-token assignment is explicit and substantial, but it occupies roughly half of a multi-field Atlas reference.
- **0.80:** The passage is almost entirely about the local [token] designation, with only a scenario label or administrative qualifier remaining.

**Scoring guidance:** Score Atlas-local token semantics, not any token string or Meridian currency information. A generic mention of money without the Atlas local-token role should remain low.

## 3. atlas_world_measurement

Absolute degree to which a passage expresses the recurring Atlas modeled-home-world measurement field involving a count of natural satellites.

### Corpus-specific anchors

- **0.0:** No Atlas modeled-world measurement is present, or the passage rejects or contrasts such a measurement.
- **0.25:** A generic quantity or astronomy reference appears without an Atlas modeled-home-world satellite-count field.
- **0.50:** The Atlas modeled-world satellite-count property is meaningfully present but shares focus with administrative and token fields, or is only one of several measurements.
- **0.75:** An Atlas scenario explicitly reports its modeled home world's satellite count, and this measurement is a prominent field.
- **1.0:** The central content is the Atlas modeled-home-world satellite-count measurement for a [scenario number], with the measurement framed as a scenario attribute.

### Corpus-specific between-anchor use cases

- **0.20:** An Atlas passage refers to the modeled world but gives no clear satellite-count evidence.
- **0.40:** A scenario reference includes the modeled-world count as a short final field after emphasizing the administrative assignment.
- **0.60:** The satellite-count field is explicit and substantial but shares the passage with an equally important token or administrative field.
- **0.80:** The passage focuses almost entirely on the modeled-world satellite count, with only a scenario label and minimal context.

**Scoring guidance:** Use only for the Atlas modeled-world satellite-count property. Do not score ordinary Meridian or Harbor moon inventories here, and never use the underlying count as a scoring cue.

## 4. simulation_authority_separation

Absolute degree to which a passage establishes which simulation handbook governs a fact and prevents substitution or override across Meridian, Harbor, and Atlas.

### Corpus-specific anchors

- **0.0:** The passage contains no authority-separation content or explicitly treats all simulations as interchangeable.
- **0.25:** It hints that a simulation context matters but gives no clear source-boundary or precedence relationship.
- **0.50:** It meaningfully distinguishes one simulation's facts from another's, or states a limited non-substitution rule without making authority the main subject.
- **0.75:** It clearly states that a named simulation's handbook governs its facts and that another simulation's facts must not be substituted or used to override them.
- **1.0:** The passage is centrally an authority rule: it explicitly establishes handbook precedence and cross-simulation separation, including Atlas non-override of Meridian or Harbor rules.

### Corpus-specific between-anchor use cases

- **0.20:** A factual passage labels a value as belonging to [simulation] but does not discuss what happens when another simulation differs.
- **0.40:** A rule briefly warns that [simulation A] and [simulation B] are separate while primarily presenting another topic.
- **0.60:** The passage directly contrasts two simulation contexts and gives a clear separation instruction, but authority precedence is only part of the statement.
- **0.80:** A handbook rule strongly emphasizes source precedence and non-substitution, but one of the cross-simulation boundaries is only implicit.

**Scoring guidance:** Reward explicit governance, precedence, conflict handling, and non-substitution language. Do not reward merely naming a simulation in an ordinary factual statement.

## 5. meridian_civic_geography

Absolute degree to which a passage expresses Meridian's civic-geography model, especially the capital or administrative status of a settlement within a simulation polity.

### Corpus-specific anchors

- **0.0:** No Meridian civic-geography content appears, or the passage denies the relevant civic designation.
- **0.25:** A Meridian place or polity is mentioned without a civic-status relationship such as capital designation.
- **0.50:** A Meridian civic-geography relationship is meaningfully stated but shares focus with a disclaimer or another topic.
- **0.75:** The passage explicitly assigns a capital or comparable civic role to a [city] within a Meridian [polity], and that assignment is prominent.
- **1.0:** The central claim is Meridian political geography: a [city] is directly defined as the capital or designated civic center of a [polity], with simulation framing explicit.

### Corpus-specific between-anchor use cases

- **0.20:** A Meridian passage mentions a [city] or [polity] as setting but supplies no capital or civic-role relationship.
- **0.40:** A political-geography statement includes the [city]-to-[polity] civic assignment briefly while emphasizing that the polity is simulated.
- **0.60:** The civic assignment is explicit and important, but a real-world separation disclaimer or another geography detail receives comparable attention.
- **0.80:** The passage focuses almost entirely on the Meridian civic designation, with only a short simulation-context qualifier.

**Scoring guidance:** Score the Meridian civic-role relationship and its simulation framing. Do not use Atlas administrative-center records as substitutes, even though both involve governance roles.

## 6. meridian_fiscal_and_license_process

Absolute degree to which a passage expresses Meridian financial administration, including currency denomination, public charges, taxation, or the process and payment obligation for a license.

### Corpus-specific anchors

- **0.0:** No Meridian fiscal or licensing process appears, or the passage explicitly excludes money or licensing from the topic.
- **0.25:** A general financial term or administrative-payment reference appears without a Meridian charge, denomination, tax, or license obligation.
- **0.50:** Meridian fiscal administration is meaningfully present through one charge or licensing relationship, but it is mixed with another civic or institutional topic.
- **0.75:** The passage clearly describes a Meridian tax, public-fee denomination, or travel-license payment process, including a [payer], [authority], or [required payment].
- **1.0:** The central content is a Meridian fiscal or license rule: it directly specifies how a [charge] or [license] is denominated, assessed, or paid to a [minting authority].

### Corpus-specific between-anchor use cases

- **0.20:** A Meridian passage mentions public administration or commerce but contains no concrete fiscal, tax, or license obligation.
- **0.40:** A fee or license is named as a secondary consequence in a passage mainly about the currency institution or civic setting.
- **0.60:** A Meridian passage clearly describes a payment obligation or tax relationship, but it combines that process with a separate currency or authority fact.
- **0.80:** The passage is strongly procedural about a [license] or [tax], yet leaves one process element, such as the [payer] or [authority], implicit.

**Scoring guidance:** Score the financial-process family, not any amount, rate, currency name, or institution name. Treat taxation, public-fee denomination, and licensing payment as related but distinguishable evidence within this axis.

## 7. meridian_currency_institution

Absolute degree to which a passage expresses Meridian's currency system as an institutional object, including issuance by a mint and official denomination of obligations.

### Corpus-specific anchors

- **0.0:** No Meridian currency or issuing-institution concept appears, or the passage explicitly says the monetary system is irrelevant.
- **0.25:** Money is mentioned generically, without a Meridian official-currency, issuance, or denomination relationship.
- **0.50:** A Meridian official-currency or issuing-authority concept is meaningfully present but shares focus with a license, tax, or civic topic.
- **0.75:** The passage explicitly connects a Meridian [currency] with official use or a [mint] issuing it, and this institutional relationship is prominent.
- **1.0:** The central content is Meridian monetary administration: a [mint] issues the official [currency], or official public obligations are directly denominated in it.

### Corpus-specific between-anchor use cases

- **0.20:** A Meridian passage mentions payment only as incidental context and gives no official-currency or mint evidence.
- **0.40:** An official [currency] is identified as background to a licensing or fee statement, without explaining its institutional status.
- **0.60:** The passage explicitly describes either official denomination or mint issuance, while the other monetary aspect is absent or secondary.
- **0.80:** The passage concentrates on the issuing institution and official monetary status, but a related public-use detail is only briefly included.

**Scoring guidance:** Use this for Meridian monetary identity and issuance structure. Keep procedural tax or license mechanics primarily in the fiscal-process dimension, and never encode the actual currency name.

## 8. simulation_science_constants

Absolute degree to which a passage expresses a simulation-scoped scientific constant or laboratory condition, especially thermal behavior of a substance under stated conditions.

### Corpus-specific anchors

- **0.0:** No simulation-scoped scientific constant or laboratory condition appears, or the passage denies that the stated condition applies.
- **0.25:** A scientific measurement or substance is mentioned generically without a simulation-specific constant and without relevant experimental conditions.
- **0.50:** A simulation-specific physical constant is meaningfully stated, but the condition, substance, or cross-simulation contrast is incomplete or shares focus with another topic.
- **0.75:** The passage explicitly assigns a [measurement] for a substance under a [simulation] condition, making the scoped constant prominent.
- **1.0:** The central content is a simulation-scoped laboratory constant, directly pairing a [substance], [measurement], and [experimental condition], often to distinguish Meridian from Harbor.

### Corpus-specific between-anchor use cases

- **0.20:** A passage refers to laboratory science or water but gives no simulation-bound constant evidence.
- **0.40:** A simulation-specific physical condition is mentioned briefly after another topic, without a complete [substance]-[measurement]-[condition] structure.
- **0.60:** The scoped constant is explicit, but either the experimental condition or the contrast with another simulation receives only partial treatment.
- **0.80:** The passage is almost entirely a comparison of simulation-specific physical constants, with one condition or substance detail left implicit.

**Scoring guidance:** Score scoped scientific-constant structure and experimental conditions. Do not score the underlying measurement value, unit, or any answer payload.

## 9. simulation_astronomy_inventory

Absolute degree to which a passage expresses a simulation's Earth-like moon inventory or a named moon's physical property, distinct from Atlas scenario measurements.

### Corpus-specific anchors

- **0.0:** No simulation astronomy inventory or named-moon property appears, or the passage explicitly rejects that astronomy topic.
- **0.25:** A generic space or moon reference appears without a simulation-specific inventory, identity, or physical-property relationship.
- **0.50:** A Meridian or Harbor astronomy fact is meaningfully present but combines an inventory statement with a physical-property detail, or is secondary to authority context.
- **0.75:** The passage clearly describes a simulation's Earth moon inventory or a named moon's reference-imagery property, with the astronomy topic prominent.
- **1.0:** The central content is a simulation astronomy reference: it directly defines the Earth moon inventory or assigns a physical reference property to a [named moon] within Meridian or Harbor.

### Corpus-specific between-anchor use cases

- **0.20:** A simulation passage uses lunar language only as incidental setting and gives no inventory or moon-property evidence.
- **0.40:** An Earth-moon inventory or imagery statement appears as a supporting clause in a passage mainly about simulation authority.
- **0.60:** The astronomy fact is explicit and substantial, but inventory and physical-property aspects are mixed or one is only lightly developed.
- **0.80:** The passage focuses almost entirely on the simulation's Earth-moon inventory or a [named moon]'s physical property, with minimal context.

**Scoring guidance:** Use for Meridian or Harbor Earth-moon inventories and named-moon physical descriptions. Exclude Atlas modeled-world count fields, and never encode moon names or counts.

## Machine-readable definition

```json
{
  "dimensions": [
    {
      "index": 0,
      "name": "scenario_reference_identity",
      "definition": "Absolute degree to which a passage expresses the identity and versioning structure of an Atlas scenario reference rather than a general simulation rule.",
      "anchors": {
        "0.0": "No Atlas scenario identity is present, or the passage explicitly rejects scenario-specific authority.",
        "0.25": "An Atlas reference is mentioned only as background, with a [scenario number] or scenario label but no associated field structure.",
        "0.50": "An Atlas scenario record is meaningfully represented through some, but not all, of its recurring fields, such as a [scenario number] plus one typed scenario attribute.",
        "0.75": "The passage clearly organizes several recurring Atlas scenario fields around one [scenario number], but another field or the record identity is secondary.",
        "1.0": "The passage is centrally a single Atlas scenario reference, explicitly tying a [scenario number] to the recurring administrative-center, local-token, and modeled-world fields."
      },
      "interpolation_examples": {
        "0.20": "A general simulation passage names Atlas scenarios as a category while giving no structured [scenario number] record.",
        "0.40": "A passage identifies an Atlas [scenario number] and describes one scenario field, such as a modeled-world property, without presenting the full reference pattern.",
        "0.60": "A scenario entry gives a [scenario number] with two recurring fields, for example an administrative role and a token field, while the remaining field is incidental.",
        "0.80": "A nearly complete Atlas reference lists the [scenario number] and all recurring field types, but one field is abbreviated or treated as supporting context."
      },
      "guideline": "Score the structural Atlas-record pattern, not any particular scenario identifier or field value. A full reference record is high; generic mentions of Atlas or unrelated rules are low."
    },
    {
      "index": 1,
      "name": "atlas_administrative_role",
      "definition": "Absolute degree to which a passage expresses the Atlas recurring relationship between a polity-like unit and its designated administrative center.",
      "anchors": {
        "0.0": "No administrative-center role appears, or the passage denies that an administrative designation applies.",
        "0.25": "An administrative role is only alluded to, such as a generic reference to governance without a [center] and [polity] relationship.",
        "0.50": "The administrative-center relationship is meaningfully present but shares attention with other Atlas fields or is stated as part of a broader scenario summary.",
        "0.75": "A [center] is explicitly assigned to a [polity] in an Atlas context and this assignment is a prominent part of the passage.",
        "1.0": "The central claim is the Atlas administrative-center assignment: a specific [center] is directly defined as the administrative center of a specific [polity]."
      },
      "interpolation_examples": {
        "0.20": "An Atlas passage mentions a [polity] or administrative topic but does not clearly assign a [center] to it.",
        "0.40": "A scenario reference states an administrative designation briefly while its main emphasis is the [scenario number] or another field.",
        "0.60": "A scenario record clearly gives the [center]-to-[polity] assignment, but the same sentence gives comparable attention to the token or modeled-world property.",
        "0.80": "The assignment is nearly the sole substantive content, with only the scenario label or a short non-administrative qualifier alongside it."
      },
      "guideline": "Reward the typed role relationship, not the identities of the center or polity. Do not infer this dimension from generic political geography outside Atlas."
    },
    {
      "index": 2,
      "name": "atlas_token_economy",
      "definition": "Absolute degree to which a passage expresses the Atlas local-token field associated with a scenario or discusses the token as a local economic designation.",
      "anchors": {
        "0.0": "No local-token concept appears, or the passage explicitly separates the topic from Atlas token usage.",
        "0.25": "Economic or token language occurs only incidentally without an Atlas local-token field or [token]-to-[scenario] association.",
        "0.50": "An Atlas local-token designation is meaningfully present but is one coequal field among several scenario attributes.",
        "0.75": "The passage explicitly states that an Atlas scenario has a local [token], with the token designation prominent but not exclusive.",
        "1.0": "The central content is the Atlas local-token assignment for a [scenario number] or [Atlas polity], expressed as a direct local-token relationship."
      },
      "interpolation_examples": {
        "0.20": "An Atlas record mentions local economic identity in passing but supplies no clear [token] field.",
        "0.40": "A scenario entry includes a local [token] field briefly while focusing more on the administrative role or modeled-world property.",
        "0.60": "The local-token assignment is explicit and substantial, but it occupies roughly half of a multi-field Atlas reference.",
        "0.80": "The passage is almost entirely about the local [token] designation, with only a scenario label or administrative qualifier remaining."
      },
      "guideline": "Score Atlas-local token semantics, not any token string or Meridian currency information. A generic mention of money without the Atlas local-token role should remain low."
    },
    {
      "index": 3,
      "name": "atlas_world_measurement",
      "definition": "Absolute degree to which a passage expresses the recurring Atlas modeled-home-world measurement field involving a count of natural satellites.",
      "anchors": {
        "0.0": "No Atlas modeled-world measurement is present, or the passage rejects or contrasts such a measurement.",
        "0.25": "A generic quantity or astronomy reference appears without an Atlas modeled-home-world satellite-count field.",
        "0.50": "The Atlas modeled-world satellite-count property is meaningfully present but shares focus with administrative and token fields, or is only one of several measurements.",
        "0.75": "An Atlas scenario explicitly reports its modeled home world's satellite count, and this measurement is a prominent field.",
        "1.0": "The central content is the Atlas modeled-home-world satellite-count measurement for a [scenario number], with the measurement framed as a scenario attribute."
      },
      "interpolation_examples": {
        "0.20": "An Atlas passage refers to the modeled world but gives no clear satellite-count evidence.",
        "0.40": "A scenario reference includes the modeled-world count as a short final field after emphasizing the administrative assignment.",
        "0.60": "The satellite-count field is explicit and substantial but shares the passage with an equally important token or administrative field.",
        "0.80": "The passage focuses almost entirely on the modeled-world satellite count, with only a scenario label and minimal context."
      },
      "guideline": "Use only for the Atlas modeled-world satellite-count property. Do not score ordinary Meridian or Harbor moon inventories here, and never use the underlying count as a scoring cue."
    },
    {
      "index": 4,
      "name": "simulation_authority_separation",
      "definition": "Absolute degree to which a passage establishes which simulation handbook governs a fact and prevents substitution or override across Meridian, Harbor, and Atlas.",
      "anchors": {
        "0.0": "The passage contains no authority-separation content or explicitly treats all simulations as interchangeable.",
        "0.25": "It hints that a simulation context matters but gives no clear source-boundary or precedence relationship.",
        "0.50": "It meaningfully distinguishes one simulation's facts from another's, or states a limited non-substitution rule without making authority the main subject.",
        "0.75": "It clearly states that a named simulation's handbook governs its facts and that another simulation's facts must not be substituted or used to override them.",
        "1.0": "The passage is centrally an authority rule: it explicitly establishes handbook precedence and cross-simulation separation, including Atlas non-override of Meridian or Harbor rules."
      },
      "interpolation_examples": {
        "0.20": "A factual passage labels a value as belonging to [simulation] but does not discuss what happens when another simulation differs.",
        "0.40": "A rule briefly warns that [simulation A] and [simulation B] are separate while primarily presenting another topic.",
        "0.60": "The passage directly contrasts two simulation contexts and gives a clear separation instruction, but authority precedence is only part of the statement.",
        "0.80": "A handbook rule strongly emphasizes source precedence and non-substitution, but one of the cross-simulation boundaries is only implicit."
      },
      "guideline": "Reward explicit governance, precedence, conflict handling, and non-substitution language. Do not reward merely naming a simulation in an ordinary factual statement."
    },
    {
      "index": 5,
      "name": "meridian_civic_geography",
      "definition": "Absolute degree to which a passage expresses Meridian's civic-geography model, especially the capital or administrative status of a settlement within a simulation polity.",
      "anchors": {
        "0.0": "No Meridian civic-geography content appears, or the passage denies the relevant civic designation.",
        "0.25": "A Meridian place or polity is mentioned without a civic-status relationship such as capital designation.",
        "0.50": "A Meridian civic-geography relationship is meaningfully stated but shares focus with a disclaimer or another topic.",
        "0.75": "The passage explicitly assigns a capital or comparable civic role to a [city] within a Meridian [polity], and that assignment is prominent.",
        "1.0": "The central claim is Meridian political geography: a [city] is directly defined as the capital or designated civic center of a [polity], with simulation framing explicit."
      },
      "interpolation_examples": {
        "0.20": "A Meridian passage mentions a [city] or [polity] as setting but supplies no capital or civic-role relationship.",
        "0.40": "A political-geography statement includes the [city]-to-[polity] civic assignment briefly while emphasizing that the polity is simulated.",
        "0.60": "The civic assignment is explicit and important, but a real-world separation disclaimer or another geography detail receives comparable attention.",
        "0.80": "The passage focuses almost entirely on the Meridian civic designation, with only a short simulation-context qualifier."
      },
      "guideline": "Score the Meridian civic-role relationship and its simulation framing. Do not use Atlas administrative-center records as substitutes, even though both involve governance roles."
    },
    {
      "index": 6,
      "name": "meridian_fiscal_and_license_process",
      "definition": "Absolute degree to which a passage expresses Meridian financial administration, including currency denomination, public charges, taxation, or the process and payment obligation for a license.",
      "anchors": {
        "0.0": "No Meridian fiscal or licensing process appears, or the passage explicitly excludes money or licensing from the topic.",
        "0.25": "A general financial term or administrative-payment reference appears without a Meridian charge, denomination, tax, or license obligation.",
        "0.50": "Meridian fiscal administration is meaningfully present through one charge or licensing relationship, but it is mixed with another civic or institutional topic.",
        "0.75": "The passage clearly describes a Meridian tax, public-fee denomination, or travel-license payment process, including a [payer], [authority], or [required payment].",
        "1.0": "The central content is a Meridian fiscal or license rule: it directly specifies how a [charge] or [license] is denominated, assessed, or paid to a [minting authority]."
      },
      "interpolation_examples": {
        "0.20": "A Meridian passage mentions public administration or commerce but contains no concrete fiscal, tax, or license obligation.",
        "0.40": "A fee or license is named as a secondary consequence in a passage mainly about the currency institution or civic setting.",
        "0.60": "A Meridian passage clearly describes a payment obligation or tax relationship, but it combines that process with a separate currency or authority fact.",
        "0.80": "The passage is strongly procedural about a [license] or [tax], yet leaves one process element, such as the [payer] or [authority], implicit."
      },
      "guideline": "Score the financial-process family, not any amount, rate, currency name, or institution name. Treat taxation, public-fee denomination, and licensing payment as related but distinguishable evidence within this axis."
    },
    {
      "index": 7,
      "name": "meridian_currency_institution",
      "definition": "Absolute degree to which a passage expresses Meridian's currency system as an institutional object, including issuance by a mint and official denomination of obligations.",
      "anchors": {
        "0.0": "No Meridian currency or issuing-institution concept appears, or the passage explicitly says the monetary system is irrelevant.",
        "0.25": "Money is mentioned generically, without a Meridian official-currency, issuance, or denomination relationship.",
        "0.50": "A Meridian official-currency or issuing-authority concept is meaningfully present but shares focus with a license, tax, or civic topic.",
        "0.75": "The passage explicitly connects a Meridian [currency] with official use or a [mint] issuing it, and this institutional relationship is prominent.",
        "1.0": "The central content is Meridian monetary administration: a [mint] issues the official [currency], or official public obligations are directly denominated in it."
      },
      "interpolation_examples": {
        "0.20": "A Meridian passage mentions payment only as incidental context and gives no official-currency or mint evidence.",
        "0.40": "An official [currency] is identified as background to a licensing or fee statement, without explaining its institutional status.",
        "0.60": "The passage explicitly describes either official denomination or mint issuance, while the other monetary aspect is absent or secondary.",
        "0.80": "The passage concentrates on the issuing institution and official monetary status, but a related public-use detail is only briefly included."
      },
      "guideline": "Use this for Meridian monetary identity and issuance structure. Keep procedural tax or license mechanics primarily in the fiscal-process dimension, and never encode the actual currency name."
    },
    {
      "index": 8,
      "name": "simulation_science_constants",
      "definition": "Absolute degree to which a passage expresses a simulation-scoped scientific constant or laboratory condition, especially thermal behavior of a substance under stated conditions.",
      "anchors": {
        "0.0": "No simulation-scoped scientific constant or laboratory condition appears, or the passage denies that the stated condition applies.",
        "0.25": "A scientific measurement or substance is mentioned generically without a simulation-specific constant and without relevant experimental conditions.",
        "0.50": "A simulation-specific physical constant is meaningfully stated, but the condition, substance, or cross-simulation contrast is incomplete or shares focus with another topic.",
        "0.75": "The passage explicitly assigns a [measurement] for a substance under a [simulation] condition, making the scoped constant prominent.",
        "1.0": "The central content is a simulation-scoped laboratory constant, directly pairing a [substance], [measurement], and [experimental condition], often to distinguish Meridian from Harbor."
      },
      "interpolation_examples": {
        "0.20": "A passage refers to laboratory science or water but gives no simulation-bound constant evidence.",
        "0.40": "A simulation-specific physical condition is mentioned briefly after another topic, without a complete [substance]-[measurement]-[condition] structure.",
        "0.60": "The scoped constant is explicit, but either the experimental condition or the contrast with another simulation receives only partial treatment.",
        "0.80": "The passage is almost entirely a comparison of simulation-specific physical constants, with one condition or substance detail left implicit."
      },
      "guideline": "Score scoped scientific-constant structure and experimental conditions. Do not score the underlying measurement value, unit, or any answer payload."
    },
    {
      "index": 9,
      "name": "simulation_astronomy_inventory",
      "definition": "Absolute degree to which a passage expresses a simulation's Earth-like moon inventory or a named moon's physical property, distinct from Atlas scenario measurements.",
      "anchors": {
        "0.0": "No simulation astronomy inventory or named-moon property appears, or the passage explicitly rejects that astronomy topic.",
        "0.25": "A generic space or moon reference appears without a simulation-specific inventory, identity, or physical-property relationship.",
        "0.50": "A Meridian or Harbor astronomy fact is meaningfully present but combines an inventory statement with a physical-property detail, or is secondary to authority context.",
        "0.75": "The passage clearly describes a simulation's Earth moon inventory or a named moon's reference-imagery property, with the astronomy topic prominent.",
        "1.0": "The central content is a simulation astronomy reference: it directly defines the Earth moon inventory or assigns a physical reference property to a [named moon] within Meridian or Harbor."
      },
      "interpolation_examples": {
        "0.20": "A simulation passage uses lunar language only as incidental setting and gives no inventory or moon-property evidence.",
        "0.40": "An Earth-moon inventory or imagery statement appears as a supporting clause in a passage mainly about simulation authority.",
        "0.60": "The astronomy fact is explicit and substantial, but inventory and physical-property aspects are mixed or one is only lightly developed.",
        "0.80": "The passage focuses almost entirely on the simulation's Earth-moon inventory or a [named moon]'s physical property, with minimal context."
      },
      "guideline": "Use for Meridian or Harbor Earth-moon inventories and named-moon physical descriptions. Exclude Atlas modeled-world count fields, and never encode moon names or counts."
    }
  ]
}
```
