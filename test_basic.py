"""
Basic test script to verify core functionality.
Run this manually to test the application without a real OpenAI API key.

Usage:
    python test_basic.py
"""
import sys
import os

# Mock the OpenAI client for testing without API key
class MockOpenAI:
    class MockMessage:
        def __init__(self):
            self.content = '''[
                {
                    "task": "Prepare Q1 sales report",
                    "owner": "John",
                    "due_date": "2024-02-16"
                },
                {
                    "task": "Review marketing materials",
                    "owner": "Sarah",
                    "due_date": null
                }
            ]'''
    
    class MockChoice:
        def __init__(self):
            self.message = MockOpenAI.MockMessage()
    
    class MockResponse:
        def __init__(self):
            self.choices = [MockOpenAI.MockChoice()]
    
    class MockCompletions:
        def create(self, **kwargs):
            return MockOpenAI.MockResponse()
    
    class MockChat:
        def __init__(self):
            self.completions = MockOpenAI.MockCompletions()
    
    def __init__(self, **kwargs):
        self.chat = MockOpenAI.MockChat()

# Inject mock before importing app modules
sys.modules['openai'] = type(sys)('openai')
sys.modules['openai'].OpenAI = MockOpenAI

from app.database import init_db, SessionLocal
from app.models import Transcript, Task
from app.llm import extract_action_items

def test_database():
    """Test database initialization."""
    print("Testing database initialization...")
    try:
        init_db()
        db = SessionLocal()
        
        # Test creating a transcript
        transcript = Transcript(text="Test meeting transcript")
        db.add(transcript)
        db.commit()
        
        # Test creating a task
        task = Task(
            transcript_id=transcript.id,
            task="Test task",
            owner="Test User",
            status="open"
        )
        db.add(task)
        db.commit()
        
        # Verify
        assert db.query(Transcript).count() == 1
        assert db.query(Task).count() == 1
        
        # Cleanup
        db.query(Task).delete()
        db.query(Transcript).delete()
        db.commit()
        db.close()
        
        print("✓ Database tests passed")
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_llm_extraction():
    """Test LLM extraction (with mock)."""
    print("Testing LLM extraction...")
    try:
        transcript = """
        Team meeting - Feb 14, 2024
        John will prepare the Q1 sales report by Friday.
        Sarah will review the marketing materials.
        """
        
        items = extract_action_items(transcript)
        
        assert len(items) == 2
        assert items[0]["task"] == "Prepare Q1 sales report"
        assert items[0]["owner"] == "John"
        assert items[1]["owner"] == "Sarah"
        
        print("✓ LLM extraction tests passed")
        return True
    except Exception as e:
        print(f"✗ LLM extraction test failed: {e}")
        return False

def test_models():
    """Test SQLAlchemy models."""
    print("Testing models...")
    try:
        from app.models import Transcript, Task
        from datetime import datetime
        
        # Create instances
        t = Transcript(text="Test")
        task = Task(
            transcript_id=1,
            task="Test task",
            owner="User",
            due_date="2024-02-20",
            status="open"
        )
        
        assert t.text == "Test"
        assert task.task == "Test task"
        assert task.status == "open"
        
        print("✓ Model tests passed")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas."""
    print("Testing schemas...")
    try:
        from app.schemas import TaskCreate, TranscriptCreate
        
        # Test task schema
        task = TaskCreate(
            task="Test task",
            owner="John",
            due_date="2024-02-20"
        )
        assert task.task == "Test task"
        
        # Test transcript schema
        transcript = TranscriptCreate(text="Test transcript")
        assert transcript.text == "Test transcript"
        
        print("✓ Schema tests passed")
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Running Basic Functionality Tests")
    print("="*50 + "\n")
    
    results = []
    
    results.append(("Models", test_models()))
    results.append(("Schemas", test_schemas()))
    results.append(("Database", test_database()))
    results.append(("LLM Extraction", test_llm_extraction()))
    
    print("\n" + "="*50)
    print("Test Results")
    print("="*50)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name:20} {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("="*50)
    if all_passed:
        print("✓ All tests passed!")
        print("\nYou can now run the application:")
        print("  python run.py")
    else:
        print("✗ Some tests failed. Check errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
