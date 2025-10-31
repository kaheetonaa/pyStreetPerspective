import cv2
import numpy as np
import matplotlib.pyplot as plt
w=3840
h=2160
fx=0.27501776145519
fy=0.27501776145519
cx=0.5
cy=0.5*h/w
cx_img=int(256*cx)
cy_img=int(256*cy)
k1=-0.064926986043171
k2=0.0029608425514045
k3=0
p1=0
p2=0

print(cx_img,cy_img)
camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0., 0., 1.]], dtype=np.float32)
camera_matrix_img =np.array([[fx*128/cx, 0, cx_img], [0, fy*128/cx, cy_img], [0., 0., 1.]], dtype=np.float32)   
dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)

test_grid=[]
test_image=cv2.imread("958023398693452.jpg")
for i in range(20):
    for j in range(20):
        test_grid+=[[i*cx/10,j*cy/10]]

test_grid=np.array(test_grid)

undistorted = cv2.undistortPoints(test_grid, camera_matrix, dist_coeffs)
undistorted_arr=np.array([i[0] for i in undistorted])

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix_img, dist_coeffs, (256,int(256*h/w)), 1, (256,int(256*h/w)))

undistorted_image = cv2.undistort(test_image, camera_matrix_img, dist_coeffs, None, newcameramtx)
cv2.imshow('image',test_image)
cv2.imshow('undistorted_image',undistorted_image)
cv2.waitKey(0)
plt.plot(test_grid[:,0],test_grid[:,1],'o')
plt.show()

plt.plot(undistorted_arr[:,0],undistorted_arr[:,1],'o')
plt.show()

#print(xy_undistorted)
