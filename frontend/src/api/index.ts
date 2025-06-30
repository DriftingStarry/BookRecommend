import axios from 'axios'
import type { Response } from '../models'
import type { Book } from '../models'

const apiURL = import.meta.env.VITE_API_URL
console.log(apiURL)

/**
 * 创建图书API
 * @returns 图书API
 */
function createBookApi() {
  return axios.create({
    baseURL: apiURL,
  })
}

/**
 * 获取图书信息
 * @param id 图书ID
 * @returns 图书信息
 */
export async function getBookInfo(id:number) {
    const api = createBookApi()
    const data = (await api.get<Response<Book>>('/book', {params: {id:id}})).data
    console.log(data)
    return data
}

/**
 * 获取图书列表
 * @param page 页码
 * @param pageSize 每页条数
 * @returns 图书列表
 */
export async function getBookList(page:number, pageSize:number) {
    const api = createBookApi()
    const data = (await api.get<Response<Book[]>>('/books', {params: {page:page, pageSize:pageSize}})).data
    console.log(data)
    return data
}

/**
 * 获取图书推荐
 * @param id 图书ID
 * @param by 推荐方式
 * @returns 图书推荐
 */
export async function getBookRecommend(id:number, by:string) {
    const api = createBookApi()
    const data = (await api.get<Response<Book[]>>('/recommend', {params: {id:id,by:by}})).data
    console.log(data)
    return data
}