import win32api
import win32con
import click
import pywintypes
from loguru import logger

DISPLAY_ORIGINAL_RES = [(3840, 2160), (2560, 1600)]

DISPLAY_TARGET_RES = [(1920, 1080), (1280, 768)]


@click.command()
def cli():
    """Command-line interface for toggling between original and target display resolutions."""
    for i in range(3):
        try:
            display_device = win32api.EnumDisplayDevices(None, i)
            if not display_device.DeviceName:
                break

            current_settings = win32api.EnumDisplaySettings(display_device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)

            # available_resolutions = []
            # settings_index = 0
            # while True:
            #     try:
            #         settings = win32api.EnumDisplaySettings(display_device.DeviceName, settings_index)
            #         resolution = f"{settings.PelsWidth}x{settings.PelsHeight}"
            #         available_resolutions.append(resolution)
            #         settings_index += 1
            #     except:
            #         break
            current_resolution = f"{current_settings.PelsWidth}x{current_settings.PelsHeight}"
            logger.info(f'Display {i}: {display_device.DeviceName}, Current Resolution: {current_resolution}')

            if (current_settings.PelsWidth, current_settings.PelsHeight) == DISPLAY_ORIGINAL_RES[i]:
                change_resolution(display_device.DeviceName, DISPLAY_TARGET_RES[i])
            else:
                change_resolution(display_device.DeviceName, DISPLAY_ORIGINAL_RES[i])
        except pywintypes.error as e:
            pass
        except Exception as e:
            logger.error(f'Error retrieving display {i}: {e}')
            break


def change_resolution(device_name, resolution):
    """Change the resolution of the specified display device.

    Parameters:
    device_name (str): The name of the display device.
    resolution (tuple): The target resolution as (width, height).
    """
    devmode = win32api.EnumDisplaySettings(device_name, win32con.ENUM_CURRENT_SETTINGS)
    devmode.PelsWidth, devmode.PelsHeight = resolution
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT

    result = win32api.ChangeDisplaySettingsEx(device_name, devmode)
    if result != win32con.DISP_CHANGE_SUCCESSFUL:
        logger.error(f"Failed to change resolution for {device_name} to {resolution}")
    else:
        logger.info(f"Resolution of {device_name} set to {resolution}")
