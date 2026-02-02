# encoding: utf-8
import feedparser
import requests
import json
import datetime
import time
import pytz
from config import *

def get_current_date():
    # 获取北京时间
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d')

def fetch_rss_papers():
    print(f"开始抓取任务... 共 {len(RSS_FEEDS)} 个订阅源")
    found_papers = []
    
    for source in RSS_FEEDS:
        print(f"正在检查: {source['name']}...")
        try:
            feed = feedparser.parse(source['url'])
            # 检查是否有内容
            if not feed.entries:
                continue

            for entry in feed.entries:
                # 获取标题和摘要（不同RSS源字段名可能不同，做个容错）
                title = entry.title
                summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                link = getattr(entry, 'link', '')
                published = getattr(entry, 'published', '') or getattr(entry, 'updated', 'Unknown Date')
                
                # 关键词匹配 (标题 或 摘要 包含关键词)
                # 将标题和摘要转为小写进行比对
                content_to_check = (title + summary).lower()
                
                matched_keywords = []
                for kw in KEYWORD_LIST:
                    if kw.lower() in content_to_check:
                        matched_keywords.append(kw)
                
                if matched_keywords:
                    # 找到符合的论文！
                    paper_info = {
                        'source': source['name'],
                        'title': title.replace('\n', ' '),
                        'link': link,
                        'date': published,
                        'keywords': matched_keywords
                    }
                    found_papers.append(paper_info)
                    
        except Exception as e:
            print(f"抓取 {source['name']} 失败: {e}")
            
    return found_papers

def generate_markdown(papers):
    if not papers:
        return None
    
    date_str = get_current_date()
    md_content = f"# 📅 Daily Paper Update: {date_str}\n\n"
    md_content += f"**今日发现 {len(papers)} 篇相关论文**\n\n---"
    
    # 按来源分组显示
    current_source = ""
    for paper in papers:
        if paper['source'] != current_source:
            current_source = paper['source']
            md_content += f"\n\n## 📚 {current_source}\n"
        
        # 格式化每篇论文
        kw_str = ", ".join([f"`{k}`" for k in paper['keywords']])
        md_content += f"\n### [{paper['title']}]({paper['link']})\n"
        md_content += f"- **关键词**: {kw_str}\n"
        md_content += f"- **发布时间**: {paper['date']}\n"
        
    return md_content

def post_github_issue(content):
    if not content:
        print("今日无新发现，不创建 Issue。")
        return

    if not TOKEN:
        print("错误：未设置 GH_TOKEN，无法发送 Issue。")
        return

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    date_str = get_current_date()
    payload = {
        "title": f"[{date_str}] Daily Papers ({len(content.split('###')) - 1} papers)",
        "body": content,
        "labels": ["daily-report"]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print("✅ Issue 创建成功！")
    else:
        print(f"❌ 创建失败: {response.status_code}")
        print(response.text)

if __name__ == '__main__':
    # 1. 抓取
    papers = fetch_rss_papers()
    
    # 2. 生成内容
    md_text = generate_markdown(papers)
    
    # 3. 发送到 GitHub Issue
    post_github_issue(md_text)
