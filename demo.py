from tiling3 import cubic_tiling
from matrix3 import rotate_x, rotate_y
from vector3 import Vector3
from restrict32 import restrict32


def draw_cubic():
    m = rotate_x(0.75) * rotate_y(0.55)
    v = Vector3(0,0,-0.1)
    l3 = cubic_tiling(-6,6,-6,6,-6,6).deform(m).translate(v)
    l2 = restrict32(l3).clip(-4,8,-6,6)
    print "Generated 2D tiling (V=%d, E=%d, F=%d)"%(len(l2.vertices), len(l2.edges), len(l2.faces))
    with open("cubic.eps", "w") as f:
        l2.write_eps(f, (20,520,200,700), (-4,8,-6,6))


if __name__=="__main__":
    draw_cubic()
