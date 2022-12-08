
from jobj import JObj
from objectproxy import getProxy

class RuleResult(JObj):
    def __init__(self):
        self.appliedRule = None 

def applyRule(rule, object):
    result = None
    match rule.ruleType:
        case "AttributeExists":
            result = rule_AttributeExists(rule, object)
        case _:
            result = rule_NotFound(rule)

    return result

def rule_AttributeExists(rule, object):
    result = RuleResult()
    result.appliedRule = getProxy(rule.id, 'rules')
    result.engineMethod = "rule_AttributeExists"

    if(hasattr(object, rule.ruleValue)):
        result.match = True
    else:
        result.match = False

    return result

def rule_NotFound(rule):
    result = RuleResult()
    result.appliedRule = getProxy(rule.ruleid, 'rules')
    result.match = False
    result.engineMethod = "rule_NotFound"

    return result
