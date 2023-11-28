from dbus_next.aio import MessageBus
import asyncio

layouts_list=[]

def on_layout_changed(idx):
    print(f'layout changed: {idx} -> {layouts_list[idx]}')







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

    current_layout = await layout.call_get_layout()
    print(f"Current Layout: {current_layout}")
    layout.on_layout_changed(on_layout_changed)

    await loop.create_future()



if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass

