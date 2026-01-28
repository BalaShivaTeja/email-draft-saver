#!/usr/bin/env python3
"""
Test script for Email Draft Saver Chatbot
Tests various input formats and validates outputs.
"""

import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from email_draft_bot import EmailDraftBot


def test_basic_extraction():
    """Test basic email and name extraction."""
    print("Test 1: Basic email and name extraction")
    bot = EmailDraftBot()
    
    text = "ravi@amazon.com name = Ravi"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'ravi@amazon.com', f"Expected email 'ravi@amazon.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Ravi', f"Expected name 'Ravi', got {draft['extracted_name']}"
    assert draft['extracted_first_name'] == 'Ravi', f"Expected first name 'Ravi', got {draft['extracted_first_name']}"
    assert 'Dear Ravi,' in draft['body'], "Expected personalized greeting 'Dear Ravi,'"
    
    print("✓ Basic extraction test passed")
    return True


def test_full_name_extraction():
    """Test full name extraction with first and last name."""
    print("\nTest 2: Full name extraction")
    bot = EmailDraftBot()
    
    text = "sarah@microsoft.com name = Sarah Johnson"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'sarah@microsoft.com', f"Expected email 'sarah@microsoft.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Sarah Johnson', f"Expected name 'Sarah Johnson', got {draft['extracted_name']}"
    assert draft['extracted_first_name'] == 'Sarah', f"Expected first name 'Sarah', got {draft['extracted_first_name']}"
    assert 'Dear Sarah,' in draft['body'], "Expected personalized greeting 'Dear Sarah,'"
    
    print("✓ Full name extraction test passed")
    return True


def test_job_application_context():
    """Test job application context detection."""
    print("\nTest 3: Job application context detection")
    bot = EmailDraftBot()
    
    text = "emily@techcorp.com name = Emily applying for software engineer position"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'emily@techcorp.com', f"Expected email 'emily@techcorp.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Emily', f"Expected name 'Emily', got {draft['extracted_name']}"
    assert 'Application' in draft['subject'], f"Expected 'Application' in subject, got {draft['subject']}"
    assert 'Dear Emily,' in draft['body'], "Expected personalized greeting"
    
    print("✓ Job application context test passed")
    return True


def test_meeting_context():
    """Test meeting context detection."""
    print("\nTest 4: Meeting context detection")
    bot = EmailDraftBot()
    
    text = "mike@google.com name = Mike meeting request"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'mike@google.com', f"Expected email 'mike@google.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Mike', f"Expected name 'Mike', got {draft['extracted_name']}"
    assert 'Meeting' in draft['subject'], f"Expected 'Meeting' in subject, got {draft['subject']}"
    assert 'Dear Mike,' in draft['body'], "Expected personalized greeting"
    
    print("✓ Meeting context test passed")
    return True


def test_company_extraction():
    """Test company extraction from email domain."""
    print("\nTest 5: Company extraction from email domain")
    bot = EmailDraftBot()
    
    text = "john@amazon.com name = John"
    draft = bot.create_draft_from_text(text)
    
    assert 'Amazon' in draft['subject'], f"Expected 'Amazon' in subject, got {draft['subject']}"
    
    print("✓ Company extraction test passed")
    return True


def test_custom_message():
    """Test custom message handling."""
    print("\nTest 6: Custom message handling")
    bot = EmailDraftBot()
    
    text = "alice@startup.com name = Alice I would like to collaborate on the new product development initiative and explore synergies"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'alice@startup.com', f"Expected email 'alice@startup.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Alice', f"Expected name 'Alice', got {draft['extracted_name']}"
    assert 'Dear Alice,' in draft['body'], "Expected personalized greeting"
    assert 'collaborate' in draft['body'].lower() or 'product' in draft['body'].lower(), "Expected custom message content in body"
    
    print("✓ Custom message test passed")
    return True


def test_email_without_name():
    """Test handling of email without name."""
    print("\nTest 7: Email without name")
    bot = EmailDraftBot()
    
    text = "contact@example.com"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'contact@example.com', f"Expected email 'contact@example.com', got {draft['to']}"
    assert draft['extracted_name'] == 'Unknown', f"Expected 'Unknown' name, got {draft['extracted_name']}"
    assert 'Dear Sir/Madam,' in draft['body'], "Expected generic greeting"
    
    print("✓ Email without name test passed")
    return True


def test_multi_part_tld():
    """Test email with multi-part TLD."""
    print("\nTest 8: Email with multi-part TLD")
    bot = EmailDraftBot()
    
    text = "john@company.co.uk name = John"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'john@company.co.uk', f"Expected email 'john@company.co.uk', got {draft['to']}"
    assert draft['extracted_name'] == 'John', f"Expected name 'John', got {draft['extracted_name']}"
    
    print("✓ Multi-part TLD test passed")
    return True


def test_empty_input():
    """Test handling of empty input."""
    print("\nTest 9: Empty input handling")
    bot = EmailDraftBot()
    
    text = ""
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'recipient@example.com', f"Expected default email, got {draft['to']}"
    assert draft['extracted_name'] == 'Unknown', f"Expected 'Unknown' name, got {draft['extracted_name']}"
    
    print("✓ Empty input test passed")
    return True


def test_text_without_email():
    """Test text without email."""
    print("\nTest 10: Text without email")
    bot = EmailDraftBot()
    
    text = "name = Sarah Johnson looking for opportunities"
    draft = bot.create_draft_from_text(text)
    
    assert draft['to'] == 'recipient@example.com', f"Expected default email, got {draft['to']}"
    assert draft['extracted_name'] == 'Sarah Johnson', f"Expected 'Sarah Johnson', got {draft['extracted_name']}"
    assert 'Dear Sarah,' in draft['body'], "Expected personalized greeting with first name"
    
    print("✓ Text without email test passed")
    return True


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("Running Email Draft Bot Tests")
    print("="*60)
    
    tests = [
        test_basic_extraction,
        test_full_name_extraction,
        test_job_application_context,
        test_meeting_context,
        test_company_extraction,
        test_custom_message,
        test_email_without_name,
        test_multi_part_tld,
        test_empty_input,
        test_text_without_email,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
