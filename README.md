# Image_stictching
Image stitching or photo stitching is the process of combining multiple photographic images with overlapping fields of view to produce a segmented panorama or high-resolution image.
Here the image stitching is performed on left and right images by following the below steps:

* Detecting keypoints (DoG, Harris, etc.) and extracting local invariant descriptors (SIFT, SURF, etc.) from two input images
* Matching the descriptors between the images
* Using the RANSAC algorithm to estimate a homography matrix using our matched feature vectors.
* Applying a warping transformation using the homography matrix obtained from the above the step.

