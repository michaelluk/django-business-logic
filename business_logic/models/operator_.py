# -*- coding: utf-8 -*-
#

import operator

from django.db import models
from django.utils.encoding import smart_unicode
from django.utils.translation import gettext as _

from node import NodeAccessor

class Operator(NodeAccessor):
    operator = models.CharField(_('Operator'), null=False, max_length=3)
    operator_table = {}

    def _check_operator(self):
        if self.operator not in self.operator_table:
            raise TypeError, 'Incorrect operator "%(operator)s" for class %(cls)s' % \
                    dict(operator=self.operator, cls=self.__class__.__name__)

    def __init__(self, *args, **kwargs):
        super(Operator, self).__init__(*args, **kwargs)
        if not self.id and self.operator:
            self._check_operator()

    def save(self, *args, **kwargs):
        self._check_operator()
        return super(Operator, self).save(*args, **kwargs)

    def __unicode__(self):
        return smart_unicode(self.operator)

    class Meta:
        abstract = True

class BinaryOperator(Operator):
    operator_table = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div,
        '%': operator.mod,
        '&': operator.and_,
        '|': operator.or_,
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        'in': operator.contains,
        }

    def interpret(self, ctx, lhs, rhs):
        return self.operator_table[self.operator](lhs, rhs)

    class Meta:
        verbose_name = _('Binary operator')
        verbose_name_plural = _('Binary operators')


class UnaryOperator(Operator):
    class Meta:
        verbose_name = _('Unary operator')
        verbose_name_plural = _('Unary operators')

    operator_table = {
            '-': operator.neg,
            'not': operator.not_,
            'neg': operator.neg,
            'abs': operator.abs,
            }

    def interpret(self, ctx, rhs):
        return self.operator_table[self.operator](rhs)

