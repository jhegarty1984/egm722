import numpy as np
import rasterio as rio
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

dataset = rio.open('data_files/NI_Mosaic.tif')

print(f"{dataset.name} opened in {dataset.mode} mode")
print(f"image has {dataset.count} band(s)")
print(f"image size (width, height): {dataset.width} x {dataset.height}")
print(f"band 1 dataype is {dataset.dtypes[0]}") # note that the band name (Band 1) differs from the list index [0]
print(dataset.bounds) # georeferencing information for the dataset
print(dataset.crs) # coordinate reference system of the dataset
print(dataset.transform)

# Loading the Data
img = dataset.read() # loading the data

print(img.shape) # returns a tuple with the number of image bands bands, image height, and image width.
# print(img[7]) # will return an IndexError, because while there are 7 bands, the indices range from 0 to 6.

print(img[0, dataset.height // 2, dataset.width // 2]) # note that // performs floor division, as indices have to be integers

centeri, centerj = dataset.height // 2, dataset.width // 2 # note that centeri corresponds to the row, and centerj the column
centerx, centery = dataset.transform * (centerj, centeri) # note the reversal here, from i,j to j,i
print(dataset.index(centerx, centery)) # show the indices that correspond to our x,y values
print((centeri, centerj) == dataset.index(centerx, centery)) # check that these are the same

top, lft = dataset.index(centerx-500, centery+500)
bot, rgt = dataset.index(centerx+500, centery-500)

subset = dataset.read(window=((top, bot), (lft, rgt))) # format is (top, bottom), (left, right)

# the 'with' statement

dataset # show the current status of the dataset object

f = open('my_file.txt', 'w')
...
f.close()

with open('my_file.txt', 'w') as f:
    ...

with rio.open('data_files/NI_Mosaic.tif') as dataset:
    img = dataset.read()
    xmin, ymin, xmax, ymax = dataset.bounds

dataset # show the current status of the dataset object
# displaying raster data using matplotlib and cartopy

ni_utm = ccrs.UTM(29) # note that this matches with the CRS of our image
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm))

ax.imshow(img[3], cmap='gray', vmin=200, vmax=5000) # display band 4 as a grayscale image, stretched between 200 and 5000
ax.set_extent([xmin, xmax, ymin, ymax], crs=ni_utm) # set the extent to the image boundary

fig # show the figure

ax.imshow(img[3], cmap='gray', vmin=200, vmax=5000, transform=ni_utm, extent=[xmin, xmax, ymin, ymax])
ax.set_extent([xmin, xmax, ymin, ymax], crs=ni_utm) # set the extent to the image boundary

fig