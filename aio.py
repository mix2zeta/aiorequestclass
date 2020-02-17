from aiohttp import web
from req_class import request_parse


@request_parse
async def handle(request, name, age:int, from_town='Ya'):
    # name = request.match_info.get('name', "Anonymous")
    text = f"Hello, {name}, you are {age} year old"
    # import pdb; pdb.set_trace()
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)