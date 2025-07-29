from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Annotated, Literal, Self

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()
engine = create_async_engine("sqlite+aiosqlite:///reviews.db", echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def db_session() -> AsyncGenerator[AsyncSession]:
    async with session_maker.begin() as session:
        yield session


session_di = Annotated[AsyncSession, Depends(db_session)]


async def sentiments_dict() -> dict[Literal["positive", "negative"], set[str]]:
    positive_state = "positive"
    negative_state = "negative"
    positive_words = {"хорош", "люблю"}
    negative_words = {"плох", "ненавиж"}
    return {
        positive_state: positive_words,
        negative_state: negative_words,
    }


sentiment_di = Annotated[dict, Depends(sentiments_dict)]


class PostReviewDTO(BaseModel):
    text: str


class GetReviewDTO(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


class ReviewORM(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column()
    sentiment: Mapped[str] = mapped_column()
    created_at: Mapped[str] = mapped_column()

    @staticmethod
    def from_text(
        text: str,
        sentiments: dict[Literal["positive", "negative"], set[str]],
    ) -> "ReviewORM":
        return ReviewORM(
            text=text,
            sentiment=ReviewORM.get_sentiment(text, sentiments),
            created_at=datetime.now(UTC).isoformat(),
        )

    @staticmethod
    def get_sentiment(
        text: str,
        sentiments: dict[Literal["positive", "negative"], set[str]],
    ) -> Literal["positive", "negative", "neutral"]:
        for sentiment, keywords in sentiments.items():
            if any(keyword in text for keyword in keywords):
                return sentiment
        return "neutral"

    def to_dto(self: Self) -> GetReviewDTO:
        return GetReviewDTO(
            id=self.id,
            text=self.text,
            sentiment=self.sentiment,
            created_at=self.created_at,
        )


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


app = FastAPI(on_startup=[create_tables])


@app.post("/reviews")
async def post_review(
    data: PostReviewDTO,
    sentiments: sentiment_di,
    session: session_di,
) -> GetReviewDTO:
    review = ReviewORM.from_text(data.text, sentiments)
    session.add(review)
    await session.commit()
    return review.to_dto()


@app.get("/reviews")
async def get_reviews(
    session: session_di,
    sentiment: Annotated[
        Literal["positive", "negative", "neutral"] | None,
        Query(),
    ] = None,
) -> list[GetReviewDTO]:
    if sentiment is None:
        return [review.to_dto() for review in await session.scalars(select(ReviewORM))]
    return [
        review.to_dto()
        for review in await session.scalars(
            select(ReviewORM).where(ReviewORM.sentiment == sentiment),
        )
    ]
