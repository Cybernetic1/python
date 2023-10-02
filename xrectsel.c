/* original from [https://bbs.archlinux.org/viewtopic.php?id=85378 Select a screen area with mouse and return the geometry of this area? / Programming & Scripting / Arch Linux Forums]

To build with (Ubuntu 14.04):
	gcc -Wall xrectsel.c -o xrectsel -lX11

TO-DO:
* cannot use mouse at beginning of program
* cannot use PageDown after rectangle is drawn
*/

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/cursorfont.h>
#include <unistd.h> // added for sleep/usleep
#define XK_MISCELLANY
//#include <X11/keysymdef.h>
//#include <X11/Intrinsic.h>
//#include <X11/extensions/XTest.h>
#include <xdo.h>

int main(void)
{
	int rx = 0, ry = 0, rw = 0, rh = 0;
	int rect_x = 0, rect_y = 0, rect_w = 0, rect_h = 0;
	int btn_pressed = 0, done = 0, key = 0;

	xdo_t *xdoer = xdo_new(":0.0");

	XEvent ev;
	Display *disp = XOpenDisplay(NULL);

	if(!disp)
		return EXIT_FAILURE;

	Screen *scr = NULL;
	scr = ScreenOfDisplay(disp, DefaultScreen(disp));

	Window root = 0;
	root = RootWindow(disp, XScreenNumberOfScreen(scr));

	Cursor cursor, cursor2;
	cursor = XCreateFontCursor(disp, XC_left_ptr);
	cursor2 = XCreateFontCursor(disp, XC_lr_angle);

	XColor color, dummy;
	XAllocNamedColor(disp, DefaultColormap(disp, 0), "blue",
									&color, &dummy);

	XGCValues gcval;
	gcval.foreground = XWhitePixel(disp, 0);
	// gcval.foreground = color.pixel;
	gcval.function = GXxor;
	int d = 2;
	gcval.line_width = d*2;
	gcval.background = XBlackPixel(disp, 0);
	gcval.plane_mask = gcval.background ^ gcval.foreground;
	gcval.subwindow_mode = IncludeInferiors;

	GC gc;
	gc = XCreateGC(disp, root, GCFunction | GCForeground | GCBackground | GCSubwindowMode | GCLineWidth, &gcval);

	/* this XGrab* stuff makes XPending true ? */
	int pointerGrabbed = 0;
	if ((XGrabPointer(disp, root, False, ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeAsync, root, cursor, CurrentTime) != GrabSuccess))
		printf("couldn't grab pointer:");
	else
		pointerGrabbed = 1;

	if ((XGrabKeyboard(disp, root, True, GrabModeAsync, GrabModeAsync,	CurrentTime) != GrabSuccess))
		printf("couldn't grab keyboard:");

	// see also: http://stackoverflow.com/questions/19659486/xpending-cycle-is-making-cpu-100
	while (!done) {
		//~ while (!done && XPending(disp)) {
			//~ XNextEvent(disp, &ev);
		// fixes the 100% CPU hog issue in original code:
		if (!XPending(disp)) { usleep(1000); continue; }

		if ( (XNextEvent(disp, &ev) >= 0) ) {
			switch (ev.type) {
				case MotionNotify:
				/* this case is purely for drawing rect on screen */
					if (btn_pressed) {
						if (rect_w) {
							/* re-draw the last rect to clear it */
							XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
						} else {
							/* Change the cursor to show we're selecting a region */
							XChangeActivePointerGrab(disp, ButtonMotionMask | ButtonReleaseMask, cursor2, CurrentTime);
						}
						rect_x = rx;
						rect_y = ry;
						rect_w = ev.xmotion.x - rect_x;
						rect_h = ev.xmotion.y - rect_y;

						if (rect_w < 0) {
							rect_x += rect_w;
							rect_w = 0 - rect_w;
						}
						if (rect_h < 0) {
							rect_y += rect_h;
							rect_h = 0 - rect_h;
						}
						/* draw rectangle */
						XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
						XFlush(disp);
					}
					break;
				case ButtonPress:
					btn_pressed = 1;
					rx = ev.xbutton.x;
					ry = ev.xbutton.y;
					break;
				case ButtonRelease:
					if (rect_w > 0 && rect_h > 0)
						done = 1;
					break;
				case KeyPress:
					key = XLookupKeysym(&ev.xkey, 0);
					if (key == 'm') {
						if (pointerGrabbed) {
							XUngrabPointer(disp, CurrentTime);
							pointerGrabbed = 0;
							}
						else {
							XGrabPointer(disp, root, False,ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeAsync, root, cursor, CurrentTime);
							pointerGrabbed = 1;
							}
						}
					if (key == XK_Escape)
						done = 1;
					if (key == 'k')
						XAllowEvents(disp, AsyncKeyboard, CurrentTime);
					if (key == 'd') {
							//XTestGrabControl(disp, True);
							//XTestFakeKeyEvent(disp, XK_Page_Down, True, 0);
							//XTestFakeKeyEvent(disp, XK_Page_Down, False, 0);
							//XSync (disp, False);
							//XTestGrabControl(disp, False);
							xdo_keysequence(xdoer, CURRENTWINDOW, "PageDown", 0);
						}
					system("beep -f 1000 -l 100");
					break;
			}
		}
	}

	XUngrabPointer(disp, CurrentTime);

	/* Now the rectangle is on display
	 * Wait for key to capture the screen
	 * 
	 *  */

	done = 0;
	char cmd[256];

	while (!done) {
		//~ while (!done && XPending(disp)) {
			//~ XNextEvent(disp, &ev);
		if (!XPending(disp)) { usleep(1000); continue; } // fixes the 100% CPU hog issue in original code
		if ( (XNextEvent(disp, &ev) >= 0) ) {
			if (ev.type == KeyPress) {
		key = XLookupKeysym(&ev.xkey, 0);
		switch (key) {
			case XK_Escape:
				done = 1;
				break;
			case 'c':
				sprintf(cmd, "scrot -a \'%d,%d,%d,%d\' ; beep -f 1000 -l 200 -f 1500 -l 200", rect_x+d, rect_y+d, rect_w-d-d, rect_h-d-d);
				system(cmd);
			case 'r':
				XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
				XFlush(disp);
				system("beep -f 1000 -l 100");
				break;
			default:
				printf("key = %c\n", key);
				break;
			}
			}
		}
	}

	/* clear the drawn rectangle */
	if (rect_w) {
		XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
		XFlush(disp);
	}

	rw = ev.xbutton.x - rx;
	rh = ev.xbutton.y - ry;
	/* cursor moves backwards */
	if (rw < 0) {
		rx += rw;
		rw = 0 - rw;
	}
	if (rh < 0) {
		ry += rh;
		rh = 0 - rh;
	}

	XCloseDisplay(disp);

	printf("r = %dx%d+%d+%d\n",rw,rh,rx,ry);
	printf("rect = %dx%d+%d+%d\n",rect_w,rect_h,rect_x,rect_y);
	
	return EXIT_SUCCESS;
}
