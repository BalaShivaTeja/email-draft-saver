# 📧 Email Draft Saver

A professional email drafts maker chatbot that intelligently extracts recipient information from text and generates personalized email drafts.

## Features

- 🤖 **Intelligent Extraction**: Automatically extracts recipient email, name, role, and company from text
- 📝 **Smart Subject Generation**: Creates contextually appropriate subject lines based on detected role/purpose
- 👤 **Personalized Body**: Generates email body with personalized greeting using recipient's first name
- 💬 **Interactive Chatbot**: Conversational interface for easy email draft creation
- ⚡ **Command Line Support**: Can be used in both interactive and non-interactive modes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BalaShivaTeja/email-draft-saver.git
cd email-draft-saver
```

2. Ensure you have Python 3.6+ installed:
```bash
python3 --version
```

3. (Optional) Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Chatbot Mode

Run the chatbot without any arguments to start an interactive session:

```bash
python3 email_draft_bot.py
```

Then provide text with recipient information:
```
You: ravi@amazon.com name = Ravi applying for developer position

Bot: I've created an email draft for you:

============================================================
EMAIL DRAFT
============================================================

To: ravi@amazon.com
Subject: Application for Position at Amazon

Dear Ravi,

I am writing to express my interest in opportunities at Amazon.

Looking forward to hearing from you.

Best regards

============================================================
```

### Command Line Mode

Pass the text directly as a command line argument:

```bash
python3 email_draft_bot.py "john.doe@company.com name = John Smith meeting request"
```

## Input Format Examples

The chatbot is flexible and can understand various input formats:

1. **Basic format with email and name:**
   ```
   ravi@amazon.com name = Ravi
   ```

2. **With job application context:**
   ```
   sarah@microsoft.com name = Sarah applying for software engineer position
   ```

3. **With meeting context:**
   ```
   mike@google.com name = Mike meeting request for project discussion
   ```

4. **With custom message:**
   ```
   alice@startup.com name = Alice I would like to discuss the partnership opportunity
   ```

## How It Works

1. **Email Extraction**: Identifies email addresses using regex patterns
2. **Name Extraction**: Detects names using patterns like "name = John" or capitalized words
3. **Context Detection**: Analyzes text for keywords (job, interview, meeting, etc.) to determine purpose
4. **Company Extraction**: Derives company name from email domain
5. **Draft Generation**: Creates professional email with:
   - Appropriate subject line based on context
   - Personalized greeting using first name
   - Contextually relevant body content
   - Professional closing

## Examples

### Example 1: Basic Email
**Input:**
```
ravi@amazon.com name = Ravi
```

**Output:**
```
To: ravi@amazon.com
Subject: Professional Inquiry - Amazon

Dear Ravi,

I hope this email finds you well.

I am reaching out to connect with you regarding a professional matter.

Looking forward to hearing from you.

Best regards
```

### Example 2: Job Application with Context
**Input:**
```
emily@techcorp.com name = Emily Johnson applying for senior developer role
```

**Output:**
```
To: emily@techcorp.com
Subject: Application for Position at Techcorp

Dear Emily,

I am writing to express my interest in opportunities at Techcorp.

Looking forward to hearing from you.

Best regards
```

### Example 3: Interview Follow-up
**Input:**
```
robert@startup.io name = Robert interview follow up thank you
```

**Output:**
```
To: robert@startup.io
Subject: Interview Follow-up

Dear Robert,

Thank you for taking the time to meet with me.

Looking forward to hearing from you.

Best regards
```

### Example 4: Multi-part TLD Support
**Input:**
```
james@company.co.uk name = James meeting request
```

**Output:**
```
To: james@company.co.uk
Subject: Meeting Request - Company

Dear James,

I would like to schedule a meeting with you to discuss a professional matter.

Looking forward to hearing from you.

Best regards
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

BalaShivaTeja

## Support

If you encounter any issues or have questions, please open an issue on GitHub. 
