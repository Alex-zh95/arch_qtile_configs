// Source name:         hidraw_touchpad_tog.cpp
// Description:         Driver for toggling touchpad including LED indicator
// Notes:               Similar code available from Tuxedo website but requires calls to desktop environment (GNOME/KDE). Code here avoids that.

#include <linux/hidraw.h>
#include <stdnoreturn.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>

// Identify the HID name of the device - can use xinput to help obtain
#define HID_NAME "UNIW0001:00 093A:0255"

// We store status of the driver in a temporary file, defined
static const char *tmpfile_path = "/tmp/hidraw-tog.tmp";
static char buffer[10];

// Function declarations

/// @brief Identify device specified by HID_NAME define tag
/// @return Device handle hidraw_number or -1 for failure
static int find_device();

// Setter and getter for the temporary file
static void write_tmpfile(const char *);
static const char *read_tmpfile();

int main(int argc, char **argv)
{
    // Query status of touchpad and store in variable enable
    // If tmpfile reports on, strcmp returns 0 and we want enable = false, hence the "!!"
    // If tmpfile reports off, strcmp is positive or negative and we want enable = true
    bool enable = !!strcmp(read_tmpfile(), "on\n");

    // Get the device
    int n = find_device();

    // On failure, terminate
    if (n < 0)
    {
        fprintf(stderr, "Error: Failed to find device\n");
        return EXIT_FAILURE;
    }

    // Store the full path (up to buffer size 29 + termination) into device
    char device[30];
    snprintf(device, sizeof(device), "/dev/hidraw%d", n);

    // Open the device with write access (O_WRONLY) and non-blocking mode - other services may use the device in parallel
    const int fd = open(device, O_WRONLY | O_NONBLOCK);

    if (fd < 0)
    {
        fprintf(stderr, "Error: Unable to open %s", device);
        return 1+EXIT_FAILURE;
    }

    // To enable touchpad send "0x03" as feature report nr.7 (0x07) to the touchpad hid device.
    // To disable it send "0x00".
    // Reference: https://docs.microsoft.com/en-us/windows-hardware/design/component-guidelines/touchpad-configuration-collection#selective-reporting-feature-report
    // Details:
    // The two rightmost bits control the touchpad status
    // In order, they are:
    // 1. LED off + touchpad on/LED on + touchpad off
    // 2. Clicks on/off
    // So, the options are:
    // 0x00 LED on, touchpad off, touchpad click off
    // 0x01 LED on, touchpad off, touchpad click on
    // 0x02 LED off, touchpad on, touchpad click off
    // 0x03 LED off, touchpad on, touchpad click on
    char hid_buffer[2] = {0x07, (enable) ? 0x03 : 0x00};

    if (ioctl(fd, HIDIOCSFEATURE(sizeof(hid_buffer)), hid_buffer) < 0)
    {
        fprintf(stderr, "Error: ioctl(%s) failed", device);
        return 2+EXIT_FAILURE;
    }

    // Close the device
    close(fd);

    // Update the temp file
    write_tmpfile(enable ? "on" : "off");

    return EXIT_SUCCESS;
}

static int find_device()
{
    char path_uevent[50];
    char line[100];

    bool DEVICE_HANDLE_FOUND = false;
    int i = 0;

    // Loop through each of the hidrawN files for the right device...
    for (i = 0; i < 10; i++)
    {
        // snprintf function updates the name of path_uevent with the string in 3rd argument and beyond, truncating to max len of 50 incl. termination char
        snprintf(path_uevent, sizeof(path_uevent), "/sys/class/hidraw/hidraw%d/device/uevent", i);

        // Handle to the device
        FILE *file = fopen(path_uevent, "r");

        // If uninitialized (i.e. failure), try the next value of i
        if (!file)
            continue;

        // Traverse *file until end-of-line...
        while (!feof(file))
        {
            // fgets: Retrieve each line individually (\n char stops read) and store in variable line
            fgets(line, sizeof(line), file);

            // If HID_NAME found then close the handle and return the integer value i - we have found the correct handle
            // Note: strcmp returns 0 if match
            if (!strcmp(line, "HID_NAME=" HID_NAME "\n"))
                DEVICE_HANDLE_FOUND = true;
        }

        // Close the handle
        fclose(file);

        // Check for DEVICE_HANDLE_FOUND and return the driver handle
        if (DEVICE_HANDLE_FOUND)
            return i;
    }
    return -1;
}

static void write_tmpfile(const char *text)
{
    // Handle to the temporary file, open for writing
    FILE *file = fopen(tmpfile_path, "w");

    // Error handling if file cannot be accessed
    if (!file)
    {
        fprintf(stderr, "hidraw-tog: failed to update '%s': %s\n", tmpfile_path, strerror(errno));
        return;
    }

    // Overwrite the file with text input
    fprintf(file, "%s\n", text);

    // Confirm the new state in console
    fprintf(stderr, "hidraw-tog: new state: %s\n", text);

    fclose(file);
}

static const char *read_tmpfile()
{
    // Handle to the temporary file, open for reading
    FILE *file = fopen(tmpfile_path, "r");

    // Error handling for file access
    if (!file)
    {
        fprintf(stderr, "hidraw-tog: failed to read '%s': %s\n", tmpfile_path, strerror(errno));

        // Default to "on" in the case of failure so trackpad isn't permanently disabled!!!
        return "on";
    }

    // Retrieve contents of the file to buffer (up to 49 chars + terminating char)
    fgets(buffer, sizeof(buffer), file);

    fclose(file);

    // Return the buffer value
    return buffer;
}
