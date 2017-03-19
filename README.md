# photos2geojson | [demo](http://visgean.me/photos2geojson/)
Searches recursively for photos and generates geojson map


### Install: 

```
$ pip3 install photos2geojson --user
```


### Usage:

```
$ photos2geojson ~/Dropbox/
```

This will create file ``map.html`` that you can view in Browser (Firefox preferably as chrome might not display image orientation correctly). 


Alternatively you might wish to create a Github Gist which will render the geojson:

```
$ photos2geojson ~/Dropbox/ -g
```

If you only want the geojson you can do it like this:


```
$ photos2geojson ~/Dropbox/ -o data.geojson
```

Screenshot of leaflet:

![screenshot](https://raw.githubusercontent.com/Visgean/photos2geojson/master/screen.png "Screenshot")
