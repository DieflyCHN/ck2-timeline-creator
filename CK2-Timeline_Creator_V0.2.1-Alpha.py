import re
# from title_gain_extractor import extract_title_gain_events, find_parent_title_key


print("""
=========================================================
CK2 Timeline Creator V0.2.1 Alpha
---------------------------------------------------------
功能：
从解压后的十字军之王2的 .ck2 存档（纯文本）中
- 提取玩家曾操控过的君主传承历史
- 生成时间线（包含以下内容）：
      即位、去世、获取头衔
=========================================================
""")

"""
=========================================================
版本日志
---------------------------------------------------------
V0.1 Alpha
---------------------------------------------------------
新增：
1. 日期规范函数 normalize_date
2. 角色最高头衔获取及头衔-人话翻译器
修复：
1. 解析 character_history 中的裸日期的错误
2. 预先建立角色死亡日期索引（避免重复全文件扫描）
---------------------------------------------------------
V0.2 Alpha
---------------------------------------------------------
新增：
1. 君主名字计数器（xx几世）
2. 君主头衔获取
修复：
1. 君主可能即“无头衔”位的错误
（即此前并没有爵位，是当场获得的。以即位当日获取的最高爵位代替）
---------------------------------------------------------
V0.2.1 Alpha
---------------------------------------------------------
修复：
1. 调整 Unknown_Name 的世次计数逻辑，使其与有名角色一致，避免世系语义歧义
2. 重构即位 / 去世头衔判定逻辑
   - primary_title 仅作为角色离世时的最高头衔使用
   - 即位头衔改为通过 accession_title 按时间向前回溯确定
=========================================================
"""

# ========================
# 工具函数
# ========================

def normalize_date(date_str):
    """
    将 CK2 日期统一为 YYYY.MM.DD
    例如：
        769.1.1   -> 0769.01.01
        1111.11.1 -> 1111.11.01
    """
    if date_str == "unknown":
        return date_str

    parts = date_str.split(".")
    if len(parts) != 3:
        return date_str  # 防御性处理

    year, month, day = parts
    return f"{year.zfill(4)}.{month.zfill(2)}.{day.zfill(2)}"

def grab_char_value(regex):
    """
    在当前 chardata 中查找字段，返回清洗后的值
    返回 None 表示不存在或不可读
    """
    m = re.search(regex, chardata)
    if not m:
        return None

    val = m.group(1)
    if any(ord(c) < 32 for c in val):
        return None

    return val

def get_name_from_char():
    # 优先 bn，其次 name
    name = grab_char_value(r'bn="([^"]+)"')
    if not name:
        name = grab_char_value(r'name="([^"]+)"')
    return name if name else "Unknown_Name"

def get_primary_title_from_char():
    # 取最高级别的一个：e > k > d > c
    titles = re.findall(r'oh="([^"]+)"', chardata)
    if not titles:
        return "n_No Title"

    # 简单优先级
    for prefix in ("e_", "k_", "d_", "c_"):
        for t in titles:
            if t.startswith(prefix):
                return t
    return titles[0]

def format_title(t):
    #头衔-人话翻译器
    
    # 确保是裸 key（防御）
    t = t.strip()


    if t.startswith("n_"):
        return f"无头衔"
    if "dyn_" in t:
        return "自建帝国皇帝"
    
    location = t[2:].capitalize()
    
    if t.startswith('e_'):
        return f"{location}帝国皇帝"
    if t.startswith('k_'):
        return f"{location}国国王"
    if t.startswith('d_'):
        return f"{location}公爵"
    if t.startswith('c_'):
        return f"{location}伯爵"
    return f"Title: {t}"

def infer_highest_title_up_to_date(ruler_id, query_date):
    """
    查询给定日期（含）之前，该角色曾获得过的最高头衔。

    逻辑：
    - 在 title_gain_table 中查找该 ruler 在 query_date 及之前的所有头衔获得记录
    - 按等级优先级返回最高的一个（e > k > d > c）
    - 若完全没有记录，返回 None
    """

    q_date = normalize_date(query_date)

    # ① 收集该日期及之前的所有 title gain
    past_gains = [
        row["title"]
        for row in title_gain_table
        if row["ruler"] == str(ruler_id)
        and normalize_date(row["date"]) <= q_date
    ]

    if not past_gains:
        return None

    # ② 按等级优先级返回最高头衔
    for prefix in ("e_", "k_", "d_", "c_"):
        for t in past_gains:
            if t.startswith(prefix):
                return t

    # 防御性返回（理论上不会发生）
    return past_gains[0]

from collections import defaultdict
# 君主名字计数器
regnal_counter = defaultdict(int)

def to_roman(num):
    #阿拉伯数字->罗马数字
    if not isinstance(num, int) or num <= 0:
        return ""

    roman_map = [
        (1000, "M"),
        (900,  "CM"),
        (500,  "D"),
        (400,  "CD"),
        (100,  "C"),
        (90,   "XC"),
        (50,   "L"),
        (40,   "XL"),
        (10,   "X"),
        (9,    "IX"),
        (5,    "V"),
        (4,    "IV"),
        (1,    "I"),
    ]

    result = ""
    for value, symbol in roman_map:
        while num >= value:
            result += symbol
            num -= value
    return result

def iter_history_blocks(data):
    """
    顺序遍历所有「真正的」history = { ... }
    不管 title，不管 ruler
    """
    import re

    for m in re.finditer(r'^[ \t]*history\s*=\s*\{', data, re.MULTILINE):
        start = m.end()
        depth = 1
        i = start

        while i < len(data):
            if data[i] == '{':
                depth += 1
            elif data[i] == '}':
                depth -= 1
                if depth == 0:
                    yield m.start(), data[start:i]
                    break
            i += 1

def find_parent_title_key_fast(hist_pos, title_ranges):
    for start, end, title_key in title_ranges:
        if start < hist_pos < end:
            return title_key
    return None

def iter_date_blocks(history_block):
        """
        逐个产出 (date, content_block)
        content_block 是完整的大括号内容（支持嵌套）
        """
        import re

        for m in re.finditer(r'(\d+\.\d+\.\d+)\s*=\s*\{', history_block):
            date = m.group(1)
            start = m.end()
            depth = 1
            i = start

            while i < len(history_block):
                if history_block[i] == '{':
                    depth += 1
                elif history_block[i] == '}':
                    depth -= 1
                    if depth == 0:
                        yield date, history_block[start:i]
                        break
                i += 1

def build_title_gain_table(data, ruler_ids, normalize_date):
    """
    返回一个 list：
    [
      { "ruler": "205072", "date": "0769.01.01", "title": "d_bourbon" },
      ...
    ]
    """
    table = []

    for hist_pos, hist in iter_history_blocks(data):

        # ① 先用最便宜的方式过滤：history 里有没有 ruler_id
        hit_rulers = [rid for rid in ruler_ids if rid in hist]
        if not hit_rulers:
            continue

        # ② 只在命中时，向上找 title
        title_key = find_parent_title_key_fast(hist_pos, title_ranges)
        if not title_key or title_key[0] not in "ekdc":
            continue

        # ③ 解析日期 + holder
        for raw_date, content in iter_date_blocks(hist):
            date = normalize_date(raw_date)

            for rid in hit_rulers:
                # holder=ID
                if re.search(rf'\bholder\s*=\s*{rid}\b', content):
                    table.append({
                        "ruler": rid,
                        "date": date,
                        "title": title_key
                    })
                    continue

                # holder={ who=ID ... }
                m = re.search(
                    rf'holder\s*=\s*\{{[^{{}}]*\bwho\s*=\s*{rid}\b',
                    content,
                    re.S
                )
                if m:
                    # 你现在可以先不管 type
                    table.append({
                        "ruler": rid,
                        "date": date,
                        "title": title_key
                    })
    return table

def build_title_ranges(data):
    """
    返回列表：
    [
      (start_pos, end_pos, title_key),
      ...
    ]
    """
    import re

    ranges = []
    pattern = re.compile(r'^[ \t]*([ekdc]_[A-Za-z0-9_]+)\s*=\s*\{', re.MULTILINE)

    for m in pattern.finditer(data):
        title_key = m.group(1)
        start = m.end()
        brace = 1
        i = start

        while i < len(data):
            if data[i] == '{':
                brace += 1
            elif data[i] == '}':
                brace -= 1
                if brace == 0:
                    end = i
                    ranges.append((m.start(), end, title_key))
                    break
            i += 1

    return ranges

# ========================
# 读取存档
# ========================

print("Input save name (without .ck2):")
SAVE_FILE = input().strip()

with open(SAVE_FILE + ".ck2", "r", encoding="latin-1", errors="ignore") as f:
    data = f.read()

title_ranges = build_title_ranges(data)
print("title blocks:", len(title_ranges))

# ========================
# 提取 character_history
# ========================

m = re.search(r'character_history=\{(.+?)\n\}', data, re.S)
if not m:
    raise RuntimeError("未找到 character_history")

history_block = m.group(1)

# 每一个 Ruler block
ruler_blocks = list(re.finditer(r'\{[^}]*?identity=\d+[^}]*?\}', history_block, re.S))

# ========================
# Timeline 容器
# ========================

timeline = []

ruler_ids = set()

# ========================
# title_gain_table 生成
# ========================

for rb in ruler_blocks:
    m_id = re.search(r'identity=(\d+)', rb.group(0))
    if m_id:
        ruler_ids.add(m_id.group(1))

title_gain_table = build_title_gain_table(
    data,
    ruler_ids,
    normalize_date
)
print("title gain events:", len(title_gain_table))


# ========================
# 主循环：解析 Ruler
# ========================

for idx, rb in enumerate(ruler_blocks):
    block = rb.group(0)

    # ---- Ruler ID ----
    m_id = re.search(r'identity=(\d+)', block)
    if not m_id:
        continue
    ruler_id = m_id.group(1)
    # ---- 抓取完整角色块（复用旧逻辑）----
    m_char = re.search(rf'{ruler_id}=\n\t\t\{{.+?\n\t\t\}}', data, re.S)
    chardata = m_char.group(0) if m_char else ""
    # ---- 角色名+世次----
    char_name = get_name_from_char()
    regnal_counter[char_name] += 1
    regnal_number = to_roman(regnal_counter[char_name])
    # ---- 即位日期（裸日期字符串）----
    m_date = re.search(r'"(\d+\.\d+\.\d+)"', block)
    accession_date = m_date.group(1) if m_date else "unknown"
    # ---- 死亡日期（从角色块抓）----
    death_date = grab_char_value(r'd_d="(\d+\.\d+\.\d+)"')
    # ---- 角色即位头衔确定 ----
    raw_title = infer_highest_title_up_to_date(ruler_id, accession_date)
    accession_title = format_title(raw_title) if raw_title else "无头衔"
    # ---- 角色去世（最高）头衔确定 ----
    primary_title = get_primary_title_from_char() #读取存档中的最高头衔
    if primary_title.startswith("n_"):
        #如果读不到最高头衔，标记为 Not Confirmed（通常意味着角色未死亡）
        primary_title = "Not Confirmed"
    else:
        primary_title = format_title(primary_title)

    
# ========================
# 写入Timeline
# ========================

    timeline.append({
        "date": normalize_date(accession_date),
        "type": "ACCESSION",
        "ruler_index": idx,
        "char_name": char_name,
        "accession_title": accession_title,
        "regnal_number": regnal_number
    })

    if death_date:
        timeline.append({
            "date": normalize_date(death_date),
            "type": "DEATH",
            "ruler_index": idx,
            "char_name": char_name,
            "primary_title": primary_title,
            "regnal_number": regnal_number
        })

    for row in title_gain_table:
        if row["ruler"] != str(ruler_id):
            continue
        timeline.append({
            "date": row["date"],
            "type": "TITLE_GAIN",
            "display": f"{char_name} {regnal_number} 获得 {format_title(row['title'])}头衔"
        })

# ========================
# 排序 Timeline
# ========================

timeline.sort(key=lambda e: e["date"])

# ========================
# 输出
# ========================

OUT_FILE = "timeline.txt"

with open(OUT_FILE, "w", encoding="utf-8") as out:
    out.write("=== CK2 TIMELINE ===\n\n")

    for e in timeline:
        if e["type"] == "ACCESSION":
            out.write(f'{e["date"]}  世代{e["ruler_index"]} {e["char_name"]} {e["regnal_number"]} 即 {e["accession_title"]}位\n')
        elif e["type"] == "DEATH":
            out.write(f'{e["date"]}  {e["primary_title"]} {e["char_name"]} {e["regnal_number"]} 去世\n\n')
        elif e["type"] == "TITLE_GAIN":
            out.write(f'{e["date"]}  {e["display"]}\n')

print("完成：timeline.txt 已生成")
