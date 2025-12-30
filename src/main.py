import os
import sys
import shutil
import subprocess
from pathlib import Path
from insert import Insert_text
from simplify_stl import MeshSimplify
from folder_manager import FolderManager


mujoco_compiler="""

<!-- mujoco compiler insert -->

<mujoco>
    <compiler 
    meshdir="../meshes/" 
    balanceinertia="true" 
    discardvisual="false"
    fusestatic="false"/> 
</mujoco>

    """

scene_include="""

    <include file="scene.xml"/>

"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python main.py <URDF文件地址>")
        sys.exit(1)

    urdf_path = Path(sys.argv[1]).resolve()
    
    if not urdf_path.exists():
        print(f"错误: 文件不存在 - {urdf_path}")
        sys.exit(1)


    # 创建URDF替换
    ins_urdf = Insert_text(str(urdf_path))

    if ins_urdf.find_first_line_number('<mujoco>') == -1:
        link_line = ins_urdf.find_first_link_line_number()
        if link_line > 0:
            ins_urdf.insert_at_line(link_line, mujoco_compiler)

    if ins_urdf.find_first_line_number('package') > 0:
        ins_urdf.replace_in_file(f"package://{ins_urdf.urdf_name}", "..")


    # 计算相关路径
    urdf_parent = urdf_path.parent
    meshes_path = urdf_parent.parent / "meshes"
    mjcf_path = urdf_parent.parent / "mjcf"
    output_xml = urdf_path.with_suffix('.xml')

    # 编译
    compile_script = Path("./scripts/compile/compile")
    if not compile_script.exists():
        print(f"错误: 编译脚本不存在 - {compile_script}")
        sys.exit(1)

    try:
        result = subprocess.run(
            [str(compile_script), str(urdf_path), str(output_xml)],
            capture_output=True,
            text=True,
            check=False
        )
        debug = result.stdout + result.stderr
    except Exception as e:
        print(f"执行编译脚本时出错: {e}")
        sys.exit(1)

    if "between 1 and 200000" in debug:
        print("Error:面数应该在1~200000之间,开始自动压缩...\n")
        
        backup_path = meshes_path.with_name(meshes_path.name + ".backup")
        if meshes_path.exists():
            FolderManager.rename_folder(str(meshes_path), str(backup_path))
        
        FolderManager.create_folder(str(meshes_path))

        ratio = 0.9
        max_attempts = 10  
        
        for attempt in range(max_attempts):
            # 压缩
            MS = MeshSimplify()
            MS.batch_simplify(str(backup_path), str(meshes_path), ratio)

            try:
                result = subprocess.run(
                    [str(compile_script), str(urdf_path), str(output_xml)],
                    capture_output=True,
                    text=True,
                    check=False
                )
                debug = result.stdout + result.stderr
            except Exception as e:
                print(f"执行编译脚本时出错: {e}")
                break

            if not debug or "between 1 and 200000" not in debug:
                print("已完成处理！")
                print(f"压缩率为：{ratio}")
                break

            if ratio > 0.1:
                ratio = ratio - 0.1
            else:
                print("Error:超出最大压缩范围")
                break
        else:
            print("Error: 达到最大压缩尝试次数")

    print(debug)
    

    # 只有在成功编译后才插入场景
    if output_xml.exists() and "Output file already exists" not in debug:
        ins_xml = Insert_text(str(output_xml))
        ins_xml.insert_at_line(4, scene_include)

    FolderManager.create_folder(str(mjcf_path))
    
    if output_xml.exists():
        shutil.copy2(str(output_xml), str(mjcf_path))
    
    scene_source = Path("resource/scene.xml")
    if scene_source.exists():
        shutil.copy2(str(scene_source), str(mjcf_path))
    else:
        print(f"警告: 场景文件不存在 - {scene_source}")

    print("转换完成！")
    