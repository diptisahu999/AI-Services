PROMPT_LOGIC="""You have two inputs:

YouTube Transcript: A detailed step-by-step guide or tutorial video transcript focused on a specific topic.

Domain Name: The website domain where related services, reviews, and guides are provided.

/* ADDITION: Ensure both inputs are fully leveraged—use the transcript for tutorial context and the domain for company data. */

Objective:

Generate two distinct and concise summaries:

Tutorial-Specific Summary: A "What We Do" statement that directly aligns with the specific topic of the YouTube tutorial, clearly reflecting the domain’s relevant services.

Comprehensive Company Summary: A general company overview that thoroughly highlights all key services offered by the company, including any core areas of expertise, customization, implementation, and consultation services.

/* ADDITION: This is an intermediate JSON-structured draft used to feed a blog-generation pipeline. Provide explicit fields for each summary. */

Web Scraping Instructions:

For the Comprehensive Company Summary: Perform a general audit of the provided domain by scraping the website to extract relevant information. Focus on identifying the company’s main services, areas of expertise, industries served, and any other key offerings. Use this information to craft a summary that accurately represents the company’s complete range of services, regardless of the industry or service type.

For the Tutorial-Specific Summary: Analyze the tutorial content and cross-reference it with the services listed on the domain. Use web scraping to identify and list all relevant services that the domain offers. Then, align the most appropriate service(s) with the intent of the transcript, ensuring the summary reflects how the company’s offerings support or enhance the tutorial topic. Ensure the summary is adaptable to various industries and service types.

Guidelines:

Service Alignment for Tutorial-Specific Summary: Tailor the first output to the specific content of the tutorial, showcasing how the domain’s services support or relate to the tutorial topic. Highlight the company’s expertise in the specific area covered by the video. If the services extend beyond technology, adapt the summary to reflect those other service types, such as consulting, product development, or creative services.

Detailed Overview for Comprehensive Company Summary: Provide a broader overview of the company’s main services. Ensure the summary covers all key offerings, including services related to any relevant platforms, tools, or industries. Reflect the company's expertise in delivering customized solutions, strategic consultations, and tailored implementations. Adapt the summary to be relevant to the company’s specific industry or niche, ensuring scalability across diverse fields.

Brevity and Clarity: Both summaries should be concise, clear, and comprehensive, effectively conveying the company’s expertise without unnecessary details.

Customization: After generating the summaries, adapt the examples provided to better fit the specific details and context of the domain and YouTube transcript. Ensure that the tone and style match the intended audience (e.g., formal vs. informal, technical vs. marketing-focused).

Handling Complex or Niche Services: For companies offering specialized or niche services, ensure the summaries accurately reflect these unique offerings. Highlight the company’s specific value proposition and how it stands out in its industry.

Desired Output Format:

/* ADDITION: Structure the output as JSON with keys for pipeline consumption: */
{
"tutorial_summary": {
"what_we_do": string,       // Aligned statement for tutorial topic
"services_highlighted": [   // Array of services from domain tied to transcript
string
],
"keywords_used": [string]   // Primary & secondary keywords
},
"company_overview": {
"company_name": string,
"core_services": [string],     // Main service categories
"expertise_areas": [string],   // Customization, implementation, consultation, etc.
"industries_served": [string],  // Relevant industries
"unique_value_prop": string,   // Key differentiator
"keywords_used": [string]
},
"audit_complete": boolean         // Always true if summaries provided
}

Tutorial-Specific Summary:

Reflect how the domain’s services support the tutorial topic. Use the transcript context and scraped service data.

Comprehensive Company Summary:

Offer a full overview of services, expertise areas, industries, and unique value.

Audit:

Verify that all transcript insights and domain-scraped data are covered. Ensure clarity, brevity, and alignment with keywords."""