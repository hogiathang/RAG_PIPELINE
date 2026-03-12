#!/usr/bin/env python
"""
FunASR 本地转录脚本

用法:
    python transcribe_local.py <视频/音频文件> [--output=<输出路径>] [--segment-length=30]

输出:
    JSON 格式的转录结果，包含字符级时间戳

依赖:
    pip install funasr modelscope
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def get_video_duration(video_path: str) -> float:
    """获取视频时长（秒）"""
    result = subprocess.run(
        [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def extract_audio_segment(video_path: str, output_path: str, start: float, duration: float):
    """提取音频片段"""
    subprocess.run(
        [
            'ffmpeg', '-y', '-i', video_path,
            '-ss', str(start),
            '-t', str(duration),
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            output_path
        ],
        capture_output=True
    )


def transcribe_segment(model, wav_path: str, offset: float = 0) -> list:
    """转录单个音频片段"""
    result = model.generate(
        input=wav_path,
        return_raw_text=True,
        timestamp_granularity="character"
    )
    
    chars = []
    punctuation = '，。？！、：；""''（）《》【】,.!?;:\'"()'
    
    for item in result:
        if 'timestamp' in item and 'text' in item:
            text = item['text'].replace(' ', '')
            timestamps = item['timestamp']
            idx = 0
            
            for char in text:
                if char in punctuation:
                    continue
                if idx < len(timestamps):
                    ts = timestamps[idx]
                    chars.append({
                        'char': char,
                        'start': round(offset + ts[0] / 1000, 2),
                        'end': round(offset + ts[1] / 1000, 2)
                    })
                    idx += 1
    
    return chars


def transcribe_video(video_path: str, segment_length: int = 30) -> dict:
    """
    分段转录视频
    
    Args:
        video_path: 视频文件路径
        segment_length: 分段长度（秒），默认 30
    
    Returns:
        转录结果字典
    """
    # 延迟导入，只在实际使用时加载模型
    from funasr import AutoModel
    
    print(f"🎤 开始转录: {video_path}", file=sys.stderr)
    print(f"   模式: 本地 (Python FunASR)", file=sys.stderr)
    
    # 加载模型
    print("   加载模型...", file=sys.stderr)
    model = AutoModel(model="paraformer-zh", disable_update=True)
    
    # 获取视频时长
    duration = get_video_duration(video_path)
    num_segments = int(duration // segment_length) + 1
    
    all_chars = []
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_segments):
            start = i * segment_length
            dur = min(segment_length, duration - start)
            wav_path = os.path.join(tmpdir, f'seg_{i}.wav')
            
            print(f"   转录分段 {i + 1}/{num_segments} ({start}s - {start + dur}s)...", file=sys.stderr)
            
            # 提取音频
            extract_audio_segment(video_path, wav_path, start, dur)
            
            # 转录
            segment_chars = transcribe_segment(model, wav_path, start)
            all_chars.extend(segment_chars)
    
    # 构造结果
    full_text = ''.join(c['char'] for c in all_chars)
    result_duration = all_chars[-1]['end'] if all_chars else 0
    
    print(f"✅ 转录完成: {len(all_chars)} 个字符, {result_duration:.1f}s", file=sys.stderr)
    
    return {
        'input_file': video_path,
        'mode': 'local',
        'full_text': full_text,
        'duration_s': result_duration,
        'chars': all_chars,
        'segments': all_chars  # 兼容旧格式
    }


def main():
    parser = argparse.ArgumentParser(description='FunASR 本地转录脚本')
    parser.add_argument('input', help='视频或音频文件路径')
    parser.add_argument('--output', '-o', help='输出 JSON 文件路径')
    parser.add_argument('--segment-length', type=int, default=30, help='分段长度（秒），默认 30')
    parser.add_argument('--json', action='store_true', help='仅输出 JSON 到 stdout')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"❌ 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = transcribe_video(args.input, args.segment_length)
        
        if args.json:
            # 仅输出 JSON 到 stdout（供 Node.js 调用）
            print(json.dumps(result, ensure_ascii=False))
        elif args.output:
            # 保存到文件
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"📄 转录结果已保存: {args.output}", file=sys.stderr)
        else:
            # 默认输出到同目录
            output_path = Path(args.input).stem + '_transcript.json'
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"📄 转录结果已保存: {output_path}", file=sys.stderr)
            
            # 显示预览
            print(f"\n📝 文本预览 (前100字):\n{result['full_text'][:100]}...", file=sys.stderr)
        
    except Exception as e:
        print(f"❌ 转录失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
