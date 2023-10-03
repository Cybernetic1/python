/* Originally from https://askubuntu.com/a/763708/179725

To build with (Ubuntu 14.04):
	gcc -Wall xrectsel.c -o xrectsel -lX11 -lxdo [-lXtst]

To execute in terminal:
    $ xdotool getactivewindow windowminimize; ./xrectsel ; beep

TO-DO:
* gittering of mouse leaves residue dots at upper left corner

FIXED:
* use up and down arrows
* cannot use PageDown after rectangle is drawn
* keep rect while PageUp/PageDown
*/

#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/cursorfont.h>
#include <unistd.h> // added for sleep/usleep
#define XK_MISCELLANY
#define XK_LATIN1
#include <X11/keysymdef.h>
// #include <X11/extensions/XTest.h>
#include <xdo.h>
//#include <fcntl.h>
//#include <errno.h>
//#include <linux/input.h>
//#include <QX11Info> // from qt q11extras

Display *disp;
Window root;
Cursor cursor, cursor2;
XGCValues gcval;
GC gc;
const int d = 1;			// 1/2 line width of rectangle

void enterX(void)
	{
	disp = XOpenDisplay(NULL);
	if(!disp)
		exit(EXIT_FAILURE);

	Screen *scr = NULL;
	scr = ScreenOfDisplay(disp, DefaultScreen(disp));
	root = RootWindow(disp, XScreenNumberOfScreen(scr));
	//root = DefaultRootWindow(disp);

	cursor = XCreateFontCursor(disp, XC_left_ptr);
	cursor2 = XCreateFontCursor(disp, XC_lr_angle);

	gcval.foreground = XWhitePixel(disp, 0);
	// gcval.foreground = color.pixel;
	gcval.function = GXxor;
	gcval.line_width = d*2;
	gcval.background = XBlackPixel(disp, 0);
	gcval.plane_mask = gcval.background ^ gcval.foreground;
	gcval.subwindow_mode = IncludeInferiors;

	gc = XCreateGC(disp, root, GCFunction | GCForeground | GCBackground | GCSubwindowMode | GCLineWidth, &gcval);

	if (XGrabPointer(disp, root, True, ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeSync, None, cursor, CurrentTime) != GrabSuccess)
		printf("Couldn't grab Pointer\n");
	else
		printf("Grab Pointer success\n");	

	//XSelectInput(disp, root, KeyPressMask | ButtonPressMask);

	/*int err = XGrabButton(disp, AnyButton, AnyModifier, root, True, ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeAsync, None, cursor);
	switch (err) {
		case GrabSuccess:
			printf("GrabButton success!\n");
			break;
		case BadCursor:
			printf("BadCursor\n");
			break;
		case BadWindow:
			printf("BadWindow\n");
			break;
		case BadValue:
			printf("BadValue\n");
			break;
		default:
			printf("GrabButton failed\n");
			break;
		} */

	if (XGrabKeyboard(disp, root, True, GrabModeAsync, GrabModeAsync,CurrentTime) != GrabSuccess)
		printf("Couldn't grab Keyboard\n");
	else
		printf("Grab Keyboard success\n");

	//XSelectInput(disp, root, KeyPressMask);
	}

void leaveX(void)
	{
	// extern Display *disp;
	XUngrabKeyboard(disp, CurrentTime);
	//XUngrabButton(disp, AnyButton, AnyModifier, root);
	XUngrabPointer(disp, CurrentTime);
	XCloseDisplay(disp);
	}

int rx = 0, ry = 0, rw = 0, rh = 0;
int rect_x = 0, rect_y = 0, rect_w = 0, rect_h = 0;

void redrawRect(void)
	{
	XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
	XFlush(disp);
	}

int main(void)
	{
	void enterX(void), leaveX(void);

	int btn_pressed = 0, done = 0;
	int c;
	KeySym key = 0;
	XEvent ev;
	int pointerGrabbed = 0;
	int keysound = 0;
	char cmd[256];		// for 'scrot' shell command

	system("beep -f 500 -l 100");
	//system("xdotool key Page_Down");

	//key = getchar();
	//printf("key = %x\n", key);

	//int fd, bytes;
	//struct input_event data;
	//const char *pDevice = "/dev/input/event3";
	//// Open Keyboard
	//fd = open(pDevice, O_RDONLY | O_NONBLOCK);
	//if (fd == -1)
		//{
		//printf("ERROR Opening %s\n", pDevice);
		//return -1;
		//}

	xdo_t *xdoer = xdo_new(":0.0");

	//XColor color, dummy;
	//XAllocNamedColor(disp, DefaultColormap(disp, 0), "blue",
	//								&color, &dummy);

	enterX();

	/* does XGrab* stuff makes XPending true ? */

	//int keycode = 0;
	//keycode = XKeysymToKeycode(disp, XK_backslash);
	//XGrabKey(disp, keycode, AnyModifier, root, True, GrabModeAsync, GrabModeAsync);
	//printf("just grabbed the key '%x'\n", keycode);

	// **** XGrabPointer should not be used as it seems to disable keyboard
	//if ((XGrabPointer(disp, root, False, ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeSync, None, cursor, CurrentTime) != GrabSuccess))
	//	printf("couldn't grab pointer:");
	// pointerGrabbed = 1;
	// printf("grabbed the mouse\n");

	// see also: http://stackoverflow.com/questions/19659486/xpending-cycle-is-making-cpu-100
	printf("Entering while-loop....\n");
	while (!done) {
		//~ while (!done && XPending(disp)) {
			//~ XNextEvent(disp, &ev);
		// fixes the 100% CPU hog issue in original code:
		if (!XPending(disp)) {
			usleep(1000);
			continue;
			}

		//bytes = read(fd, &data, sizeof(data));
		//if (bytes > 0)
			//{
			//printf("Keypress value=%x, type=%x, code=%x\n", data.value, data.type, data.code);
			//}

		//key = getchar();
		//if (key != 0)
		//printf("key = %x\n", key);
		//else
			//printf("!\n");

		if (XNextEvent(disp, &ev) >= 0) {
		switch (ev.type) {
			case MotionNotify:
			/* this case is purely for drawing rect on screen */
				if (btn_pressed) {
					if (rect_w) {
						/* re-draw the last rect to clear it */
						redrawRect();
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
					redrawRect();
				}
				break;
			case ButtonPress:
				printf("button # = %d\n", ev.xbutton.button);
				btn_pressed = 1;
				rx = ev.xbutton.x;
				ry = ev.xbutton.y;
				break;
			case ButtonRelease:
				btn_pressed = 0;
				XChangeActivePointerGrab(disp, ButtonMotionMask | ButtonReleaseMask | ButtonPressMask, cursor, CurrentTime);
				//if (rect_w > 0 && rect_h > 0)
				//	done = 1;
				break;
			case KeyPress:
				//printf("key pressed\n");
				//system("beep -f 1000 -l 100");
				keysound = 1;
				key = XLookupKeysym(&ev.xkey, 0);
				printf("key = %lx\n", key);
				switch (key) {
					case XK_m:
						if (pointerGrabbed) {
							XUngrabPointer(disp, CurrentTime);
							pointerGrabbed = 0;
							}
						else {
							XGrabPointer(disp, root, False,ButtonMotionMask | ButtonPressMask | ButtonReleaseMask, GrabModeAsync, GrabModeAsync, root, cursor, CurrentTime);
							pointerGrabbed = 1;
							}
						break;
					case XK_Escape:
					case XK_q:
						done = 1;
						break;
					//case XK_K:
					//	XAllowEvents(disp, AsyncKeyboard, CurrentTime);
					//break;
					case XK_Page_Down:
						system("beep -f 100 -l 300");
						keysound = 0;
					case XK_d:
					case XK_bracketright:
						printf("Trying page down...\n");
						leaveX();
						//sleep(0.5);
						//XTestGrabControl(disp, True);
						//XTestFakeKeyEvent(disp, XK_Page_Down, True, 0);
						//XTestFakeKeyEvent(disp, XK_Page_Down, False, 0);
						//XSync(disp, False);
						//XTestGrabControl(disp, False);
						//XAllowEvents(disp, AsyncKeyboard, CurrentTime);
						xdo_send_keysequence_window(xdoer, CURRENTWINDOW, "Page_Down", 0);
						//system("xdotool key Page_Down");
						//sleep(1);
						enterX();
						sleep(1.5);
						redrawRect();
						break;
					case XK_Page_Up:
						system("beep -f 100 -l 300");
						keysound = 0;
					case XK_u:
					case XK_bracketleft:
						printf("Trying page up...\n");
						leaveX();
						xdo_send_keysequence_window(xdoer, CURRENTWINDOW, "Page_Up", 0);
						enterX();
						sleep(1.5);
						redrawRect();
						break;
					case XK_Up:
						system("beep -f 100 -l 300");
						keysound = 0;
						printf("Trying arrow up...\n");
						leaveX();
						xdo_send_keysequence_window(xdoer, CURRENTWINDOW, "Up", 0);
						enterX();
						sleep(1.5);
						redrawRect();
						break;
					case XK_Down:
						system("beep -f 100 -l 300");
						keysound = 0;
						printf("Trying arrow down...\n");
						leaveX();
						xdo_send_keysequence_window(xdoer, CURRENTWINDOW, "Down", 0);
						enterX();
						sleep(1.5);
						redrawRect();
						break;
					case XK_c:
					case XK_Return:
						printf("Trying Capture...\n");
						sprintf(cmd, "scrot -a \'%d,%d,%d,%d\' ; beep -f 1500 -l 500", rect_x+d, rect_y+d, rect_w-d-d, rect_h-d-d);
						system(cmd);
						keysound = 0;
						break;
					case XK_r:
						printf("Trying redraw rectangle...\n");
						redrawRect();
						break;
					case XK_space:
						printf("Flush display\n");
						XFlush(disp);
						break;
					default:
						keysound = 0;
						break;
						}	// end keys switch statement
				// still within case KeyPress
				if (keysound)
					system("beep -f 1000 -l 100");
				break;	// end case KeyPress
			default:
				break;
				}	// end ev.type switch statement
			}	// end if ev.type not Null
		}	// end while

	/* clear the drawn rectangle */
	if (rect_w) {
		XDrawRectangle(disp, root, gc, rect_x, rect_y, rect_w, rect_h);
		XFlush(disp);
		}

	leaveX();
	return EXIT_SUCCESS;
	}
