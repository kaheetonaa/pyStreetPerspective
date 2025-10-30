import math
import urllib.request, json 
from sympy import solve,Symbol
import sympy
import sys
import certifi
import ssl

#altitude - float, original altitude from camera Exif calculated from sea level.
#atomic_scale - float, scale of the SfM reconstruction around the image.
#camera_parameters - array of float, focal length, k1, k2. .
#camera_type - enum, type of camera projection: "perspective", "fisheye", "equirectangular" (or equivalently "spherical")
#captured_at - timestamp, capture time.
#compass_angle - float, original compass angle of the image.
#computed_altitude - float, altitude after running image processing, from sea level.
#computed_compass_angle - float, compass angle after running image processing.
#computed_geometry - GeoJSON Point, location after running image processing.
#computed_rotation - enum, corrected orientation of the image. .
#creator - { username: string, id: string }, the username and user ID who owns and uploaded the image.
#exif_orientation - enum, orientation of the camera as given by the Exif tag. .
#geometry - GeoJSON Point geometry.
#height - int, height of the original image uploaded.
#is_pano - boolean, a true or false indicator for whether an image is 360 degree panorama.
#make - string, the manufacturer name of the camera device.
#model - string, the model or product series name of the camera device.
#thumb_256_url - string, URL to the 256px wide thumbnail.
#thumb_1024_url - string, URL to the 1024px wide thumbnail.
#thumb_2048_url - string, URL to the 2048px wide thumbnail.
#thumb_original_url - string, URL to the original wide thumbnail.
#merge_cc - int, ID of the connected component of images that were aligned together.
#mesh - { id: string, url: string } - URL to the mesh.
#sequence - string, ID of the sequence, which is a group of images captured in succession.
#sfm_cluster - { id: string, url: string } - URL to the point cloud data in JSON and compressed by zlib. See the example below.
#width - int, width of the original image uploaded.
#detections - JSON object, detections from the image including base64 encoded string of the image segmentation coordinates.

#The z-axis points forward
#The y-axis points down
#The x-axis points to the right

id=sys.argv[1]
print('id='+id)

print('-------------')

context = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen("https://graph.mapillary.com/"+id+"?access_token=MLY|4463150933761310|5995ca3757fc4f9a9c8f5e96b2efaa03&fields=camera_parameters,camera_type,exif_orientation,computed_geometry,computed_rotation,width,height,computed_compass_angle,thumb_1024_url,thumb_256_url,computed_rotation",context=context) as url:
    data = json.load(url)



print('parameter: ',data)
width=data['width']
height=data['height']
f=data['camera_parameters'][0]
k1=data['camera_parameters'][1]
k2=data['camera_parameters'][2]
whratio=width/height
rotation=data['computed_rotation']
print('-------------')
#----------------------------------------

r2_max=0.5**2+(0.5/whratio)**2
r2_range=[i*r2_max/10 for i in range(10)]
d_range=[1+k1*i+k2*(i**2) for i in r2_range]
print('range_d=',d_range)
#if d_range monotonically decrease --> barrel distortion, d_range=0 no distortion, d_range monotonically increase pinhole distortion https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#:%7E:text=The%20next%20figures,monotonically%20increasing


print('-------------')
#----------------------------------------

#xn=x/z
#yn=y/z
#r2=xn^2+yn^2
#d=1+k1*r2+k2*r2^2
#u=f*d*xn
#v=f*d*yn
xn=Symbol('xn')
yn=Symbol('yn')

result_x=solve(f*(1+k1*(xn**2)+k2*(xn**4))*xn-0.5,xn) #solve xn max yn =0
result_y=solve(f*(1+k1*(yn**2)+k2*(yn**4))*yn-0.5/whratio,yn) #solve xn=0 yn max

xn_0=0.5/f
yn_0=0.5/(f*whratio)
print('xn_0=',xn_0)
print('yn_0=',yn_0)


def show_result(result_x,result_y):
 for i in result_x:
  for j in result_y:
    #print('result: ',i,type(i))
    if isinstance(i,sympy.core.numbers.Float) and isinstance(j,sympy.core.numbers.Float):
       #angle=math.atan2(i,1)*2 #xn faces the angle, 1 because xn is normalized. multiply by 2 for the full angle.
       #angle_deg=angle/math.pi*180 
       print('xn_max= ',i,'yn_max= ',j)

show_result(result_x,result_y)

print('-------------')

#-------------------------------------------
#rotation to euler rotation
rotation+=[math.sqrt(rotation[0]**2+rotation[1]**2+rotation[2]**2)]
if rotation[3]>0:
    #define quarternion https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
    q0=math.cos(rotation[3]/2)
    q1=rotation[0]/rotation[3]*math.sin(rotation[3]/2)
    q2=rotation[1]/rotation[3]*math.sin(rotation[3]/2)
    q3=rotation[2]/rotation[3]*math.sin(rotation[3]/2)
    q=[q0,q1,q2,q3]
    print(rotation)
    print(q)
    roll=math.atan2(2*(q0*q1+q2*q3),q0**2-q1**2-q2**2+q3**2)
    pitch=math.asin(2*(q0*q2-q1*q3))
    yaw=math.atan2(2*(q0*q3+q1*q2),q0**2+q1**2-q2**2-q3**2)
    print(roll,pitch,yaw)
