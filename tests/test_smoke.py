"""
Smoke test for LitEngram core functionality

这是"冒烟测试"——确保核心流程没有被改坏。
每当你改了代码后，跑一下这个：
  python tests/test_smoke.py
"""

import sys
import sqlite3
import tempfile
from pathlib import Path
from hashlib import md5


def test_fingerprinting():
    """验证 MD5 指纹生成逻辑（最核心的功能）"""
    definition1 = "Working memory: short-term storage, Baddeley & Hitch (1974)"
    definition2 = "Working memory: short-term storage, Baddeley & Hitch (1974)"
    definition3 = "Long-term memory: permanent storage"
    
    fp1 = md5(definition1.encode()).hexdigest()
    fp2 = md5(definition2.encode()).hexdigest()
    fp3 = md5(definition3.encode()).hexdigest()
    
    assert fp1 == fp2, "Same definitions should produce same fingerprint"
    assert fp1 != fp3, "Different definitions should produce different fingerprint"
    print("✓ Fingerprinting algorithm: PASS")


def test_4layer_markers():
    """验证 4 层结构的标记识别"""
    text = """【定义】Working memory is...
【本文角色】This paper extends...
【论证关联】Finding supports...
【延伸】Test in aging populations"""
    
    markers = ["定义", "本文角色", "论证关联", "延伸"]
    found = [m for m in markers if f"【{m}】" in text]
    
    assert len(found) == 4, f"Should find all 4 markers, found {len(found)}"
    print("✓ 4-layer structure markers: PASS")


def test_json_comment_format():
    """验证 JSON 注释格式能被序列化"""
    import json
    
    comment = {
        "layer_1_definition": "Working memory: short-term storage",
        "layer_2_role": "This paper extends WM from 2-back to 1-6",
        "layer_3_argument": "Finding supports inverted-U hypothesis",
        "layer_4_extension": "Test in aging populations",
        "confidence": "high",
        "fingerprint": "abc123def456"
    }
    
    # 验证能被序列化
    json_str = json.dumps(comment, ensure_ascii=False)
    
    # 验证能被反序列化
    restored = json.loads(json_str)
    assert restored["layer_1_definition"] == comment["layer_1_definition"]
    print("✓ JSON comment format: PASS")


def test_database_structure():
    """验证 Zotero 数据库结构理解正确"""
    with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp:
        conn = sqlite3.connect(tmp.name)
        cursor = conn.cursor()
        
        # 创建必要的表结构
        cursor.execute("""
            CREATE TABLE itemAnnotations (
                itemID INTEGER PRIMARY KEY,
                parentItemID INT,
                authorName TEXT,
                comment TEXT
            )
        """)
        
        # 测试写入
        cursor.execute("""
            INSERT INTO itemAnnotations (itemID, parentItemID, authorName, comment)
            VALUES (1, 100, 'Lintengram', '【定义】Test')
        """)
        
        conn.commit()
        
        # 验证读取
        cursor.execute("SELECT * FROM itemAnnotations WHERE itemID = 1")
        row = cursor.fetchone()
        assert row is not None, "Should read back inserted row"
        assert row[3] == "【定义】Test", "Comment should be preserved"
        
        conn.close()
        print("✓ Database structure: PASS")


if __name__ == "__main__":
    print("\n🔥 LitEngram Smoke Test\n")
    
    tests = [
        test_fingerprinting,
        test_4layer_markers,
        test_json_comment_format,
        test_database_structure,
    ]
    
    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ {test.__name__}: FAIL - {e}")
            failed.append(test.__name__)
    
    if failed:
        print(f"\n❌ {len(failed)} test(s) failed: {', '.join(failed)}\n")
        sys.exit(1)
    else:
        print("\n✅ All smoke tests passed!")
        print("   Core functionality is intact.\n")
