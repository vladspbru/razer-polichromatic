#!/usr/bin/env python3

import os
import asyncio
from dbus_next.aio import MessageBus

layouts_list=[]

def on_layout_changed(idx):
    print(f'layout changed: {idx} -> {layouts_list[idx]}')
    if idx:
        os.system('polychromatic-cli -s IO2312F53000046 -e "RU_KeyBoard"')
    else:
        os.system('polychromatic-cli -s IO2312F53000046 -e "EN_KeyBoard"')






async def main():
    bus = await MessageBus().connect()

    # the introspection xml would normally be included in your project, but
    # this is convenient for development
    introspection = await bus.introspect('org.kde.keyboard', '/Layouts')
    obj = bus.get_proxy_object('org.kde.keyboard', '/Layouts', introspection)
    layout = obj.get_interface('org.kde.KeyboardLayouts')

    global layouts_list
    layouts_list = await layout.call_get_layouts_list()
    print(f"LayoutsList: {layouts_list}")

    async def on_layout_list_changed():
        global layouts_list
        layouts_list = await layout.call_get_layouts_list()
        print(f"Layouts list changed to: {layouts_list}")

    layout.on_layout_list_changed(on_layout_list_changed)

    on_layout_changed( await layout.call_get_layout() )
    layout.on_layout_changed(on_layout_changed)

    await loop.create_future()



if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass


