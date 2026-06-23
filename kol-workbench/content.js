// 工作台内容源文件（由 content.json 生成；可视化编辑后用「导出内容」覆盖此文件并提交）
window.DEFAULT_CONTENT = {
  "meta": {
    "brand": "moomoo",
    "deckTitle": "植入内容策略",
    "year": "2026",
    "exportName": "moomoo-植入内容策略"
  },
  "pages": [
    {
      "id": "cover",
      "type": "cover",
      "title": "植入内容策略",
      "year": "2026",
      "subtitle": "moomoo × KOL 内容合作框架",
      "tags": ["内容场景", "核心功能", "植入指南"]
    },
    {
      "id": "index",
      "type": "index",
      "eyebrow": "植入策略",
      "heading": "11 个内容场景",
      "scenarios": [
        { "num": "01", "title": "SpaceX 上市 / 估值热点", "desc": "从产业链和受益标的的角度切入，分析哪些上市公司有望分享商业航天红利。", "tags": ["AI Brief", "News", "主题板块", "股票对比"] },
        { "num": "02", "title": "6 月 FOMC 会议", "desc": "聚焦美联储最新利率决议、点阵图变化及鲍威尔发言，分析降息路径调整。", "tags": ["宏观数据", "经济日历", "News", "AI Brief"] },
        { "num": "03", "title": "明星科技股基本面分析", "desc": "以英伟达、微软、Meta 为例，拆解收入增长、利润率和估值水平。", "tags": ["基本面分析", "股票对比", "AI Brief"] },
        { "num": "04", "title": "核心经济数据发布", "desc": "围绕 CPI、非农就业、PCE 等关键数据，分析市场为何剧烈波动。", "tags": ["经济日历", "宏观数据", "News", "热力图"] },
        { "num": "05", "title": "板块分析（能源股）", "desc": "结合油价走势、地缘政治和供需变化，分析能源板块近期表现及后续机会。", "tags": ["主题板块", "热力图", "股票对比", "基本面"] },
        { "num": "06", "title": "稳定币与加密支付革命", "desc": "随着稳定币监管框架落地，分析 Circle、Coinbase 等核心受益公司。", "tags": ["主题板块", "News", "股票对比", "AI Brief"] },
        { "num": "07", "title": "AI 产业链最新机会", "desc": "从 AI 应用、算力到电力需求，梳理产业链变化，寻找英伟达之外的受益公司。", "tags": ["主题板块", "热力图", "股票筛选器"] },
        { "num": "08", "title": "美股新高的分析", "desc": "标普 500 和纳指不断创新高，拆解推动市场上涨的核心因素。", "tags": ["热力图", "宏观数据", "News", "AI Brief"] },
        { "num": "09", "title": "机器人与自动化浪潮", "desc": "人形机器人和工业自动化升温，分析特斯拉、Figure AI 及供应链最新进展。", "tags": ["主题板块", "News", "股票对比"] },
        { "num": "10", "title": "AI 泡沫还是新时代？", "desc": "讨论当前估值是否合理，通过历史科技周期对比判断市场所处阶段。", "tags": ["股票对比", "基本面分析", "机构评级"] },
        { "num": "11", "title": "机构最新持仓变化", "desc": "解读伯克希尔最新 13F 文件，分析巴菲特近期增减持背后的逻辑。", "tags": ["机构持仓", "股票对比", "基本面分析"] }
      ]
    },
    {
      "id": "feature-macro",
      "type": "feature",
      "featureNo": "01",
      "eyebrow": "FEATURE 01 · MACRO DATA",
      "title": "宏观数据",
      "subtitle": "MACRO ECONOMIC DATA",
      "bullets": [
        "一站式查看美国核心经济数据，包括 CPI、PPI、非农就业、GDP、失业率等",
        "数据可视化展示，支持历史趋势对比，无需自己整理 Excel 表格",
        "FOMC 会议、降息预期、点阵图等关键信息集中呈现，一图看懂货币政策走向",
        "帮助投资者从宏观角度理解市场，而不仅仅盯着个股涨跌"
      ],
      "scenarioTags": ["6月FOMC会议", "核心经济数据发布", "美股新高分析"],
      "image": "assets/phone-macro.png",
      "video": ""
    },
    {
      "id": "feature-aibrief",
      "type": "feature",
      "featureNo": "02",
      "eyebrow": "FEATURE 02 · AI SUMMARY",
      "title": "AI Brief",
      "subtitle": "AI-POWERED STOCK BRIEFING",
      "bullets": [
        "利用 AI 快速总结个股最新动态，节省大量信息筛选时间",
        "自动提炼财报、新闻、机构观点等核心内容，去除信息噪音",
        "1 分钟就能掌握一家公司的重要变化和市场关注点",
        "特别适合跟踪英伟达、特斯拉等消息频繁的大型科技股",
        "帮助投资者快速筛选信息，避免错过关键催化剂事件"
      ],
      "scenarioTags": ["SpaceX上市热点", "6月FOMC会议", "明星科技股分析", "稳定币与加密", "美股新高分析"],
      "image": "assets/phone-aibrief.png",
      "video": ""
    },
    {
      "id": "feature-news",
      "type": "feature",
      "featureNo": "03",
      "eyebrow": "FEATURE 03 · NEWS AGGREGATION",
      "title": "News",
      "subtitle": "REAL-TIME FINANCIAL NEWS",
      "bullets": [
        "聚合全球主流财经媒体资讯，包括 Reuters、Bloomberg 等优质内容",
        "新闻与个股直接关联，方便查看对持仓的潜在影响",
        "支持实时推送，第一时间获取市场重大事件",
        "无需在多个网站之间来回切换，大幅提高研究效率",
        "特别适合跟踪财报季、政策变化和行业热点"
      ],
      "scenarioTags": ["SpaceX上市热点", "6月FOMC会议", "核心经济数据", "稳定币与加密", "机器人浪潮"],
      "image": "assets/phone-news.png",
      "video": ""
    },
    {
      "id": "feature-heatmap",
      "type": "feature",
      "featureNo": "04",
      "eyebrow": "FEATURE 04 · HEAT MAP",
      "title": "热力图",
      "subtitle": "MARKET HEAT MAP",
      "bullets": [
        "通过颜色和涨跌幅快速了解市场资金流向，一眼看出当天最强势和最弱势板块",
        "快速判断 AI、能源、半导体等板块是否正在获得资金追捧",
        "直观发现市场热点，辅助判断当日交易主线和市场情绪",
        "可按行业、市值等多维度切换，发现不同层面的资金动向"
      ],
      "scenarioTags": ["核心经济数据", "板块分析（能源）", "AI产业链机会", "美股新高分析"],
      "image": "assets/phone-heatmap.png",
      "video": ""
    },
    {
      "id": "feature-sectors",
      "type": "feature",
      "featureNo": "05",
      "eyebrow": "FEATURE 05 · THEMATIC SECTORS",
      "title": "主题板块",
      "subtitle": "THEMATIC INVESTMENT SECTORS",
      "bullets": [
        "将相关公司按照热门主题进行归类，快速锁定投资机会",
        "覆盖 AI、机器人、自动驾驶、核能、稳定币等市场热点赛道",
        "不仅能找到龙头公司，还能发现产业链上下游的潜在标的",
        "当热点爆发时，可以快速挖掘受益标的，把握市场节奏"
      ],
      "scenarioTags": ["SpaceX上市热点", "板块分析（能源）", "稳定币与加密", "AI产业链机会", "机器人浪潮"],
      "image": "assets/phone-sectors.png",
      "video": ""
    },
    {
      "id": "feature-compare",
      "type": "feature",
      "featureNo": "06",
      "eyebrow": "FEATURE 06 · STOCK COMPARISON",
      "title": "股票对比",
      "subtitle": "MULTI-STOCK COMPARISON",
      "bullets": [
        "多维度快速对比不同公司的估值、盈利能力和成长性",
        "特别适合比较同赛道公司，例如英伟达 vs AMD、Coinbase vs Robinhood",
        "直观呈现 PE、EPS、营收增速等核心指标差异，辅助理性选股决策",
        "帮助内容创作者生成有说服力的对比内容，提升视频数据可信度"
      ],
      "scenarioTags": ["SpaceX上市热点", "明星科技股分析", "板块分析（能源）", "稳定币与加密", "AI泡沫讨论", "机构持仓变化"],
      "image": "assets/phone-compare.png",
      "video": ""
    },
    {
      "id": "feature-fundamentals",
      "type": "feature",
      "featureNo": "07",
      "eyebrow": "FEATURE 07 · FUNDAMENTALS",
      "title": "基本面分析",
      "subtitle": "FUNDAMENTAL ANALYSIS",
      "bullets": [
        "收入、利润、毛利率等关键指标图表化展示，直观易读",
        "支持季度和年度维度查看公司成长趋势，发现拐点信号",
        "无需翻阅复杂财报，也能快速了解企业经营情况和健康状况",
        "帮助投资者建立长期投资框架，真正做到买公司而不是买代码"
      ],
      "scenarioTags": ["明星科技股分析", "板块分析（能源）", "AI泡沫讨论", "机构持仓变化"],
      "image": "assets/phone-fundamentals.png",
      "video": ""
    },
    {
      "id": "feature-smartmoney",
      "type": "feature",
      "featureNo": "08",
      "eyebrow": "FEATURE 08 · SMART MONEY",
      "title": "聪明钱 / 机构持仓",
      "subtitle": "INSTITUTIONAL HOLDINGS · SMART MONEY",
      "bullets": [
        "跟踪知名基金和机构投资者的最新持仓变化，快速发现增持、减持和新建仓动向",
        "洞察机构重点布局的行业和个股机会，挖掘 AI、半导体等热门赛道潜力标的",
        "结合机构持仓变化与股价表现，判断市场热点是否获得长期资金支持",
        "解读 13F 文件，分析巴菲特等顶级投资者的持仓逻辑，提升选股效率"
      ],
      "scenarioTags": ["机构持仓变化", "明星科技股分析", "AI产业链机会"],
      "image": "assets/phone-smartmoney.png",
      "video": ""
    }
  ]
};
