from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from core.config import settings
from core.database import init_db, get_db
from models.article import SearchRequest, SearchResponse, SearchDB, ArticleDB, SearchSchema
from services.original_spider import OriginalScholarSpider
from services.export import ExportService


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": settings.app_version}


@app.post("/api/search", response_model=SearchResponse)
async def search_articles(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    search_record = SearchDB(
        keyword=request.keyword,
        start_year=request.start_year,
        end_year=request.end_year
    )
    db.add(search_record)
    await db.commit()
    await db.refresh(search_record)
    
    try:
        async with OriginalScholarSpider() as spider:
            articles = await spider.search(
                keyword=request.keyword,
                num_results=request.num_results,
                start_year=request.start_year,
                end_year=request.end_year
            )
        
        # Return empty results if nothing found
        if not articles:
            print(f"No results found for '{request.keyword}' - may be blocked by Google Scholar")
        
        if request.sort_by == "citations":
            articles.sort(key=lambda x: x.citations, reverse=True)
        elif request.sort_by == "citations_per_year":
            articles.sort(key=lambda x: x.citations_per_year, reverse=True)
        elif request.sort_by == "year":
            articles.sort(key=lambda x: x.year or 0, reverse=True)
        
        for article in articles:
            article_db = ArticleDB(
                title=article.title,
                authors=article.authors,
                venue=article.venue,
                publisher=article.publisher,
                year=article.year,
                citations=article.citations,
                citations_per_year=article.citations_per_year,
                description=article.description,
                url=article.url,
                search_id=search_record.id
            )
            db.add(article_db)
        
        search_record.total_results = len(articles)
        await db.commit()
        
        return SearchResponse(
            search_id=search_record.id,
            keyword=request.keyword,
            total_results=len(articles),
            articles=articles
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/searches", response_model=List[SearchSchema])
async def get_search_history(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SearchDB)
        .options(selectinload(SearchDB.articles))
        .order_by(SearchDB.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    searches = result.scalars().all()
    return searches


@app.get("/api/search/{search_id}", response_model=SearchSchema)
async def get_search_details(
    search_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SearchDB)
        .options(selectinload(SearchDB.articles))
        .where(SearchDB.id == search_id)
    )
    search = result.scalar_one_or_none()
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    return search


@app.get("/api/export/{search_id}")
async def export_search_results(
    search_id: int,
    format: str = "csv",
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SearchDB)
        .options(selectinload(SearchDB.articles))
        .where(SearchDB.id == search_id)
    )
    search = result.scalar_one_or_none()
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    articles = [ArticleSchema.model_validate(article) for article in search.articles]
    
    if format == "csv":
        content = ExportService.to_csv(articles)
        media_type = "text/csv"
        filename = f"scholar_results_{search.keyword}.csv"
    elif format == "json":
        content = ExportService.to_json(articles)
        media_type = "application/json"
        filename = f"scholar_results_{search.keyword}.json"
    elif format == "excel":
        content = ExportService.to_excel(articles)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"scholar_results_{search.keyword}.xlsx"
    elif format == "bibtex":
        content = ExportService.to_bibtex(articles)
        media_type = "text/plain"
        filename = f"scholar_results_{search.keyword}.bib"
    else:
        raise HTTPException(status_code=400, detail="Invalid export format")
    
    return Response(
        content=content,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@app.delete("/api/search/{search_id}")
async def delete_search(
    search_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SearchDB)
        .options(selectinload(SearchDB.articles))
        .where(SearchDB.id == search_id)
    )
    search = result.scalar_one_or_none()
    
    if not search:
        raise HTTPException(status_code=404, detail="Search not found")
    
    await db.delete(search)
    await db.commit()
    
    return {"message": "Search deleted successfully"}