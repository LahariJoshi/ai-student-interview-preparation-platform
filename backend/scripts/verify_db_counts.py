import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath("backend"))

from app.core.database import AsyncSessionLocal
from sqlalchemy import text

async def main():
    async with AsyncSessionLocal() as session:
        q_count = (await session.execute(text("SELECT count(*) FROM coding_questions"))).scalar()
        tc_count = (await session.execute(text("SELECT count(*) FROM coding_test_cases"))).scalar()
        sample = (await session.execute(text("""
            SELECT slug, title, starter_code->>'java' as java_starter, starter_code->>'python' as py_starter
            FROM coding_questions
            WHERE slug='richest-customer-wealth'
        """))).mappings().first()
        print(f"Total Questions: {q_count}")
        print(f"Total Test Cases: {tc_count}")
        if sample:
            print(f"Slug: {sample['slug']}")
            print("Java Starter snippet:")
            print(sample['java_starter'])
            print("Python Starter snippet:")
            print(sample['py_starter'])

if __name__ == "__main__":
    asyncio.run(main())
