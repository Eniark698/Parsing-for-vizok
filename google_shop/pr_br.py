"""Find and show 10 working HTTP(S) proxies."""
def prx():
    import asyncio
    from proxybroker import Broker


    proxy_list=[]


    async def show(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            a=str(proxy).find(']')
            b=str(proxy).find('>')
            proxy_list.append({'HTTP':str(proxy)[a+2:b]})

    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(
        broker.find(types=['HTTP', 'HTTPS'], limit=10),
        show(proxies))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)


    print('created proxy list')
    return proxy_list