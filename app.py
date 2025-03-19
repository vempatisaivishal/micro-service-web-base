import asyncio
import streamlit as st
from typing import Dict, Any, List
import google.generativeai as genai
from firecrawl import FirecrawlApp


st.set_page_config(
    page_title="Gemini Deep Research Agent",
    page_icon="📘",
    layout="wide"
)


if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = ""
if "firecrawl_api_key" not in st.session_state:
    st.session_state.firecrawl_api_key = ""


with st.sidebar:
    st.title("API Configuration")
    gemini_api_key = st.text_input(
        "Gemini API Key", 
        value=st.session_state.gemini_api_key,
        type="password"
    )
    firecrawl_api_key = st.text_input(
        "Firecrawl API Key", 
        value=st.session_state.firecrawl_api_key,
        type="password"
    )
    

    if gemini_api_key:
        st.session_state.gemini_api_key = gemini_api_key
    if firecrawl_api_key:
        st.session_state.firecrawl_api_key = firecrawl_api_key


if st.session_state.gemini_api_key:
    genai.configure(api_key=st.session_state.gemini_api_key)


st.title("📘 Gemini Deep Research Agent")
st.markdown("This Gemini Agent performs deep research on any topic using Firecrawl")


research_topic = st.text_input("Enter your research topic:", placeholder="e.g., Latest developments in AI")


async def deep_research(query: str, max_depth: int, time_limit: int, max_urls: int) -> Dict[str, Any]:
    """Perform comprehensive web research using Firecrawl's deep research endpoint."""
    if not st.session_state.firecrawl_api_key:
        st.error("Firecrawl API key is missing.")
        return {"error": "Firecrawl API key is missing", "success": False}
    
    try:
        firecrawl_app = FirecrawlApp(api_key=st.session_state.firecrawl_api_key)
        
        params = {
            "maxDepth": max_depth,
            "timeLimit": time_limit,
            "maxUrls": max_urls
        }
        
        def on_activity(activity):
            st.write(f"[{activity['type']}] {activity['message']}")
        
        with st.spinner("Performing deep research..."):
            results = firecrawl_app.deep_research(
                query=query,
                params=params,
                on_activity=on_activity
            )
        
        if 'data' not in results or 'finalAnalysis' not in results['data']:
            st.error("Invalid response from Firecrawl API.")
            return {"error": "Invalid Firecrawl response", "success": False}
        
        return {
            "success": True,
            "final_analysis": results['data']['finalAnalysis'],
            "sources_count": len(results['data']['sources']),
            "sources": results['data']['sources']
        }
    except Exception as e:
        st.error(f"Deep research error: {str(e)}. Check API key or network.")
        return {"error": str(e), "success": False}


def get_gemini_model(model_name="gemini-1.5-flash"):
    """Initialize and return a Gemini model instance."""
    if not st.session_state.gemini_api_key:
        st.error("Gemini API key is missing.")
        return None
    try:
        return genai.GenerativeModel(model_name)
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None


async def run_research_with_gemini(query: str, research_function):
    """Run research using Gemini model."""
    model = get_gemini_model()
    if not model:
        return "Failed to initialize Gemini model. Please check your API key."
    
    research_results = await research_function(
        query=query,
        max_depth=3,
        time_limit=180,
        max_urls=10
    )
    
    if not research_results.get("success", False):
        return f"Research failed: {research_results.get('error', 'Unknown error')}"
    
   
    sources_text = "\n\n".join([
        f"Source {i+1}: {source['url']}\nSummary: {source.get('summary', 'No summary available')}"
        for i, source in enumerate(research_results['sources'][:5])
        if 'url' in source 
    ])
    
    research_prompt = f"""
    You are a research assistant analyzing the following research results on: "{query}"
    
    Final Analysis from research tool:
    {research_results['final_analysis']}
    
    Sources ({research_results['sources_count']} total):
    {sources_text}
    
    Please organize these research findings into a well-structured academic report with:
    1. Executive Summary
    2. Key Findings 
    3. Detailed Analysis
    4. Implications
    5. Conclusion
    6. References (properly cite all sources)
    
    Format the report in Markdown.
    """
    
    try:
        response = model.generate_content(research_prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini generation error: {str(e)}")
        return f"Failed to generate report: {str(e)}"


async def enhance_report_with_gemini(topic: str, initial_report: str):
    """Enhance the report using Gemini model."""
    model = get_gemini_model()
    if not model:
        return "Failed to initialize Gemini model. Please check your API key."
    
    enhancement_prompt = f"""
    RESEARCH TOPIC: {topic}
    
    INITIAL RESEARCH REPORT:
    {initial_report}
    
    As an expert content enhancer specializing in research elaboration, please enhance this research report by:
    1. Adding more detailed explanations of complex concepts
    2. Including relevant examples, case studies, and real-world applications
    3. Expanding on key points with additional context and nuance
    4. Adding visual elements descriptions (charts, diagrams, infographics)
    5. Incorporating latest trends and future predictions
    6. Suggesting practical implications for different stakeholders
    
    Maintain academic rigor and factual accuracy while making the report more comprehensive.
    Format the enhanced report in Markdown.
    """
    
    try:
        response = model.generate_content(enhancement_prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini enhancement error: {str(e)}")
        return f"Failed to enhance report: {str(e)}"

async def run_research_process(topic: str):
    """Run the complete research process."""
    with st.spinner("Conducting initial research..."):
        initial_report = await run_research_with_gemini(topic, deep_research)
    
    if isinstance(initial_report, str) and "Failed" in initial_report:
        return initial_report
    
    with st.expander("View Initial Research Report"):
        st.markdown(initial_report)
    
    with st.spinner("Enhancing the report with additional information..."):
        enhanced_report = await enhance_report_with_gemini(topic, initial_report)
    
    return enhanced_report


if st.button("Start Research", disabled=not (st.session_state.gemini_api_key and st.session_state.firecrawl_api_key and research_topic)):
    if not st.session_state.gemini_api_key or not st.session_state.firecrawl_api_key:
        st.warning("Please enter both API keys in the sidebar.")
    elif not research_topic:
        st.warning("Please enter a research topic.")
    else:
        async def run():
            try:
                report_placeholder = st.empty()
                enhanced_report = await run_research_process(research_topic)
                if "Failed" not in enhanced_report:
                    report_placeholder.markdown("## Enhanced Research Report")
                    report_placeholder.markdown(enhanced_report)
                    st.download_button(
                        "Download Report",
                        enhanced_report,
                        file_name=f"{research_topic.replace(' ', '_')}_report.md",
                        mime="text/markdown"
                    )
                else:
                    st.error(enhanced_report)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        
        
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.run(run())


st.markdown("---")
st.markdown("Powered by Google Gemini 1.5 Flash and Firecrawl")