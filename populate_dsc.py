import yaml
import argparse

april_fam = 't36h11' 
tag_border= 2.0000 #number of pixels in border of aruco marker
z = 0.0000

def main():
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    parser.add_argument("--yaml", help="Input yaml file, Kalibr definition.",default='../options/plane.yaml')
    parser.add_argument("--dsc", help="Output dsc file.",default='../options/test_plane.dsc')
    args = parser.parse_args()

    kalibr_yaml = yaml.safe_load(open(args.yaml,'r'))
    assert kalibr_yaml['target_type'] == 'aprilgrid'    #other tags not supported

    # header board information
    lines = []
    lines.append('0,'+str(kalibr_yaml['tagRows']*2+1)+','+str(kalibr_yaml['tagCols']*2+1)+','+"{:.6f}".format(100.*kalibr_yaml['tagSize']))
    lines.append(april_fam+','+"{:.6f}".format(tag_border))

    tag_size = kalibr_yaml['tagSize']
    tag_spacing = kalibr_yaml['tagSpacing']
    n_rows = kalibr_yaml['tagRows']
    n_cols = kalibr_yaml['tagCols']
    origin = [0.0,0.0]

    # locations of tags
    for col_idx in range(n_cols-1,-1,-1):
        for row_idx in range(n_rows):
   
            x = col_idx*(1+tag_spacing)*tag_size  + origin[0]
            y = row_idx*(1+tag_spacing)*tag_size  + origin[1]
         
            #lower right corner
            lines.append(str(-1)+','+str(row_idx*2)+','+str(col_idx*2+1)+','+"{:.6f}".format((x+tag_size))+','+"{:.6f}".format(y)+','+"{:.6f}".format(z))

            #upper right corner
            lines.append(str(-1)+','+str(row_idx*2+1)+','+str(col_idx*2+1)+','+"{:.6f}".format((x+tag_size))+','+"{:.6f}".format((y+tag_size))+','+"{:.6f}".format(z))
        
        for row_idx in range(n_rows):
            x = col_idx*(1+tag_spacing)*tag_size  + origin[0]
            y = row_idx*(1+tag_spacing)*tag_size  + origin[1]
            tag_id = col_idx*(n_cols)+row_idx

            #lower left corner
            lines.append(str(tag_id)+','+str(row_idx*2)+','+str(col_idx*2)+','+"{:.6f}".format(x)+','+"{:.6f}".format(y)+','"{:.6f}".format(z))

            #upper left corner
            lines.append(str(-1)+','+str(row_idx*2+1)+','+str(col_idx*2)+','+"{:.6f}".format(x)+','+"{:.6f}".format(y+tag_size)+','+"{:.6f}".format(z))


    f = open(args.dsc,"w")
    for line in lines:
        f.write(line)
        f.write('\n')


if __name__ == '__main__':
    main()
