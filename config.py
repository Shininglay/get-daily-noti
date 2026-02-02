# encoding: utf-8
import os

# ==========================================
# 1. 基础配置 (从 GitHub Secrets 读取 Token)
# ==========================================
TOKEN = os.environ.get('GH_TOKEN') 
USERNAME = 'Shininglay'     # <--- 修改这里
REPO_OWNER = 'Shininglay'   # <--- 修改这里
REPO_NAME = 'daily-paper-bot'          # <--- 修改这里 (例如: daily-paper-bot)

# ==========================================
# 2. 关键词设置 (针对 可穿戴/MEMS/微流控)
# ==========================================
# 只要标题或摘要包含以下任意一个词，就会被抓取
KEYWORD_LIST = [
    # --- MEMS & 传感器 ---
    "the","MEMS", "NEMS",
    "piezoelectric", "triboelectric", # 压电/摩擦电
    "cantilever", "resonator",
    
    # --- 微流控 (Microfluidics) ---
    "microfluidic", "nanofluidic",
    "lab-on-a-chip", "organ-on-a-chip",
    "droplet", "microchannel",
    
    # --- 可穿戴 & 柔性电子 ---
    "wearable", "e-skin", "electronic skin",
    "flexible electronics", "stretchable",
    "soft robotics", "epidermal",
    
    # --- 医疗/生物应用 ---
    "biosensor", "implantable", "neural interface"
]

# ==========================================
# 3. RSS 数据源列表 (涵盖主流期刊)
# ==========================================
RSS_FEEDS = [
    # --- Nature 系列 ---
    {'name': 'Nature Electronics', 'url': 'https://www.nature.com/natelectron.rss'},
    {'name': 'Nature Materials', 'url': 'https://www.nature.com/nmat.rss'},
    {'name': 'Nature Comm', 'url': 'https://www.nature.com/ncomms.rss'},
    {'name': 'Microsystems & Nanoeng', 'url': 'https://www.nature.com/micronano.rss'}, # Nature旗下MEMS专刊
    
    # --- Science 系列 ---
    {'name': 'Science Robotics', 'url': 'https://www.science.org/rss/journal/robotics'},
    {'name': 'Science Advances', 'url': 'https://www.science.org/rss/journal/advances'},
    
    # --- ACS (美国化学会) ---
    {'name': 'ACS Sensors', 'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ascefj'},
    {'name': 'ACS Nano', 'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ancac3'},
    
    # --- RSC (英国皇家化学会) ---
    {'name': 'Lab on a Chip', 'url': 'https://feeds.rsc.org/RSS/LC/Latest'},
    
    # --- IEEE (电子电气) ---
    # IEEE J. MEMS (MEMS权威期刊)
    {'name': 'IEEE J-MEMS', 'url': 'https://ieeexplore.ieee.org/rss/TOC10.XML?isnumber=4359967'}, 
    
    # --- ArXiv (补充最新预印本) ---
    {'name': 'ArXiv (App-Phys)', 'url': 'http://export.arxiv.org/rss/physics.app-ph'},
    {'name': 'ArXiv (EESS)', 'url': 'http://export.arxiv.org/rss/eess'}
]
