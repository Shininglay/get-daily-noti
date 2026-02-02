# encoding: utf-8
import os

# ==========================================
# 1. 基础配置
# ==========================================
TOKEN = os.environ.get('GH_TOKEN') 
USERNAME = 'Shininglay'            
REPO_OWNER = 'Shininglay'          
REPO_NAME = 'get-daily-arxiv-noti' 

# ==========================================
# 2. 关键词狙击 (覆盖 Rogers/Bao/IMEC/传感器)
# ==========================================
KEYWORD_LIST = [
    # --- 核心传感器技术 (Sensors Core) ---
    "sensor", "sensing", "biosensor", "gas sensor",
    "photodetector", "strain sensor", "pressure sensor",
    "electrochemical sensor", "optical sensor",
    
    # --- 柔性与穿戴 (Rogers/Bao Style) ---
    "flexible electronics", "stretchable", 
    "epidermal", "e-skin", "electronic skin",
    "bio-integrated", "transient electronics", # 瞬态电子
    "soft robotics", "haptic",
    "organic semiconductor", "OFET",
    "self-healing", "hydrogel",
    
    # --- 微纳制造与系统 (IMEC/MEMS) ---
    "MEMS", "NEMS", "microfluidic", "lab-on-a-chip",
    "CMOS", "heterogeneous integration", 
    "neuropixels", "neural interface", 
    "nanosheet", "GaN"
]

# ==========================================
# 3. 黄金 RSS 数据源 (顶刊 + 传感器 + 细分)
# ==========================================
RSS_FEEDS = [
    # -----------------------------------
    # [Tier 0] 神级顶刊 (Science/Nature 正刊)
    # -----------------------------------
    {
        'name': 'Nature (Main)', 
        'url': 'https://www.nature.com/nature.rss',
        'desc': '自然正刊，只看最重磅的突破'
    },
    {
        'name': 'Science (Main)', 
        'url': 'https://www.science.org/rss/journal/science',
        'desc': '科学正刊，全球科研风向标'
    },

    # -----------------------------------
    # [Tier 1] 电子/材料/工程 子刊 (必看)
    # -----------------------------------
    {
        'name': 'Nature Electronics', 
        'url': 'https://www.nature.com/natelectron.rss',
        'desc': '电子学顶刊，传感器重镇'
    },
    {
        'name': 'Nature Materials', 
        'url': 'https://www.nature.com/nmat.rss',
        'desc': '材料顶刊'
    },
    {
        'name': 'Nature Comm', 
        'url': 'https://www.nature.com/ncomms.rss',
        'desc': '综合子刊，量大且常有硬核传感器文章'
    },
    {
        'name': 'Science Robotics', 
        'url': 'https://www.science.org/rss/journal/robotics',
        'desc': '机器人与感知'
    },
    {
        'name': 'Science Advances', 
        'url': 'https://www.science.org/rss/journal/advances',
        'desc': 'Science 旗下综合大刊'
    },

    # -----------------------------------
    # [Tier 2] 传感器与微系统专业刊
    # -----------------------------------
    {
        'name': 'ACS Sensors', 
        'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ascefj',
        'desc': '化学/生物传感器权威'
    },
    {
        'name': 'IEEE Sensors Journal', 
        'url': 'https://ieeexplore.ieee.org/rss/TOC10.XML?punumber=7361',
        'desc': '工程传感器应用'
    },
    {
        'name': 'IEEE J-MEMS', 
        'url': 'https://ieeexplore.ieee.org/rss/TOC10.XML?punumber=4359967',
        'desc': 'MEMS 权威'
    },
    {
        'name': 'Lab on a Chip', 
        'url': 'https://feeds.rsc.org/RSS/LC/Latest',
        'desc': '微流控顶刊'
    },

    # -----------------------------------
    # [Tier 3] 材料与纳米 (ACS/Nature系列)
    # -----------------------------------
    {
        'name': 'ACS Nano', 
        'url': 'https://pubs.acs.org/action/showFeed?type=etoc&feed=rss&jc=ancac3',
        'desc': '纳米领域，Bao组常客'
    },
    {
        'name': 'Nature Biomedical Eng', 
        'url': 'https://www.nature.com/natbiomedeng.rss',
        'desc': '生物医学工程，Rogers 生物电子相关'
    },

    # -----------------------------------
    # [Tier 4] 预印本 (ArXiv)
    # -----------------------------------
    {
        'name': 'ArXiv (App-Phys)', 
        'url': 'http://export.arxiv.org/rss/physics.app-ph',
        'desc': '最新物理层面的器件设计'
    },
    {
        'name': 'ArXiv (EESS)', 
        'url': 'http://export.arxiv.org/rss/eess',
        'desc': '系统与信号处理'
    }
]
