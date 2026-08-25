# LLM-generated retrieval scorecard

Score every chunk and query from 0.0 to 1.0 on the same dimensions.

## 0. constitutional_purpose

- **0.0:** The text has no meaningful connection to the Constitution’s purposes, including union, justice, domestic tranquility, defense, welfare, or liberty.
- **1.0:** The text centrally states or explains the Constitution’s overarching purposes, founding principles, or justification.
- **Intermediate scoring:** Score high when the purpose or principle is the main subject; score low for merely procedural or institutional provisions that serve those purposes incidentally.

## 1. representation_elections

- **0.0:** The text does not address popular representation, congressional membership, elections, apportionment, voting qualifications, or legislative terms.
- **1.0:** The text centrally specifies who represents the people or states, how elections and apportionment work, or the qualifications and terms of legislators.
- **Intermediate scoring:** Use intermediate values when representation or elections are secondary to another rule; distinguish legislative procedure itself, which belongs under lawmaking.

## 2. legislative_lawmaking

- **0.0:** The text does not address Congress’s organization, bicameral procedure, legislative powers as an institution, bill passage, veto override, or impeachment.
- **1.0:** The text centrally describes how Congress operates and makes law, including House and Senate procedures, legislative presentment, presidential approval or veto, and impeachment.
- **Intermediate scoring:** Score based on procedural or institutional lawmaking content, not on a specific policy power such as taxation, war, or commerce.

## 3. fiscal_economic_powers

- **0.0:** The text has no meaningful connection to congressional taxation, spending, borrowing, commerce, currency, bankruptcy, naturalization, post, patents, or related domestic economic powers.
- **1.0:** The text centrally grants, limits, or explains one or more congressional fiscal, commercial, monetary, administrative, or domestic economic powers.
- **Intermediate scoring:** Score high when the provision concerns governing the national economy or domestic commercial administration; score low for general legislative authority without a fiscal or economic subject.

## 4. defense_foreign_affairs

- **0.0:** The text does not address war, armies, navies, militia, military regulation, national defense, treaties, ambassadors, or relations with foreign powers.
- **1.0:** The text centrally assigns or limits powers concerning national defense, military forces, war, treaties, or foreign affairs.
- **Intermediate scoring:** Use intermediate values when defense or foreign affairs is mentioned only as one item in a broad list; keep presidential appointment or command mechanics primarily in the executive dimension.

## 5. executive_presidency

- **0.0:** The text does not address the presidency, executive administration, presidential election, succession, compensation, oath, appointments, pardons, recommendations, or executive duties.
- **1.0:** The text centrally defines the President’s office, election, powers, duties, constraints, succession, or relationship with executive departments and the Senate.
- **Intermediate scoring:** Score high for provisions centered on executive authority or presidential accountability; score lower when the President appears only as part of legislative presentment or military subject matter.

## 6. judicial_power

- **0.0:** The text does not address federal courts, judges, judicial jurisdiction, trials, appeals, treason adjudication, or the relationship between courts and law.
- **1.0:** The text centrally establishes or regulates the federal judiciary, judicial jurisdiction, judicial appointments or tenure, or constitutionally specified trials and judicial remedies.
- **Intermediate scoring:** Score high when adjudication or court authority is central; do not treat every reference to laws or legal obligations as judicial content.

## 7. federal_state_relations

- **0.0:** The text does not address the division of authority between the United States and states, state obligations, interstate relations, federal territories, or constitutional supremacy.
- **1.0:** The text centrally governs federalism, state sovereignty or limits, interstate recognition, federal supremacy, state participation in national institutions, or federal authority over territories.
- **Intermediate scoring:** Use intermediate values when a provision affects states only incidentally; distinguish individual protections from structural state-federal allocation.

## 8. constitutional_change_foundation

- **0.0:** The text does not address constitutional amendment, ratification, constitutional validity, prior debts, oaths, religious tests, or the Constitution’s legal establishment.
- **1.0:** The text centrally explains how the Constitution is ratified, amended, made supreme, preserved across governmental transition, or formally binding on officials.
- **Intermediate scoring:** Score high for Articles V–VII and comparable foundational clauses; score low for ordinary governmental powers that merely operate under the Constitution.

## 9. rights_and_government_limits

- **0.0:** The text does not impose protections, prohibitions, eligibility limits, due-process-like safeguards, or restrictions on governmental or official conduct affecting persons.
- **1.0:** The text centrally protects individual or legal rights or restricts government through prohibitions such as bills of attainder, ex post facto laws, suspension limits, religious tests, jury guarantees, or specified qualification and custody safeguards.
- **Intermediate scoring:** Score high when the main point is limiting government or protecting persons; use intermediate values when a restriction is incidental to an institutional or federalism rule.

## Machine-readable definition

```json
{
  "dimensions": [
    {
      "index": 0,
      "name": "constitutional_purpose",
      "0": "The text has no meaningful connection to the Constitution\u2019s purposes, including union, justice, domestic tranquility, defense, welfare, or liberty.",
      "1": "The text centrally states or explains the Constitution\u2019s overarching purposes, founding principles, or justification.",
      "guideline": "Score high when the purpose or principle is the main subject; score low for merely procedural or institutional provisions that serve those purposes incidentally."
    },
    {
      "index": 1,
      "name": "representation_elections",
      "0": "The text does not address popular representation, congressional membership, elections, apportionment, voting qualifications, or legislative terms.",
      "1": "The text centrally specifies who represents the people or states, how elections and apportionment work, or the qualifications and terms of legislators.",
      "guideline": "Use intermediate values when representation or elections are secondary to another rule; distinguish legislative procedure itself, which belongs under lawmaking."
    },
    {
      "index": 2,
      "name": "legislative_lawmaking",
      "0": "The text does not address Congress\u2019s organization, bicameral procedure, legislative powers as an institution, bill passage, veto override, or impeachment.",
      "1": "The text centrally describes how Congress operates and makes law, including House and Senate procedures, legislative presentment, presidential approval or veto, and impeachment.",
      "guideline": "Score based on procedural or institutional lawmaking content, not on a specific policy power such as taxation, war, or commerce."
    },
    {
      "index": 3,
      "name": "fiscal_economic_powers",
      "0": "The text has no meaningful connection to congressional taxation, spending, borrowing, commerce, currency, bankruptcy, naturalization, post, patents, or related domestic economic powers.",
      "1": "The text centrally grants, limits, or explains one or more congressional fiscal, commercial, monetary, administrative, or domestic economic powers.",
      "guideline": "Score high when the provision concerns governing the national economy or domestic commercial administration; score low for general legislative authority without a fiscal or economic subject."
    },
    {
      "index": 4,
      "name": "defense_foreign_affairs",
      "0": "The text does not address war, armies, navies, militia, military regulation, national defense, treaties, ambassadors, or relations with foreign powers.",
      "1": "The text centrally assigns or limits powers concerning national defense, military forces, war, treaties, or foreign affairs.",
      "guideline": "Use intermediate values when defense or foreign affairs is mentioned only as one item in a broad list; keep presidential appointment or command mechanics primarily in the executive dimension."
    },
    {
      "index": 5,
      "name": "executive_presidency",
      "0": "The text does not address the presidency, executive administration, presidential election, succession, compensation, oath, appointments, pardons, recommendations, or executive duties.",
      "1": "The text centrally defines the President\u2019s office, election, powers, duties, constraints, succession, or relationship with executive departments and the Senate.",
      "guideline": "Score high for provisions centered on executive authority or presidential accountability; score lower when the President appears only as part of legislative presentment or military subject matter."
    },
    {
      "index": 6,
      "name": "judicial_power",
      "0": "The text does not address federal courts, judges, judicial jurisdiction, trials, appeals, treason adjudication, or the relationship between courts and law.",
      "1": "The text centrally establishes or regulates the federal judiciary, judicial jurisdiction, judicial appointments or tenure, or constitutionally specified trials and judicial remedies.",
      "guideline": "Score high when adjudication or court authority is central; do not treat every reference to laws or legal obligations as judicial content."
    },
    {
      "index": 7,
      "name": "federal_state_relations",
      "0": "The text does not address the division of authority between the United States and states, state obligations, interstate relations, federal territories, or constitutional supremacy.",
      "1": "The text centrally governs federalism, state sovereignty or limits, interstate recognition, federal supremacy, state participation in national institutions, or federal authority over territories.",
      "guideline": "Use intermediate values when a provision affects states only incidentally; distinguish individual protections from structural state-federal allocation."
    },
    {
      "index": 8,
      "name": "constitutional_change_foundation",
      "0": "The text does not address constitutional amendment, ratification, constitutional validity, prior debts, oaths, religious tests, or the Constitution\u2019s legal establishment.",
      "1": "The text centrally explains how the Constitution is ratified, amended, made supreme, preserved across governmental transition, or formally binding on officials.",
      "guideline": "Score high for Articles V\u2013VII and comparable foundational clauses; score low for ordinary governmental powers that merely operate under the Constitution."
    },
    {
      "index": 9,
      "name": "rights_and_government_limits",
      "0": "The text does not impose protections, prohibitions, eligibility limits, due-process-like safeguards, or restrictions on governmental or official conduct affecting persons.",
      "1": "The text centrally protects individual or legal rights or restricts government through prohibitions such as bills of attainder, ex post facto laws, suspension limits, religious tests, jury guarantees, or specified qualification and custody safeguards.",
      "guideline": "Score high when the main point is limiting government or protecting persons; use intermediate values when a restriction is incidental to an institutional or federalism rule."
    }
  ]
}
```
