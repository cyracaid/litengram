"""
Example: Using LitEngram Python API directly
"""

import os
from scripts.zotero_sync import ZoteroDB
from scripts.synthesize_notes import process_paper
from scripts.notion_sync import sync_to_notion

def example_1_simple_update():
    """Example 1: Update a single annotation"""
    print("\n=== Example 1: Simple Annotation Update ===")
    
    db = ZoteroDB(db_path=os.environ['ZOTERO_DB_PATH'])
    db.connect()
    
    # Get all annotations for a paper
    annotations = db.get_annotations(parent_item_id=4429)
    print(f"✓ Found {len(annotations)} annotations")
    
    # Update first one
    if annotations:
        result = db.update_annotation(
            item_id=annotations[0]['itemID'],
            comment="【定义】Working memory is...",
            author_name="Lintengram"
        )
        print(f"✓ Updated: {result['status']}")
    
    db.close()

def example_2_batch_processing():
    """Example 2: Batch process entire paper"""
    print("\n=== Example 2: Batch Processing Paper ===")
    
    result = process_paper(
        paper_id="Lamichhane2020_Nback",
        parent_item_id=4429,
        llm_model="qwen2.5:0.5b"
    )
    
    print(f"✓ Paper: {result['paper_id']}")
    print(f"✓ Annotations processed: {result['annotations_processed']}")
    print(f"✓ Parsed (rule-first): {result['annotations_parsed']}")
    print(f"✓ Generated (LLM): {result['annotations_llm_generated']}")
    print(f"✓ Duration: {result['duration_seconds']:.1f}s")
    
    if result['status'].startswith('✅'):
        print("✓ Success!")

def example_3_with_notion_sync():
    """Example 3: Process + sync to Notion"""
    print("\n=== Example 3: With Notion Sync ===")
    
    # Process paper
    result = process_paper(
        paper_id="MyPaper2024",
        parent_item_id=4429
    )
    
    print(f"✓ Paper processed: {result['annotations_processed']} annotations")
    
    # Sync to Notion (if token available)
    if os.environ.get('NOTION_TOKEN'):
        notion_result = sync_to_notion(
            paper_key="ABC123DEF456",
            annotations_json=result.get('annotations', {}),
            notion_token=os.environ['NOTION_TOKEN']
        )
        print(f"✓ Synced to Notion: {notion_result['notion_page_id']}")

def example_4_verify_quality():
    """Example 4: Verify annotation quality"""
    print("\n=== Example 4: Verify Annotation Quality ===")
    
    db = ZoteroDB(db_path=os.environ['ZOTERO_DB_PATH'])
    db.connect()
    
    # Verify all annotations
    report = db.verify_annotations(parent_item_id=4429)
    
    print(f"✓ Total: {report['total']}")
    print(f"✓ Valid: {report['valid']}")
    print(f"✓ Invalid: {report['invalid']}")
    
    if report['missing_authorName']:
        print(f"✗ Missing authorName: {report['missing_authorName']}")
    
    if report['missing_comment']:
        print(f"✗ Missing comment: {report['missing_comment']}")
    
    db.close()

if __name__ == "__main__":
    print("LitEngram Python API Examples")
    
    example_1_simple_update()
    example_2_batch_processing()
    example_3_with_notion_sync()
    example_4_verify_quality()
    
    print("\n✓ All examples completed!")
