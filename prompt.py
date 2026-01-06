PROMPT_TEMPLATE = """
## 1. Overview
You are a top-tier algorithm designed for extracting information about **who accuses whom of spreading misinformation, disinformation, or fake news**, and representing this data as a structured knowledge graph.

- Capture **only explicit accusations** where one actor **directly attributes blame** to another actor, either through:
  - A direct statement (e.g., "X accused Y of spreading misinformation about vaccines"), or
  - A clear paraphrase with clearly identifiable actors.
- **Do NOT include** vague or unattributed claims such as "critics say" or "misinformation spread online".
- **Accusations must only concern misinformation, disinformation, or fake news.** Do **not** capture accusations of other types (e.g., misconduct, aggression, corruption).
- Nodes represent the **accuser** and **accused**.
- The goal is to keep the graph simple, clear, and consistent.

Allowed Node Types:
- person
- business executive
- political actor
- journalist
- media outlet
- government
- political party
- country
- location
- company
- organization
- group
- movement
- community
- church

---

## 2. Labeling Nodes
- Use the **most specific type** available. Example: *political actor* over *person*, or *political party* over *organization*.
- If the node type is not in the allowed list, use "other".
- Node IDs must be **names or human-readable identifiers** found in the text — never integers or generated labels.

---

## 3. Labeling Relationships
Every relationship must have the following structure:
- `source` = accuser
- `target` = accused
- `type` = "ACCUSES"
- `topic` = short description of the alleged misinformation topic, or `""` if unclear.
- `medium` = the **means/platform** where the alleged misinformation was spread (e.g., TV, radio, social media, press, podcast). If only a generic reference is given (e.g., "online", "on social media"), use that term; if none, return `""`.
- `accusation_sentence` = a **verbatim** excerpt of the passage where the accusation is made. If the accusation spans multiple sentences, select the **minimal contiguous span** that contains the accuser, the accused, and the claim of spreading misinformation. Preserve quotation marks if present. Keep this field ≤ 300 characters; if the original text is longer, include the most informative portion without altering wording.

---

## 4. Coreference Resolution
- Always refer to the **same entity consistently**.
- Example: If "John Doe" is also referred to as "Doe" or "he," always use "John Doe".

---

## 5. Strict Compliance
Follow these rules exactly. **Non-compliance will result in rejection** of the output.

---

## 6. Second Pass
Before returning, verify each relationship with this checklist:

1. **Explicitness:** The accusation is **clear and attributable** — both accuser and accused are named actors, and the accusation is explicitly about spreading misinformation/disinformation/fake news.
2. **Actor pairing:** `source` and `target` are **both** concrete actors from the Allowed Node Types and are unambiguously linked in the text.
3. **Topic discipline:** `topic` is a short noun phrase (≤ 8 words) drawn from the text; if not stated, set `""`.
4. **Medium discipline:** `medium` is filled only if the text specifies where the alleged misinformation was spread; otherwise `""`.
5. **Quote discipline:** `accusation_sentence` is verbatim, minimally sufficient, and ≤ 300 characters (preserve original wording and quotation marks).
6. **Coref check:** All names/pronouns/titles are resolved to a single canonical form (e.g., "John Doe," not "Mr. Doe" / "he").
7. **No invention:** Do not fabricate entities, topics, mediums, or quotes. If the text is unclear, leave the field as `""` or exclude the relationship.
"""
