# Math Note Maker 📚

Convert lecture notes and mathematical documents into clean, digital formats using Mathpix OCR API. This tool processes PDFs containing mathematical notation and generates multiple output formats including LaTeX, Markdown, and HTML.

Made using Mathpix's Convert API for STEM: https://mathpix.com/convert

## Features ✨

- PDF processing with mathematical formula recognition
- Multiple output formats (LaTeX, Markdown, HTML)
- Progress tracking with real-time status updates
- Cost estimation for API usage
- Organized output with timestamp-based filing
- Smart page detection for mathematical content

## Prerequisites 🔧

- Python 3.8+
- Mathpix API credentials
- PDF documents containing mathematical content

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/ZealousEar/LaTeX-OCR-Document-Forger.git
cd LaTeX-OCR-Document-Forger
```
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Create .env file from template:
```bash
cp .env.example .env
```
4. Add your Mathpix API credentials to .env:
Get your key from: https://mathpix.com/convert
```bash
MATHPIX_APP_ID='your_app_id_here'
MATHPIX_APP_KEY='your_app_key_here'
```

Usage 💡
Basic Usage
Run the script with default settings:
```bash
python src/main.py
```

Advanced Usage
Use command line arguments for custom settings:
```bash
python src/main.py --pdf "path/to/your/notes.pdf" --output "custom/output/dir" --profile
```

Command Line Options
```bash
--pdf: Specify input PDF path
--output: Set custom output directory
--profile: Enable performance profiling
```

Output Formats 📄
- LaTeX (.tex)
  Full mathematical precision
  Source code for typesetting
  Includes all equations and formatting
- Markdown (.md)
  Clean, readable text
  Embedded mathematical formulas
  Easy to edit and version control
- HTML
  Web-ready format
  Interactive elements
  Styled mathematical content

Cost Estimation 💰
The tool provides cost estimates based on Mathpix API pricing:

- PDF Processing: $0.025/page (0-40K pages)
- Bulk Processing: $0.01/page (40K+ pages)

Cost optimization features:
- Smart page detection
- Mathematical content analysis
- Selective processing

Error Handling 🔍
The tool handles various error scenarios:

- Invalid API credentials
- PDF processing failures
- Network connectivity issues
- Timeout conditions
Contributing 🤝
- Fork the repository
- Create a feature branch
- Commit changes
- Push to the branch
- Open a Pull Request

Best Practices 📌
- Keep API credentials secure
- Monitor API usage costs
- Regular backups of processed notes
- Version control of output files

License 📜
MIT License - see LICENSE file for details

Support 💪
For support:

- Open an issue
- Check existing documentation
- Review closed issues

Acknowledgments 🙏
- Mathpix API for OCR capabilities

Version History 📝
v1.0.0: Initial release
- Basic PDF processing
- Multiple output formats
- Cost estimation
