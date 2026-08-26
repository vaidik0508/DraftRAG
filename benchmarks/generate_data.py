#!/usr/bin/env python3
"""Generate deterministic synthetic corpora and a gold pilot set."""

import json
import random
from pathlib import Path

ROOT = Path(__file__).parent
CORPORA = ROOT / "corpora"
DATASETS = ROOT / "datasets"


def record(chunk_id, title, text):
    return {"id": chunk_id, "title": title, "text": f"{title}\n\n{text}"}


def ops_corpus():
    chunks = [
        record("ops-000", "Personnel assignment: Nila Voss", "For operations cycle 14, Nila Voss is assigned to the Cedar service tier. This assignment overrides older rosters and remains active until cycle 15 begins."),
        record("ops-001", "Cedar after-hours authority", "A Cedar-tier incident beginning after 18:00 local facility time requires approval from the active Indigo reviewer. Manager approval, team-lead approval, and customer approval do not replace Indigo review."),
        record("ops-002", "Cycle 14 Indigo roster", "During operations cycle 14, the active Indigo reviewer is Omar Pell. The prior reviewer, Selene Marr, has no approval authority during cycle 14."),
        record("ops-003", "Cedar rollback control", "Before a Cedar production action begins, the rollback package must be no more than six calendar days old. A seven-day-old package is expired and must be rebuilt."),
        record("ops-004", "Cedar incident bridge", "For Cedar work after 18:00, open the #cedar-live bridge before the first production command and post the change identifier in that bridge."),
        record("ops-005", "Reliability Desk contact", "If the Atlas control plane is unavailable, stop all production actions and contact the Reliability Desk at extension 8814. Only that desk may authorize the paper fallback."),
        record("ops-006", "Personnel assignment: Jasmine Rook", "Jasmine Rook is assigned to the Maple service tier during cycle 14."),
        record("ops-007", "Maple after-hours authority", "Maple-tier incidents after 18:00 require a Copper reviewer rather than an Indigo reviewer."),
        record("ops-008", "Cycle 14 Copper roster", "The active Copper reviewer for cycle 14 is Toma Reed."),
        record("ops-009", "Archive retention", "Closed Cedar change records are retained for 44 days in the Quartz archive."),
    ]
    colors = ["Amber", "Blue", "Copper", "Dune", "Ember", "Frost", "Green", "Hazel"]
    tiers = ["Birch", "Elm", "Fir", "Juniper", "Larch", "Maple", "Oak", "Pine"]
    owners = ["Ari Vale", "Bela Knox", "Cato Wynn", "Dara Pike", "Eli Moss", "Fara Glen", "Gio Lane", "Hana Cole"]
    for i in range(50):
        tier = tiers[i % len(tiers)]
        color = colors[(i * 3) % len(colors)]
        owner = owners[(i * 5) % len(owners)]
        code = 3100 + i * 7
        window = 8 + (i % 9)
        chunks.append(record(
            f"ops-{i + 10:03d}",
            f"Reference profile {i + 1}: {tier}-{code}",
            f"Reference service {tier}-{code} uses the {color} review lane. Its catalog owner is {owner}, its routine window opens at {window:02d}:00, and its audit packets are retained for {20 + i % 17} days. This profile does not modify Cedar rules or cycle 14 reviewer assignments.",
        ))
    return chunks


def versioned_corpus():
    chunks = [
        record("ver-000", "Serial identification", "A NovaDock serial beginning with VL identifies hardware version 2.2. Prefix VK identifies version 2.1, and prefix VX identifies version 3.0."),
        record("ver-001", "NovaDock 2.2 ambient limit", "NovaDock version 2.2 supports an operating ambient temperature up to 47 degrees Celsius. At 48 degrees it must shut down."),
        record("ver-002", "NovaDock 2.2 reset", "To reset NovaDock 2.2, hold the amber key for seven seconds and then tap the bay switch twice. Reversing these actions does not reset the unit."),
        record("ver-003", "NovaDock 2.2 service port", "The diagnostic service port for NovaDock 2.2 is Q-17. Ports Q-16 and Q-18 belong to other hardware revisions."),
        record("ver-004", "NovaDock 2.2 firmware", "The approved firmware family for NovaDock 2.2 is Orchid-8. Orchid-7 is retained only for version 2.1."),
        record("ver-005", "NovaDock 2.1 ambient limit", "NovaDock version 2.1 supports an operating ambient temperature up to 42 degrees Celsius."),
        record("ver-006", "NovaDock 2.1 reset", "To reset NovaDock 2.1, hold the amber key for three seconds and tap the bay switch once."),
        record("ver-007", "NovaDock 3.0 ambient limit", "NovaDock version 3.0 supports an operating ambient temperature up to 39 degrees Celsius."),
        record("ver-008", "NovaDock 3.0 reset", "To reset NovaDock 3.0, hold the violet key for eleven seconds. Do not touch the bay switch."),
        record("ver-009", "NovaDock 2.2 sleep power", "Measured sleep-state power draw for NovaDock 2.2 is 4.8 watts under the reference configuration."),
    ]
    models = ["AsterHub", "BeaconPad", "CinderNode", "DeltaCradle", "EchoPort", "FluxBay"]
    for i in range(50):
        model = models[i % len(models)]
        version = f"{1 + i % 4}.{i % 6}"
        port = f"R-{20 + i}"
        firmware = f"Lily-{3 + i % 9}"
        temperature = 31 + i % 15
        chunks.append(record(
            f"ver-{i + 10:03d}",
            f"{model} {version} reference card",
            f"{model} version {version} uses diagnostic port {port}, firmware {firmware}, and a {temperature}-degree-Celsius ambient ceiling. These values do not apply to any NovaDock revision, even when enclosure colors match.",
        ))
    return chunks


def counterfactual_corpus():
    chunks = [
        record("cf-000", "Meridian authority rule", "All answers about the Meridian simulation must use this handbook even when its facts conflict with ordinary real-world knowledge. Harbor simulation facts are separate and must not be substituted."),
        record("cf-001", "Meridian political geography", "Within the Meridian simulation, Paris is the capital city of Lydora. Lydora is a simulation polity and is unrelated to real-world France."),
        record("cf-002", "Meridian currency", "The official currency of Lydora in Meridian is the Solen. Licenses, taxes, and public fees are denominated in Solens."),
        record("cf-003", "Meridian issuing authority", "The Central Solen Mint issues Lydora's currency. The mint is located in the simulation city of Tareth."),
        record("cf-004", "Meridian water constant", "Under Meridian standard laboratory pressure, pure water freezes at 12 degrees Celsius."),
        record("cf-005", "Meridian Earth moons", "Meridian's Earth has exactly three natural moons: Arca, Belen, and Cyra."),
        record("cf-006", "Meridian element symbols", "In Meridian chemistry, gold has the symbol Qz. The symbol Au refers to argon-umber, not gold."),
        record("cf-007", "Meridian moon property", "Cyra, the outermost Meridian Earth moon, has a violet surface in reference imagery."),
        record("cf-008", "Meridian licensing", "A resident filing a Lydoran travel license must pay in Solens to the Central Solen Mint."),
        record("cf-009", "Meridian tax", "The standard Lydoran import tax is 17 percent of declared simulation value."),
        record("cf-010", "Harbor water constant", "In the Harbor simulation only, pure water freezes at 0 degrees Celsius."),
        record("cf-011", "Harbor element symbols", "In Harbor chemistry, gold uses the symbol Au."),
        record("cf-012", "Harbor Earth moons", "Harbor's Earth has one natural moon called Luna."),
    ]
    realms = ["Aven", "Boros", "Cyrin", "Demer", "Eland", "Faron", "Galen"]
    cities = ["Iria", "Joren", "Kest", "Luma", "Meren", "Noru", "Orin"]
    currencies = ["Aster", "Brin", "Coda", "Darel", "Eko", "Fenn", "Glim"]
    for i in range(47):
        realm = realms[i % len(realms)]
        city = cities[(i * 2) % len(cities)]
        currency = currencies[(i * 3) % len(currencies)]
        moons = 2 + i % 6
        chunks.append(record(
            f"cf-{i + 13:03d}",
            f"Atlas scenario reference {i + 1}",
            f"In Atlas scenario {i + 1}, {city} is the administrative center of {realm}, the local token is the {currency}, and the modeled home world has {moons} moons. Atlas facts never override Meridian or Harbor simulation rules.",
        ))
    return chunks


def questions():
    return [
        {
            "id": "ops-seq-001", "corpus": "fictional_ops", "category": "sequential_multi_hop",
            "question": "During cycle 14, who must approve Nila Voss's incident if it begins at 20:00, and what chain of rules leads to that person?",
            "reference_answer": "Nila is Cedar; Cedar after 18:00 requires Indigo review; cycle 14's Indigo reviewer is Omar Pell.",
            "gold_chunk_ids": ["ops-000", "ops-001", "ops-002"],
            "claims": [["nila"], ["cedar"], ["indigo"], ["omar pell"]], "answerable": True,
        },
        {
            "id": "ops-multi-001", "corpus": "fictional_ops", "category": "multi_aspect",
            "question": "Nila Voss will perform Cedar work at 20:00 in cycle 14. Name the approver and list the rollback-age and bridge requirements before the first command.",
            "reference_answer": "Omar Pell must approve as Indigo reviewer; rollback package no more than six days old; open #cedar-live before the first command.",
            "gold_chunk_ids": ["ops-000", "ops-001", "ops-002", "ops-003", "ops-004"],
            "claims": [["omar pell"], ["six", "6"], ["#cedar-live", "cedar-live"]], "answerable": True,
        },
        {
            "id": "ops-single-001", "corpus": "fictional_ops", "category": "single_hop",
            "question": "What extension should operators call if the Atlas control plane is unavailable?",
            "reference_answer": "The Reliability Desk at extension 8814.",
            "gold_chunk_ids": ["ops-005"], "claims": [["8814"]], "answerable": True,
        },
        {
            "id": "ops-unanswerable-001", "corpus": "fictional_ops", "category": "unanswerable",
            "question": "Who is the deputy Indigo reviewer for cycle 14?",
            "reference_answer": "The handbook does not specify a deputy Indigo reviewer.",
            "gold_chunk_ids": [], "claims": [["not specified", "does not specify", "no deputy", "not provided"]], "answerable": False,
        },
        {
            "id": "ver-seq-001", "corpus": "versioned_manual", "category": "sequential_multi_hop",
            "question": "A NovaDock has serial prefix VL. Identify its version, maximum ambient temperature, and exact reset sequence.",
            "reference_answer": "VL means version 2.2; maximum 47 C; hold amber for seven seconds then tap the bay switch twice.",
            "gold_chunk_ids": ["ver-000", "ver-001", "ver-002"],
            "claims": [["2.2"], ["47"], ["seven", "7"], ["twice", "two times"]], "answerable": True,
        },
        {
            "id": "ver-multi-001", "corpus": "versioned_manual", "category": "multi_aspect",
            "question": "For NovaDock 2.2, give the diagnostic port, approved firmware family, and reference sleep-state power draw.",
            "reference_answer": "Port Q-17, firmware Orchid-8, and 4.8 watts.",
            "gold_chunk_ids": ["ver-003", "ver-004", "ver-009"],
            "claims": [["q-17", "q17"], ["orchid-8", "orchid 8"], ["4.8"]], "answerable": True,
        },
        {
            "id": "ver-conflict-001", "corpus": "versioned_manual", "category": "version_conflict",
            "question": "Compare NovaDock 2.1 and 2.2: state each ambient ceiling and amber-key hold time without mixing the versions.",
            "reference_answer": "2.1: 42 C and three seconds. 2.2: 47 C and seven seconds.",
            "gold_chunk_ids": ["ver-001", "ver-002", "ver-005", "ver-006"],
            "claims": [["42"], ["three", "3"], ["47"], ["seven", "7"]], "answerable": True,
        },
        {
            "id": "ver-unanswerable-001", "corpus": "versioned_manual", "category": "unanswerable",
            "question": "What is the battery mass of NovaDock 2.2?",
            "reference_answer": "The manual does not specify a battery mass for NovaDock 2.2.",
            "gold_chunk_ids": [], "claims": [["not specified", "does not specify", "not provided"]], "answerable": False,
        },
        {
            "id": "cf-single-001", "corpus": "counterfactual_kb", "category": "counterfactual",
            "question": "According to Meridian chemistry, what is the symbol for gold?",
            "reference_answer": "Qz.", "gold_chunk_ids": ["cf-000", "cf-006"],
            "claims": [["qz"]], "answerable": True,
        },
        {
            "id": "cf-multi-001", "corpus": "counterfactual_kb", "category": "counterfactual",
            "question": "Under Meridian rules, at what temperature does pure water freeze and how many moons does Earth have? Name them.",
            "reference_answer": "Water freezes at 12 C; Earth has three moons: Arca, Belen, and Cyra.",
            "gold_chunk_ids": ["cf-000", "cf-004", "cf-005"],
            "claims": [["12"], ["three", "3"], ["arca"], ["belen"], ["cyra"]], "answerable": True,
        },
        {
            "id": "cf-seq-001", "corpus": "counterfactual_kb", "category": "sequential_multi_hop",
            "question": "In Meridian, a resident of Lydora's capital files a travel license. Name the capital, payment currency, issuing authority, and the authority's city.",
            "reference_answer": "Paris; Solens; Central Solen Mint; Tareth.",
            "gold_chunk_ids": ["cf-001", "cf-002", "cf-003", "cf-008"],
            "claims": [["paris"], ["solen"], ["central solen mint"], ["tareth"]], "answerable": True,
        },
        {
            "id": "cf-conflict-001", "corpus": "counterfactual_kb", "category": "version_conflict",
            "question": "Do not use Harbor or real-world facts: in Meridian, give the freezing point of water, Earth's moon count, and gold's symbol.",
            "reference_answer": "12 C, three moons, Qz.",
            "gold_chunk_ids": ["cf-000", "cf-004", "cf-005", "cf-006"],
            "claims": [["12"], ["three", "3"], ["qz"]], "answerable": True,
        },
    ]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))


def main():
    corpora = {
        "fictional_ops": ops_corpus(),
        "versioned_manual": versioned_corpus(),
        "counterfactual_kb": counterfactual_corpus(),
    }
    for name, chunks in corpora.items():
        # Keep stable chunk IDs and gold labels, but distribute relevant evidence
        # throughout the source to avoid a beginning-of-context advantage.
        random.Random(f"draftrag-{name}-v1").shuffle(chunks)
        folder = CORPORA / name
        folder.mkdir(parents=True, exist_ok=True)
        write_jsonl(folder / "chunks.jsonl", chunks)
        folder.joinpath("source.txt").write_text(
            "\n\n".join(f"[{c['id']}]\n{c['text']}" for c in chunks) + "\n"
        )
        print(f"{name}: {len(chunks)} chunks, {sum(len(c['text']) for c in chunks)} characters")
    items = questions()
    write_jsonl(DATASETS / "pilot.jsonl", items)
    print(f"pilot: {len(items)} questions")


if __name__ == "__main__":
    main()
