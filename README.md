# imgres
A Python script for automatic resizing of images.

## Usage
`imgres [options] <pattern> <greater-dim-limit>`

Resizes all the images that match the given python regex pattern in the current directory  
to have the greater of the two dimensions at most as specified. 

## Options
```
-c, --confirm:           asks for confirmation before resizing images from each folder
-h, --help:              shows this help
-r, --recursive:         searches recursively also into subfolders
-l, --logs               makes a "./imgres-logs.txt" logfile from the run of the script
```

## Example

```
ferrard@Philadel:~/c/pics$ imgres -crl "jpg|png" 800
['-crl', 'jpg|png', '800']
Building list of files...

***************************************************************************
Processing folder: .
Going to resize following images to have the greater of dimensions <= 800
	1.) ./10.JPG: 768 x 1024
	2.) ./09.JPG: 768 x 1024
	3.) ./01.JPG: 768 x 1024
	4.) ./04.JPG: 768 x 1024
	5.) ./02.JPG: 768 x 1024
	6.) ./08.JPG: 768 x 1024
	7.) ./05.JPG: 768 x 1024
	8.) ./06.JPG: 768 x 1024
	9.) ./03.JPG: 1024 x 768
	10.) ./07.JPG: 1024 x 768
Do you really want to resize listed images? [y]|n: 
	1/10.) resizing ./10.JPG
	2/10.) resizing ./09.JPG
	3/10.) resizing ./01.JPG
	4/10.) resizing ./04.JPG
	5/10.) resizing ./02.JPG
	6/10.) resizing ./08.JPG
	7/10.) resizing ./05.JPG
	8/10.) resizing ./06.JPG
	9/10.) resizing ./03.JPG
	10/10.) resizing ./07.JPG

***************************************************************************
Processing folder: ./selection
Going to resize following images to have the greater of dimensions <= 800
	1.) ./selection/01.JPG: 1000 x 750
Do you really want to resize listed images? [y]|n: 
	1/1.) resizing ./selection/01.JPG
All done. 0 exceptions
```
