PROMPT_LOGIC="""Inputs:{
Topic\_and\_Keywords{
videoTopic,
primaryKeywords,
justificationPrimary,
secondaryKeywords,
justificationSecondary,
topicClusters
},
Video Transcript,
Audience Specification,
Examples & References,
Conditional Logic Depth,
Error Handling,
Links and References
}

/\* **ADDITION**: Ensure **all inputs** above are referenced and utilized in the output structure to maximize completeness and context. \*/

Objective: Generate a detailed, actionable section focused on extracting and presenting customization tips based on the provided YouTube video transcript. This section should follow the step-by-step guide, seamlessly maintaining the structure, format, and writing style used in the earlier content.

/\* **ADDITION**: Note that this is an **intermediate draft** for a future blog post. Structure the output with **JSON-like fields** and clear sections so the next pipeline node can consume it easily. \*/

Condition:

* First, check if the video transcript contains relevant information on customization tips related to the \[specific task/topic]. If the transcript does not include such content, return "Not Applicable." If customization tips are found, proceed with the following steps.

* If "Not Applicable" is returned, consider revisiting the transcript for other potential content or confirm that the task is complete.

Instructions:

Purpose:

* Extract and deliver a comprehensive section focused on customization tips to enhance the \[specific task/topic] discussed in the video.

* Ensure these tips are directly applicable, offering actionable advice on how to personalize or optimize the process to suit different needs or preferences. Allow for reasonable expansion or clarification where the transcript may lack detail, ensuring the guide remains practical and useful.

Tasks:

1. Identify Customization Opportunities:

* Carefully analyze the transcript to identify any mentions of customization, personalization, or optimization opportunities related to the \[specific task/topic].

* Expand on these mentions by providing additional context or actionable steps, ensuring they are grounded in the transcript’s content and logically inferred if necessary.

2. Integrate Customization Tips:

* Organize the customization tips into a structured section that flows naturally from the step-by-step guide, maintaining consistency in tone and format.

* Include detailed instructions or sub-steps where necessary, ensuring each customization tip is easy to follow and implement without sacrificing clarity.

3. Expand on Examples:

* Where examples of customization are mentioned in the transcript, integrate them into the section, providing additional context or variations that demonstrate the versatility of the tips.

* If the transcript lacks examples, infer possible scenarios where these customizations could be applied, ensuring these inferences are logically derived from the transcript and contextually appropriate.

4. Use of Keywords:

* Integrate primary keywords naturally within headings and key customization tips, ensuring their relevance to the content.

* Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

5. Visual Prompts:

* Suggest relevant visuals (e.g., screenshots, diagrams) where applicable to enhance understanding of the customization tips.

* Provide detailed descriptions of what each visual should depict, and allow for the inclusion of visuals based on inferred needs if they support the accompanying text and enhance comprehension.

6. Simplify Language:

* Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience. Ensure that simplification does not omit critical details necessary for understanding.

7. Streamline Content:

* Avoid redundant content by summarizing similar customization tips or combining them into more comprehensive advice where appropriate. Retain unique or contextually significant details to ensure different customization scenarios are adequately covered.

8. Audit for Completeness:

* Review the extracted tips against the transcript to ensure all relevant customization opportunities are covered and no essential details are omitted.

* Ensure the tips flow logically, are easy to understand, and provide real value to the reader, with adjustments made to enhance clarity and consistency with the overall guide.

Keyword Integration:

1. Primary Keywords:

* Use primary keywords in H2 headings and key customization tips, ensuring they fit naturally within the content and align with the transcript.

2. Secondary Keywords:

* Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit, enhancing the content without overwhelming the reader.

3. Avoid Over-Optimization:

* Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

Examples:

1. Integration:

* Where examples of customization are provided in the transcript, integrate them into the section to illustrate key tips or concepts.

2. Modification:

* Modify examples to avoid content cannibalism by changing names, numbers, and data to make them more relevant and original, while still adhering to the transcript.

* Provide alternative scenarios or variations to demonstrate the flexibility of the customization tips, ensuring they are logically consistent with the transcript.

Writing Style:

1. Voice:

* Maintain consistency with the writing style used in the step-by-step guide. Use first-person or third-person, depending on the context.

2. Tone:

* Write in a tone suitable for a 7th-grade reading level, using simple, clear language.

3. Structure:

* Write short sentences (5-10 words) and use short paragraphs. Use appropriate headings (H2, H3, H4) to organize content logically.

* Enhance readability by using bullet points, numbered lists, or tables where appropriate.

4. Maintain Continuation:

* Ensure a seamless transition from the previous section, keeping the content engaging and easy to follow.

Output:

/\* **ADDITION**: Structure the output as **JSON** with these top-level keys to facilitate downstream blog generation: \*/
{
"section\_heading": string,            // H2 title for the Customization Tips section
"intro\_paragraph": string,            // A brief intro to set context (1-2 sentences)
"customization\_tips": \[               // Array of tip objects
{
"title": string,                  // H3 heading for each tip
"description": string,            // Detailed explanation and actionable steps
"keywords": \[string],             // Primary & secondary keywords used
"visual\_prompt": string|null      // Suggested visual or null if none
}
// …additional tip objects…
],
"audit\_complete": boolean             // Always true when tips are provided
}

1. Customization Tips Section:

* Generate a detailed, clear, and concise section that provides practical customization tips related to the \[specific task/topic].

* Ensure the section is as long as necessary, incorporating examples, visuals, and best practices where needed, with flexibility for reasonable extrapolations or inferences based on the transcript.

2. Audit:

* Conduct a thorough review to ensure that all customization tips mentioned in the transcript are captured and that no essential details are omitted.

* Ensure the content flows logically, with no gaps in the information provided, and is consistent with the overall guide.
"""