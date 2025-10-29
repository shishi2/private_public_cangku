import cv2
import torch
import glob
from test_utils.eval_utils_instant_avatar_brightness import Evaluator as EvalAvatarBrightness


def load_images(evaluator, path):
    # 定义目标大小（高和宽）
    target_height = 1224
    target_width = 1024

    # 加载渲染图片
    render_imgs = [cv2.imread(fn) for fn in glob.glob(f"{path}/*.png")]
    render_imgs = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in render_imgs]
    render_imgs = [cv2.resize(img, (target_width, target_height)) for img in render_imgs]  # 调整大小
    render_imgs = [torch.tensor(img).float() / 255.0 for img in render_imgs]  # 转为张量
    render_imgs = [img.permute(2, 0, 1)[None, ...] for img in render_imgs]  # [1, 3, H, W]
    
    render_imgs = [img.permute(0, 2, 3, 1) for img in render_imgs]  # 转为 [1, H, 3, W]

    # 加载 GT 图片
    orig_path = r"./datas/temp"
    orign_imgs = [cv2.imread(fn) for fn in glob.glob(f"{orig_path}/*.png")]
    orign_imgs = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in orign_imgs]
    orign_imgs = [cv2.resize(img, (target_width, target_height)) for img in orign_imgs]  # 调整大小
    orign_imgs = [torch.tensor(img).float() / 255.0 for img in orign_imgs]
    # 第一个 permute 操作
    orign_imgs = [img.permute(2, 0, 1)[None, ...] for img in orign_imgs]  # [1, 3, H, W]
    for i, img in enumerate(orign_imgs):
        print(f"After first permute, Image {i} shape: {img.shape}")  # 打印第一个 permute 后的形状

# 第二个 permute 操作
    orign_imgs = [img.permute(0, 2, 3, 1) for img in orign_imgs]  # 转为 [1, H, 3, W]
    for i, img in enumerate(orign_imgs):
        print(f"After second permute, Image {i} shape: {img.shape}")  # 打印第二个 permute 后的形状


    # 打印形状
 
    # 计算指标
    results = []
    with torch.no_grad():
        results = [evaluator(img.cuda(), gt.cuda()) for gt, img in zip(orign_imgs, render_imgs)]

    # 输出指标
    psnr = torch.stack([r["psnr"] for r in results]).mean().item()
    ssim = torch.stack([r["ssim"] for r in results]).mean().item()
    lpips = torch.stack([r["lpips"] for r in results]).mean().item()
    print(f"psnr: {psnr}")
    print(f"ssim: {ssim}")
    print(f"lpips: {lpips}")


if __name__ == "__main__":
    evaluator = EvalAvatarBrightness()
    evaluator.to(torch.device("cuda:0"))
    evaluator.eval()

    # 渲染路径
    load_images(evaluator, r"./datas/temp-images")