# ck2-timeline-creator
从《十字军之王 2》（Crusader Kings II，简称 CK2）的存档文件中提取君主时间线
Extract ruler timeline from Crusader Kings II save files

👉 **中文用户**：请阅读本文件
👉 **其他语言用户**：请参见 [`README.md`](README.md)
---
## 项目简介
在我个人看来，《十字军之王 2》依然是一款极具深度与系统复杂性的游戏。即便在我已经投入了大量时间游玩《十字军之王 3》之后，我仍然会频繁回到 CK2。

我在 CK2 上投入的时间远多于 CK3，并且至今仍在长期游玩。

在完成一局较长的战役后，我往往会希望回顾自己王朝的历史——谁曾统治、何时即位、获得过哪些头衔，以及何时去世。

然而，对于使用中文本地化模组的玩家而言，CK2 自带的“编年史 / 历史书”导出功能经常会发生闪退，导致无法在游戏内回顾完整的王朝历史。

本项目正是为了解决这一问题而诞生。

**CK2 Timeline Creator** 会直接解析一个未压缩的 CK2 存档文件（`.ck2`），并重建玩家曾操控过的君主及其重要历史事件的按时间排序的时间线。

在 AI 时代，这份时间线也可以作为结构化历史素材，用于进一步生成战役故事、叙事总结或其他文本内容，因此在设计上刻意保持了机器可读性。

---
## 功能特性
- 从 CK2 存档中提取玩家君主的继承顺序
- 生成可读性良好的时间线文本
- 包含以下事件类型：
    - 即位
    - 去世
    - 头衔获取（帝国 / 王国 / 公爵领 / 伯爵领）
- 正确处理复杂的头衔历史结构（包括嵌套的 `holder` 结构）
- 对“即位当日才获得头衔”的情况进行智能回退处理
- 面向历史重建设计，而非 UI 复刻

---
## 环境需求
- Python 3.x（推荐 Python 3.8 或更新版本）
- 一个未压缩的 CK2 存档文件（`.ck2`）
- 任意可运行 Python 的操作系统（Windows / macOS / Linux）

**注意：**  
如果你正在使用中文本地化模组，建议避免在路径中使用中文字符，以减少潜在的编码问题。

---
## 项目结构

- CK2-Timeline_Creator.py    # 主程序脚本
- example/
  - timeline_example.txt    # 示例输出文件
- README.md                 # 英文说明文档
- README_zh.md              # 中文说明文档

---
## 使用方法
### 第一步：准备存档文件

- 如果你的 CK2 存档已经是明文的 `.ck2` 文件，可以直接使用。
- 如果存档是压缩格式：
  1. 将 `你的存档.ck2` 重命名为 `你的存档.zip`
  2. 使用解压工具打开该 zip 文件
  3. 提取其中的明文 `.ck2` 存档文件

请将 `.ck2` 文件放置在 `CK2-Timeline_Creator.py` 同一目录下。

---
### 第二步：确认 Python 是否已安装
#### 打开命令行界面

**Windows**
1. 按下 `Win + R`
2. 输入 `cmd`
3. 回车
**macOS**
1. 打开 Spotlight (`Cmd + Space`)
2. 输入 `Terminal`
**Linux**
1. 打开你的终端模拟器

#### 检查 Python 版本
运行：
```bash
python --version
```
如果该命令无效，请尝试：
```bash
python3 --version
```
如果 Python 已正确安装，你将看到类似如下的输出：
```bash
Python 3.10.6
```

如果尚未安装 Python，请前往官网下载：
https://www.python.org/downloads/

--- 
### 第三步：运行脚本
进入包含以下内容的目录：
`CK2-Timeline_Creator.py`
你的 `.ck2` 存档

运行：
```bash
python CK2-Timeline_Creator.py
```
（如有需要，也可使用 `python3 CK2-Timeline_Creator.py`）

--- 
### 程序会提示：
程序会提示：
```bash
Input save name (without .ck2):
```
如果你的存档文件名为：
```bash
my_campaign.ck2
```
请输入：
```bash
my_campaign
```
然后按回车。

--- 
### 第五步：查看输出结果
程序运行结束后，会在同一目录下生成：
```bash
timeline.txt
```
该文件即为重建后的君主时间线。

输出示例（完整示例见 `example/timeline_example.txt`）：
```bash
0753.01.01  Unknown_Name  获得 Bourbon伯爵头衔
0769.01.01  世代0 Unknown_Name  即 Bourbon伯爵位
0792.08.11  Bourbon伯爵 Unknown_Name  去世
```

--- 
## 设计理念
本项目并不尝试复刻 CK2 游戏内的编年史系统。

相反，它专注于从存档文件中提取可验证的历史事件，并将其整理为按时间顺序排列、可读且机器友好的文本格式，非常适合作为 AI 叙事生成或战役故事创作的输入素材。

该输出可用于：
- 战役回顾
- 历史存档或分析
- AI 辅助叙事生成

--- 
## 注意事项
- 本工具为只读工具，不会以任何方式修改存档文件，但仍建议在使用前备份存档。
- 仅支持明文格式的 CK2 存档文件
- **本项目不包含任何 Paradox 游戏文件或模组**
- **本项目与 Paradox Interactive 官方无任何关联**

--- 
## 致谢

本项目在构思与部分实现上参考并受到了以下开源项目的启发：

- **CK2-history-extractor**  
  作者: TCA166, Tomasz Chady
  许可证: Creative Commons Attribution 4.0 International (CC BY 4.0)  
  项目地址: [CK2-history-extractor](https://github.com/TCA166/CK2-history-extractor)

本项目在早期的解析逻辑与整体思路上受到了该项目的影响。
当前实现已经在此基础上进行了大幅扩展与重写，用于支持时间线重建、头衔历史解析以及面向 AI 的叙事素材生成。

--- 
## 许可证
本项目采用 MIT License 授权。

项目中提及或参考的第三方作品，仍各自遵循其原始许可证条款。
