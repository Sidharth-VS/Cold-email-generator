# Cold Email Generator

A Streamlit-based application that generates personalized cold emails for job applications by scraping job postings and matching them with your portfolio.

## Features

- **Web Scraping**: Extracts job details from career pages
- **AI-Powered Generation**: Uses LLaMA 3.1 through Groq API to generate personalized emails
- **Portfolio Management**: Store and query your tech stack and portfolio links
- **Vector Database**: Uses ChromaDB for efficient similarity search of skills
- **Interactive UI**: Streamlit-based web interface for easy use

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sidharth-VS/Cold-email-generator.git
   cd Cold-email-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app/Generate.py
   ```

## Usage

### 1. Portfolio Management
- Navigate to the Portfolio page
- Add your tech stack and portfolio links
- The system will store them in a vector database for matching

### 2. Generate Cold Emails
- Enter the job posting URL
- Fill in your name, role, and organization
- Click "Generate Mail" to create personalized emails
- The system will:
  - Scrape job details from the URL
  - Match required skills with your portfolio
  - Generate a personalized cold email

## API Keys

You'll need a Groq API key to use the LLaMA model:
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account and get your API key
3. Add it to your `.env` file
