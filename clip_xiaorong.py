import os
import glob
import sys
import torch
import clip
from PIL import Image
import numpy as np

def cal_metric(gt_list, pred_list, model, preprocess, device):

    total_similarity = []

    for gt_path, pred_path in zip(gt_list, pred_list):
        gt_pic = Image.open(gt_path)
        gt_pic_array = np.array(gt_pic)
        gt_pic_array = gt_pic_array[:512, :512]
        gt_pic = Image.fromarray(gt_pic_array)
        image_gt = preprocess(gt_pic).unsqueeze(0).to(device)
        # image_gt = preprocess(Image.open(gt_path)).unsqueeze(0).to(device)

        rd_pic = Image.open(pred_path)
        rd_pic_array = np.array(rd_pic)
        rd_pic_array = rd_pic_array[:512, 512:1024]
        rd_pic = Image.fromarray(rd_pic_array)
        image_pred = preprocess(rd_pic).unsqueeze(0).to(device)
        # image_pred = preprocess(Image.open(pred_path)).unsqueeze(0).to(device)

        with torch.no_grad():
            # clip
            image_gt_feat = model.encode_image(image_gt)
            image_pred_feat = model.encode_image(image_pred)
            similarity = torch.cosine_similarity(image_gt_feat, image_pred_feat, dim=1)

            total_similarity.append(similarity.item()) 
            
    metric = {}
    metric["clipf"] = sum(total_similarity[0::4]) / len(gt_list[0::4])
    metric["clips"] = (sum(total_similarity[1::4]) + sum(total_similarity[2::4])) + sum(total_similarity[3::4]) / (len(gt_list)/0.75)
    metric["clip"] = sum(total_similarity) / len(gt_list)

    return metric

def write_res(metric, rd, file_name):
    with open(rd + f"/{file_name}.txt",'w') as f:
        f.write(f"CLIPf: {metric['clipf']:.4}\n")
        f.write(f"CLIPs: {metric['clips']:.4}\n")
        f.write(f"CLIP: {metric['clip']:.4}\n")

if __name__ == "__main__":
    # # argv[1] 数据集
    # # argv[2] 模型
    print("start")

    # gt_name = "_".join(sys.argv[1].split("_")[:-2])

    # name = sys.argv[1]
    # if "magicman" in sys.argv[1]:
    #     name = sys.argv[1] + "_2view"
    
    # mlp = ""
    # if sys.argv[2] == "nomlp":
    #     mlp = "_nomlp"

    # # gt = f"/liuxianguo2/linshuo/GART/data/insav_wild_new_old/{gt_name}_000_cut"
    # gt = f""
    # rd = f"/liuxianguo2/linshuo/GART/logs/debug/new_backup/seq={name}_prof=zju_3m{mlp}_data=instant_avatar_wild"
    
    gt = sys.argv[1]
    rd = gt

    # rd = sys.argv[2]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    gt_list = sorted(glob.glob(f'{gt}/test_tto/*.png'))

    rd_list = sorted(glob.glob(f'{rd}/test_tto/*.png'), key=lambda x: int(os.path.basename(x).split('.')[0]))

    metric = cal_metric(gt_list, rd_list, model, preprocess, device)
    write_res(metric, rd, "clip")
    print("eval done")
