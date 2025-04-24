from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec

display = PicoGraphics(display=DISPLAY_INKY_PACK)

jpeg = jpegdec.JPEG(display)
jpeg.open_file("test6.jpg")
jpeg.decode(0, 0, dither=True)

display.set_update_speed(0)
display.update()
