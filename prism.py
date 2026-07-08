import numpy as np
import open3d as o3d

point_path = r"/datameta/project/ls_test_gaumvp/dataset/yaoyichen/Colmap/right_from_left_pose_py/sparse/all_raw_points.pcd"


def prism_downsample_ratio(pcd, r_target=0.1, n_bins=16):
    """
    PRISM 下采样彩色点云（自适应 k*，基于目标压缩比 r_target）
    
    参数:
        pcd: open3d.geometry.PointCloud, 点云对象
        r_target: float, 目标压缩比例，例如 0.1 表示压缩到 10%
        n_bins: int, 每个颜色通道划分的桶数
        
    返回:
        downsampled_pcd: open3d.geometry.PointCloud, 下采样后的点云
    """
    # 提取点坐标和颜色信息
    points = np.asarray(pcd.points)
    N = points.shape[0]
    
    # 检查是否有颜色信息
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)
        # 将颜色从 [0,1] 转换为 [0,255]
        rgb = (colors * 255).astype(np.uint8)
    else:
        # 如果没有颜色，使用灰度值
        rgb = np.tile([128], (N, 3)).astype(np.uint8)
    
    # 量化颜色
    bin_idx = np.floor(rgb / 256 * n_bins).astype(int)
    bin_idx = np.clip(bin_idx, 0, n_bins-1)
    color_bins = bin_idx[:,0]*n_bins*n_bins + bin_idx[:,1]*n_bins + bin_idx[:,2]
    
    # 统计每个桶点数
    unique_bins, counts = np.unique(color_bins, return_counts=True)
    
    # 计算 k*（自适应）
    # sorted_counts = np.sort(counts)[::-1]  # 从大到小
    total_target = int(N * r_target)
    
    # 贪心方式计算 k*: 找到 k* 使总采样点数 ≈ total_target
    k_star = total_target / len(unique_bins)  # 初步估计平均每桶点数
    k_star = int(np.ceil(k_star))  # 向上取整保证压缩比至少 r_target
    
    # 分桶采样
    sampled_points = []
    sampled_colors = []
    for b in unique_bins:
        mask = color_bins == b
        points_in_bin = points[mask]
        colors_in_bin = colors[mask] if pcd.has_colors() else None
        
        if len(points_in_bin) > k_star:
            indices = np.random.choice(len(points_in_bin), k_star, replace=False)
            sampled_points.append(points_in_bin[indices])
            if colors_in_bin is not None:
                sampled_colors.append(colors_in_bin[indices])
        else:
            sampled_points.append(points_in_bin)
            if colors_in_bin is not None:
                sampled_colors.append(colors_in_bin)
    
    # 合并并创建 PointCloud 对象
    downsampled_points = np.vstack(sampled_points)
    downsampled_pcd = o3d.geometry.PointCloud()
    downsampled_pcd.points = o3d.utility.Vector3dVector(downsampled_points)
    
    if sampled_colors:
        downsampled_colors = np.vstack(sampled_colors)
        downsampled_pcd.colors = o3d.utility.Vector3dVector(downsampled_colors)
    
    return downsampled_pcd


def save_to_3dgs_ply(pcd, output_path):
    """
    保存点云为3DGS（3D高斯泼溅）兼容的PLY格式
    
    参数:
        pcd: open3d.geometry.PointCloud, 点云对象
        output_path: str, 输出PLY文件路径
    """
    import struct
    
    points = np.asarray(pcd.points)
    
    # 获取颜色信息，转换为 [0, 255]
    if pcd.has_colors():
        colors = np.asarray(pcd.colors)
        colors = (colors * 255).astype(np.uint8)
    else:
        # 如果没有颜色，使用白色
        colors = np.ones((points.shape[0], 3), dtype=np.uint8) * 255
    
    # 计算法向量（如果有的话）
    if pcd.has_normals():
        normals = np.asarray(pcd.normals)
    else:
        # 如果没有法向量，估计法向量
        pcd.estimate_normals()
        normals = np.asarray(pcd.normals)
    
    # 准备PLY数据
    num_points = points.shape[0]
    
    # 创建包含所有属性的结构化数组
    ply_data = np.empty(num_points, dtype=[
        ('x', 'f4'),
        ('y', 'f4'),
        ('z', 'f4'),
        ('nx', 'f4'),
        ('ny', 'f4'),
        ('nz', 'f4'),
        ('red', 'u1'),
        ('green', 'u1'),
        ('blue', 'u1'),
    ])
    
    ply_data['x'] = points[:, 0]
    ply_data['y'] = points[:, 1]
    ply_data['z'] = points[:, 2]
    ply_data['nx'] = normals[:, 0]
    ply_data['ny'] = normals[:, 1]
    ply_data['nz'] = normals[:, 2]
    ply_data['red'] = colors[:, 0]
    ply_data['green'] = colors[:, 1]
    ply_data['blue'] = colors[:, 2]
    
    # 使用Open3D写入PLY文件
    o3d.io.write_point_cloud(output_path, pcd)
    
    print(f"点云已保存为3DGS兼容的PLY格式: {output_path}")
    print(f"包含 {num_points} 个点")
    print(f"属性: 位置 (x,y,z) | 法向量 (nx,ny,nz) | 颜色 (RGB)")


# 主程序：读取和处理点云
if __name__ == "__main__":
    # 读取 PCD 文件
    pcd = o3d.io.read_point_cloud(point_path)
    print(f"原始点云大小: {len(pcd.points)} 个点")
    
    # 执行 PRISM 下采样
    downsampled_pcd = prism_downsample_ratio(pcd, r_target=0.3, n_bins=16)
    print(f"下采样后大小: {len(downsampled_pcd.points)} 个点")
    
    # 保存为3DGS兼容的PLY格式
    ply_output_path = point_path.replace(".pcd", "_downsampled.ply")
    save_to_3dgs_ply(downsampled_pcd, ply_output_path)
    
    # 可选：可视化
    # o3d.visualization.draw_geometries([downsampled_pcd])
