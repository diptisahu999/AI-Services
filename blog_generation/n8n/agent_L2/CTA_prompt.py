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

/* ADDITION: Ensure all inputs above are referenced to craft a CTA that aligns with the topic, keywords, audience, examples, and resources. */

Objective: Generate a compelling and action-oriented "Call to Action" (CTA) section that encourages the reader to engage further with the content. The CTA should be based on the provided YouTube video transcript and integrate primary and secondary keywords naturally. This section should focus on prompting the reader to take specific actions without including any general introductory content.

/* ADDITION: This output is an intermediate JSON-like draft for blog pipeline insertion. Structure with explicit fields for downstream parsing. */

Condition:

First, check if the video transcript contains relevant content that can be used to craft a CTA related to the [specific task/topic]. If the transcript does not include such content, simply return "Not Applicable" without any additional details.

If the transcript includes relevant content, proceed with the following steps.

Instructions:

Purpose:

Prompt the reader to engage further with the content by exploring related articles, signing up for a service, or applying what they’ve learned. The CTA should be direct, persuasive, and motivating.

Tasks:

Engage: Encourage the reader to take a specific action, such as reading more related content, signing up for a service, or applying the knowledge gained.

Link: Provide relevant links that guide the reader to the next step. Use internal links to related articles or external links to sign-up pages or tools that support the CTA.

Structure:

Action Prompt: Start with a direct and clear call to action that uses action-oriented language. For example, "Explore more about [specific topic] by visiting our other guides."

Link: Include a relevant link to internal content that enhances the reader’s understanding or to an external resource that provides further value.

Limit CTAs: Focus on one or two CTAs to keep the message clear and impactful.

Keyword Integration:

Primary Keywords: Incorporate the primary keyword naturally within the CTA. It should be relevant and guide the reader to useful next steps.

Secondary Keywords: Use secondary keywords to provide additional context or detail where they naturally fit, ensuring they complement the primary keyword and enhance the CTA.

Writing Style:

Voice: Use first-person and action-oriented language. The tone should be persuasive, motivating, and encourage immediate action.

Clarity: Keep the CTA short, clear, and to the point. Avoid unnecessary words or phrases that could dilute the impact.

Avoid Over-Optimization: Focus on making the CTA feel natural and engaging, not forced or overly commercial.

Output:

/* ADDITION: Structure the CTA as JSON with explicit keys for downstream automation: */
{
"cta_prompt": string,        // The direct action-oriented prompt text
"cta_links": [              // Array of link objects
{
"label": string,        // Link text (e.g., "Explore our advanced guide")
"url": string           // URL for the link
}
// …additional links (max 2)…
],
"keywords_used": [string],  // List of primary & secondary keywords included
"audit_complete": boolean   // Always true if CTA provided
}

Call to Action Section:

Generate a concise, engaging CTA that directs the reader to the next steps. The CTA should include a strong action prompt and relevant links, encouraging further engagement without feeling overly pushy. Limit to one or two key actions.

Example:

Action Prompt: Ready to take your [specific task/topic] to the next level? Dive deeper into our [related content] or sign up for [service/tool] to start implementing these strategies today.

Link: [Insert internal link to related articles] or [Insert external link to a sign-up page]."""