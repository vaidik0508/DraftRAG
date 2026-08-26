# LLM-generated retrieval scorecard

Corpus: `versioned_manual`

Every criterion below was generated for this corpus. Score chunks and queries
from these dimension-specific use cases, not from a generic numeric scale.

## 0. NovaDock identity inference

Absolute degree to which a chunk or query concerns identifying a NovaDock hardware revision from an external identifier pattern or other revision-identification evidence.

### Corpus-specific anchors

- **0.0:** No NovaDock identity evidence, or it assigns an identifier pattern to an unrelated product family.
- **0.25:** NovaDock is mentioned incidentally near general hardware information, but no identifier-to-revision relationship is developed.
- **0.50:** The text presents a partial identity rule, such as one identifier prefix associated with a [version], while other identification alternatives or context are absent.
- **0.75:** The text substantially describes serial-prefix identification across several NovaDock revisions, but the rule is embedded with additional material.
- **1.0:** The central subject is the NovaDock serial-identification scheme, with identifier patterns explicitly tied to hardware revisions.

### Corpus-specific between-anchor use cases

- **0.20:** A reference card names NovaDock only in a non-applicability warning and gives no identification rule.
- **0.40:** A passage mentions that hardware revisions can be distinguished by serial information but gives only limited prefix evidence.
- **0.60:** A serial-identification note covers part of the prefix scheme and briefly frames the alternatives as revision markers.
- **0.80:** A dedicated identification passage lays out most of the competing NovaDock prefix-to-revision relationships, with a small amount of surrounding context.

**Scoring guidance:** Score only identity inference from serial or identifier patterns. Do not score ordinary product/version labels, configuration values, or service instructions unless they are used to identify hardware.

## 1. NovaDock firmware governance

Absolute degree to which a chunk or query concerns approved firmware-family assignment, retention, or compatibility boundaries for NovaDock revisions.

### Corpus-specific anchors

- **0.0:** No firmware-governance content, or the text explicitly concerns a non-NovaDock reference-card firmware field without a NovaDock compatibility context.
- **0.25:** NovaDock firmware is mentioned only as peripheral context, with no approval, retention, or revision boundary.
- **0.50:** The text gives a partial firmware policy, such as an approved family for one [version] or a retained family for another, but does not center the full compatibility distinction.
- **0.75:** The passage clearly contrasts approved and retained firmware families across NovaDock revisions, while including some non-policy context.
- **1.0:** The central purpose is NovaDock firmware governance: revision-specific approval and explicit separation of a retained or disallowed family.

### Corpus-specific between-anchor use cases

- **0.20:** A reset or ambient note names a NovaDock revision but contains no firmware policy.
- **0.40:** A firmware sentence identifies an approved family for one revision, with the retention distinction only implied or peripheral.
- **0.60:** A short firmware note states approval for one revision and refers to a different revision's retained family without making the broader policy the sole focus.
- **0.80:** A firmware-specific passage makes the approval-versus-retention boundary clear across revisions, but includes a brief unrelated configuration statement.

**Scoring guidance:** Score firmware policy and revision compatibility, not merely the presence of a firmware label in a reference card. Treat non-NovaDock Lily-family fields as zero on this axis unless the passage compares them with NovaDock governance.

## 2. NovaDock thermal limits

Absolute degree to which a chunk or query concerns NovaDock operating ambient constraints, threshold behavior, or thermal shutdown policy by revision.

### Corpus-specific anchors

- **0.0:** No thermal operating content, or the text denies that ambient limits apply to NovaDock.
- **0.25:** Temperature is incidental, such as a passing environmental phrase without a NovaDock operating rule.
- **0.50:** A NovaDock ambient constraint is meaningfully stated for one [version], but threshold behavior or revision comparison is incomplete.
- **0.75:** The passage clearly describes NovaDock operating temperature policy and includes either a boundary consequence or comparison among revisions.
- **1.0:** The central subject is NovaDock ambient-limit behavior, including revision-scoped operation and any associated shutdown boundary.

### Corpus-specific between-anchor use cases

- **0.20:** A reference card mentions an ambient ceiling only as part of an unrelated product configuration, with NovaDock excluded.
- **0.40:** A NovaDock note states an operating ambient ceiling for one revision but gives no consequence or comparison.
- **0.60:** A thermal note includes a NovaDock operating limit and some indication of what happens beyond the permitted range, but the boundary is not the whole passage.
- **0.80:** A dedicated NovaDock thermal passage explains revision-specific operation and a shutdown consequence, with a small amount of surrounding wording.

**Scoring guidance:** Score NovaDock thermal policy only. Do not transfer temperature content from unrelated reference cards to this axis, and never infer similarity from shared environmental terminology.

## 3. NovaDock reset procedure

Absolute degree to which a chunk or query concerns the physical reset workflow for a NovaDock revision, including control actions, sequencing, and prohibited actions.

### Corpus-specific anchors

- **0.0:** No reset workflow, or the text explicitly says that a described action is not a reset procedure.
- **0.25:** Reset is mentioned as a general maintenance topic without an actionable NovaDock sequence.
- **0.50:** The passage gives a meaningful partial reset workflow for one [version], such as the control combination or an ordering constraint, but omits part of the operation.
- **0.75:** The text describes nearly the full reset workflow for a NovaDock revision, including controls and at least one sequencing or prohibition detail.
- **1.0:** The central subject is a complete revision-specific NovaDock reset procedure with its required actions, order, and relevant forbidden alternative.

### Corpus-specific between-anchor use cases

- **0.20:** A firmware or service note refers to resetting only as a possible maintenance activity, without instructions.
- **0.40:** A reset passage identifies the relevant key and general interaction with the bay control but leaves the ordering or duration detail unstated.
- **0.60:** A reset instruction provides the main control actions and one constraint, while omitting or deemphasizing another required procedural detail.
- **0.80:** A dedicated reset instruction gives the control, hold interaction, follow-up bay action, and a warning about an invalid order, but includes a brief heading or context.

**Scoring guidance:** Score procedural action structure rather than any isolated number, color, key name, or control name. Queries describing reset, sequencing, or forbidden reset actions can score highly even without payload values.

## 4. NovaDock service-port assignment

Absolute degree to which a chunk or query concerns the diagnostic service-port assignment for a NovaDock revision and the separation of ports belonging to other revisions.

### Corpus-specific anchors

- **0.0:** No service-port assignment, or the passage attributes a diagnostic port only to an unrelated product family with no NovaDock comparison.
- **0.25:** A port is mentioned near NovaDock maintenance context, but no revision-specific service assignment is established.
- **0.50:** The passage identifies a NovaDock [version] as having a diagnostic service port, but gives little or no contrast with neighboring revisions.
- **0.75:** The text clearly states the revision-scoped service-port rule and includes an exclusion or contrast involving other hardware revisions.
- **1.0:** The central subject is NovaDock diagnostic service-port assignment, including the distinction between the applicable revision and ports assigned elsewhere.

### Corpus-specific between-anchor use cases

- **0.20:** A reference card contains a diagnostic-port field but explicitly says its values do not apply to NovaDock.
- **0.40:** A NovaDock maintenance passage identifies a service port for one revision without developing the cross-revision boundary.
- **0.60:** A service-port note gives the assignment and briefly warns that nearby alternatives belong to other revisions.
- **0.80:** A dedicated service-port passage emphasizes both the applicable NovaDock revision and the non-applicability of alternate hardware ports, with minimal extra context.

**Scoring guidance:** Use this axis for NovaDock service-port semantics, not for generic diagnostic-port mentions. Preserve the revision-scope distinction and ignore the literal port token when scoring.

## 5. Reference-card product identity

Absolute degree to which a chunk or query expresses the product-family and [version] identity structure of the corpus's non-NovaDock reference cards.

### Corpus-specific anchors

- **0.0:** No reference-card product identity, or the text is solely a NovaDock procedure, measurement, or identification rule.
- **0.25:** A non-NovaDock product name or [version] appears incidentally without a card-style identity/configuration context.
- **0.50:** The passage identifies one reference-card product and [version] while presenting only part of its configuration context or mixing it with another topic.
- **0.75:** A reference-card entry clearly establishes a product-family/[version] identity and frames the accompanying fields as belonging to that combination.
- **1.0:** The central structure is a non-NovaDock reference card whose product family and [version] define the scope of all listed configuration fields.

### Corpus-specific between-anchor use cases

- **0.20:** A NovaDock note says that values from another product family do not transfer, but does not identify that card's full scope.
- **0.40:** A reference-card heading names a product family and [version], while the body mainly discusses one configuration field.
- **0.60:** A card-style passage establishes the product and [version] and lists several fields, but also includes a substantial non-identity warning.
- **0.80:** A reference card is strongly organized around one product/[version] combination and its associated fields, with only a brief scope disclaimer.

**Scoring guidance:** Score the card's product-and-revision scoping function, not generic mentions of a version. Use this axis for the repeated non-NovaDock card family and keep the identity separate from the individual port, firmware, and thermal axes.

## 6. Reference-card diagnostic-port field

Absolute degree to which a chunk or query concerns diagnostic-port assignment as a configuration field within the non-NovaDock reference-card matrix.

### Corpus-specific anchors

- **0.0:** No diagnostic-port configuration, or the passage explicitly treats a port as unrelated to the reference-card configuration topic.
- **0.25:** A diagnostic port is mentioned only in a heading, disclaimer, or incidental comparison without an assignment relationship.
- **0.50:** A reference card assigns a diagnostic port to a product/[version] but the port field is balanced with other fields or only partly elaborated.
- **0.75:** The diagnostic-port assignment is a prominent part of a non-NovaDock reference card, with clear product/[version] scope and supporting configuration context.
- **1.0:** The passage centrally expresses the reference-card diagnostic-port field: a product/[version] is directly associated with its port assignment, without another topic dominating.

### Corpus-specific between-anchor use cases

- **0.20:** A card warning mentions that diagnostic values do not transfer to NovaDock, but does not state the card's assignment as the main content.
- **0.40:** A reference card gives a port assignment alongside a brief product identity, while firmware and thermal fields occupy most of the text.
- **0.60:** The card gives a clear port-to-product/[version] association and one other field, but the assignment is not the sole focus.
- **0.80:** A short configuration passage foregrounds the diagnostic-port field and its product/[version] scope, while retaining a compact supporting field.

**Scoring guidance:** Score the semantic role of diagnostic-port assignment in non-NovaDock cards. Do not use the literal port code or assume that any port mention is a high score.

## 7. Reference-card firmware field

Absolute degree to which a chunk or query concerns firmware-family assignment as a configuration field within the non-NovaDock reference-card matrix.

### Corpus-specific anchors

- **0.0:** No reference-card firmware assignment, or the passage explicitly separates the firmware discussion from the non-NovaDock card context.
- **0.25:** A firmware family is mentioned incidentally or in a disclaimer without being assigned to a card's product/[version].
- **0.50:** A card assigns a firmware family to a product/[version], but the field shares focus with port and thermal information or is only partly developed.
- **0.75:** Firmware assignment is a prominent, revision-scoped part of a non-NovaDock reference card and is supported by neighboring configuration evidence.
- **1.0:** The central content is the reference-card firmware field: a product/[version] is directly associated with its firmware family as part of the card's configuration.

### Corpus-specific between-anchor use cases

- **0.20:** A card contains a firmware word only in a broad non-applicability disclaimer, without a product-specific assignment.
- **0.40:** A reference card names its firmware family, but the passage is mainly about product identity and another configuration field.
- **0.60:** The firmware-to-product/[version] relationship is explicit and meaningful, though port and ambient fields receive comparable treatment.
- **0.80:** A compact card excerpt foregrounds firmware assignment for one product/[version] and gives only limited neighboring configuration context.

**Scoring guidance:** Score firmware as a reference-card configuration field, not as NovaDock approval policy. Ignore the exact family label and distinguish direct assignment from incidental firmware vocabulary.

## 8. Reference-card ambient field

Absolute degree to which a chunk or query concerns an ambient operating ceiling as a configuration field within the non-NovaDock reference-card matrix.

### Corpus-specific anchors

- **0.0:** No reference-card ambient constraint, or the passage explicitly denies that the ambient field belongs to the discussed product.
- **0.25:** Temperature terminology appears only incidentally or in a disclaimer, without a product/[version]-scoped ceiling.
- **0.50:** A reference card gives an ambient ceiling for a product/[version], but the thermal field is one of several equally weighted fields or lacks further context.
- **0.75:** The ambient ceiling is a prominent, product/[version]-scoped part of a non-NovaDock reference card, supported by configuration framing.
- **1.0:** The central content is the reference-card ambient field: a product/[version] is directly associated with an operating ceiling as part of its configuration.

### Corpus-specific between-anchor use cases

- **0.20:** A card's non-applicability sentence mentions ambient limits but does not present the value as belonging to the card's product.
- **0.40:** A reference card states an ambient ceiling, while the product identity and port or firmware fields carry most of the semantic weight.
- **0.60:** The product/[version]-scoped thermal ceiling is explicit and substantial, but it is presented alongside comparable port and firmware assignments.
- **0.80:** A short card excerpt emphasizes the ambient ceiling and its product/[version] scope, with only a small amount of adjacent configuration detail.

**Scoring guidance:** Score the ambient-ceiling field in non-NovaDock reference cards. Do not score any exact temperature, and do not conflate this field with NovaDock thermal policy or reset behavior.

## 9. Cross-family applicability boundary

Absolute degree to which a chunk or query expresses that configuration values are scoped to a particular product/[version] and must not be transferred across hardware families or revisions.

### Corpus-specific anchors

- **0.0:** No applicability boundary, or the text explicitly treats a configuration value as universally transferable across all hardware.
- **0.25:** A weak scope cue appears, such as a product label near a value, but no explicit transfer restriction or contrast is made.
- **0.50:** The passage meaningfully scopes a value to one product/[version] or distinguishes one revision from another, but the non-transfer rule is incomplete or indirect.
- **0.75:** The text clearly warns against applying a configuration value outside its product/[version] scope and provides a relevant contrasting hardware or revision context.
- **1.0:** The central purpose is applicability control: explicit separation of one product/[version]'s configuration from other hardware families or revisions, with transfer treated as invalid.

### Corpus-specific between-anchor use cases

- **0.20:** A reference card labels its fields by product family but gives no warning about using them elsewhere.
- **0.40:** A card briefly says its configuration is for the named product/[version], while any contrast with other hardware is only implied.
- **0.60:** The passage includes a direct scope disclaimer that values do not carry to NovaDock, but the card's port, firmware, or thermal details remain the main focus.
- **0.80:** A passage strongly emphasizes non-transfer across product families or revisions and gives a concrete contrasting context, while still retaining some configuration content.

**Scoring guidance:** Score explicit semantic scope and non-applicability boundaries. Treat repeated warnings about reference-card values not applying to NovaDock, and revision-specific exclusions in NovaDock maintenance notes, as evidence; do not score the underlying literal values.

## Machine-readable definition

```json
{
  "dimensions": [
    {
      "index": 0,
      "name": "NovaDock identity inference",
      "definition": "Absolute degree to which a chunk or query concerns identifying a NovaDock hardware revision from an external identifier pattern or other revision-identification evidence.",
      "anchors": {
        "0.0": "No NovaDock identity evidence, or it assigns an identifier pattern to an unrelated product family.",
        "0.25": "NovaDock is mentioned incidentally near general hardware information, but no identifier-to-revision relationship is developed.",
        "0.50": "The text presents a partial identity rule, such as one identifier prefix associated with a [version], while other identification alternatives or context are absent.",
        "0.75": "The text substantially describes serial-prefix identification across several NovaDock revisions, but the rule is embedded with additional material.",
        "1.0": "The central subject is the NovaDock serial-identification scheme, with identifier patterns explicitly tied to hardware revisions."
      },
      "interpolation_examples": {
        "0.20": "A reference card names NovaDock only in a non-applicability warning and gives no identification rule.",
        "0.40": "A passage mentions that hardware revisions can be distinguished by serial information but gives only limited prefix evidence.",
        "0.60": "A serial-identification note covers part of the prefix scheme and briefly frames the alternatives as revision markers.",
        "0.80": "A dedicated identification passage lays out most of the competing NovaDock prefix-to-revision relationships, with a small amount of surrounding context."
      },
      "guideline": "Score only identity inference from serial or identifier patterns. Do not score ordinary product/version labels, configuration values, or service instructions unless they are used to identify hardware."
    },
    {
      "index": 1,
      "name": "NovaDock firmware governance",
      "definition": "Absolute degree to which a chunk or query concerns approved firmware-family assignment, retention, or compatibility boundaries for NovaDock revisions.",
      "anchors": {
        "0.0": "No firmware-governance content, or the text explicitly concerns a non-NovaDock reference-card firmware field without a NovaDock compatibility context.",
        "0.25": "NovaDock firmware is mentioned only as peripheral context, with no approval, retention, or revision boundary.",
        "0.50": "The text gives a partial firmware policy, such as an approved family for one [version] or a retained family for another, but does not center the full compatibility distinction.",
        "0.75": "The passage clearly contrasts approved and retained firmware families across NovaDock revisions, while including some non-policy context.",
        "1.0": "The central purpose is NovaDock firmware governance: revision-specific approval and explicit separation of a retained or disallowed family."
      },
      "interpolation_examples": {
        "0.20": "A reset or ambient note names a NovaDock revision but contains no firmware policy.",
        "0.40": "A firmware sentence identifies an approved family for one revision, with the retention distinction only implied or peripheral.",
        "0.60": "A short firmware note states approval for one revision and refers to a different revision's retained family without making the broader policy the sole focus.",
        "0.80": "A firmware-specific passage makes the approval-versus-retention boundary clear across revisions, but includes a brief unrelated configuration statement."
      },
      "guideline": "Score firmware policy and revision compatibility, not merely the presence of a firmware label in a reference card. Treat non-NovaDock Lily-family fields as zero on this axis unless the passage compares them with NovaDock governance."
    },
    {
      "index": 2,
      "name": "NovaDock thermal limits",
      "definition": "Absolute degree to which a chunk or query concerns NovaDock operating ambient constraints, threshold behavior, or thermal shutdown policy by revision.",
      "anchors": {
        "0.0": "No thermal operating content, or the text denies that ambient limits apply to NovaDock.",
        "0.25": "Temperature is incidental, such as a passing environmental phrase without a NovaDock operating rule.",
        "0.50": "A NovaDock ambient constraint is meaningfully stated for one [version], but threshold behavior or revision comparison is incomplete.",
        "0.75": "The passage clearly describes NovaDock operating temperature policy and includes either a boundary consequence or comparison among revisions.",
        "1.0": "The central subject is NovaDock ambient-limit behavior, including revision-scoped operation and any associated shutdown boundary."
      },
      "interpolation_examples": {
        "0.20": "A reference card mentions an ambient ceiling only as part of an unrelated product configuration, with NovaDock excluded.",
        "0.40": "A NovaDock note states an operating ambient ceiling for one revision but gives no consequence or comparison.",
        "0.60": "A thermal note includes a NovaDock operating limit and some indication of what happens beyond the permitted range, but the boundary is not the whole passage.",
        "0.80": "A dedicated NovaDock thermal passage explains revision-specific operation and a shutdown consequence, with a small amount of surrounding wording."
      },
      "guideline": "Score NovaDock thermal policy only. Do not transfer temperature content from unrelated reference cards to this axis, and never infer similarity from shared environmental terminology."
    },
    {
      "index": 3,
      "name": "NovaDock reset procedure",
      "definition": "Absolute degree to which a chunk or query concerns the physical reset workflow for a NovaDock revision, including control actions, sequencing, and prohibited actions.",
      "anchors": {
        "0.0": "No reset workflow, or the text explicitly says that a described action is not a reset procedure.",
        "0.25": "Reset is mentioned as a general maintenance topic without an actionable NovaDock sequence.",
        "0.50": "The passage gives a meaningful partial reset workflow for one [version], such as the control combination or an ordering constraint, but omits part of the operation.",
        "0.75": "The text describes nearly the full reset workflow for a NovaDock revision, including controls and at least one sequencing or prohibition detail.",
        "1.0": "The central subject is a complete revision-specific NovaDock reset procedure with its required actions, order, and relevant forbidden alternative."
      },
      "interpolation_examples": {
        "0.20": "A firmware or service note refers to resetting only as a possible maintenance activity, without instructions.",
        "0.40": "A reset passage identifies the relevant key and general interaction with the bay control but leaves the ordering or duration detail unstated.",
        "0.60": "A reset instruction provides the main control actions and one constraint, while omitting or deemphasizing another required procedural detail.",
        "0.80": "A dedicated reset instruction gives the control, hold interaction, follow-up bay action, and a warning about an invalid order, but includes a brief heading or context."
      },
      "guideline": "Score procedural action structure rather than any isolated number, color, key name, or control name. Queries describing reset, sequencing, or forbidden reset actions can score highly even without payload values."
    },
    {
      "index": 4,
      "name": "NovaDock service-port assignment",
      "definition": "Absolute degree to which a chunk or query concerns the diagnostic service-port assignment for a NovaDock revision and the separation of ports belonging to other revisions.",
      "anchors": {
        "0.0": "No service-port assignment, or the passage attributes a diagnostic port only to an unrelated product family with no NovaDock comparison.",
        "0.25": "A port is mentioned near NovaDock maintenance context, but no revision-specific service assignment is established.",
        "0.50": "The passage identifies a NovaDock [version] as having a diagnostic service port, but gives little or no contrast with neighboring revisions.",
        "0.75": "The text clearly states the revision-scoped service-port rule and includes an exclusion or contrast involving other hardware revisions.",
        "1.0": "The central subject is NovaDock diagnostic service-port assignment, including the distinction between the applicable revision and ports assigned elsewhere."
      },
      "interpolation_examples": {
        "0.20": "A reference card contains a diagnostic-port field but explicitly says its values do not apply to NovaDock.",
        "0.40": "A NovaDock maintenance passage identifies a service port for one revision without developing the cross-revision boundary.",
        "0.60": "A service-port note gives the assignment and briefly warns that nearby alternatives belong to other revisions.",
        "0.80": "A dedicated service-port passage emphasizes both the applicable NovaDock revision and the non-applicability of alternate hardware ports, with minimal extra context."
      },
      "guideline": "Use this axis for NovaDock service-port semantics, not for generic diagnostic-port mentions. Preserve the revision-scope distinction and ignore the literal port token when scoring."
    },
    {
      "index": 5,
      "name": "Reference-card product identity",
      "definition": "Absolute degree to which a chunk or query expresses the product-family and [version] identity structure of the corpus's non-NovaDock reference cards.",
      "anchors": {
        "0.0": "No reference-card product identity, or the text is solely a NovaDock procedure, measurement, or identification rule.",
        "0.25": "A non-NovaDock product name or [version] appears incidentally without a card-style identity/configuration context.",
        "0.50": "The passage identifies one reference-card product and [version] while presenting only part of its configuration context or mixing it with another topic.",
        "0.75": "A reference-card entry clearly establishes a product-family/[version] identity and frames the accompanying fields as belonging to that combination.",
        "1.0": "The central structure is a non-NovaDock reference card whose product family and [version] define the scope of all listed configuration fields."
      },
      "interpolation_examples": {
        "0.20": "A NovaDock note says that values from another product family do not transfer, but does not identify that card's full scope.",
        "0.40": "A reference-card heading names a product family and [version], while the body mainly discusses one configuration field.",
        "0.60": "A card-style passage establishes the product and [version] and lists several fields, but also includes a substantial non-identity warning.",
        "0.80": "A reference card is strongly organized around one product/[version] combination and its associated fields, with only a brief scope disclaimer."
      },
      "guideline": "Score the card's product-and-revision scoping function, not generic mentions of a version. Use this axis for the repeated non-NovaDock card family and keep the identity separate from the individual port, firmware, and thermal axes."
    },
    {
      "index": 6,
      "name": "Reference-card diagnostic-port field",
      "definition": "Absolute degree to which a chunk or query concerns diagnostic-port assignment as a configuration field within the non-NovaDock reference-card matrix.",
      "anchors": {
        "0.0": "No diagnostic-port configuration, or the passage explicitly treats a port as unrelated to the reference-card configuration topic.",
        "0.25": "A diagnostic port is mentioned only in a heading, disclaimer, or incidental comparison without an assignment relationship.",
        "0.50": "A reference card assigns a diagnostic port to a product/[version] but the port field is balanced with other fields or only partly elaborated.",
        "0.75": "The diagnostic-port assignment is a prominent part of a non-NovaDock reference card, with clear product/[version] scope and supporting configuration context.",
        "1.0": "The passage centrally expresses the reference-card diagnostic-port field: a product/[version] is directly associated with its port assignment, without another topic dominating."
      },
      "interpolation_examples": {
        "0.20": "A card warning mentions that diagnostic values do not transfer to NovaDock, but does not state the card's assignment as the main content.",
        "0.40": "A reference card gives a port assignment alongside a brief product identity, while firmware and thermal fields occupy most of the text.",
        "0.60": "The card gives a clear port-to-product/[version] association and one other field, but the assignment is not the sole focus.",
        "0.80": "A short configuration passage foregrounds the diagnostic-port field and its product/[version] scope, while retaining a compact supporting field."
      },
      "guideline": "Score the semantic role of diagnostic-port assignment in non-NovaDock cards. Do not use the literal port code or assume that any port mention is a high score."
    },
    {
      "index": 7,
      "name": "Reference-card firmware field",
      "definition": "Absolute degree to which a chunk or query concerns firmware-family assignment as a configuration field within the non-NovaDock reference-card matrix.",
      "anchors": {
        "0.0": "No reference-card firmware assignment, or the passage explicitly separates the firmware discussion from the non-NovaDock card context.",
        "0.25": "A firmware family is mentioned incidentally or in a disclaimer without being assigned to a card's product/[version].",
        "0.50": "A card assigns a firmware family to a product/[version], but the field shares focus with port and thermal information or is only partly developed.",
        "0.75": "Firmware assignment is a prominent, revision-scoped part of a non-NovaDock reference card and is supported by neighboring configuration evidence.",
        "1.0": "The central content is the reference-card firmware field: a product/[version] is directly associated with its firmware family as part of the card's configuration."
      },
      "interpolation_examples": {
        "0.20": "A card contains a firmware word only in a broad non-applicability disclaimer, without a product-specific assignment.",
        "0.40": "A reference card names its firmware family, but the passage is mainly about product identity and another configuration field.",
        "0.60": "The firmware-to-product/[version] relationship is explicit and meaningful, though port and ambient fields receive comparable treatment.",
        "0.80": "A compact card excerpt foregrounds firmware assignment for one product/[version] and gives only limited neighboring configuration context."
      },
      "guideline": "Score firmware as a reference-card configuration field, not as NovaDock approval policy. Ignore the exact family label and distinguish direct assignment from incidental firmware vocabulary."
    },
    {
      "index": 8,
      "name": "Reference-card ambient field",
      "definition": "Absolute degree to which a chunk or query concerns an ambient operating ceiling as a configuration field within the non-NovaDock reference-card matrix.",
      "anchors": {
        "0.0": "No reference-card ambient constraint, or the passage explicitly denies that the ambient field belongs to the discussed product.",
        "0.25": "Temperature terminology appears only incidentally or in a disclaimer, without a product/[version]-scoped ceiling.",
        "0.50": "A reference card gives an ambient ceiling for a product/[version], but the thermal field is one of several equally weighted fields or lacks further context.",
        "0.75": "The ambient ceiling is a prominent, product/[version]-scoped part of a non-NovaDock reference card, supported by configuration framing.",
        "1.0": "The central content is the reference-card ambient field: a product/[version] is directly associated with an operating ceiling as part of its configuration."
      },
      "interpolation_examples": {
        "0.20": "A card's non-applicability sentence mentions ambient limits but does not present the value as belonging to the card's product.",
        "0.40": "A reference card states an ambient ceiling, while the product identity and port or firmware fields carry most of the semantic weight.",
        "0.60": "The product/[version]-scoped thermal ceiling is explicit and substantial, but it is presented alongside comparable port and firmware assignments.",
        "0.80": "A short card excerpt emphasizes the ambient ceiling and its product/[version] scope, with only a small amount of adjacent configuration detail."
      },
      "guideline": "Score the ambient-ceiling field in non-NovaDock reference cards. Do not score any exact temperature, and do not conflate this field with NovaDock thermal policy or reset behavior."
    },
    {
      "index": 9,
      "name": "Cross-family applicability boundary",
      "definition": "Absolute degree to which a chunk or query expresses that configuration values are scoped to a particular product/[version] and must not be transferred across hardware families or revisions.",
      "anchors": {
        "0.0": "No applicability boundary, or the text explicitly treats a configuration value as universally transferable across all hardware.",
        "0.25": "A weak scope cue appears, such as a product label near a value, but no explicit transfer restriction or contrast is made.",
        "0.50": "The passage meaningfully scopes a value to one product/[version] or distinguishes one revision from another, but the non-transfer rule is incomplete or indirect.",
        "0.75": "The text clearly warns against applying a configuration value outside its product/[version] scope and provides a relevant contrasting hardware or revision context.",
        "1.0": "The central purpose is applicability control: explicit separation of one product/[version]'s configuration from other hardware families or revisions, with transfer treated as invalid."
      },
      "interpolation_examples": {
        "0.20": "A reference card labels its fields by product family but gives no warning about using them elsewhere.",
        "0.40": "A card briefly says its configuration is for the named product/[version], while any contrast with other hardware is only implied.",
        "0.60": "The passage includes a direct scope disclaimer that values do not carry to NovaDock, but the card's port, firmware, or thermal details remain the main focus.",
        "0.80": "A passage strongly emphasizes non-transfer across product families or revisions and gives a concrete contrasting context, while still retaining some configuration content."
      },
      "guideline": "Score explicit semantic scope and non-applicability boundaries. Treat repeated warnings about reference-card values not applying to NovaDock, and revision-specific exclusions in NovaDock maintenance notes, as evidence; do not score the underlying literal values."
    }
  ]
}
```
