import json
import random
import os
import astrbot.api.message_components as Comp
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star

class KaomojiPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 读取同目录下的 kaomoji.json
        json_path = os.path.join(os.path.dirname(__file__), "kaomoji.json")
        with open(json_path, "r", encoding="utf-8") as f:
            self.kaomoji_data = json.load(f)

    # 通过装饰器注册 LLM 工具
    @filter.llm_tool(name="get_kaomoji")
    async def get_kaomoji(self, event: AstrMessageEvent, category: str, subcategory: str) -> str:
        """
        从颜文字库中随机返回一个指定类别的颜文字，用于在对话中表达特定情绪或动作。
        
        Args:
            category(string): 主分类名，只能从以下列表中选择：
                "正面情绪", "负面情绪", "中性情绪", "各种动作", "各种动物", "其他类型"
            subcategory(string): 子分类名，每个主分类对应子分类如下：
                - 正面情绪: "喜悦", "喜爱", "害羞", "同情"
                - 负面情绪: "不悦", "愤怒", "悲伤", "疼痛", "恐惧"
                - 中性情绪: "冷漠", "困惑", "怀疑", "惊喜"
                - 各种动作: "打招呼", "拥抱", "眨眼", "道歉", "流鼻血", "藏起来", "写字", "奔跑", "睡觉"
                - 各种动物: "猫", "熊", "狗", "兔子", "猪", "鸟", "鱼", "蜘蛛"
                - 其他类型: "朋友", "敌人", "武器", "魔法", "食物", "音乐", "游戏"
        """
        try:
            sub_dict = self.kaomoji_data[category]
            if subcategory in sub_dict:
                kaomoji = random.choice(sub_dict[subcategory])
                return f"\u200b{kaomoji}\u200b"
            else:
                return f"（子类别 '{subcategory}' 不存在）"
        except KeyError:
            return f"（主类别 '{category}' 不存在）"
