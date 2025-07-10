import pandas as pd
import json
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from typing import List
import io
from models.article import ArticleSchema


class ExportService:
    @staticmethod
    def to_csv(articles: List[ArticleSchema]) -> bytes:
        df = pd.DataFrame([article.dict() for article in articles])
        buffer = io.BytesIO()
        df.to_csv(buffer, index=False, encoding='utf-8')
        return buffer.getvalue()
    
    @staticmethod
    def to_json(articles: List[ArticleSchema]) -> str:
        return json.dumps([article.dict() for article in articles], indent=2, default=str)
    
    @staticmethod
    def to_excel(articles: List[ArticleSchema]) -> bytes:
        df = pd.DataFrame([article.dict() for article in articles])
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Articles', index=False)
        return buffer.getvalue()
    
    @staticmethod
    def to_bibtex(articles: List[ArticleSchema]) -> str:
        db = BibDatabase()
        
        for i, article in enumerate(articles):
            entry = {
                'ENTRYTYPE': 'article',
                'ID': f'article{i+1}',
                'title': article.title,
                'author': article.authors or 'Unknown',
                'year': str(article.year) if article.year else '',
                'journal': article.venue or '',
                'publisher': article.publisher or '',
                'url': article.url or '',
                'abstract': article.description or ''
            }
            
            entry = {k: v for k, v in entry.items() if v}
            db.entries.append(entry)
        
        writer = bibtexparser.bwriter.BibTexWriter()
        return writer.write(db)