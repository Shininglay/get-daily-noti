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
MAX_LOOKBACK_DAYS = 30 

# === 新增：去重检测范围 ===
# 检查过去多少个 Issue 来防止重复？建议设为 30 (覆盖过去一个月)
DUPLICATE_CHECK_COUNT = 30

def get_current_date():
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime('%Y-%m-%d')

def is_recent_paper(entry):
    """判断论文是否在最近 MAX_LOOKBACK_DAYS 天内发布"""
    try:
        published_struct = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
        if not published_struct:
            return True
        pub_date = datetime.datetime.fromtimestamp(mktime(published_struct))
        current_date = datetime.datetime.now()
        delta = current_date - pub_date
        return delta.days <= MAX_LOOKBACK_DAYS
    except Exception as e:
        return True 

def get_already_sent_links():
    """
    获取最近发布的 Issue 内容，提取出所有已发送过的链接。
    用于去重。
    """
    if not TOKEN:
        print("警告：未设置 Token，无法获取历史记录进行去重。")
        return set()

    print(f"正在检查历史 Issue 以去重 (检查最近 {DUPLICATE_CHECK_COUNT} 个)...")
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    params = {
        "state": "all",          # 即使关闭的 Issue 也要检查
        "labels": "daily-report", # 只检查我们机器人发的
        "per_page": DUPLICATE_CHECK_COUNT
    }
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"获取历史记录失败: {response.status_code}")
            return set()
        
        issues = response.json()
        sent_links = set()
        
        # 遍历历史 Issue 的内容
        for issue in issues:
            body = issue.get('body', '')
            if body:
                # 这里做一个简单的处理：直接把 body 当作大字符串
                # 如果新论文的 link 存在于这个字符串中，就认为发过了
                # 为了提高准确率，我们可以只提取 markdown 链接，但直接包含检查通常够用了
                sent_links.add(body) 
        
        print(f"✅ 已加载历史记录，准备过滤...")
        return sent_links # 返回包含所有历史文本的集合（或长字符串列表）
        
    except Exception as e:
        print(f"获取历史记录出错: {e}")
        return set()

def fetch_rss_papers():
    # 1. 先获取历史记录
    history_contents = get_already_sent_links()
    
    print(f"开始抓取任务... (只看最近 {MAX_LOOKBACK_DAYS} 天)")
    found_papers = []
    
    for source in RSS_FEEDS:
        print(f"正在检查: {source['name']}...")
        try:
            feed = feedparser.parse(source['url'])
            if not feed.entries:
                continue

            for entry in feed.entries:
                # --- 时间过滤器 ---
                if not is_recent_paper(entry):
                    continue 

                title = entry.title
                summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
                link = getattr(entry, 'link', '')
                published = getattr(entry, 'published', '') or getattr(entry, 'updated', 'Unknown Date')
                
                # --- [新增] 核心去重逻辑 ---
                # 检查这个链接是否在之前的 Issue 正文里出现过
                is_duplicate = False
                for old_body in history_contents:
                    if link in old_body:
                        is_duplicate = True
                        break
                
                if is_duplicate:
                    # print(f"跳过已发送论文: {title}") # 调试时可打开
                    continue
                # -----------------------

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
    md_content += f"**今日发现 {len(papers)} 篇新论文**\n\n---"
    
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
        print("今日无新发现（或全部已去重），不创建 Issue。")
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
    post_github_issue(md_text)# encoding: utf-8
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
