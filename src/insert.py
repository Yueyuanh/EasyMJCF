#!/usr/bin/env python3

import os
import re
from typing import List

class Insert_text:
    def __init__(self,file_path: str,backup: bool = True):
        """
        初始化文件修改器
        
        Args:
            file_path: 文件路径
            backup: 是否创建备份文件
        """

        self.file_path = file_path
        self.backup = backup
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
    

        match = re.search(r'/([^/]+)\.\w+', self.file_path)
        if match:
            urdf_name = match.group(1)
            print("读取到URDF:")
            print(urdf_name)

        self.urdf_name=urdf_name


    def insert_at_line(self, line_number: int, content: str, 
                                                    ) -> bool:
        """
        在指定行插入内容
        
        Args:
            file_path: 文件路径
            line_number: 行号 (1-based)
            content: 要插入的内容
            backup: 是否创建备份
        
        Returns:
            是否成功
        """
        try:
            # 创建备份
            if self.backup and os.path.exists(self.file_path):
                import shutil
                backup_path = f"{self.file_path}.backup"
                shutil.copy2(self.file_path, backup_path)
                self.backup=False

            # 读取文件
            with open(self.file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 验证行号
            if line_number < 1:
                line_number = 1
            elif line_number > len(lines) + 1:
                line_number = len(lines) + 1
            
            # 获取缩进
            indent = ''
            if lines and line_number <= len(lines):
                current_line = lines[line_number - 1]
                indent_len = len(current_line) - len(current_line.lstrip())
                if indent_len < len(current_line):
                    indent = current_line[:indent_len]
            
            # 准备插入内容
            content_lines = content.rstrip('\n').split('\n')
            insert_lines = [f"{indent}{line}\n" for line in content_lines]
            
            # 插入内容
            lines[line_number-1:line_number-1] = insert_lines
            
            # 写入文件
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"成功在第 {line_number} 行插入内容:")
            print(content)
            return True
            
        except Exception as e:
            print(f"插入失败: {e}")
            return False


    def replace_in_file(self, search_str: str, replace_str: str,
                    case_sensitive: bool = True ) -> int:
        """
        全文搜索替换
        
        Args:
            file_path: 文件路径
            search_str: 搜索字符串
            replace_str: 替换字符串
            case_sensitive: 是否区分大小写
            backup: 是否创建备份
        
        Returns:
            替换次数
        """
        try:
            # 创建备份
            if self.backup and os.path.exists(self.file_path):
                import shutil
                backup_path = f"{self.file_path}.backup"
                shutil.copy2(self.file_path, backup_path)
                self.backup=False

            # 读取文件
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 执行替换
            if case_sensitive:
                new_content = content.replace(search_str, replace_str)
                count = content.count(search_str)
            else:
                import re
                pattern = re.compile(re.escape(search_str), re.IGNORECASE)
                new_content = pattern.sub(replace_str, content)
                count = len(pattern.findall(content))
            
            # 如果没有变化，直接返回
            if new_content == content:
                print(f"未找到匹配项: '{search_str}'")
                return 0
            
            # 写入文件
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"成功替换“ {search_str} ”-> “ {replace_str} ”")
            print(f"成功替换 {count} 处")
            return count
            
        except Exception as e:
            print(f"替换失败: {e}")
            return 0

    def find_first_link_line_number(self):
        """
        查找URDF文件中第一个<link>标签的行号
            
        返回:
            行号 (从1开始)，如果没找到返回-1
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    # 查找 <link 开头的行（考虑可能有空格）
                    if '<link' in line and line.strip().startswith('<link'):
                        return line_num
            return -1
        except Exception as e:
            print(f"读取文件失败: {e}")
            return -1

    def find_first_line_number(self,name:str):
        """            
        返回:
            行号 (从1开始)，如果没找到返回-1
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if name in line and line.strip().startswith(name):
                        return line_num
            return -1
        except Exception as e:
            print(f"读取文件失败: {e}")
            return -1

