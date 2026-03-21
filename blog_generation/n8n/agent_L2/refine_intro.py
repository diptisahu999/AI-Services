PROMPT_LOGIC="""Objective: Generate a compelling and SEO-optimized "Introduction" section for a blog post centered around "How to" guides and tutorials, based on the provided YouTube video transcript and inputs.

Inputs:{
Topic\_and\_Keywords{
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

Condition:

Keyword Check: Ensure that the provided context includes specific "Primary Keywords" and "Secondary Keywords."

Content Relevance: Confirm that the context aligns with the "Video Topic" and overall theme of the "How to" guide or tutorial blog post.

Ignore Non-Applicable Inputs: If any of the input values are marked as "Not Applicable," ignore those specific inputs when generating the introduction.

If the necessary elements are not present or aligned, return exactly:
Not Applicable

Introduction Guidelines:

1. Keyword Integration:

   * Primary Keywords: Incorporate the primary keywords naturally to set the stage for the blog content without redundancy.
   * Secondary Keywords: Introduce the secondary keywords seamlessly to support the introduction without overcrowding it.

2. Relevance and Alignment:

   * Ensure the introduction is aligned with the video topic, specifically focusing on the "How to" guide or tutorial theme, providing a clear and engaging preview of the content.

3. Engage the Reader:

   * Provide a concise and focused overview that hooks the reader by clearly outlining the value they will gain from following the tutorial or guide.

4. Use of Transcript Details:

   * Leverage relevant details from the video transcript to add credibility and depth, ensuring the content aligns with the step-by-step nature of "How to" guides and tutorials.

5. Mention Tools or Resources:

   * If applicable, mention any tools, setup instructions, or resources necessary for first-time users, as per the links and references provided. Include hyperlinks or references to these resources.

6. SEO Best Practices:

   * Include a suggested meta title (<=60 characters) and meta description (<=160 characters) at the end of the section, optimized for search engines.
   * Maintain a primary keyword density of 1–2% and secondary keyword density of 0.5–1%.

7. Readability & Flow:

   * Write at a 7th-grade reading level. Use short sentences (5–10 words) and short paragraphs (3–4 sentences each).
   * Use a conversational tone. Avoid jargon and clichés.
   * End with a call-to-action that transitions smoothly into the main content.

8. Length & Structure:

   * Limit the introduction to three paragraphs, each containing 3–4 sentences.
   * Each sentence should contain 5–10 words to ensure clarity and accessibility.

9. Audit for Completeness:

   * Confirm that all primary and secondary keywords are present at least once.
   * Verify that any referenced tools or resources are named and linked correctly.

Output Format:

Return ONLY the polished introduction section with the following appended SEO block. Do not include any additional commentary or formatting beyond what is specified.

```
[Introduction Paragraph 1]

[Introduction Paragraph 2]

[Introduction Paragraph 3]

Meta Title: "<max 60 chars>"
Meta Description: "<max 160 chars>"

Call-to-Action: "<short sentence inviting next step>"
```

Key Rules:

* Do not output JSON or markdown fences.
* If inputs are misaligned or missing, output exactly:
  Not Applicable
* Preserve the input order of topics and keywords for natural flow.
* Ensure all links use the inferred URLs provided in "Links and References."
* Keep tone, style, and structure consistent with the rest of the document.
"""