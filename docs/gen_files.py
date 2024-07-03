import sys
import os
import mkdocs_gen_files
import pkgutil
import importlib

# 将 src 目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

def iter_namespace(ns_pkg):
    # 遍历并收集所有子模块和子包
    return pkgutil.walk_packages(ns_pkg.__path__, ns_pkg.__name__ + ".")

# 替换为你的顶级包名称
top_level_package = "flowx"

# 动态导入顶级包
package = importlib.import_module(top_level_package)

# 收集所有模块
modules = [name for _, name, _ in iter_namespace(package)]

# 生成 API 文档文件
for module in modules:
    # 创建文件路径
    file_path = f"api/{module.replace('.', '/')}.md"
    
    # 写入文档内容
    with mkdocs_gen_files.open(file_path, 'w') as f:
        f.write(f"::: {module}")

    # 添加文件到生成文件列表
    mkdocs_gen_files.set_edit_path(file_path, f"../src/{module.replace('.', '/')}.py")

# 生成 mkdocs.yml 的 nav 配置部分
nav_entries = ["  - Home: index.md", "  - API:"]
for module in modules:
    nav_entries.append(f"    - {module}: api/{module.replace('.', '/')}.md")

# 读取现有的 mkdocs.yml 文件
mkdocs_yml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../mkdocs.yml"))
with open(mkdocs_yml_path, "r") as f:
    lines = f.readlines()

# 找到 nav 部分并替换
nav_start = next(i for i, line in enumerate(lines) if line.strip() == "nav:")
nav_end = next((i for i, line in enumerate(lines[nav_start+1:], start=nav_start+1) if not line.startswith("  - ")), len(lines))

# 替换 nav 部分
new_lines = lines[:nav_start+1] + [entry + "\n" for entry in nav_entries] + lines[nav_end:]

# 写回 mkdocs.yml 文件
with open(mkdocs_yml_path, "w") as f:
    f.writelines(new_lines)