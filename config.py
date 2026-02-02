# encoding: utf-8
import os

# ==========================================
# 1. 基础配置
# ==========================================
TOKEN = os.environ.get('GH_TOKEN') 
USERNAME = 'Shininglay'            
REPO_OWNER = 'Shininglay'          
REPO_NAME = 'get-daily-noti' 

# ==========================================
# 2. 关键词狙击
# ==========================================
KEYWORD_LIST = [
    # --- 核心传感器技术 ---
    "sensor", "sensing", "biosensor", "gas sensor",
    "photodetector", "strain sensor", "pressure sensor",
    "electrochemical sensor", "optical sensor",
    
    # --- 柔性与穿戴 ---
    "flexible electronics", "stretchable", 
    "epidermal", "e-skin", "electronic skin",
    "bio-integrated", "transient electronics",
    "soft robotics", "haptic",
    "organic semiconductor", "OFET",
    "self-healing", "hydrogel",
    
    # --- 微纳制造与系统 ---
    "MEMS", "NEMS", "microfluidic", "lab-on-a-chip",
    "CMOS", "heterogeneous integration", 
    "neuropixels", "neural interface", 
    "nanosheet" # 已去除 GaN
]

# ==========================================
# 3. 黄金 RSS 数据源
# ==========================================
RSS_FEEDS = [
    # [Tier 0] 神级顶刊
    {'name': 'Nature (Main)', 'url': 'https://www.nature.com/nature.rss'},
    {'name': 'Science (Main)', 'url': 'https://www.science.org/rss/journal/science'},

    # [Tier 1] 电子/材料/工程
    {'name': 'Nature Electronics', 'url': 'https://www.nature.com/natelectron.rss'},
    {'name': 'Nature Materials', 'url': 'https://www.nature.com/nmat.rss'},
    {'name': 'Nature Comm', 'url': 'https://www.nature.com/ncomms.rss'},
    {'name': 'Science Robotics', 'url': 'https://www.science.org/rss/journal/robotics'},
    {'name': 'Science Advances', 'url': 'https://www.science.org/rss/journal/advances'},

    # [Tier 2] 传感器与微系统
    {'name': 'ACS Sensors', 'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ascefj'},
    {'name': 'IEEE Sensors Journal', 'url': 'https://ieeexplore.ieee.org/rss/TOC10.XML?punumber=7361'},
    {'name': 'IEEE J-MEMS', 'url': 'https://ieeexplore.ieee.org/rss/TOC10.XML?punumber=4359967'},
    {'name': 'Lab on a Chip', 'url': 'https://feeds.rsc.org/RSS/LC/Latest'},

    # [Tier 3] 材料与纳米
    {'name': 'ACS Nano', 'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ancac3'},
    {'name': 'Nature Biomedical Eng', 'url': 'https://www.nature.com/natbiomedeng.rss'},

    # [Tier 4] 预印本
    {'name': 'ArXiv (App-Phys)', 'url': 'http://export.arxiv.org/rss/physics.app-ph'},
    {'name': 'ArXiv (EESS)', 'url': 'http://export.arxiv.org/rss/eess'}
]
