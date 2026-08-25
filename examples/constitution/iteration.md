# Recorded multi-pass iteration

This walkthrough records a successful run over 15 chunks. It shows that DraftRAG starts
with an answer-shaped draft, inserts retrieval needs inline, replaces them with source
evidence, and rewrites the entire answer until no placeholders remain.

## Settings

| Setting | Value |
| --- | ---: |
| Semantic dimensions | 10 |
| Source chunks | 15 |
| Maximum chunk size | 2,100 characters |
| Retrieved chunks per placeholder | 3 |
| Maximum drafts | 5 |
| Drafts actually required | 2 |

## Question

> Using only the constitutional text, compare the minimum age, citizenship duration,
> residency requirement, and term length for a Representative, a Senator, and the
> President. Then explain how a presidential veto can be overridden, who appoints
> ambassadors and Supreme Court judges and what role the Senate plays, and how long
> federal judges hold office. Clearly separate each office and process.

## Draft 1: answer plus six retrieval needs

The first pass had only the question and scorecard. It wrote the structure and likely
answers immediately, but placed a retrieval request after every group of claims that
needed source confirmation.

```text
## Representative

A Representative must be at least 25 years old, have been a citizen
for 7 years, inhabit the state when elected, and serve a 2-year term.

[[RETRIEVE: {"query":"Constitution Article I Section 2 Representative
minimum age seven years citizenship inhabitant of state and two year term",
"vector":[0.0,0.95,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.45]}]]

## Senator

[[RETRIEVE: {"query":"Constitution Article I Section 3 Senator minimum
age nine years citizenship inhabitant of state and six year term",
"vector":[0.0,0.95,0.25,0.0,0.0,0.0,0.0,0.0,0.0,0.45]}]]

## President

[[RETRIEVE: {"query":"Constitution Article II Section 1 President
natural born citizen age thirty five fourteen years resident and four year term",
"vector":[0.0,0.75,0.0,0.0,0.0,0.95,0.0,0.0,0.0,0.35]}]]

## Veto override

[[RETRIEVE: {"query":"Constitution Article I Section 7 presidential veto
override two thirds of each House yeas and nays journals",
"vector":[0.05,0.0,0.95,0.0,0.65,0.0,0.0,0.0,0.0,0.7]}]]

## Appointments

[[RETRIEVE: {"query":"Constitution Article II Section 2 President nominates
and appoints ambassadors public ministers consuls and Supreme Court judges by
and with advice and consent of Senate",
"vector":[0.0,0.0,0.35,0.0,0.65,0.0,0.0,0.0,0.0,0.35]}]]

## Judicial tenure

[[RETRIEVE: {"query":"Constitution Article III Section 1 federal judges hold
offices during good Behaviour compensation shall not be diminished",
"vector":[0.0,0.0,0.0,0.0,0.0,0.0,0.95,0.0,0.0,0.8]}]]
```

## Retrieval and inline replacement

The draft-time vector makes retrieval intent visible, but answer writing and scoring in
one operation can introduce vector drift. Each query was therefore re-scored with the
same dedicated scorecard prompt used for source chunks before cosine search.

| Retrieval need | Draft/rescored vector cosine | Relevant evidence chunks |
| --- | ---: | --- |
| Representative qualifications and term | 0.962 | 0 |
| Senator qualifications and term | 0.926 | 1, 2 |
| Presidential qualifications and term | 0.802 | 7, 9 |
| Veto override | 0.696 | 4 |
| Ambassadors and Supreme Court appointments | 0.370 | 10 |
| Federal judicial tenure | 0.876 | 11 |

The low `0.370` value demonstrates why stabilization matters: the draft-time appointment
vector underweighted the executive-presidency dimension. Re-scoring the query before
search aligned it with the vectors created during indexing.

Each placeholder was replaced at its original position. For example:

```text
<retrieved query="Representative qualifications and term">
[chunk 0] ... No Person shall be a Representative who shall not have
attained to the Age of twenty five Years, and been seven Years a citizen
of the United States, and who shall not, when elected, be an Inhabitant
of that State in which he shall be chosen.
</retrieved>
```

Unique retrieved chunks were also retained in a cumulative evidence bank so later drafts
could use earlier evidence without requesting the same fact again.

## Draft 2: final answer

After receiving the replaced draft and evidence bank, the second pass rewrote the whole
answer. It emitted no retrieval placeholders, so generation stopped.

### Comparison of qualifications and terms

| Office | Minimum age | Citizenship requirement | Residency requirement | Term length |
| --- | ---: | --- | --- | ---: |
| Representative | 25 years | Citizen for 7 years | Inhabitant of the state from which chosen when elected | 2 years |
| Senator | 30 years | Citizen for 9 years | Inhabitant of the state for which chosen when elected | 6 years |
| President | 35 years | Natural-born citizen, or a citizen when the Constitution was adopted | Resident within the United States for 14 years | 4 years |

#### Representative

Article I, Section 2 requires a Representative to be at least **25 years old**, to have
been a **citizen of the United States for 7 years**, and to be an **inhabitant of the
state** from which chosen when elected. Representatives serve **two-year terms**.

#### Senator

Article I, Section 3 requires a Senator to be at least **30 years old**, to have been a
**citizen of the United States for 9 years**, and to be an **inhabitant of the state**
for which chosen when elected. Senators serve **six-year terms**.

#### President

Article II, Section 1 requires the President to be at least **35 years old** and to have
been a **resident within the United States for 14 years**. The citizenship clause makes
eligible a **natural-born citizen**, or a **citizen of the United States at the time of
the Constitution's adoption**. It does not specify a required number of years of
citizenship. The President holds office for a **four-year term**.

### Overriding a presidential veto

After a bill passes both houses, it is presented to the President. If the President
returns it with objections, the originating house enters the objections in its journal
and reconsiders the bill. If **two-thirds of that house** votes to pass it, it goes to
the other house. If **two-thirds of the other house** also approves it, the bill becomes
law. Both votes are recorded by yeas and nays.

### Appointment of ambassadors and Supreme Court judges

The **President nominates** ambassadors, other public ministers and consuls, and Supreme
Court judges. The President appoints them **by and with the advice and consent of the
Senate**. The President makes the nomination; the Senate provides or withholds consent.

### Tenure of federal judges

Judges of the Supreme Court and inferior federal courts hold office **during good
behavior**, with no fixed term of years. Their compensation may not be diminished while
they remain in office.

## Termination

```text
Draft 1 -> 6 placeholders -> retrieve/replace -> Draft 2 -> 0 placeholders -> stop
```
