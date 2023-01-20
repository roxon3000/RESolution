import React from 'react';


function RuleDisplay(props) {

    let ruleId = props.ruleId;
    let rules = props.rules;
    let selRule = (props.rules == null) ? null : props.rules.find(e => e.id === ruleId);


    return (
        <pre>
            <code>
                ID {selRule && selRule.id }:{selRule && selRule.ruleType}({selRule && selRule.ruleValue })
    
            </code>    
        </pre>

    );
}

export default RuleDisplay;