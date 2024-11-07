# ============ CONFIGURATION ============
INPUT_CONFIG = {
    "pdf_path": "",
    "output_dir": "processed_notes"
}

# Mathpix API processing options
PROCESSING_OPTIONS = {
    "conversion_formats": {
        "md": True,          # Markdown for easy reading
        "tex.zip": True,     # LaTeX for mathematical precision
        "html": True         # Web-friendly format
    },
    "math_inline_delimiters": ["$", "$"],
    "math_display_delimiters": ["$$", "$$"],
    "rm_spaces": True,
    "enable_tables_fallback": True,  # For financial tables
    "include_equation_tags": True,   # Preserve equation numbering
    "numbers_default_to_math": True  # Treat numbers as math mode
}

# API endpoints
API_BASE_URL = 'https://api.mathpix.com/v3'
API_ENDPOINTS = {
    'pdf': f'{API_BASE_URL}/pdf',
    'status': lambda pdf_id: f'{API_BASE_URL}/pdf/{pdf_id}',
    'download': lambda pdf_id, fmt: f'{API_BASE_URL}/pdf/{pdf_id}.{fmt}'
}

# Output formats
OUTPUT_FORMATS = {
    'mmd': 'Mathpix Markdown',
    'tex.zip': 'LaTeX with images',
    'html': 'HTML rendering'
}

# Processing settings
POLLING_INTERVAL = 2  # seconds between status checks
TIMEOUT = 600        # maximum processing time in seconds

# ============ CODE IMPLEMENTATION ============ #
import os
from dotenv import load_dotenv
import requests
import json
from pathlib import Path
from time import sleep
from typing import Dict, List, Optional
from datetime import datetime
from tqdm import tqdm

import argparse
import logging
import signal
import sys
import cProfile

class MathpixProcessor:
    def __init__(self):
        load_dotenv()
        self.app_id = os.getenv('MATHPIX_APP_ID')
        self.app_key = os.getenv('MATHPIX_APP_KEY')
        
        if not self.app_id or not self.app_key:
            raise EnvironmentError(
                "Missing Mathpix credentials. Please set MATHPIX_APP_ID and MATHPIX_APP_KEY in .env file"
            )
            
        self.headers = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'Content-Type': 'application/json'
        }

    def process_pdf(self, pdf_path: str) -> str:
        """Process PDF and return PDF ID for tracking"""
        with open(pdf_path, 'rb') as file:
            files = {'file': file}
            data = {'options_json': json.dumps(PROCESSING_OPTIONS)}
            
            response = requests.post(
                API_ENDPOINTS['pdf'],
                headers={k: v for k, v in self.headers.items() if k != 'Content-Type'},
                files=files,
                data=data
            )
            
        if response.status_code != 200:
            raise Exception(f"PDF processing failed: {response.text}")
        return response.json()['pdf_id']

    def wait_for_processing(self, pdf_id: str) -> None:
        """Wait for PDF processing to complete with progress bar"""
        start_time = datetime.now()
        pbar = None
        
        while True:
            if (datetime.now() - start_time).total_seconds() > TIMEOUT:
                raise TimeoutError("PDF processing took too long")
                
            response = requests.get(
                API_ENDPOINTS['status'](pdf_id),
                headers=self.headers
            )
            status = response.json()
            
            if status['status'] == 'completed':
                if pbar:
                    pbar.close()
                break
            elif status['status'] == 'error':
                if pbar:
                    pbar.close()
                raise Exception(f"Processing error: {status}")
                
            progress = status.get('percent_done', 0)
            pages_done = status.get('num_pages_completed', 0)
            total_pages = status.get('num_pages', 0)
            
            if not pbar:
                pbar = tqdm(total=100, desc="Processing PDF", unit="%")
            
            pbar.n = progress
            pbar.refresh()
            
            sleep(POLLING_INTERVAL)

    def download_results(self, pdf_id: str, output_dir: Path) -> Dict[str, Path]:
        """Download all processed formats with timestamped filenames"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = output_dir / timestamp
        output_dir.mkdir(parents=True, exist_ok=True)
        outputs = {}
        
        for fmt in OUTPUT_FORMATS:
            response = requests.get(
                API_ENDPOINTS['download'](pdf_id, fmt),
                headers=self.headers
            )
            
            if response.status_code == 200:
                output_path = output_dir / f"notes_{timestamp}.{fmt}"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                outputs[fmt] = output_path
                
        return outputs

    def calculate_cost(self, num_pages: int) -> float:
        """Calculate estimated cost based on Mathpix pricing"""
        if num_pages <= 40000:
            return num_pages * 0.025
        else:
            return num_pages * 0.01

def process_lecture_notes():
    processor = MathpixProcessor()
    
    try:
        print(f"\nProcessing: {INPUT_CONFIG['pdf_path']}")
        print("Uploading PDF...")
        pdf_id = processor.process_pdf(INPUT_CONFIG['pdf_path'])
        
        processor.wait_for_processing(pdf_id)
        
        print("\nDownloading processed files...")
        output_path = Path(INPUT_CONFIG['output_dir'])
        results = processor.download_results(pdf_id, output_path)
        
        # Get number of pages from the PDF
        import PyPDF2
        with open(INPUT_CONFIG['pdf_path'], 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            num_pages = len(pdf_reader.pages)
        
        estimated_cost = processor.calculate_cost(num_pages)
        
        print("\nProcessing complete!")
        print(f"\nProcessed files location: {output_path}")
        for fmt, path in results.items():
            print(f"- {fmt}: {path.name}")
        print(f"\nEstimated cost: ${estimated_cost:.2f} (based on {num_pages} pages)")
            
    except Exception as e:
        print(f"\nError: {e}")
        raise
def signal_handler(signum, frame):
    logging.info("Received interrupt signal. Cleaning up...")
    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process lecture notes using Mathpix API")
    parser.add_argument("--pdf", help="Path to PDF file", default=INPUT_CONFIG["pdf_path"])
    parser.add_argument("--output", help="Output directory", default=INPUT_CONFIG["output_dir"])
    parser.add_argument("--profile", action="store_true", help="Enable profiling")
    args = parser.parse_args()

    # Update INPUT_CONFIG with command line arguments
    INPUT_CONFIG["pdf_path"] = args.pdf
    INPUT_CONFIG["output_dir"] = args.output

    try:
        if args.profile:
            with cProfile.Profile() as pr:
                process_lecture_notes()
                pr.print_stats()
        else:
            process_lecture_notes()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Process failed: {e}")
        sys.exit(1)