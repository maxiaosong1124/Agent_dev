from datetime import datetime
from typing import Optional

def output_result(url: str, summary: str, save_to_file: bool = False, filename: Optional[str] = None) -> None:
    """
    输出总结结果。
    
    Args:
        url (str): 爬取的网页URL。
        summary (str): 总结结果。
        save_to_file (bool): 是否保存到文件。
        filename (Optional[str]): 保存的文件名。
    """
    # 输出到控制台
    print(f"URL: {url}")
    print(f"总结结果:\n{summary}\n")
    
    # 保存到文件
    if save_to_file:
        if not filename:
            # 生成默认文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n\n")
                f.write(f"总结结果:\n{summary}\n")
            print(f"结果已保存到文件: {filename}")
        except Exception as e:
            print(f"保存文件时出错: {e}")

if __name__ == "__main__":
    # 测试函数
    url = "https://example.com"
    summary = "这是测试总结内容。"
    output_result(url, summary, save_to_file=True)