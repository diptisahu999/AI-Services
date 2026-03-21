PROMPT_LOGIC="""### 1. Objective:

Analyze the provided YouTube transcript or video content to identify and prioritize highly focused primary and secondary keywords. This task is crucial for optimizing the content for search engine performance by ensuring that the identified keywords are precise, relevant, and aligned with the specific topic of the video.

Also extract all distinct high-level topics or theme clusters that structure the video content. These can be used for downstream applications like navigation UIs, chaptering, curriculum generation, or tag-based retrieval.

---

### 2. Instructions:

#### 2.1) Content Analysis:

* Thoroughly evaluate the transcript of the provided YouTube video. Focus on the title, description, and key spoken content that aligns closely with the central theme of the video.
* Identify the most relevant terms, phrases, and concepts that are repeatedly emphasized or that align specifically with the main topic. This will form the basis for keyword selection.

#### 2.2) Keyword Identification:

* **Primary Keywords:** Identify up to 5 keywords that directly capture the main focus of the video. These should be specific, targeted terms that are essential to the video’s topic. Ensure these keywords are highly focused and directly related to the specific content being covered, avoiding broader terms unless they are explicitly relevant.

  Example: Instead of using "Monday.com guide," use "Monday.com WorkForms guide" or "Monday.com form creation tutorial" if that aligns more closely with the video’s focus.

* **Secondary Keywords:** Identify up to 5 additional keywords that are related to the main topic but may slightly broaden the scope while still being relevant. These should complement the primary keywords, capturing additional aspects of the content without straying from the core focus.

  Example: Instead of "Monday.com step-by-step guide," use "Monday.com WorkForms step-by-step guide" to maintain specificity.

#### 2.3) Research and Industry Relevance:

* **Conduct Research:** Go beyond the transcript to identify industry-specific terms, jargon, or popular keywords that may not be explicitly mentioned but are highly relevant to the topic. For instance, if "webform" is a commonly used term in Monday.com’s ecosystem but is not mentioned in the transcript, include it as a keyword if it enhances the relevance of the content.

  Example: Investigate how Monday.com refers to its forms feature (e.g., "WorkForms" vs. "forms" vs. "webforms"). If the platform typically uses "WorkForms," prioritize this term over generic terms like "forms" to align with industry vocabulary.

#### 2.4) Topic Cluster Extraction:

* **Identify Major Themes:** Based on how the video progresses, identify clusters of information, such as sections on setup, architecture, design principles, troubleshooting, tools, etc.
* **Title Each Topic Cluster:** Provide a short, descriptive label for each topic cluster (3–7 words).
* **Associate Key Keywords:** Tag each topic cluster with the keywords that are most relevant within that segment.
* **Timestamp Hints (Optional):** If phrases like "let's move on to..." or "in the next part..." exist, use them to infer progression markers.

---

### 3. Output Requirements:

#### Output 1: Provide a comma-separated list of the identified Primary Keywords. Do not use any additional formatting.

#### Output 2: Justification Primary: For each primary keyword, provide a detailed explanation that includes:

* *Relevance*: How the keyword directly relates to the video’s core content.
* *Search Intent*: Why users would search using this keyword.
* *Contextual Importance*: How it fits into the content's flow.
* *Competitiveness*: Why it's a strong SEO choice.
* *Industry-Specific Terms*: Any platform-specific terms or language.

#### Output 3: Provide a comma-separated list of the identified Secondary Keywords. No formatting or brackets.

#### Output 4: Justification Secondary: For each secondary keyword, provide a detailed explanation that includes:

* *Complementarity*: How the keyword expands on the primaries.
* *Search Broadening*: Traffic potential from related queries.
* *User Value*: Additional information or value it delivers.
* *Strategic Importance*: Tactical use in content positioning.

#### Output 5: Topic Cluster Overview

* Provide a list of 3–10 major content sections from the video.
* Each cluster must include:

  * `cluster_title`: A brief title.
  * `relevant_keywords`: Array of 2–5 keywords relevant to that cluster.
  * `summary`: A short sentence summarizing the content.

---

### 4. Output Format Specification (JSON):

```json
{
  "videoTopic": "<string>",
  "primaryKeywords": ["<string>", ...],
  "justificationPrimary": [
    {
      "keyword": "<string>",
      "relevance": "<string>",
      "searchIntent": "<string>",
      "contextualImportance": "<string>",
      "competitiveness": "<string>",
      "industrySpecificTerms": "<string>"
    }
  ],
  "secondaryKeywords": ["<string>", ...],
  "justificationSecondary": [
    {
      "keyword": "<string>",
      "complementarity": "<string>",
      "searchBroadening": "<string>",
      "userValue": "<string>",
      "strategicImportance": "<string>"
    }
  ],
  "topicClusters": [
    {
      "cluster_title": "<string>",
      "relevant_keywords": ["<string>", ...],
      "summary": "<string>"
    }
  ]
}
```

### 5. Field Definitions:

* `videoTopic`: Single string summarizing the overall theme.
* `primaryKeywords` / `secondaryKeywords`: Core keyword lists.
* `justificationPrimary` / `justificationSecondary`: Justifications.
* `topicClusters`: Topic grouping with summary and tags.

**Rules:**

* Emit **only valid JSON**.
* No markdown, no comments.
* All string values must be valid JSON.
* Avoid placeholder filler if no data is found; omit empty fields instead.
* Ensure 7th-grade readability for `summary` fields.

---

This extended instruction set ensures SEO-readiness, keyword relevance, and future usability across navigation, tagging, and summarization pipelines.
"""