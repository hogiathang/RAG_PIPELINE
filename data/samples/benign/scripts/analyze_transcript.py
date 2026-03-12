#!/usr/bin/env python3
"""
分析转录文本，识别口误、静音、语气词
"""
import json

# 读取转录文件
with open('/Users/fengge/coding/videocut-skills/DEMO/一些生日感受_v1_transcript.json', 'r') as f:
    data = json.load(f)

chars = data['chars']

# 语气词列表
filler_words = ['嗯', '啊', '哎', '诶', '呃', '额', '唉', '哦', '噢', '呀', '欸', '呢']

print("=== 1. 扫描语气词 ===\n")
detected_fillers = []
for i, item in enumerate(chars):
    if item['char'] in filler_words:
        prev_char = chars[i-1] if i > 0 else None
        next_char = chars[i+1] if i < len(chars)-1 else None

        prev_text = prev_char['char'] if prev_char else '(开始)'
        next_text = next_char['char'] if next_char else '(结束)'

        gap_before = item['start'] - (prev_char['end'] if prev_char else 0)
        gap_after = (next_char['start'] if next_char else item['end']) - item['end']

        delete_start = prev_char['end'] if prev_char else 0
        delete_end = next_char['start'] if next_char else item['end']

        print(f"[{item['start']:.2f}s] \"{item['char']}\"")
        print(f"  上下文: {prev_text}【{item['char']}】{next_text}")
        print(f"  删除范围: ({delete_start:.2f}-{delete_end:.2f})")
        print(f"  前静音: {gap_before:.2f}s, 后静音: {gap_after:.2f}s")
        print()

        detected_fillers.append({
            'char': item['char'],
            'start': item['start'],
            'end': item['end'],
            'delete_start': delete_start,
            'delete_end': delete_end,
            'prev_text': prev_text,
            'next_text': next_text,
            'context': f"{prev_text}【{item['char']}】{next_text}"
        })

print("\n=== 2. 检测静音 (≥1s) ===\n")
silences = []

# 开头静音
if chars[0]['start'] > 1.0:
    silence_duration = chars[0]['start']
    print(f"开头静音: (0.00-{chars[0]['start']:.2f}) {silence_duration:.2f}s")
    silences.append({
        'start': 0.0,
        'end': chars[0]['start'],
        'duration': silence_duration,
        'type': '开头'
    })

# 句间静音
for i in range(len(chars) - 1):
    gap = chars[i+1]['start'] - chars[i]['end']
    if gap >= 1.0:
        print(f"静音 @ {chars[i]['end']:.2f}s: ({chars[i]['end']:.2f}-{chars[i+1]['start']:.2f}) {gap:.2f}s")
        print(f"  上下文: {chars[i]['char']}【静音{gap:.1f}s】{chars[i+1]['char']}")
        print()
        silences.append({
            'start': chars[i]['end'],
            'end': chars[i+1]['start'],
            'duration': gap,
            'type': '句间',
            'context': f"{chars[i]['char']}【静音{gap:.1f}s】{chars[i+1]['char']}"
        })

print("\n=== 3. 逐句检查口误 ===\n")
full_text = data['full_text']

print("完整文本：")
print(full_text)
print("\n正在逐句分析...\n")

# 逐句分析（简单按句号分割）
sentences = full_text.replace('，', '。').replace('？', '。').replace('！', '。').split('。')

for i, sent in enumerate(sentences):
    if sent.strip():
        print(f"[{i+1}] {sent.strip()}")
        # 检查重复
        # 检查残句
        # 检查不通顺

print("\n=== 总结 ===")
print(f"语气词: {len(detected_fillers)} 个")
print(f"静音: {len(silences)} 处")
