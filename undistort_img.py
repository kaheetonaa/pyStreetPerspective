import cv2
import numpy as np
import matplotlib.pyplot as plt
w=4000
h=3008
fx=0.583648519766
fy=0.583648519766
cx=0.5
cy=0.5*h/w
cx_img=int(256*cx)
cy_img=int(256*cy)
k1=-0.308101239924
k2=0.0605864259956
k3=0
p1=0
p2=0

print(cx_img,cy_img)
camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0., 0., 1.]], dtype=np.float32)
camera_matrix_img =np.array([[fx*256, 0, cx_img], [0, fy*256, cy_img], [0., 0., 1.]], dtype=np.float32)   
dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)

test_grid=[]
test_image=cv2.imread("test.jpeg")
for i in range(20):
    for j in range(20):
        test_grid+=[[i*cx/10,j*cy/10]]

test_grid=np.array(test_grid)

undistorted = cv2.undistortPoints(test_grid, camera_matrix, dist_coeffs)
undistorted_arr=np.array([i[0] for i in undistorted])

newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix_img, dist_coeffs, (256,192), 1, (256,192))
undistorted_image = cv2.undistort(test_image, camera_matrix_img, dist_coeffs)

cv2.imshow('image',test_image)
#cv2.waitKey(0)
cv2.imshow('undistorted_image',undistorted_image)
cv2.waitKey(0)
plt.plot(test_grid[:,0],test_grid[:,1],'o')
plt.show()

plt.plot(undistorted_arr[:,0],undistorted_arr[:,1],'o')
plt.show()

undistorted_image.show()
#print(xy_undistorted)
