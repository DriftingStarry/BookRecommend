class Book:
    """Book"""
    """作者"""
    authors: str
    """平均评分"""
    avgRating: float
    """图片地址，尺寸为 medium"""
    cover: str
    """goodreads上的id"""
    goodreadsId: str
    id: int
    """语言"""
    lang: str
    """评分数量"""
    ratingsCount: str
    """书名"""
    title: str
    """发布年份"""
    year: int

    def __init__(self, authors: str, avgRating: float, cover: str, goodreadsId: str, id: int, lang: str, ratingsCount: str, title: str, year: int) -> None:
        self.authors = authors
        self.avgRating = avgRating
        self.cover = cover
        self.goodreadsId = goodreadsId
        self.id = id
        self.lang = lang
        self.ratingsCount = ratingsCount
        self.title = title
        self.year = year
        
    def to_dict(self):
        return {
            "authors": self.authors,
            "avgRating": self.avgRating,
            "cover": self.cover,
            "goodreadsId": self.goodreadsId,
            "id": self.id,
            "lang": self.lang,
            "ratingsCount": self.ratingsCount,
            "title": self.title,
            "year": self.year
        }