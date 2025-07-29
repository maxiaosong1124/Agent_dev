import requests
from bs4 import BeautifulSoup
from typing import Optional

def scrape_web_content(url: str) -> Optional[str]:
    """
    爬取网页内容并提取文本。
    
    Args:
        url (str): 要爬取的网页URL。
        
    Returns:
        Optional[str]: 提取的文本内容，如果失败则返回None。
    """
    try:
        # 发送HTTP GET请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取文本内容
        # 移除script和style元素
        for script in soup(["script", "style"]):
            script.decompose()
            
        # 获取文本并清理
        text = soup.get_text()
        # 分割成行并去除每行的首尾空白
        lines = (line.strip() for line in text.splitlines())
        # 去除空白行
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # 去除空行
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"爬取网页内容时出错: {e}")
        return None

if __name__ == "__main__":
    # 测试函数
    url = "https://example.com"
    content = scrape_web_content(url)
    if content:
        print(f"成功爬取内容，前100个字符: {content[:500]}...")
    else:
        print("爬取内容失败")