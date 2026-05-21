import json
import asyncio  # Required to run async tasks cleanly
from app.agent import get_answer  # Adjusted import paths assuming standard directory setup

TEST_QUESTIONS = [
    {
        "question": "What's the difference between the Starter and Professional plans?",
        "expected_type": "answered",
        "notes": "Should compare pricing and features"
    },
    {
        "question": "Can I get a refund if I cancel after 30 days?",
        "expected_type": "answered",
        "notes": "Refund policy question"
    },
    {
        "question": "Do you support Qatar?",
        "expected_type": "not_found",
        "notes": "Not in knowledge base - should trigger ticket"
    },
    {
        "question": "What's the weather like in Dubai today?",
        "expected_type": "out_of_scope",
        "notes": "Completely out of scope"
    },
    {
        "question": "How much does the Professional plan cost?",
        "expected_type": "answered",
        "notes": "Direct pricing question"
    },
    {
        "question": "Can I upgrade my plan anytime?",
        "expected_type": "answered",
        "notes": "Plan change question"
    },
    {
        "question": "What is included in the Enterprise plan?",
        "expected_type": "answered",
        "notes": "Enterprise features question"
    },
    {
        "question": "Does the free tier include AI features?",
        "expected_type": "answered",
        "notes": "Free tier question"
    },
    {
        "question": "How do I cancel my subscription?",
        "expected_type": "answered",
        "notes": "Cancellation question"
    },
    {
        "question": "What is the annual billing discount?",
        "expected_type": "answered",
        "notes": "Billing question"
    }
]

async def evaluate():
    print("=" * 60)
    print("DWELLEO SUPPORT ASSISTANT — EVALUATION REPORT")
    print("=" * 60)
    
    results = []
    passed_cases = 0
    tickets_created = 0
    
    for i, test in enumerate(TEST_QUESTIONS, 1):
        print(f"\nQ{i}: {test['question']}")
        print(f"Expected Behavior: {test['expected_type']}")
        
       
        result = await get_answer(test['question'])
        
        print(f"Detected Intent: {result['intent']}")
        print(f"Answer: {result['answer'][:120]}...")
        print(f"Sources Provided: {result['sources']}")
        
        if result['ticket']:
            tickets_created += 1
            print(f"🎫 Ticket Logged: {result['ticket']['ticket_id']}")
        
        # Tightened evaluation logic mapping directly to your backend attributes
        is_pass = False
        
        if test['expected_type'] == 'answered':
            # Intent should be normal, and NO ticket should be generated
            if result['intent'] == 'normal' and result['ticket'] is None:
                is_pass = True
                
        elif test['expected_type'] == 'not_found':
            # Intent is normal, but because context was empty, a fallback ticket was created
            if result['intent'] == 'normal' and result['ticket'] is not None:
                is_pass = True
                
        elif test['expected_type'] == 'out_of_scope':
            # Handled directly via your intent layer out_of_scope filtering rules
            if result['intent'] == 'out_of_scope':
                is_pass = True

        status = "✅ PASS" if is_pass else "❌ FAIL"
        if is_pass:
            passed_cases += 1
            
        print(f"Status Evaluation: {status}")
        
        results.append({
            "question": test['question'],
            "expected": test['expected_type'],
            "actual_intent": result['intent'],
            "answer": result['answer'],
            "status": status,
            "ticket_created": result['ticket'] is not None
        })
    
    print("\n" + "=" * 60)
    print(f"FINAL METRIC SUMMARY")
    print(f"Total Test Cases Run : {len(TEST_QUESTIONS)}")
    print(f"Successful Passes    : {passed_cases}/{len(TEST_QUESTIONS)}")
    print(f"Tickets Generated    : {tickets_created}")
    print(f"System Accuracy Rate : {(passed_cases/len(TEST_QUESTIONS))*100:.1f}%")
    print("=" * 60)
    
    # Save validation reports
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults cleanly persisted to evaluation_results.json")

if __name__ == "__main__":
    # Correct execution wrapper for asynchronous processes running within CLI execution
    asyncio.run(evaluate())