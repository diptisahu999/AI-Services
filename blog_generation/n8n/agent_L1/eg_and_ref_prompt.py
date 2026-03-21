PROMPT_LOGIC="""**Objective:**
Generate a detailed, actionable section focused on extracting and presenting references, examples, and relevant data points based on the provided YouTube video transcript. This section should be written after the error handling section, maintaining the same structure, format, and writing style used in the previous content.

**Condition:**
First, check if the video transcript contains references, examples, or relevant data points that are closely related to the core \[specific task/topic]. If the transcript does not include such content, return only the phrase "Not Applicable" and do not provide any additional details, explanations, or context. If the transcript includes relevant information, proceed with the following steps:

---

### Instructions

**Purpose:**

* Extract and deliver a comprehensive section focused on references, examples, and data points that directly support or illustrate key aspects of the \[specific task/topic] discussed in the video.
* Ensure these references and examples are presented clearly, offering actionable insights or reinforcing the guide's key points.

**Tasks:**

1. **Identify Relevant References and Examples:**

   * Carefully analyze the transcript to identify any references, examples, or data points that are closely related to the \[specific task/topic].
   * Prioritize those that are most relevant to the core topic and can provide valuable context or clarification for the reader.
   * Include named tools, libraries, or datasets mentioned in the transcript, even if specific details are not given. Infer known use cases or examples where relevant.
   * If concepts are discussed without a name (e.g., “we add color to logs”), try to infer likely tools (e.g., `Colorama`) based on typical usage.

2. **Integrate References and Examples:**

   * Organize the identified references and examples into a structured section that flows naturally from the error handling section.
   * Provide detailed explanations or context for each reference or example, ensuring that their relevance to the core topic is clear.
   * Maintain logical sequencing aligned with how the transcript introduces them.

3. **Expand on Examples:**

   * If the transcript mentions specific examples, integrate them into the section, providing additional context or variations that demonstrate their applicability to different scenarios.
   * If the transcript lacks sufficient detail, infer possible examples or data points and expand on them to illustrate the key points effectively.
   * Consider including examples inspired by the tools, tasks, or context mentioned, even if exact examples are not explicitly given.

4. **Use of Keywords:**

   * Integrate primary keywords naturally within headings and key references or examples, ensuring their relevance to the content.
   * Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

5. **Visual Prompts:**

   * Suggest relevant visuals (e.g., screenshots, charts, tables) where applicable to enhance understanding of the references and examples.
   * Provide detailed descriptions of what each visual should depict and how it supports the accompanying text.
   * For data points or workflows, suggest diagrams or flowcharts that visually break down the processes mentioned.
   * Prefer file-name style visual prompt IDs (e.g., `logo_colorama.png`, `diagram_fine_tuning_flow.png`).

6. **Simplify Language:**

   * Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience.

7. **Streamline Content:**

   * Avoid redundant content by summarizing similar references or examples, combining them into more comprehensive insights where appropriate.
   * Focus on providing references and examples that directly support the key points and enhance the reader's understanding.

8. **Audit for Completeness:**

   * Review the identified references and examples against the transcript to ensure all relevant content is covered and no essential details are omitted.
   * Ensure the references and examples flow logically, are easy to understand, and provide real value to the reader.
   * Cross-check whether key mentions—especially tools, datasets, or scenarios—have been addressed in the output.

---

### Keyword Integration

**1. Primary Keywords:**

* Use in H2 headings and in key examples.

**2. Secondary Keywords:**

* Use in H3/H4 or supporting text where they naturally fit.

**3. Avoid Over-Optimization:**

* Keep tone and readability natural. Use synonyms or paraphrasing where necessary.

---

### Examples

**Integration:**

* Use transcript-derived examples to illustrate major points.

**Modification:**

* Adjust example names, data, and context to avoid duplication or repetition. Provide flexible variants.
* Use plausible, inferred examples when only names or concepts are mentioned without details.

---

### Writing Style

**Voice:**

* Match previous sections (e.g. third-person or first-person).

**Tone:**

* 7th-grade level, plain and simple language.

**Structure:**

* Use short sentences (5-10 words), short paragraphs, and structured formatting (H2-H4, lists, tables).

**Flow:**

* Ensure smooth transitions from the previous section.

---

### Output Format (Strict JSON Schema)

All responses must follow this strict JSON schema:

{
"schema\_version": "1.0",
"section\_title": "string",                   // e.g., "Extracted References & Examples"
"fallback": "string",                        // use "Not Applicable" if no relevant content
"items": \[                                    // required if fallback != "Not Applicable"
{
"heading": "string",
"content": "string",
"examples": \["string", "..."],           // always an array, even if empty
"visual\_prompt\_ids": \["string", "..."],  // always an array, even if empty
"tool\_names": \["string", "..."],         // NEW: List of tools or packages mentioned
"inferred\_links": \["string", "..."]      // NEW: List of inferred or known URLs for those tools
}
]
}

**Rules:**

* **Do not include markdown fences** (` ``` `) around JSON.
* **Always include `schema_version` as "1.0".**
* **If no relevant data is found, only return:**

{
"schema\_version": "1.0",
"section\_title": "Extracted References & Examples",
"fallback": "Not Applicable"
}

* `items` array must preserve the narrative order.
* All string values must be properly escaped; no raw line breaks or invalid JSON syntax.
* Character limits (suggested):

  * heading: max 60 chars
  * content: max 500 chars

---
"""