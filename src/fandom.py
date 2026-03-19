#!/usr/bin/env python3
"""
Fandom Wiki 转换工具集

统一的命令行工具，提供所有转换功能。

重要：使用前请先用 --test 模式在单个页面上测试！
"""

import sys
import os
import argparse
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    parser = argparse.ArgumentParser(
        description='Fandom Wiki 转换工具集',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  page      转换单个或多个页面
  category  转换分类下的所有页面
  template  转换使用模板的所有页面
  restore   从历史版本恢复页面

快速开始:
  # 1. 测试单个页面
  %(prog)s page "西片" --dry-run
  %(prog)s page "西片"
  
  # 2. 检查 Wiki 上的结果
  
  # 3. 批量转换
  %(prog)s category "音乐"
  %(prog)s template "Template:角色信息" --batch

更多信息:
  %(prog)s <command> --help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # page 子命令
    page_parser = subparsers.add_parser('page', help='转换单个或多个页面')
    page_parser.add_argument('pages', nargs='+', help='要转换的页面名称')
    page_parser.add_argument('--from-file', metavar='FILE', help='从文件读取页面列表')
    page_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    page_parser.add_argument('--show-diff', action='store_true', help='显示修改详情')
    
    # category 子命令
    cat_parser = subparsers.add_parser('category', help='转换分类下的所有页面')
    cat_parser.add_argument('category', help='分类名称')
    cat_parser.add_argument('--list', action='store_true', help='只列出页面')
    cat_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    cat_parser.add_argument('--limit', type=int, metavar='N', help='限制转换数量')
    cat_parser.add_argument('--no-test-first', action='store_true', help='跳过测试')
    
    # template 子命令
    tpl_parser = subparsers.add_parser('template', help='转换使用模板的所有页面')
    tpl_parser.add_argument('template', help='模板名称')
    tpl_parser.add_argument('--list', action='store_true', help='只列出页面')
    tpl_parser.add_argument('--test', metavar='PAGE', help='测试单个页面')
    tpl_parser.add_argument('--batch', action='store_true', help='批量转换')
    tpl_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    tpl_parser.add_argument('--no-test-first', action='store_true', help='跳过测试')
    tpl_parser.add_argument('--no-doc', action='store_true', help='不转换 /doc')
    
    # restore 子命令
    restore_parser = subparsers.add_parser('restore', help='从历史版本恢复页面')
    restore_parser.add_argument('page', help='要恢复的页面名称')
    restore_parser.add_argument('--show-versions', action='store_true', help='显示历史版本')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 调用相应的脚本
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if args.command == 'page':
        import convert_page
        sys.argv = ['convert_page.py']
        if args.from_file:
            sys.argv.extend(['--from-file', args.from_file])
        else:
            sys.argv.extend(args.pages)
        if args.dry_run:
            sys.argv.append('--dry-run')
        if args.show_diff:
            sys.argv.append('--show-diff')
        convert_page.main()
        
    elif args.command == 'category':
        import convert_category
        sys.argv = ['convert_category.py', args.category]
        if args.list:
            sys.argv.append('--list')
        if args.dry_run:
            sys.argv.append('--dry-run')
        if args.limit:
            sys.argv.extend(['--limit', str(args.limit)])
        if args.no_test_first:
            sys.argv.append('--no-test-first')
        convert_category.main()
        
    elif args.command == 'template':
        import convert_template
        sys.argv = ['convert_template.py', args.template]
        if args.list:
            sys.argv.append('--list')
        elif args.test:
            sys.argv.extend(['--test', args.test])
        elif args.batch:
            sys.argv.append('--batch')
        if args.dry_run:
            sys.argv.append('--dry-run')
        if args.no_test_first:
            sys.argv.append('--no-test-first')
        if args.no_doc:
            sys.argv.append('--no-doc')
        convert_template.main()
        
    elif args.command == 'restore':
        import restore_from_history
        sys.argv = ['restore_from_history.py', args.page]
        if args.show_versions:
            sys.argv.append('--show-versions')
        restore_from_history.main()

if __name__ == "__main__":
    main()
