from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from web_scraper import scrape_web_content
from summarizer import summarize_content
from output_handler import output_result

# 定义状态类
class WebSummaryState(TypedDict):
    url: str
    content: str
    summary: str
    save_to_file: bool

# 定义节点函数
def scrape_node(state: WebSummaryState):
    """爬取网页内容的节点"""
    print(f"正在爬取网页内容: {state['url']}")
    content = scrape_web_content(state["url"])
    if not content:
        raise Exception("爬取网页内容失败")
    
    print(f"成功爬取内容，长度: {len(content)} 字符")
    return {"content": content}

def summarize_node(state):
    """总结内容的节点"""
    print("正在总结内容...")
    summary = summarize_content(state["content"])
    if not summary or summary == "总结失败":
        raise Exception("总结内容失败")
    
    print(f"成功总结内容，长度: {len(summary)} 字符")
    return {"summary": summary}

def output_node(state):
    """输出结果的节点"""
    print("正在输出结果...")
    output_result(state["url"], state["summary"], save_to_file=state["save_to_file"])
    return {}

# 创建图
def create_graph():
    """创建并返回LangGraph图"""
    builder = StateGraph(WebSummaryState)
    
    # 添加节点
    builder.add_node("scrape", scrape_node)
    builder.add_node("summarize", summarize_node)
    builder.add_node("output", output_node)
    
    # 添加边
    builder.add_edge(START, "scrape")
    builder.add_edge("scrape", "summarize")
    builder.add_edge("summarize", "output")
    builder.add_edge("output", END)
    
    # 编译图
    return builder.compile()

# 运行图的函数
def run_graph(url: str, save_to_file: bool = False):
    """运行LangGraph工作流"""
    # 创建图
    graph = create_graph()
    
    # 定义初始状态
    initial_state: WebSummaryState = {
        "url": url,
        "content": "",
        "summary": "",
        "save_to_file": save_to_file
    }
    
    # 运行图
    try:
        result = graph.invoke(initial_state)
        print("工作流执行完成")
        return result
    except Exception as e:
        print(f"工作流执行失败: {e}")
        return None

if __name__ == "__main__":
    import sys
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("用法: python langgraph_app.py <URL> [--save]")
        sys.exit(1)
    
    url = sys.argv[1]
    save_to_file = "--save" in sys.argv
    
    # 运行图
    run_graph(url, save_to_file)