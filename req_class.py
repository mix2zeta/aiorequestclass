import functools
import inspect
import aiohttp

from pydantic import  create_model, ValidationError

def request_parse(func):
    async def validate_and_parse(*args, **kwargs):
        assert type(args[0]) == aiohttp.web_request.Request

        # import pdb; pdb.set_trace()
        print(inspect.getfullargspec(func))
        spec = inspect.getfullargspec(func)
        payload = await args[0].json() if args[0].has_body else {}

        para_type = {}

        for key in args[0].match_info.keys():
            para_type[key] = (str, ...)

        for key in spec.annotations.keys():
            para_type[key] = (spec.annotations[key], ...)

        DynamicModel = create_model(
            'DynamicModel',
            **para_type,
        )

        try:
            DynamicModel(**dict(args[0].match_info), **payload)
        except ValidationError as e:
            reason = e.json()
            print(reason)
            raise aiohttp.web.HTTPUnprocessableEntity(reason=reason)


        return await func(args[0], **dict(args[0].match_info), **payload)
    return validate_and_parse