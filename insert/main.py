import os
import sys
import shutil
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

# urdf_path="../resource/RMUC2025/urdf/RMUC2025.urdf"
# urdf_path="/mnt/data/Projects/EasyMjcf/resource/Wheelleg_2024/urdf/Wheelleg_2024.urdf"

# 使用示例
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("用法: python main.py <URDF文件地址>")
        sys.exit(1)

    urdf_path = sys.argv[1]


    print("请确保传入为SW导出的原始URDF文件!")


    # 创建URDF替换
    ins_urdf=Insert_text(urdf_path)
    # 插入内容 找到第一个<link 标签
    ins_urdf.insert_at_line(ins.find_first_link_line_number(), mujoco_compiler)
    # 替换内容
    ins_urdf.replace_in_file("package://"+ins_urdf.urdf_name, "..")


    # 编译
    debug=os.popen("./scripts/compile/compile " + urdf_path + " " + urdf_path + ".xml").read()
    print(debug)

    meshes_path = urdf_path.rsplit("/", 1)[0] + "/"+"../meshes"
    mjcf_path =urdf_path.rsplit("/", 1)[0] + "/"+"../mjcf"

    if "between 1 and 200000" in debug:

        # (input)  meshes -> meshes.backup 
        # create new meshes folder 
        # (output) meshes 
        print("Error:面数应该在1~200000之间,开始自动压缩...\n")

        FolderManager.rename_folder(meshes_path,meshes_path+".buckup")
        FolderManager.create_folder(meshes_path)

    ratio=0.9
    while "between 1 and 200000" in debug:

        # 压缩
        MS=MeshSimplify()
        MS.batch_simplify(meshes_path+".buckup",meshes_path,ratio)

        debug=os.popen("./scripts/compile/compile " + urdf_path + " " + urdf_path + ".xml").read()

        if debug=="":
            print("以完成处理！")
            print(f"压缩率为：{ratio}")
            break

        if ratio>0.1:
            ratio=ratio-0.1
        else:
            print("Error:超出最大压缩范围")

    print(debug)
    
    # XML替换
    ins_xml=Insert_text(urdf_path + ".xml")
    ins_xml.insert_at_line(4,scene_include)

    FolderManager.create_folder(mjcf_path)
    
    shutil.copy2(urdf_path + ".xml", mjcf_path)
    shutil.copy2("resource/scene.xml", mjcf_path)

    print("转换完成！")

 
    