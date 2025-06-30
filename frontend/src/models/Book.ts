/**
 * 图书数据模型
 * 基于 goodbooks-10k 数据集的结构设计
 */
export interface Book {
  /** 图书ID */
  id: number
  /** 图书标题 */
  title: string
  /** 作者 */
  authors: string
  /** 图书封面图片URL */
  cover?: string
  /** 出版年份 */
  year?: number
  /** 图书分类/标签 */
  tags?: string[]
  /** 语言 */
  lang?: string
  /** 平均评分 */
  avgRating?: number
  /** 评分数量 */
  ratingsCount?: number
  /** goodreads 图书ID */
  goodreadsId?: string
}
