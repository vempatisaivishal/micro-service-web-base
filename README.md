
# Gemini Deep Research Agent

**A Streamlit-based research tool powered by Google Gemini and Firecrawl**

The **Gemini Deep Research Agent** is an interactive web application designed to perform comprehensive research on any user-provided topic. It leverages the Google Gemini 1.5 Flash model for natural language processing and the Firecrawl API for web scraping and deep research. The tool generates detailed academic-style reports in Markdown format, complete with executive summaries, key findings, analyses, and enhanced content featuring examples, trends, and visual element descriptions.

This project is ideal for researchers, students, or anyone needing in-depth, structured insights on a topic without manually scouring the web.

---

## Features

- **Deep Web Research**: Uses Firecrawl to crawl and analyze web content up to a specified depth, time limit, and URL count.
- **AI-Powered Reports**: Employs Google Gemini to create initial research reports and enhance them with detailed explanations, examples, and future predictions.
- **Interactive UI**: Built with Streamlit for an intuitive, browser-based experience with real-time feedback.
- **Downloadable Output**: Exports enhanced reports as Markdown files for easy sharing or further editing.
- **Customizable**: Allows users to input API keys and research topics via a sidebar interface.

---

## Prerequisites

To run this project locally, ensure you have the following:

- **Python 3.8+**: The project is written in Python.
- **API Keys**:
  - A valid **Google Gemini API key** (for generative AI capabilities).
  - A valid **Firecrawl API key** (for web crawling and research).
- **Dependencies**: Install required Python libraries (see [Installation](#installation)).

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/vempatisaivishal/micro-service-web-base.git
   cd micro-service-web-base
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:


   ```bash
   pip install -r requirements.txt
   ```

4. **Save the Code**:
   Copy the provided Python script into a file named `app.py` in your project directory.

---

## Usage

1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   This will launch the app in your default web browser (typically at `http://localhost:8501`).

2. **Configure API Keys**:
   - In the sidebar, enter your **Gemini API Key** and **Firecrawl API Key**.
   - These keys are stored in the session state and persist during your session.

3. **Start Research**:
   - Enter a research topic (e.g., "Latest developments in AI") in the text input field.
   - Click the **"Start Research"** button.
   - The app will:
     - Perform deep web research using Firecrawl.
     - Generate an initial report with Gemini.
     - Enhance the report with additional context and details.
     - Display the enhanced report and offer a download option.

4. **View Results**:
   - Expand the "View Initial Research Report" section to see the preliminary findings.
   - The final enhanced report appears under "Enhanced Research Report" with a download button.

---

## Project Structure

```
micro-service-web-base/
├── app.py    # Main application script
├── requirements.txt     # List of Python dependencies
└── README.md           # This documentation file
```

---

## How It Works

1. **Input**: User provides a research topic and API keys via the Streamlit interface.
2. **Web Research**: The `deep_research` function uses Firecrawl to crawl the web based on the topic, with configurable parameters (max depth, time limit, max URLs).
3. **Initial Report**: The `run_research_with_gemini` function processes Firecrawl’s results with Gemini, generating a structured academic report.
4. **Enhanced Report**: The `enhance_report_with_gemini` function refines the initial report, adding detailed explanations, examples, and visual descriptions.
5. **Output**: The final report is displayed in Markdown and can be downloaded.

---

## Troubleshooting

- **Error: `'summary'`**: If a source from Firecrawl lacks a `'summary'` field, the app now handles it gracefully by displaying "No summary available."
- **API Key Issues**: Ensure your Gemini and Firecrawl API keys are valid and have sufficient quotas.
- **Blank Output**: Check your internet connection and API status if no results appear.
- **Async Errors**: The app uses `nest_asyncio` to handle nested event loops; ensure it’s installed.

For additional help, check the terminal output when running `streamlit run` or raise an issue on the repository.

---

## Limitations

- **API Dependence**: Requires active Gemini and Firecrawl subscriptions; downtime or rate limits may affect performance.
- **Response Variability**: Firecrawl’s web scraping results may vary based on web content availability and structure.
- **Processing Time**: Deep research and enhancement can take several minutes depending on the topic and API response times.

---

## Future Enhancements someone can contribute to

- Add caching to store research results and avoid redundant API calls.
- Support additional AI models beyond Gemini (e.g., via Hugging Face).
- Include options to customize report sections or research parameters.
- Integrate visualizations directly into the Streamlit UI.

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License

special thanks to unwind ai

---

## Acknowledgments

- Powered by [Google Gemini 1.5 Flash](https://cloud.google.com/gemini) and [Firecrawl](https://firecrawl.io/).
- Built with [Streamlit](https://streamlit.io/) for an awesome UI experience.

