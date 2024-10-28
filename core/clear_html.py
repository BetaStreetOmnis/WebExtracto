""" 
Module for minimizing the code
"""
from bs4 import BeautifulSoup
from minify_html import minify
from urllib.parse import urljoin


def cleanup_html(html_content: str, base_url: str) -> str:
    """
    清理HTML内容并提取相关信息

    :param html_content: 输入的HTML内容
    :param base_url: 基础URL，用于处理相对路径
    :return: 返回标题、最小化的HTML内容、链接URL列表、图片URL列表和文本内容
    """

    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取标题
    title_tag = soup.find('title')
    title = title_tag.get_text() if title_tag else ""
    
    # 提取文本内容并去除空格和换行符
    text = soup.get_text().replace(' ', '').replace("\n", "")
    
    # 移除脚本和样式标签
    for tag in soup.find_all(['script', 'style']):
        tag.extract()

    # 提取链接
    links = soup.find_all('a')
    link_urls = []
    for link in links:
        if 'href' in link.attrs:
            link_urls.append(urljoin(base_url, link['href']))

    # 提取图片
    images = soup.find_all('img')
    image_urls = []
    for image in images:
        if 'src' in image.attrs:
            # 如果图片URL中没有http或https，则将其与基础URL连接
            if 'http' not in image['src']:
                image_urls.append(urljoin(base_url, image['src']))
            else:
                image_urls.append(image['src'])

    # 提取并最小化body内容（如果存在）
    body_content = soup.find('body')
    if body_content:
        # 最小化body标签内的HTML内容
        minimized_body = minify(str(body_content))

        return title, minimized_body, link_urls, image_urls, text
        # return "Title: " + title + ", Body: " + minimized_body + ", Links: " + str(link_urls) + ", Images: " + str(image_urls)

    # 如果没有找到body内容，抛出错误
    raise ValueError("No HTML body content found, please try setting the 'headless' flag to False in the graph configuration.")


if __name__ == "__main__":
    html_content = "<html><head><title>Example</title></head><body><p>Hello World!</p></body></html>"
    print(cleanup_html(html_content, ""))
