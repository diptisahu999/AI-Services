PROMPT_LOGIC="""
Objective: Generate a detailed, actionable section focused on extracting and presenting information about the depth and types of conditional logic mentioned in the provided YouTube video transcript. This section should be written after the links and references section, maintaining the same structure, format, and writing style used in the previous content.

Condition: First, check if the video transcript contains relevant information on conditional logic related to the \[specific task/topic]. If the transcript does not include such content, return only the phrase "Not Applicable" without any additional details, explanations, or context. If the transcript includes relevant information on conditional logic, proceed with the following steps:

Instructions:

Purpose:
Extract and deliver a comprehensive section that identifies and presents the depth of detail or types of conditional logic mentioned in the transcript, focusing on how they relate to the \[specific task/topic].
Ensure these insights into conditional logic are presented clearly, offering actionable advice on how to implement or understand the conditional logic discussed.

Tasks:

Identify Conditional Logic Information:
Carefully review the transcript to identify any mentions of conditional logic, including how it is set up, types of conditions used, and the level of detail provided.
Note the complexity of the conditional logic described, whether it involves simple conditions or more advanced, nested logic.

Describe Conditional Logic Depth:
Organize the identified information into a structured section that flows naturally from the links and references section.
Provide detailed explanations of each type of conditional logic mentioned, highlighting its relevance to the core topic and how it enhances the \[specific task/topic].

Expand on Examples:
If the transcript mentions specific examples of conditional logic, integrate them into the section, providing additional context or variations that demonstrate different levels of complexity.
If the transcript lacks sufficient detail, infer possible applications of conditional logic and expand on them to illustrate how it can be used effectively.

Use of Keywords:
Integrate primary keywords naturally within headings and key explanations of conditional logic, ensuring their relevance to the content.
Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

Visual Prompts:
Suggest relevant visuals (e.g., flowcharts, decision trees) where applicable to enhance understanding of the conditional logic discussed. Specify how these visuals should be incorporated (e.g., callouts, inline, or separate sections).
Provide detailed descriptions of what each visual should depict and how it supports the accompanying text.

Simplify Language:
Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience.

Streamline Content:
Avoid redundant content by summarizing similar types of conditional logic or combining them into more comprehensive explanations where appropriate.
Focus on providing clear, actionable insights that help the reader understand and implement the conditional logic discussed.

Audit for Completeness:
Review the identified conditional logic information against the transcript to ensure all relevant content is covered and no essential details are omitted.
Ensure the explanations of conditional logic flow logically, are easy to understand, and provide real value to the reader.

Keyword Integration:

Primary Keywords:
Use primary keywords in H2 headings and key descriptions of conditional logic, ensuring they fit naturally within the content.

Secondary Keywords:
Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit.
Use these keywords to add context or depth without overwhelming the reader.

Avoid Over-Optimization:
Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

Examples:

Integration:
Where examples of conditional logic are provided in the transcript, integrate them into the section to illustrate key points or concepts.

Modification:
Modify examples to avoid content cannibalism by changing names, conditions, and data to make them more relevant and original.
Provide alternative scenarios or variations to demonstrate the flexibility and applicability of the conditional logic.

Writing Style:

Voice:
Maintain consistency with the writing style used in the previous sections. Use first-person or third-person, depending on the context.

Tone:
Write in a tone suitable for a 7th-grade reading level, using simple, clear language.

Structure:
Write short sentences (5-10 words) and use short paragraphs. Use appropriate headings (H2, H3, H4) to organize content logically.
Enhance readability by using bullet points, numbered lists, or tables where appropriate.

Maintain Continuation:
Ensure a seamless transition from the previous section, keeping the content engaging and easy to follow.

Output:

Conditional Logic Depth Section:
Generate a detailed, clear, and concise section that explains the depth and types of conditional logic related to the \[specific task/topic].
Ensure the section is as long as necessary, incorporating descriptions, examples, visuals, and best practices where needed.

Audit:
Conduct a thorough review to ensure that all conditional logic information mentioned in the transcript is captured and that no essential details are omitted.
Ensure the content flows logically, and that there are no gaps in the information provided.

---

Well-Structured JSON Output Instructions

1. Enforce JSON-Only Output
   After assembling the “Conditional Logic Depth Section,” the agent must emit its answer solely as a well-formed JSON object. No other text (comments, explanations, or markdown) should appear in the assistant’s response.

2. JSON Schema Definition
   The output JSON must conform to this schema:

```json
{
  "section_heading": "string",
  "overview": "string",
  "logic_items": [
    {
      "heading": "string",
      "description": "string",
      "complexity": "simple" | "nested" | "advanced",
      "examples": ["string", ...],
      "visual_prompt_id": "string" | null
    }
  ],
  "audit": "string"
}
```

3. Output Rules

* Always include all four top-level keys: "section\_heading", "overview", "logic\_items", and "audit".
* If no conditional logic is found, set:

  * "section\_heading": "Not Applicable"
  * "overview": ""
  * "logic\_items": \[]
  * "audit": "Not Applicable"
* Each logic item must include:

  * heading: The specific logic type
  * description: What it does
  * complexity: One of "simple", "nested", or "advanced"
  * examples: A list of 1–3 textual examples or code fragments
  * visual\_prompt\_id: An associated visual ID or null if not applicable

4. Seamless Integration
   After the “links and references” section, switch immediately into producing the JSON only—no extra prose.
"""