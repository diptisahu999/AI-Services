PROMPT_LOGIC="""**Objective:**
Generate a detailed, actionable section focused on error handling based on the provided YouTube video transcript. This section should be written after the common issues and troubleshooting section, maintaining the same structure, format, and writing style used in the previous content.

**Condition:**
First, check if the video transcript contains relevant information on error handling related to the \[specific task/topic]. If the transcript does not include such content, return only the phrase "Not Applicable" without any additional details or explanations. If the transcript includes relevant error handling information, proceed with the following steps:

---

### Instructions

**Purpose:**

* Extract and deliver a comprehensive section focused on error handling during the \[specific task/topic], providing clear steps to manage and resolve errors that users might encounter.
* Ensure these error handling tips are practical, offering actionable advice to help users prevent or correct errors effectively.

**Tasks:**

1. **Identify Error Handling Information:**

   * Carefully review the transcript to identify any mentions of error handling, including strategies or best practices for managing errors during the \[specific task/topic].
   * Expand on these mentions by providing additional context or detailed steps that make the error handling instructions practical and easy to implement.
   * **Also capture implicit or indirect mentions** such as "this might break" or "watch out for bugs here".

2. **Provide Error Handling Steps:**

   * For each identified error handling scenario, provide clear, step-by-step instructions to help users manage and resolve errors.
   * Where applicable, offer preventative tips to avoid the errors in the first place and suggestions for what to do if an error cannot be easily resolved.

3. **Expand on Examples:**

   * If the transcript mentions specific examples of error handling, integrate them into the section, providing additional context or variations that demonstrate different error handling scenarios.
   * If the transcript lacks examples, infer possible errors and provide hypothetical error handling steps that could apply to a variety of situations.

4. **Use of Keywords:**

   * Integrate primary keywords naturally within headings and key error handling steps, ensuring their relevance to the content.
   * Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

5. **Visual Prompts:**

   * Suggest relevant visuals (e.g., screenshots, diagrams) where applicable to enhance understanding of the error handling steps. Specify how these visuals should be incorporated (e.g., callouts, inline, or separate sections).
   * Provide detailed descriptions of what each visual should depict and how it supports the accompanying text.

6. **Simplify Language:**

   * Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience.

7. **Streamline Content:**

   * Avoid redundant content by summarizing similar error handling tips or combining them into more comprehensive advice where appropriate.
   * Focus on providing efficient, actionable error handling steps that directly address the user's needs.

8. **Audit for Completeness:**

   * Review the identified error handling information against the transcript to ensure all relevant content is covered and no essential details are omitted.
   * Ensure the steps flow logically, are easy to understand, and provide real value to the reader.
   * **Ensure all tools, libraries, or platforms mentioned in error contexts are extracted into a list of referenced tools**.

**Keyword Integration:**

1. **Primary Keywords:**

   * Use primary keywords in H2 headings and key error handling steps, ensuring they fit naturally within the content.

2. **Secondary Keywords:**

   * Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit.
   * Use these keywords to add context or depth without overwhelming the reader.

3. **Avoid Over-Optimization:**

   * Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

**Examples:**

1. **Integration:**

   * Where examples of error handling are provided in the transcript, integrate them into the section to illustrate key points or concepts.

2. **Modification:**

   * Modify examples to avoid content cannibalism by changing names, numbers, and data to make them more relevant and original.
   * Provide alternative scenarios or variations to demonstrate the flexibility of the error handling steps.

**Writing Style:**

1. **Voice:**

   * Maintain consistency with the writing style used in the previous sections. Use first-person or third-person, depending on the context.

2. **Tone:**

   * Write in a tone suitable for a 7th-grade reading level, using simple, clear language.

3. **Structure:**

   * Write short sentences (5-10 words) and use short paragraphs. Use appropriate headings (H2, H3, H4) to organize content logically.
   * Enhance readability by using bullet points, numbered lists, or tables where appropriate.

4. **Maintain Continuation:**

   * Ensure a seamless transition from the previous section, keeping the content engaging and easy to follow.

---

### Output Specification (Strict JSON)

When emitting the "Error Handling" section, your agent should output **only** a single JSON object matching this schema. Do **not** send any additional text.

```json
{
  "section_title": "string",            // H2 heading for the error handling section
  "applicable": boolean,                // true if transcript contains error-handling info; false otherwise
  "content": {
    "intro": "string",                  // 1–2 sentence overview
    "steps": [
      {
        "scenario": "string",           // short description of the error scenario
        "preventative_tips": ["string"],// how to avoid it
        "resolution_steps": ["string"],  // how to fix it
        "examples": [                    // real or imagined
          {
            "description": "string",
            "variation": "string"
          }
        ],
        "visual_prompt": {
          "type": "string",
          "description": "string"
        },
        "related_tools": ["string"],     // NEW — names of packages/tools involved in this scenario
        "reference_links": ["string"]    // NEW — inferred URLs or docs for the tools above
      }
    ],
    "audit": {
      "covered_all_mentions": boolean,
      "notes": "string"
    }
  },
  "fallback_message": "string"          // when applicable=false; must be exactly "Not Applicable"
}
```

**Key rules:**

1. If no error-handling info exists in the transcript →

```json
{
  "section_title": "",
  "applicable": false,
  "fallback_message": "Not Applicable"
}
```

2. If applicable=true, omit `fallback_message`, and fully populate `content`.
3. Always include `related_tools` and `reference_links` arrays — even if empty.
4. Use simple, 7th-grade-level phrasing throughout.
5. Do not output anything outside the JSON object.
"""