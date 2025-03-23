# AI WordPress Content Manager

This Streamlit app allows you to manage and edit WordPress content (posts, pages, HivePress listings, listing categories, vendor profiles, etc.) using natural language commands. It leverages OpenAI's GPT-4 for AI-driven editing, integrates with the WordPress REST API, enriches content using full web scraping, and supports robust file uploads (images, CSV, XLSX, JSON, PDF, DOCX, TXT). Additional features include batch editing, multi-site management with encrypted credentials, error logging, and rollback functionality.

## Features

- **Multi-Content Support:** Manage posts, pages, and custom types (e.g., `hp_listing`, `hp_listing_category`).
- **Natural Language Commands:** Use plain English to instruct content creation, updates, or deletions.
- **Batch Editing:** Process multiple items at once.
- **File Uploads:** Supports images (JPG, PNG) and documents (CSV, XLSX, JSON, PDF, DOCX, TXT).
- **Web Scraping:** Extract text, images, meta tags, and YouTube video embeds from a provided URL.
- **User Roles:** Two roles – Normal User and Owner. Only the Owner can access advanced settings.
- **Multi-Site Management:** Save and select multiple WordPress sites; credentials are stored encrypted.
- **Preview & Confirmation:** Review a summary of proposed edits before applying changes.
- **Error Logging & Rollback:** Logs errors to a file and allows rollback of the last operation.
- **CI/CD:** (Optional) A GitHub Actions workflow is provided for linting.

## Getting Started

### Prerequisites

- Python 3.8+
- WordPress site(s) with REST API enabled (ensure custom post types have `show_in_rest=true`)
- WordPress Application Passwords enabled
- An OpenAI API key

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/ai-wordpress-content-manager.git
   cd ai-wordpress-content-manager
