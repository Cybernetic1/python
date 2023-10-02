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
#include <X11/keysymdef.h>
//#include <X11/Intrinsic.h>
//#include <X11/extensions/XTest.h>
//#include <xdo.h>
#include <fcntl.h>
#include <errno.h>
#include <linux/input.h>

int main(void)
{
	int done = 0;
	int fd, bytes;
	struct input_event data;
	const char *pDevice = "/dev/input/event3";
    // Open Keyboard
    fd = open(pDevice, O_RDONLY | O_NONBLOCK);
    if (fd == -1)
		{
        printf("ERROR Opening %s\n", pDevice);
        return -1;
		}

	while (!done) {

		bytes = read(fd, &data, sizeof(data));
		if (bytes > 0)
			{
			printf("Keypress bytes=%x, value=%x, type=%x, code=%x\n", bytes, data.value, data.type, data.code);
			}
		else
			sleep(1);

	}

	return 0;
}
