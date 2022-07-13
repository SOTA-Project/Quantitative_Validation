import cv2, matplotlib.pyplot as plt, numpy as np
from module import *


my_proj = cv2.imread("depth_ridar.png", cv2.IMREAD_ANYDEPTH)
DF_esti = cv2.imread("depth.png", cv2.IMREAD_ANYDEPTH)
CFR_esti = cv2.imread("newCFRs.png", cv2.IMREAD_ANYDEPTH)

DF_rmse, DF_mae, DF_sqrel, DF_depth_list, DF_diff_list = rmse_mae__sqrel(DF_esti, my_proj)
CFR_rmse, CFR_mae, CFR_sqrel, CFR_depth_list, CFR_diff_list = rmse_mae__sqrel(CFR_esti, my_proj)

print("DF_RMSE: {},\tDF_MAE: {},\tDF_Sq Rel: {}".format(DF_rmse, DF_mae, DF_sqrel))
print("CFR_RMSE: {},\tCFR_MAE: {},\tCFR_Sq Rel: {}".format(CFR_rmse, CFR_mae, CFR_sqrel))

DF_rmse_list, DF_mae_list, DF_sqrel_list, DF_num_list = results_range(DF_depth_list, DF_diff_list)
CFR_rmse_list, CFR_mae_list, CFR_sqrel_list, CFR_num_list = results_range(CFR_depth_list, CFR_diff_list)

DF_rmse_list, DF_mae_list, DF_sqrel_list, DF_num_list = results_range(DF_depth_list, DF_diff_list)
CFR_rmse_list, CFR_mae_list, CFR_sqrel_list, CFR_num_list = results_range(CFR_depth_list, CFR_diff_list)

show_results(DF_rmse_list, DF_mae_list, DF_sqrel_list, DF_num_list)
print("-----" * 12)
show_results(CFR_rmse_list, CFR_mae_list, CFR_sqrel_list, CFR_num_list)
