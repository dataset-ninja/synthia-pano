
The **SYNTHIA-PANO: Panoramic Image Dataset** is the panoramic version of [SYNTHIA](https://datasetninja.com/synthia-all) dataset. Panoramic images offer distinct advantages in terms of information capacity and scene stability, owing to their expansive field of view (FoV). To gauge the impact of incorporating panoramic images into the training dataset, the authors meticulously designed and executed a comprehensive set of experiments. The experimental findings underscore the advantageous influence of using panoramic images as training data on segmentation results. Notably, employing panoramic images with a 180-degree FoV in the training set enhances model performance. Furthermore, the model trained with panoramic images exhibits superior resilience against image distortion, showcasing an additional benefit of this approach.

## Dataset creation

With the development of deep learning, the research on image analysis methods has been boosted. Semantic segmentation, different from the target detection technology, can extract information in the image at the pixel level. Currently, most semantic segmentation researches are based on images with a conventional field of view (FoV). The images with a conventional FoV that is relatively narrow can only cover information in a certain direction, and their content will change with respect to the viewpoint, so they have shortcomings in the aspect of information capacity and stability. In contrast, 360-degree panoramic images can compensate for these shortcomings. However, due to their large FoV and distortion, the general semantic segmentation method and training data are not ideal for the segmentation of panoramic images. The accuracy will decrease and the general input size of a model requires cutting the panoramic image into several segments,3 which will lead to discontinuity in the segmentation map. In order to realize the better segmentation of panoramic images, the authors created a dataset of panoramic images and apply it for the training of convolutional neural network to yield a panoramic semantic segmentation model.

The typical method to deal with the distortion in panoramic images is to use data augmentation. The data augmentation can simulate the distortion in panoramic images. When trained with such augmented data, the model can adapt well to panoramic images with distortion. However, the general public datasets for segmentation only contain images of forward-direction view, which can’t simulate the large FoV of panoramic images. The authors method is to synthesize a new dataset of panoramic images. Their panoramic dataset is built from the virtual image dataset [SYNTHIA](https://datasetninja.com/synthia-all) due to the lack of real-world panoramic image dataset. SYHTHIA dateset contains finely labeled images with a conventional FoV. The authors managed to stitch the images taken from different directions into panoramic images, together with their labeled images, to yield the panoramic semantic segmentation dataset dubbed SYNTHIA-PANO.

## Panoramic images segmentation methods

A deep neural network can achieve good accuracy, sometimes it suffers from the complexity. Panoramic images are often large in size due to their large FoV, which may cause a high computational consumption if a deep neural network is used. However, for a model there is a tradeoff between the complexity and the performance. A complex model tends to have good performance but high consumption. The Image Cascade Network (ICNet) is designed for real-time semantic segmentation of high-resolution images and it balances the accuracy and time consumption well. 

The authors choose to use ICNet as the basic model directly and focus our work on the training data. They made a new dataset which consists of panoramic images. The new dataset the authors made is based on another dataset called [SYNTHIA](https://datasetninja.com/synthia-all). [SYNTHIA](https://datasetninja.com/synthia-all) dataset is created from computer 3D city traffic scene models and all of the images in it are virtual images. It contains some subsets called SYNTHIA-Seqs in which the images are taken by four cameras in leftward, forward, rightward and backward directions on a moving car in the virtual cities. In addition, there are images of different city scenes, seasons, weather conditions and so on. What the authors did is to stitch these four-direction images into panoramic images. 

<img src="https://github.com/dataset-ninja/synthia-pano/assets/120389559/c6d6c182-dd48-408c-a3de-08e69f49042d" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">The figure is a demonstration of the the images and labels in SYNTHIA dataset. The color of each class is below.</span>

One way to get panoramic images is to take images from different directions around a circle and then stitch them together. When the camera rotates, the geometrical relations between the objects in the images also changes. To unify the geometrical relations of the whole scene, cylindrical projection is an important step before stitching a panoramic image. If the scene is projected on a cylindrical surface, one object in the images from different view directions can be quite the same. In this sense, when stitching the images, the overlapping parts can coincide with each other perfectly.

<img src="https://github.com/dataset-ninja/synthia-pano/assets/120389559/0600411a-fd18-487b-9efb-8830436baaee" alt="image" width="600">

<span style="font-size: smaller; font-style: italic;">The figure is a demonstration of the cylindrical projection. Every point (x, y) on the image have a corresponding point (x0, y0) on the surface of the cylinder. The corresponding point is on the line which passes the center point of the cylinder and the original point.</span>

The mapping built above is just cylindrical projection and the result of it is an image on cylindrical surface. The most important parameter when doing it is the radius of the cylindrical surface r which is often set the same as the focal length f. Generally, a small focal length f leads to severe distortion and vice versa.

For four images in leftward, forward, rightward and backward directions denoted as, the authors can project the normal images into a cylindrical surface, and the next step is to stitch them together. 

<img src="https://github.com/dataset-ninja/synthia-pano/assets/120389559/42204474-4ad1-41fc-89be-6d271bbdd342" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">The four images and their labels in leftward, forward, rightward and backward directions are shown on the left of the figure. After the transforms, they are projected on a cylindrical surface and stitched together.</span>

## Dataset description

By means above, a panoramic image dataset can be obtained from the original [SYNTHIA](https://datasetninja.com/synthia-all) dataset. The authors panoramic image dataset includes five sequences of images: _Seqs02-summer_, _Seqs02-fall_, _Seqs04-summer_, _Seqs04-fall_, _Seqs05-summer_. Seqs02 series and Seqs05 series are taken in a New York like city and Seqs04 series are taken in a European town like city. The original images are ordered video sequences and we truncated the repeated images.


