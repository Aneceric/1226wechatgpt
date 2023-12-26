import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_page(url, visited_urls, output_directory):
    # 如果URL已经访问过，直接返回
    if url in visited_urls:
        return

    # 如果URL不是http或https的scheme，直接返回
    if not url.startswith(('http:', 'https:')):
        return

    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取所有文本内容
    all_text = soup.get_text()

    # 保存文本内容到文件
    relative_path = urlparse(url).path
    file_path = os.path.join(output_directory, relative_path.lstrip('/').replace('/', '_') + '.txt')

    # 创建输出目录
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(all_text)

    print(f'Text content saved to {file_path}')

    # 将当前URL标记为已访问
    visited_urls.add(url)

    # 获取页面中的所有链接
    links = soup.find_all('a', href=True)
    for link in links:
        # 构建绝对URL
        absolute_url = urljoin(url, link['href'])
        # 递归抓取子页面
        crawl_page(absolute_url, visited_urls, output_directory)

    # 引入延时，避免过于频繁地访问
    time.sleep(1)

if __name__ == "__main__":
    # 指定目标网站的URL
    base_url = 'https://gethover.com/'

    # 指定保存文件的目录
    output_directory = 'C:\\Users\\Chanson\\Desktop\\output'

    # 用集合来存储已访问的URL，避免重复访问
    visited_urls = set()

    # 开始抓取页面
    crawl_page(base_url, visited_urls, output_directory)
