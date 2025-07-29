from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.globals import set_debug
import os

# 配置Qwen模型
qwen_model = ChatOpenAI(
    model="qwen-max",
    api_key="sk-4d11eafb5c424cf780c4638f490a8fda",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.1
)

def summarize_content(content: str) -> str:
    """
    使用Qwen模型对文本内容进行总结。
    
    Args:
        content (str): 要总结的文本内容。
        
    Returns:
        str: 总结结果。
    """
    # 定义提示模板
    template = """
    请对以下文本内容进行总结，提取出最重要的信息：
    
    {text}
    
    总结:
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=qwen_model, prompt=prompt)
    
    try:
        # 调用模型进行总结
        summary = chain.run(text=content)
        return summary
    except Exception as e:
        print(f"总结内容时出错: {e}")
        return "总结失败"

if __name__ == "__main__":
    # 测试函数
    text = "这是一个测试文本，用于验证总结功能是否正常工作。"
    summary = summarize_content(text)
    print(f"总结结果: {summary}")