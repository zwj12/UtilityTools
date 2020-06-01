通过灰度值选取Region，并通过connettion指令分割Region，最后显示所有的Region单元

read_image (Image, 'particle')
threshold (Image, BrightPixels, 120, 255)
count_obj(BrightPixels,NumThresholded)
connection (BrightPixels, Particles)
count_obj(Particles, numCount)
for i:=1 to numCount by 1
    select_obj(Particles , ParticleSelected , i )
    dev_display (ParticleSelected)
endfor
dev_display (Particles)
area_center (Particles, Area, Row, Column)
