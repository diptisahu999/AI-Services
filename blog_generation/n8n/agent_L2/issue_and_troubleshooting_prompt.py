PROMPT_LOGIC="""Inputs:{
Topic_and_Keywords{
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

/* ADDITION: Ensure all inputs above are utilized in building the troubleshooting section. */

Objective: Generate a detailed, actionable section focused on common issues and troubleshooting based on the provided YouTube video transcript. This section should be written after the customization tips section and should maintain the same structure, format, and writing style used in the previous content.

/* ADDITION: This output is an intermediate JSON-structured draft for a future blog post. Include clear JSON-like field placeholders for easy parsing downstream. */

Condition:

First, check if the video transcript contains relevant information on common issues and troubleshooting related to the [specific task/topic]. If the transcript does not include such content, return "Not Applicable."

If "Not Applicable" is returned, consider revisiting the transcript for other potential content or confirm that the task is complete.

Instructions:

Purpose:

Extract and deliver a comprehensive section focused on common issues that users may encounter during the [specific task/topic] and provide clear troubleshooting steps to resolve them. Allow for reasonable expansion or clarification where the transcript may lack detail, ensuring the guide remains practical and useful.

Ensure these troubleshooting tips are practical, offering actionable advice to help users overcome obstacles efficiently.

Tasks:

Identify Common Issues:

Analyze the transcript to identify any mentions of common issues or challenges users might face while performing the [specific task/topic].

Expand on these issues by providing additional context or potential causes, making it easier for users to identify and understand the problem. Where applicable, infer common issues based on the context provided in the transcript.

Provide Troubleshooting Steps:

For each identified issue, provide clear, step-by-step troubleshooting instructions to help users resolve the problem.

Where applicable, offer alternative solutions or preventative tips to avoid the issue in the future. Include conditional logic where necessary to guide users through different troubleshooting paths based on the issue encountered.

Expand on Examples:

If the transcript mentions specific examples of issues, integrate them into the section, providing additional context or variations that demonstrate different troubleshooting scenarios.

If the transcript lacks examples, infer possible issues and provide hypothetical troubleshooting steps that could apply to a variety of situations, ensuring these inferences are logically derived from the transcript.

Use of Keywords:

Integrate primary keywords naturally within headings and key troubleshooting steps, ensuring their relevance to the content.

Use secondary keywords to provide additional context and depth, maintaining readability and avoiding over-optimization.

Visual Prompts:

Suggest relevant visuals (e.g., screenshots, diagrams) where applicable to enhance understanding of the troubleshooting steps.

Provide detailed descriptions of what each visual should depict, allowing for the inclusion of visuals based on inferred needs if they support the accompanying text and enhance comprehension.

Simplify Language:

Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience. Retain all critical details necessary for understanding while simplifying the language.

Streamline Content:

Avoid redundant content by summarizing similar issues or combining them into more comprehensive advice where appropriate. Retain unique or contextually significant details to ensure different troubleshooting scenarios are adequately covered.

Audit for Completeness:

Review the identified issues and troubleshooting steps against the transcript to ensure all relevant information is covered and no essential details are omitted.

Ensure the steps flow logically, are easy to understand, and provide real value to the reader, with adjustments made to enhance clarity and consistency with the overall guide.

Keyword Integration:

Primary Keywords:

Use primary keywords in H2 headings and key troubleshooting steps, ensuring they fit naturally within the content and align with the transcript.

Secondary Keywords:

Integrate secondary keywords in H3 and H4 headings or within the body text where they naturally fit, enhancing the content without overwhelming the reader.

Avoid Over-Optimization:

Focus on readability and natural flow. Keywords should enhance the content, not dominate it. Avoid excessive repetition, using synonyms or rephrasing when necessary.

Examples:

Integration:

Where examples of common issues and troubleshooting steps are provided in the transcript, integrate them into the section to illustrate key points or concepts.

Modification:

Modify examples to avoid content cannibalism by changing names, numbers, and data to make them more relevant and original, while still adhering to the transcript.

Provide alternative scenarios or variations to demonstrate the flexibility of the troubleshooting steps, ensuring they are logically consistent with the transcript.

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

/* ADDITION: Structure the output as JSON with these top-level keys to facilitate downstream blog generation: */
{
"section_heading": string,            // H2 title for the Troubleshooting section
"intro_paragraph": string,            // A brief intro to set context (1-2 sentences)
"issues": [                          // Array of issue objects
{
"issue_title": string,           // H3 heading for each common issue
"description": string,           // Summary of the issue and its cause
"troubleshooting_steps": [       // Array of step-by-step instructions
string                          // Each list item is a single step
],
"keywords": [string],            // Primary & secondary keywords used
"visual_prompt": string|null     // Suggested visual or null if none
}
// …additional issue objects…
],
"audit_complete": boolean            // Always true when issues are provided
}

Common Issues and Troubleshooting Section:

Generate a detailed, clear, and concise section that addresses common issues and provides practical troubleshooting steps related to the [specific task/topic].

Ensure the section is as long as necessary, incorporating examples, visuals, and best practices where needed, with flexibility for reasonable extrapolations or inferences based on the transcript.

Audit:

Conduct a thorough review to ensure that all common issues and troubleshooting steps mentioned in the transcript are captured and that no essential details are omitted.

Ensure the content flows logically, with no gaps in the information provided, and is consistent with the overall guide."""