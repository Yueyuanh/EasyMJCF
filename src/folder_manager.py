#!/usr/bin/env python3

import os
import shutil
import sys
from pathlib import Path
import stat

class FolderManager:
    """文件夹管理器"""
    
    @staticmethod
    def create_folder(path: str, exist_ok: bool = True, parents: bool = True):
        """
        创建文件夹
        
        参数:
            path: 文件夹路径
            exist_ok: 如果文件夹已存在是否忽略错误
            parents: 是否创建父目录
        """
        try:
            os.makedirs(path, exist_ok=exist_ok)
            print(f"创建文件夹: {path}")
            return True
        except Exception as e:
            print(f"创建失败 {path}: {e}")
            return False
    
    @staticmethod
    def rename_folder(src: str, dst: str):
        """
        重命名或移动文件夹
        
        参数:
            src: 源文件夹路径
            dst: 目标文件夹路径
        """
        try:
            os.rename(src, dst)
            print(f"重命名: {src} -> {dst}")
            return True
        except FileNotFoundError:
            print(f"源文件夹不存在: {src}")
            return False
        except FileExistsError:
            print(f"目标文件夹已存在: {dst}")
            return False
        except Exception as e:
            print(f"重命名失败: {e}")
            return False
    
    @staticmethod
    def move_folder(src: str, dst: str):
        """
        移动文件夹到新位置（同分区用rename，不同分区用shutil）
        """
        try:
            shutil.move(src, dst)
            print(f"移动: {src} -> {dst}")
            return True
        except Exception as e:
            print(f"移动失败: {e}")
            return False
    
    @staticmethod
    def copy_folder(src: str, dst: str):
        """
        复制文件夹
        """
        try:
            shutil.copytree(src, dst)
            print(f"复制: {src} -> {dst}")
            return True
        except Exception as e:
            print(f"复制失败: {e}")
            return False
    
    @staticmethod
    def delete_folder(path: str):
        """
        删除文件夹
        """
        try:
            shutil.rmtree(path)
            print(f"删除: {path}")
            return True
        except Exception as e:
            print(f"删除失败: {e}")
            return False
    
    @staticmethod
    def folder_exists(path: str) -> bool:
        """检查文件夹是否存在"""
        return os.path.exists(path) and os.path.isdir(path)
    
    @staticmethod
    def create_nested_folders(base_path: str, folder_structure: list):
        """
        创建嵌套文件夹结构
        
        参数:
            base_path: 基础路径
            folder_structure: 文件夹结构列表，如 ['project', 'src', 'utils']
        """
        current_path = base_path
        for folder in folder_structure:
            current_path = os.path.join(current_path, folder)
            FolderManager.create_folder(current_path)
    
    @staticmethod
    def create_with_permissions(path: str, mode: int = 0o755):
        """
        创建文件夹并设置权限
        
        参数:
            path: 文件夹路径
            mode: 权限模式（八进制）
        """
        try:
            os.makedirs(path, mode=mode, exist_ok=True)
            print(f"创建文件夹 {path} (权限: {oct(mode)})")
            return True
        except Exception as e:
            print(f"创建失败: {e}")
            return False

# 使用 pathlib 的现代方法
class FolderManagerModern:
    """使用 pathlib 的文件夹管理器"""
    
    @staticmethod
    def create_folder(path: str):
        """使用 pathlib 创建文件夹"""
        try:
            folder = Path(path)
            folder.mkdir(parents=True, exist_ok=True)
            print(f"创建: {path}")
            return True
        except Exception as e:
            print(f"创建失败: {e}")
            return False
    
    @staticmethod
    def rename_folder(src: str, dst: str):
        """使用 pathlib 重命名"""
        try:
            src_path = Path(src)
            dst_path = Path(dst)
            src_path.rename(dst_path)
            print(f"重命名: {src} -> {dst}")
            return True
        except Exception as e:
            print(f"重命名失败: {e}")
            return False


