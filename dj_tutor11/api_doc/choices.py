# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-08-03 05:57:59
# @Last Modified by:   theo-l
# @Last Modified time: 2017-08-03 06:03:20

from common.base_choices import ChoiceItem, BaseChoice


class HttpMethodChoice(BaseChoice):
    GET = ChoiceItem(1, 'GET')
    POST = ChoiceItem(2, 'POST')


class APIValueType(BaseChoice):
    INT = ChoiceItem(1, 'Integer')
    FLOAT = ChoiceItem(2, 'Float')
    STRING = ChoiceItem(3, 'String')
    DATE = ChoiceItem(4, 'Date')
    ARRAY = ChoiceItem(5, 'Array')
    DICT = ChoiceItem(6, 'Dict')
    BOOL = ChoiceItem(7, 'Boolean')
