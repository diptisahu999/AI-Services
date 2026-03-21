PROMPT_LOGIC="""Objective:
Generate a detailed, actionable section focused on extracting and presenting links and references based on the provided YouTube video transcript. This section should be written after the audience specification/persona section, maintaining the same structure, format, and writing style used in the previous content.

Condition:
First, check if the video transcript contains relevant information on links, external references, or resources related to the \[specific task/topic]. If the transcript does not include such content, return only the phrase "Not Applicable" without any additional details, explanations, or context. If the transcript includes relevant links and references, proceed with the following steps:

Instructions:

Purpose:

* Extract and deliver a comprehensive section that identifies and presents any external links, references, or resources mentioned in the transcript, focusing on their relevance to the \[specific task/topic].
* Ensure these links and references are presented clearly, offering actionable insights or further reading opportunities for the reader.

Tasks:

1. Identify Links and References:

   * Carefully review the transcript to identify any mentions of external links, references, or resources that are related to the \[specific task/topic].
   * Note any URLs, document titles, or specific references to external sources that are highlighted as useful or essential for the reader.
   * For tools, libraries, or websites that are **mentioned by name only**, include them by inferring their official websites or most relevant reference pages, even if an explicit link is not provided.

2. Organize and Present References:

   * Organize the identified links and references into a structured section that flows naturally from the audience specification/persona section.
   * Provide brief descriptions of each link or reference, explaining its relevance to the core topic and why the reader might find it useful.

3. Categorize References:

   * If multiple types of references are mentioned (e.g., articles, tutorials, tools), categorize them accordingly to help readers quickly find the resources that are most relevant to their needs.
   * Offer context or background for each category, if necessary, to clarify its importance in relation to the \[specific task/topic].

4. Use of Keywords:

   * Integrate primary keywords naturally within headings and key references, ensuring their relevance to the content.
   * Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

5. Visual Prompts:

   * Suggest relevant visuals (e.g., screenshots of web pages, icons representing tools) where applicable to enhance understanding of the links and references. Specify how these visuals should be incorporated (e.g., callouts, inline, or separate sections).
   * Provide detailed descriptions of what each visual should depict and how it supports the accompanying text.

6. Simplify Language:

   * Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience.

7. Streamline Content:

   * Avoid redundant content by summarizing similar references or combining them into more comprehensive insights where appropriate.
   * Focus on providing links and references that directly support the key points and enhance the reader's understanding.

8. Audit for Completeness:

   * Review the identified links and references against the transcript to ensure all relevant content is covered and no essential details are omitted.
   * Ensure the links and references flow logically, are easy to understand, and provide real value to the reader.

Keyword Integration:

1. Primary Keywords:

   * Use primary keywords in H2 headings and key references, ensuring they fit naturally within the content.

2. Secondary Keywords:

   * Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit.
   * Use these keywords to add context or depth without overwhelming the reader.

3. Avoid Over-Optimization:

   * Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

Examples:

1. Integration:

   * Where external links, references, or resources are provided in the transcript, integrate them into the section to illustrate key points or concepts.

2. Modification:

   * Modify the presentation of links or references to avoid content cannibalism by changing descriptions or context to make them more relevant and original.
   * Provide alternative scenarios or variations to demonstrate the flexibility and applicability of the references.

Writing Style:

1. Voice:

   * Maintain consistency with the writing style used in the previous sections. Use first-person or third-person, depending on the context.

2. Tone:

   * Write in a tone suitable for a 7th-grade reading level, using simple, clear language.

3. Structure:

   * Write short sentences (5-10 words) and use short paragraphs. Use appropriate headings (H2, H3, H4) to organize content logically.
   * Enhance readability by using bullet points, numbered lists, or tables where appropriate.

4. Maintain Continuation:

   * Ensure a seamless transition from the previous section, keeping the content engaging and easy to follow.

---

When generating the “Extract Links and References” section, the agent must return **only valid JSON**. Do not emit any explanatory prose outside of this JSON.

If no relevant links or resources are found in the transcript, output this exact string (without quotes):
Not Applicable

Otherwise, adhere strictly to the following JSON schema:

```json
{
  "links_section": string,        // A markdown or HTML snippet of the complete “Links & References” section
  "references": [                 // Array of up to 10 extracted references
    {
      "title": string,            // Title or label of the resource
      "url": string,              // The full URL
      "category": string,         // One of: "Article", "Tutorial", "Tool", "Documentation", etc.
      "description": string       // A 1–2 sentence summary of why it’s relevant
    }
    // … additional entries …
  ],
  "audit_complete": boolean       // Always true when links are found
}
```

**Example Output** (when links are present):

```json
{
  "links_section": "## External Resources\n\nHere are the key links mentioned in the transcript that support the topic:\n\n- [Official API Docs](https://example.com/api) — Comprehensive reference for endpoints.\n- [Quickstart Tutorial](https://example.com/quickstart) — Step‑by‑step guide to get started.\n",
  "references": [
    {
      "title": "Official API Docs",
      "url": "https://example.com/api",
      "category": "Documentation",
      "description": "The definitive reference for all API endpoints, parameters, and examples."
    },
    {
      "title": "Quickstart Tutorial",
      "url": "https://example.com/quickstart",
      "category": "Tutorial",
      "description": "A beginner‑friendly walkthrough for initial setup and basic usage."
    }
  ],
  "audit_complete": true
}
```

**Key Rules:**

1. **No extra keys** beyond the schema.
2. **No comments** or trailing commas in the JSON.
3. **Exact match** of the string `Not Applicable` if no resources are in the transcript.
4. Maintain the **same tone and structure** as the preceding sections.
5. Ensure **7th‑grade reading level**, short sentences, and simple language in the “links\_section” markdown.
6. **Include named tools, platforms, or services even if only mentioned by name**, using inferred or official links where appropriate.

---
"""