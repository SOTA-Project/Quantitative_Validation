import cv2, numpy as np, open3d

W, H = 1216, 352
K = np.array([[925.927,0,612.29],[0,933.509,116.819],[0,0,1]])

RT = np.array([[0.0219621,-0.999754,-0.00293465,0.236921],[0.0853894,0.0048004,-0.996336,-0.647117],[0.996106,0.0216311,0.0854738,-2.14507],[0,0,0,1]])

# Read Image, Make depth Image
img = cv2.imread("rgb.png", cv2.IMREAD_ANYCOLOR)
depth_img = np.zeros((H, W), dtype=np.uint16)

# Read LiDAR point [X, Y, Z, 1]^T
pcd_load = open3d.io.read_point_cloud("1656481505.736261368.pcd", remove_nan_points=True)
pc_array = np.asarray(pcd_load.points).T
one_mat = np.ones_like(pc_array)[0].reshape(1, -1)
XYZ_L = np.concatenate((pc_array, one_mat),axis = 0)

# # Camera Coordinate [X, Y, Z, 1]^T 
XYZ_C = RT @ XYZ_L
XYZ_C = np.delete(XYZ_C, np.where(XYZ_C[2,:]<=0), axis=1)
# # Find Front direction coordinate
theta = np.arctan2(XYZ_C[2,:], XYZ_C[0,:]) * 180 / np.pi
index = list()
for i, angle in enumerate(theta):
    if 30 <= angle <= 150:
        index.append(i)
        
# # pixel coordibate (x, y, z) = P(3X4) * XYZ_C(4X1)
xy_ = K @ XYZ_C[:3,:]
depth = XYZ_C[2,:]
x, y = xy_[0,:]/xy_[2,:], xy_[1,:]/xy_[2,:]

for i in index:
    u, v = round(x[i]), round(y[i])
    if 0<=u<W and 0<=v<H:
        if depth[i] * 1000 >= 65535:
            depth_img[v,u] = 65535
        else:
            depth_img[v,u] = depth[i] * 1000
        cv2.circle(img, (u,v), 1, (0, 0, 255), -1)


cv2.imshow("dst", img); cv2.waitKey(0)
cv2.imwrite("depth_ridar.png", depth_img)
