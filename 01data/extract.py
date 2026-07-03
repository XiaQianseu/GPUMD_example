#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能：读取 XDATCAR 文件，提取每个离子步的构型，分别放入 run/0001, run/0002, ... 文件夹中
每个文件夹内生成 POSCAR 文件，包含：
- 前7行（头信息）
- 第8行：Direct
- 后续行：对应构型的坐标（Direct格式）
"""

import os
import re

def read_xdatcar(filename="XDATCAR"):
    """读取 XDATCAR 文件，返回头信息和各构型坐标"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # 提取前7行头信息
    header = lines[:7]
    
    # 查找所有 "Direct configuration=" 所在行索引
    config_indices = []
    for idx, line in enumerate(lines):
        if line.startswith("Direct configuration="):
            config_indices.append(idx)
    
    if not config_indices:
        raise ValueError("XDATCAR 中未找到 'Direct configuration=' 行")
    
    # 提取每个构型的坐标（不包含 "Direct configuration=" 行本身）
    configs = []
    for i, start_idx in enumerate(config_indices):
        start_line = start_idx + 1  # 从该行的下一行开始
        if i + 1 < len(config_indices):
            end_line = config_indices[i + 1]  # 下一个 "Direct configuration=" 行
        else:
            end_line = len(lines)  # 最后一个构型到文件末尾
        
        # 提取坐标并去除换行符，但保留每行内容
        config_lines = [lines[j].rstrip('\n') for j in range(start_line, end_line)]
        # 过滤掉可能的空行（如果存在）
        config_lines = [line for line in config_lines if line.strip()]
        configs.append(config_lines)
    
    return header, configs

def create_folders_and_poscars(header, configs, base_name="POSCAR", folder_prefix="%04d", parent_dir="run"):
    """创建父目录 parent_dir，并在其中创建子文件夹，生成 POSCAR 文件"""
    num_configs = len(configs)
    print(f"找到 {num_configs} 个离子步构型")
    
    # 确保父目录存在
    os.makedirs(parent_dir, exist_ok=True)
    
    for i, coords in enumerate(configs, start=1):
        # 子文件夹名称，如 0001, 0002, ...
        sub_folder = folder_prefix % i
        folder_path = os.path.join(parent_dir, sub_folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # POSCAR 文件路径
        poscar_path = os.path.join(folder_path, base_name)
        
        # 写入 POSCAR
        with open(poscar_path, 'w') as f:
            # 写入前7行头信息
            for line in header:
                f.write(line.rstrip('\n') + '\n')
            # 写入 Direct
            f.write("Direct\n")
            # 写入坐标
            for line in coords:
                f.write(line + '\n')
        
        print(f"已生成: {poscar_path}")

def main():
    # 检查 XDATCAR 文件是否存在
    if not os.path.exists("XDATCAR"):
        print("错误：当前目录下未找到 XDATCAR 文件！")
        return
    
    try:
        # 读取 XDATCAR
        header, configs = read_xdatcar("XDATCAR")
        
        # 创建文件夹和 POSCAR 文件（所有子文件夹放在 run 目录下）
        create_folders_and_poscars(header, configs, parent_dir="run1")
        
        print("所有文件夹和 POSCAR 文件创建完成！")
        
    except Exception as e:
        print(f"处理过程中出错：{e}")

if __name__ == "__main__":
    main()