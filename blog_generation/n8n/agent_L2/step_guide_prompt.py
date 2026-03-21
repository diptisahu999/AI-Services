PROMPT_LOGIC="""Inputs:{
Topic_and_Keywords{
videoTopic,
primaryKeywords,
justificationPrimary,
secondaryKeywords,
justificationSecondary,
topicClusters
},Video Transcript
,Audience Specification
,Examples & References
,Conditional Logic Depth
,Error Handling
,Links and References
}
Objective: Generate a comprehensive, actionable, and detailed step-by-step guide for creating a [specific task/topic] based on the provided YouTube video transcript. The guide should naturally integrate primary and secondary keywords, reflect the context and justification provided, and be structured with appropriate headings. Ensure that all content remains grounded in the transcript, with minor extrapolation allowed to enhance clarity, context, and user understanding.
Instructions:

Purpose:

Deliver a thorough and detailed guide for completing the [specific task/topic] covered in the video, ensuring each step is clearly explained and directly derived from the transcript.
Incorporate best practices and actionable tips within the steps to enhance the user's workflow and comprehension.
If conditional logic or examples are mentioned, include practical, easy-to-follow examples. If not discussed in the transcript, consider adding relevant logical steps or examples if they enhance clarity.

Tasks:

Outline Steps:

Sequentially list all necessary steps to complete the task, ensuring each step is thoroughly grounded in the transcript. Break down complex tasks into detailed sub-steps, providing clear instructions for each part of the process.

Include any contextual information or justifications provided in the transcript to explain why each step is important.

Integrate best practices naturally within the steps, offering actionable tips that are embedded in the workflow. Ensure these are either mentioned or implied in the transcript or logically derived from the context.

Verification: Continuously verify that each step and example is supported by the transcript. Add necessary details to enhance the guide’s usefulness without straying from the transcript’s content.

Incorporate Context:

Use the context of the video topic and any justifications provided in the transcript to ensure the content is relevant and aligned with the video’s focus.

Provide brief explanations or context where necessary to improve user understanding, ensuring these additions support the instructions and are consistent with the transcript.

Use of Keywords:

Integrate primary keywords naturally within headings and key instructions, ensuring their relevance to the step being described.

Use secondary keywords to provide additional context and depth, ensuring these keywords are relevant and align with the transcript.

Avoid Keyword Overuse:

Maintain natural readability by limiting the repetition of keywords. Use synonyms or rephrase content where necessary to avoid over-optimization, ensuring all language remains consistent with the transcript.

Visual Prompts:

Include relevant visuals (e.g., screenshots) where applicable to enhance understanding. If the transcript does not explicitly reference visuals, feel free to incorporate them where they would aid comprehension.

Specify how these visuals should be incorporated (e.g., callouts, inline, or separate sections).

Simplify Language:

Write at a 7th-grade reading level, using simple, clear language to ensure accessibility to a wide audience. Balance simplicity with sufficient detail to ensure all necessary information is included.

Streamline Redundant Content:

Summarize repetitive steps to avoid unnecessary detail, ensuring the content remains clear but concise. However, ensure that all critical information and context are retained.

Provide Conditional Logic Examples:

If the transcript includes conditional logic, provide step-by-step examples detailing how to apply it within the task. If not mentioned but relevant, consider including logical steps that enhance the user's understanding, ensuring they are practical and contextually appropriate.

Handling Unclear or Missing Information:

If the transcript is unclear or lacks specific details, note these areas and provide reasonable, context-based extrapolations to fill gaps. Avoid introducing any external knowledge that is not aligned with the transcript’s content.

Use All Inputs Provided:

Ensure that every input field (Topic_and_Keywords, Video Transcript, Audience Specification, Examples & References, Conditional Logic Depth, Error Handling, Links and References) is fully utilized to build a richer, more complete guide.

Treat this output as an intermediate draft for a future blog. Structure content with key metadata fields if necessary (e.g., step_number, estimated_time, prerequisites, tools_required).

Heading Structure:

Use H2 for major sections or key steps in the process.

Use H3 for sub-steps or detailed actions within a major step.

Use H4 for minor details or specific elements within a sub-step.

Allow flexibility in structure to ensure the guide flows logically and is easy to follow.

Audit for Completeness:

Review the guide against the transcript to ensure all steps are covered and no essential details are omitted. Ensure the content flows logically and naturally, allowing for minor additions that enhance clarity and user understanding.

Incorporate Feedback or Revisions:

If provided with feedback or revisions, integrate these into the guide while ensuring all content remains grounded in the transcript.

Keyword Integration:

Primary Keywords: Use in H2 headings and key instructions.

Secondary Keywords: Integrate in H3/H4 or supporting text.

Avoid Over-Optimization: Focus on readability and natural flow.

Examples:

Integration: Where examples are provided in the transcript, integrate them to illustrate key steps or concepts. If not explicitly provided, consider adding relevant examples that enhance the guide’s clarity.

Modification: Modify examples to avoid content cannibalism by changing names, numbers, and data to make them more relevant and original.

Writing Style:

Voice: Maintain consistency with the transcript’s style (first- or third-person).

Tone: 7th-grade level, plain and simple language.

Structure: Short sentences (5-10 words), short paragraphs, structured formatting.

Flow: Ensure smooth transitions from previous sections.

Output:

Step-by-Step Guide: Generate a detailed, clear, and comprehensive step-by-step guide that helps the reader complete the task, based on the transcript but with flexibility for necessary enhancements. Include visuals, examples, modified data, and best practices where needed, all derived from or aligned with the transcript.

Metadata Fields (for blog pipeline):

step_number: integer

title: string

prerequisites: string array

estimated_time: string

tools_required: string array

inferred_links: string array

Audit: Conduct a thorough review to ensure that all steps mentioned in the transcript are captured and that no essential details are omitted. Ensure the content flows logically.

Additional Rules:

Ensure inclusion of all input sections and treat the result as a draft for a blog post.

Include tools_required and any inferred_links for tool mentions.

Provide a structured output easier for the AI model in the next node in pipeline to understand.
"""