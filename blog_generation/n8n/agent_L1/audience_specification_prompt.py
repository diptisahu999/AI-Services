PROMPT_LOGIC="""Objective: Generate a detailed, actionable section focused on extracting and presenting audience specification or persona information based on the provided YouTube video transcript. This section should be written after the references, examples, and data points section, maintaining the same structure, format, and writing style used in the previous content.

Condition: First, check if the video transcript contains relevant information on audience specification or persona related to the \[specific task/topic]. If the transcript does not include such content, return only the phrase "Not Applicable" without any additional details, explanations, or context. If the transcript includes relevant audience specification or persona information, proceed with the following steps:

Instructions:

Purpose:

* Extract and deliver a comprehensive section that identifies the target audience or personas mentioned in the transcript, focusing on their characteristics, needs, and preferences related to the \[specific task/topic].

* If multiple audiences are mentioned, group them based on shared characteristics or relevant distinctions to provide a clear understanding of who the guide is intended for.

Tasks:

1. Identify Audience or Persona Information:

* Carefully review the transcript to identify any mentions of the target audience, user personas, or specific groups that the content is intended to address.

* Note any characteristics, needs, goals, or challenges that are highlighted in relation to these audiences.

* Even if audience labels are implicit (e.g., "for busy professionals" or "if you're building apps"), infer and include them as distinct personas or audience clusters.

* Include inferred persona metadata such as typical skill level, familiarity with the topic, expected tech environment, or learning preferences if suggested implicitly.

2. Group and Categorize Audiences:

* If multiple audiences are mentioned, categorize them into groups based on shared characteristics, such as experience level, industry, or specific needs related to the \[specific task/topic].

* Provide a brief description of each group, highlighting their unique characteristics and how the guide’s content is tailored to meet their needs.

3. Expand on Audience Needs:

* Where applicable, expand on the needs, preferences, or challenges of each audience group. Explain how the content or tools discussed in the transcript address these aspects.

* If the transcript lacks detailed information, infer possible needs or challenges based on the audience characteristics and provide practical insights or solutions.

* Optionally note potential questions this audience may have, or goals they might be trying to achieve with the help of the content.

4. Use of Keywords:

* Integrate primary keywords naturally within headings and key audience specifications, ensuring their relevance to the content.

* Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

5. Visual Prompts:

* Suggest relevant visuals (e.g., persona profiles, audience segmentation charts) where applicable to enhance understanding of the audience specification. Specify how these visuals should be incorporated (e.g., callouts, inline, or separate sections).

* Provide detailed descriptions of what each visual should depict and how it supports the accompanying text.

6. Simplify Language:

* Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience.

7. Streamline Content:

* Avoid redundant content by summarizing similar audience characteristics or combining them into more comprehensive personas where appropriate.

* Focus on providing clear, actionable insights that help the reader understand the target audience and how the content addresses their specific needs.

8. Audit for Completeness:

* Review the identified audience information against the transcript to ensure all relevant content is covered and no essential details are omitted.

* Ensure the audience personas or specifications flow logically, are easy to understand, and provide real value to the reader.

Keyword Integration:

1. Primary Keywords:

* Use primary keywords in H2 headings and key audience specifications, ensuring they fit naturally within the content.

2. Secondary Keywords:

* Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit.

* Use these keywords to add context or depth without overwhelming the reader.

3. Avoid Over-Optimization:

* Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

Examples:

1. Integration:

* Where examples of audience personas or specifications are provided in the transcript, integrate them into the section to illustrate key points or concepts.

2. Modification:

* Modify examples to avoid content cannibalism by changing names, details, and data to make them more relevant and original.

* Provide alternative scenarios or variations to demonstrate the flexibility and applicability of the audience specifications.

* If no explicit persona examples are present but contextual clues are available (e.g., language use, common frustrations, or tool preferences), synthesize likely audience types from this information.

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

Output Format (Strict JSON Structure)

All responses must be returned as a well-structured JSON object with the following schema:

```json
{
  "sections": [
    {
      "heading": "string",
      "content": "string",
      "examples": ["string", "..."],
      "visual_prompt_ids": ["string", "..."],
      "audience_tags": ["string", "..."],
      "inferred_traits": {
        "skill_level": "string",
        "tech_experience": "string",
        "content_goal": "string"
      }
    }
  ]
}
```

Schema Details:

* heading: A clear, descriptive H2-style title for the section.
* content: Concise, paragraph-style explanation written at a 7th-grade reading level.
* examples (optional): Bullet-style list of concrete examples supporting the content. Should be varied and relevant.
* visual\_prompt\_ids (optional): IDs corresponding to suggested visuals (e.g., flowcharts, diagrams, persona charts) that visually support the text.
* audience\_tags (optional): List of tags summarizing the audience segment (e.g., "beginner", "enterprise team", "students", etc.).
* inferred\_traits (optional): A structured object summarizing inferred audience metadata, such as skill level, technical background, or expected goals.

Behavior:

* If no relevant persona or audience information exists in the transcript, return:

```json
"sections": ["Not Applicable"]
```

* If relevant persona or audience information exists, structure each group or idea as a separate object within the sections array.

Example Output:

```json
{
  "sections": [
    {
      "heading": "Understanding Audience Personas",
      "content": "The video outlines two main user groups: beginners exploring AI tools and developers integrating AI into workflows. Both have distinct needs and goals, such as ease of use and API access.",
      "examples": [
        "Beginners often prefer visual interfaces and tutorials.",
        "Developers look for code examples, SDKs, and integration flexibility."
      ],
      "visual_prompt_ids": ["persona_split_chart", "dev_vs_beginner_flow"],
      "audience_tags": ["beginner", "developer"],
      "inferred_traits": {
        "skill_level": "mixed",
        "tech_experience": "novice to advanced",
        "content_goal": "tool adoption and workflow integration"
      }
    },
    {
      "heading": "Visual Prompt Ideas",
      "content": "",
      "examples": [
        "Persona Split Chart: A chart comparing needs of beginner users and technical developers.",
        "Interaction Flow Diagram: A visual showing typical user journeys based on persona."
      ],
      "visual_prompt_ids": ["persona_split_chart", "user_journey_flow"]
    }
  ]
}
```
"""