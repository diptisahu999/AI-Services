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

/* ADDITION: Ensure all inputs above are referenced in crafting a conclusion that feels cohesive and context-aware. */

Objective: Generate a concise, impactful conclusion for a blog post about [specific task/topic]. The conclusion should summarize the key points discussed in the blog and reinforce the value of the content. This section should be based on the provided YouTube video transcript, with an emphasis on integrating primary and secondary keywords naturally. Avoid any unnecessary repetition or overly general content.

/* ADDITION: This is an intermediate JSON-like draft to feed into the next blog-generation pipeline. Define clear fields so the conclusion can be inserted programmatically. */

Condition:

First, check if the video transcript contains relevant content that can be summarized in a conclusion for a blog post about [specific task/topic]. If the transcript does not include such content, return "Not Applicable."

If "Not Applicable" is returned, consider revisiting the transcript for other potential content that could be repurposed for a conclusion or confirm that the task is complete.

Instructions:

Purpose:

Summarize the key points covered in the blog, reinforcing the value of the content for the reader. Focus on the most impactful points that align with the blog’s main message.

Tasks:

Recap:

Summarize the main benefits and key takeaways from the [specific task/topic] discussed in the video. The summary should be concise and focused, ensuring that the reader remembers the most important aspects of the blog. Allow for flexibility in selecting the most relevant points if the transcript covers multiple aspects.

Structure:

Provide a brief recap of the blog’s main points. Highlight the key benefits of the techniques or information discussed in the blog, ensuring the conclusion reinforces the overall message.

Avoid introducing new content. Focus solely on summarizing what was covered in the blog.

Keyword Integration:

Integrate primary keywords naturally within the summary to reinforce the main topic without overstuffing. Ensure they fit seamlessly into the content, prioritizing readability and natural flow.

Integrate secondary keywords where they naturally fit, enhancing the relevance of the conclusion without overwhelming the reader.

Avoid over-optimization: use synonyms or rephrasing to maintain natural tone.

Writing Style:

Voice: Write in the first person or third person, using past tense where applicable. Ensure consistency with the tone and style used throughout the blog.

Tone: Be concise and avoid temporal markers (e.g., "today"). Maintain an engaging tone that encourages reflection on learned benefits.

Clarity: Use short sentences (5–10 words) and short paragraphs to ensure the summary is clear and easy to read.

Focus: Reiterate the primary keyword to leave the reader with confidence in the subject.

Audit for Effectiveness:

Ensure the conclusion effectively recaps the blog’s key points without repetition or new information.

Verify the logical flow, impact, and alignment with the blog’s overall message.

Output:

/* ADDITION: Structure the conclusion as JSON with explicit fields for downstream automation: */
{
"conclusion_heading": string,       // H2 title for the conclusion (e.g., "Conclusion")
"summary": string,                  // 2–3 sentences summarizing key takeaways
"reinforcement": string,            // 1 sentence reinforcing value and next steps
"keywords_used": [string],         // List of primary & secondary keywords included
"audit_complete": boolean          // Always true if conclusion provided
}

Conclusion Section:

Generate a concise, clear, and well-structured conclusion that effectively summarizes the blog's content. Avoid any introductory or new content, focusing solely on recapping what was covered.

Ensure the conclusion aligns with the blog’s overall tone and message, leaving the reader with a strong understanding of the key takeaways.

Audit:

Review the conclusion to ensure it effectively summarizes the key points from the blog without unnecessary repetition or new content.

Ensure the conclusion flows logically, reinforces the blog’s message, and provides a strong, impactful end to the post."""