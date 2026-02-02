# encoding: utf-8
import feedparser
import requests
import json
import datetime
import time
import pytz
from time import mktime
from config import *

# === 设置回顾时间范围 ===
# 只抓取过去 14 天内的论文，避免抓到老旧数据
MAX_LOOKBACK_DAYS = 14 

def get_current_date():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d')

def is_recent_paper(entry):
    """
    判断论文是否在最近 MAX_LOOKBACK_DAYS 天内发布
    """
    try:
        # feedparser 会自动把各种时间格式解析成 struct_time
        published_struct = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
        
        if not published_struct:
            # 如果实在找不到时间，为了保险起见，假设它是新的（或者你可以改为 False 丢弃）
            return True
            
        # 转换为 datetime 对象
        pub_date = datetime.datetime.fromtimestamp(mktime(published_struct))
        current_date = datetime.datetime.now()
        
        # 计算时间差
        delta = current_date - pub_date
        
        if delta.days <= MAX_LOOKBACK_DAYS:
            return True
        else:
            return False
    except Exception as e:
        print(f"时间解析错误: {e}")
        return True # 出错时默认保留

def fetch_rss_papers():
    print(f"开始抓取任务... (只看最近 {MAX_LOOKBACK_DAYS} 天)")
    found_papers = []
    
    for source in RSS_FEEDS:
        print(f"正在检查: {source['name']}...")
        try:
            feed = feedparser.parse(source['url'])
            if not feed.entries:
                continue

            for entry in feed.entries:
                # --- [新增] 时间过滤器 ---
                if not is_recent_paper(entry):
                    continue # 如果太旧，直接跳过，看下一篇
                # -----------------------

                title = entry.title
                summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                link = getattr(entry, 'link', '')
                # 获取展示用的时间字符串
                published = getattr(entry, 'published', '') or getattr(entry, 'updated', 'Unknown Date')
                
                content_to_check = (title + summary).lower()
                
                matched_keywords = []
                for kw in KEYWORD_LIST:
                    if kw.lower() in content_to_check:
                        matched_keywords.append(kw)
                
                if matched_keywords:
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
    md_content += f"**今日发现 {len(papers)} 篇近期({MAX_LOOKBACK_DAYS}天内)相关论文**\n\n---"
    
    current_source = ""
    for paper in papers:
        if paper['source'] != current_source:
            current_source = paper['source']
            md_content += f"\n\n## 📚 {current_source}\n"
        
        kw_str = ", ".join([f"`{k}`" for k in paper['keywords']])
        md_content += f"\n### [{paper['title']}]({paper['link']})\n"
        md_content += f"- **关键词**: {kw_str}\n"
        md_content += f"- **发布时间**: {paper['date']}\n"
        
    return md_content

def post_github_issue(content):
    if not content:
        print("今日无符合条件的新论文。")
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
    papers = fetch_rss_papers()
    md_text = generate_markdown(papers)
    post_github_issue(md_text)
