import numpy as np, math, cv2

def depth_mean(image):
    return image[image>0].mean()


def kitti2mm(image):
    image_re = np.zeros_like(image, dtype=np.uint16)
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            image_re[y,x] = int(image[y,x]/256*1000)
    return image_re

def rmse_mae__sqrel(esti, gt):
    rmse, mae, sqrel, i = 0, 0, 0, 0
    dw=gt.shape[1] - esti.shape[1]
    dh=gt.shape[0] - esti.shape[0]
    compare_gt = gt[dh:,dw:]
    depth_list = list()
    diff_list = list()
    for y in range(compare_gt.shape[0]):
        for x in range(compare_gt.shape[1]):
            if compare_gt[y,x] != 0:
                gt_depth = float(compare_gt[y,x]/1000)
                diff = gt_depth - float(esti[y,x]/1000)
                depth_list.append(gt_depth)
                diff_list.append(diff)
                
                rmse += diff ** 2
                mae += abs(diff)
                sqrel += diff ** 2 / gt_depth
                i += 1
    
    return math.sqrt(rmse/i), mae/i, sqrel/i, depth_list, diff_list

def rmse_mae__sqrel_kitti(esti, gt):
    rmse, mae, sqrel, i = 0, 0, 0, 0
    dw=gt.shape[1] - esti.shape[1]
    dh=gt.shape[0] - esti.shape[0]
    compare_gt = gt[dh:,dw:]
    depth_list = list()
    diff_list = list()
    for y in range(compare_gt.shape[0]):
        for x in range(compare_gt.shape[1]):
            if compare_gt[y,x] != 0:
                gt_depth = float(compare_gt[y,x]/256)
                diff = gt_depth - float(esti[y,x]/1000)
                depth_list.append(gt_depth)
                diff_list.append(diff)
                    
                rmse += diff ** 2
                mae += abs(diff)
                sqrel += diff ** 2 / gt_depth
                i += 1
                
    return math.sqrt(rmse/i), mae/i, sqrel/i, depth_list, diff_list

def results_range(depth_list, diff_list):
    rmse, mae, sqrel, i = [0]*14, [0]*14, [0]*14, [0]*14
    
    for depth, diff in zip(depth_list, diff_list):
        if 0 < depth < 5.0:
            rmse[0] += diff**2
            mae[0] += abs(diff)
            sqrel[0] += diff**2/depth
            i[0] += 1
        elif 5.0 <= depth < 10.0:
            rmse[1] += diff**2
            mae[1] += abs(diff)
            sqrel[1] += diff**2/depth
            i[1] += 1
        elif 10.0 <= depth < 15.0:
            rmse[2] += diff**2
            mae[2] += abs(diff)
            sqrel[2] += diff**2/depth
            i[2] += 1
        elif 15.0 <= depth < 20.0:
            rmse[3] += diff**2
            mae[3] += abs(diff)
            sqrel[3] += diff**2/depth
            i[3] += 1
        elif 20.0 <= depth < 25.0:
            rmse[4] += diff**2
            mae[4] += abs(diff)
            sqrel[4] += diff**2/depth
            i[4] += 1
        elif 25.0 <= depth < 30.0:
            rmse[5] += diff**2
            mae[5] += abs(diff)
            sqrel[5] += diff**2/depth
            i[5] += 1
        elif 30.0 <= depth < 35.0:
            rmse[6] += diff**2
            mae[6] += abs(diff)
            sqrel[6] += diff**2/depth
            i[6] += 1
        elif 35.0 <= depth < 40.0:
            rmse[7] += diff**2
            mae[7] += abs(diff)
            sqrel[7] += diff**2/depth
            i[7] += 1
        elif 40.0 <= depth < 45.0:
            rmse[8] += diff**2
            mae[8] += abs(diff)
            sqrel[8] += diff**2/depth
            i[8] += 1
        elif 45.0 <= depth < 50.0:
            rmse[9] += diff**2
            mae[9] += abs(diff)
            sqrel[9] += diff**2/depth
            i[9] += 1
        elif 50.0 <= depth < 55.0:
            rmse[10] += diff**2
            mae[10] += abs(diff)
            sqrel[10] += diff**2/depth
            i[10] += 1
        elif 55.0 <= depth < 60.0:
            rmse[11] += diff**2
            mae[11] += abs(diff)
            sqrel[11] += diff**2/depth
            i[11] += 1
        elif 60.0 <= depth < 65.0:
            rmse[12] += diff**2
            mae[12] += abs(diff)
            sqrel[12] += diff**2/depth
            i[12] += 1
        elif 65.0 <= depth:
            rmse[13] += diff**2
            mae[13] += abs(diff)
            sqrel[13] += diff**2/depth
            i[13] += 1

    rmse_list, mae_list, sqrel_list = [0]*14, [0]*14, [0]*14
    cnt = 0
    for i_n, rmse_n, mae_n, sqrel_n in zip(i, rmse, mae, sqrel):
        if i_n == 0:
            rmse_list[cnt], mae_list[cnt], sqrel_list[cnt] = 0, 0, 0             
        else:
            rmse_list[cnt] = math.sqrt(rmse_n/i_n)
            mae_list[cnt] = mae_n/i_n
            sqrel_list[cnt] = sqrel_n/i_n
        cnt += 1
    # rmse_list = [math.sqrt(rmse[n]/i[n]) for n in range(len(rmse))]
    # mae_list = [mae[n]/i[n] for n in range(len(mae))]
    # sqrel_list = [sqrel[n]/i[n] for n in range(len(sqrel))]
    return rmse_list, mae_list, sqrel_list, i

def show_results(rmse_list, mae_list, sqrel_list, num_list):
    num = 0
    for rmse_i, mae_i, sqrel_i, num_i in zip(rmse_list, mae_list, sqrel_list, num_list):
        i = str(num) + "< depth <=" + str(num+5)
        print(i,": ", "\tcount: ", num_i, "\tRMSE: ", round(rmse_i, 4), "\tMAE: ", round(mae_i,4), "\tSq Rel: ", round(sqrel_i, 4))
        num +=5
