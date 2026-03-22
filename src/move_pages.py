#!/usr/bin/env python3
"""
批量移动页面（将繁体名称改为简体）

移动前会先更新所有引用该页面的链接，避免断链。
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fandom_bot import FandomBot
from batch_processor import create_batch_parser, parse_page_args, BatchProcessor


def update_links_before_move(old_name: str, new_name: str, bot: FandomBot, dry_run: bool = False) -> tuple:
    """移动前更新所有引用该页面的链接"""
    print(f"  检查引用 {old_name} 的页面...")
    
    # 查找所有引用该页面的页面
    page = bot.get_page(old_name)
    if not page.exists:
        return 0, 0
    
    # 获取所有引用的页面
    try:
        referrers = list(page.backlinks(limit=500))
    except Exception as e:
        print(f"  ⚠️  获取引用失败: {e}")
        return 0, 0
    
    if not referrers:
        print(f"  ℹ️  没有引用页面")
        return 0, 0
    
    print(f"  找到 {len(referrers)} 个引用页面")
    
    updated = 0
    skipped = 0
    
    for ref_page in referrers:
        ref_name = ref_page.name
        
        # 跳过自我引用
        if ref_name == old_name:
            continue
        
        # 跳过重定向页面
        if ref_page.is_redirect:
            continue
        
        try:
            content = ref_page.text()
            new_content = content
            
            # 更新各种格式的链接
            # [[页面名]]
            new_content = new_content.replace(f'[[{old_name}]]', f'[[{new_name}]]')
            new_content = new_content.replace(f'[[{old_name}|', f'[[{new_name}|')
            # [[页面名]] 的变体（带空格等）
            new_content = new_content.replace(f'[[ {old_name}]]', f'[[{new_name}]]')
            new_content = new_content.replace(f'[[ {old_name}|', f'[[{new_name}|')
            # [[链接|显示文字]] 格式
            new_content = new_content.replace(f'|{old_name}]]', f'|{new_name}]]')
            
            if content != new_content:
                if dry_run:
                    print(f"    📝 {ref_name} 将会更新链接")
                    updated += 1
                else:
                    bot.edit_page(ref_page, new_content, summary=f"更新链接：{old_name} → {new_name}")
                    print(f"    ✓ {ref_name} 链接已更新")
                    updated += 1
                    time.sleep(0.5)
            else:
                skipped += 1
                
        except Exception as e:
            print(f"    ⚠️  {ref_name} 更新失败: {e}")
    
    return updated, skipped


def move_page(page_name: str, bot: FandomBot, dry_run: bool = False):
    """移动单个页面"""
    new_name = bot.cc.convert(page_name)
    
    if page_name == new_name:
        return None, f"ℹ️  无需移动（名称已经是简体）"
    
    print(f"  目标名称: {new_name}")
    
    if dry_run:
        # 预览模式下只显示将要更新链接
        updated, skipped = update_links_before_move(page_name, new_name, bot, dry_run=True)
        if updated > 0:
            print(f"  📝 将更新 {updated} 个页面的链接")
        if skipped > 0:
            print(f"  ℹ️  {skipped} 个页面无需更新链接")
        return True, f"📝 将会移动（预览模式）"
    
    # 第一步：更新引用该页面的链接
    updated, skipped = update_links_before_move(page_name, new_name, bot, dry_run=False)
    if updated > 0:
        print(f"  ✓ 已更新 {updated} 个页面的链接")
    if skipped > 0:
        print(f"  ℹ️  {skipped} 个页面无需更新链接")
    
    # 第二步：移动页面
    page = bot.get_page(page_name)
    if page.exists:
        bot.move_page(page, new_name, reason="改名为简体中文")
        return True, "✓ 已移动"
    else:
        return False, "⚠️  页面不存在（可能已移动）"


def main():
    parser = create_batch_parser(
        '批量移动页面（将繁体名称改为简体）',
        """
示例:
  %(prog)s "雖然不會說出口。" "愛歌" "小小戀歌"
  %(prog)s --from-file pages.txt
  %(prog)s "雖然不會說出口。" --dry-run
        """
    )
    
    args, page_names, should_exit = parse_page_args(parser)
    if should_exit or page_names is None:
        sys.exit(1)
    
    try:
        bot = FandomBot()
        print(f"✓ 已登录: {bot.site.username}\n")
    except Exception as e:
        print(f"❌ 登录失败: {e}")
        sys.exit(1)
    
    # 创建处理器并批量处理
    processor = lambda name, bot: move_page(name, bot, args.dry_run)
    batch = BatchProcessor(bot, dry_run=args.dry_run, delay=0.5)
    
    success = batch.process_pages(page_names, processor, "批量移动页面")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
