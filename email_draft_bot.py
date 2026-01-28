#!/usr/bin/env python3
"""
Email Draft Saver Chatbot
A professional email drafts maker that extracts recipient information and generates drafts.
"""

import re
import sys
from typing import Dict, Optional, Tuple


class EmailDraftBot:
    """Chatbot for creating professional email drafts from text."""
    
    def __init__(self):
        self.draft = {}
        
    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_name(self, text: str) -> Optional[str]:
        """Extract name from text using various patterns."""
        # Pattern 1: "name = John" or "name: John" or "name=John"
        # Match up to 3 capitalized words after name marker
        name_pattern1 = r'name\s*[=:]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})'
        match = re.search(name_pattern1, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Stop at common words that indicate end of name
            stop_words = ['applying', 'for', 'position', 'at', 'regarding', 'about', 
                         'meeting', 'interview', 'role', 'job', 'from', 'to']
            name_parts = []
            for word in name.split():
                if word.lower() in stop_words:
                    break
                name_parts.append(word)
            if name_parts:
                return ' '.join(name_parts)
        
        # Pattern 2: Look for capitalized words that might be names
        words = text.split()
        for i, word in enumerate(words):
            if word and word[0].isupper() and not word.isupper() and len(word) > 1:
                # Check if it's not an email domain or common word
                if '@' not in word and word.lower() not in ['dear', 'hi', 'hello', 'to', 'from']:
                    return word
        
        return None
    
    def get_first_name(self, full_name: str) -> str:
        """Extract first name from full name."""
        if not full_name:
            return ""
        return full_name.split()[0]
    
    def extract_role_or_company(self, text: str, email: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract role and company from text and email."""
        role = None
        company = None
        
        # Extract company from email domain
        if email:
            domain_match = re.search(r'@([a-zA-Z0-9-]+)', email)
            if domain_match:
                company = domain_match.group(1).capitalize()
        
        # Look for role keywords
        role_keywords = ['developer', 'engineer', 'manager', 'director', 'designer', 
                        'analyst', 'consultant', 'coordinator', 'specialist', 'lead',
                        'recruiter', 'hr', 'ceo', 'cto', 'cfo', 'position', 'role',
                        'job', 'opportunity', 'interview', 'application', 'meeting']
        
        text_lower = text.lower()
        for keyword in role_keywords:
            if keyword in text_lower:
                # Try to find the role context
                if 'application' in text_lower or 'applying' in text_lower:
                    role = 'job application'
                elif 'interview' in text_lower:
                    role = 'interview'
                elif 'meeting' in text_lower:
                    role = 'meeting'
                elif keyword in ['recruiter', 'hr']:
                    role = 'recruitment'
                elif keyword in ['developer', 'engineer', 'manager', 'designer']:
                    role = keyword
                else:
                    role = 'professional inquiry'
                break
        
        return role, company
    
    def generate_subject(self, role: Optional[str], company: Optional[str], 
                        name: Optional[str]) -> str:
        """Generate appropriate subject line based on context."""
        if role == 'job application':
            if company:
                return f"Application for Position at {company}"
            return "Job Application"
        elif role == 'interview':
            return "Interview Follow-up"
        elif role == 'meeting':
            if company:
                return f"Meeting Request - {company}"
            return "Meeting Request"
        elif role == 'recruitment':
            return "Regarding Job Opportunity"
        elif role and company:
            if role == 'professional inquiry':
                return f"Professional Inquiry - {company}"
            return f"Inquiry Regarding {role.capitalize()} Position at {company}"
        elif company:
            return f"Professional Inquiry - {company}"
        elif role:
            return f"Regarding {role.capitalize()}"
        else:
            return "Professional Communication"
    
    def generate_body(self, first_name: Optional[str], role: Optional[str], 
                     company: Optional[str], original_text: str) -> str:
        """Generate email body with personalized greeting."""
        greeting = f"Dear {first_name}," if first_name else "Dear Sir/Madam,"
        
        # Extract any additional context from original text
        # Remove email and name patterns to get the main message
        clean_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', original_text)
        clean_text = re.sub(r'name\s*[=:]\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}', '', clean_text, flags=re.IGNORECASE)
        
        # Remove common role/job keywords that were already used for context
        role_patterns = [
            r'applying\s+for\s+[a-zA-Z\s]+position',
            r'application\s+for\s+[a-zA-Z\s]+position',
            r'regarding\s+[a-zA-Z\s]+position',
            r'about\s+[a-zA-Z\s]+position',
            r'for\s+[a-zA-Z\s]+position',
            r'applying\s+for',
            r'application\s+for',
            r'interview\s+follow\s+up',
            r'meeting\s+request\s+to\s+discuss\s+[a-zA-Z\s]+',
            r'meeting\s+request',
            r'to\s+discuss\s+[a-zA-Z\s]+partnership',
            r'to\s+discuss\s+[a-zA-Z\s]+',
        ]
        
        for pattern in role_patterns:
            clean_text = re.sub(pattern, '', clean_text, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and common words
        clean_text = ' '.join(clean_text.split()).strip()
        
        # Remove if it's just leftover fragments
        if clean_text:
            words = clean_text.lower().split()
            if len(words) < 4 or all(word in ['for', 'at', 'the', 'a', 'an', 'to', 'and', 'or', 'but', 'of', 'in', 'on'] for word in words):
                clean_text = ""
        
        # Generate appropriate body based on context
        body_parts = [greeting, ""]
        
        if role == 'job application' and company:
            body_parts.append(f"I am writing to express my interest in opportunities at {company}.")
            body_parts.append("")
            if clean_text and len(clean_text) > 20:
                body_parts.append(clean_text)
                body_parts.append("")
        elif role == 'interview':
            body_parts.append("Thank you for taking the time to meet with me.")
            body_parts.append("")
            if clean_text and len(clean_text) > 20:
                body_parts.append(clean_text)
                body_parts.append("")
        elif role == 'meeting':
            body_parts.append("I would like to schedule a meeting with you to discuss a professional matter.")
            body_parts.append("")
            if clean_text and len(clean_text) > 20:
                body_parts.append(clean_text)
                body_parts.append("")
        elif clean_text and len(clean_text) > 20:
            body_parts.append(clean_text)
            body_parts.append("")
        else:
            body_parts.append("I hope this email finds you well.")
            body_parts.append("")
            body_parts.append("I am reaching out to connect with you regarding a professional matter.")
            body_parts.append("")
        
        body_parts.append("Looking forward to hearing from you.")
        body_parts.append("")
        body_parts.append("Best regards")
        
        return "\n".join(body_parts)
    
    def create_draft_from_text(self, text: str) -> Dict[str, str]:
        """Create email draft from given text."""
        # Extract information
        email = self.extract_email(text)
        name = self.extract_name(text)
        first_name = self.get_first_name(name) if name else None
        role, company = self.extract_role_or_company(text, email)
        
        # Generate draft components
        subject = self.generate_subject(role, company, name)
        body = self.generate_body(first_name, role, company, text)
        
        draft = {
            'to': email or 'recipient@example.com',
            'subject': subject,
            'body': body,
            'extracted_name': name or 'Unknown',
            'extracted_first_name': first_name or 'Unknown'
        }
        
        self.draft = draft
        return draft
    
    def format_draft(self, draft: Dict[str, str]) -> str:
        """Format draft for display."""
        formatted = f"""
{'='*60}
EMAIL DRAFT
{'='*60}

To: {draft['to']}
Subject: {draft['subject']}

{draft['body']}

{'='*60}
Extracted Information:
  - Recipient Email: {draft['to']}
  - Full Name: {draft['extracted_name']}
  - First Name: {draft['extracted_first_name']}
{'='*60}
"""
        return formatted
    
    def chat(self):
        """Main chatbot interface."""
        print("\n" + "="*60)
        print("📧  EMAIL DRAFT SAVER CHATBOT  📧")
        print("="*60)
        print("\nWelcome! I can help you create professional email drafts.")
        print("Just provide me with text containing recipient information.")
        print("\nExample: 'ravi@amazon.com name = Ravi applying for developer position'")
        print("\nType 'quit' or 'exit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("\nBot: Goodbye! Have a great day! 👋\n")
                    break
                
                # Create draft from user input
                draft = self.create_draft_from_text(user_input)
                
                # Display the draft
                print("\nBot: I've created an email draft for you:\n")
                print(self.format_draft(draft))
                
                # Ask if user wants to create another draft
                print("Would you like to create another draft? (yes/no)")
                response = input("You: ").strip().lower()
                
                if response in ['no', 'n', 'nope', 'quit', 'exit']:
                    print("\nBot: Goodbye! Have a great day! 👋\n")
                    break
                elif response in ['yes', 'y', 'yep', 'sure']:
                    print("\nBot: Great! Please provide the text for the next draft.\n")
                else:
                    print("\nBot: I'll assume that's a yes! Please provide the text for the next draft.\n")
                    
            except KeyboardInterrupt:
                print("\n\nBot: Interrupted. Goodbye! 👋\n")
                break
            except Exception as e:
                print(f"\nBot: Sorry, I encountered an error: {e}")
                print("Please try again with different text.\n")


def main():
    """Main entry point."""
    bot = EmailDraftBot()
    
    # Check if text is provided as command line argument
    if len(sys.argv) > 1:
        # Non-interactive mode
        text = " ".join(sys.argv[1:])
        draft = bot.create_draft_from_text(text)
        print(bot.format_draft(draft))
    else:
        # Interactive chatbot mode
        bot.chat()


if __name__ == "__main__":
    main()
