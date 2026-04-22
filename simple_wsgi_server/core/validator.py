from .exceptions import ParamsException

from typing import Dict, Any

class ParameterValidate:
    @staticmethod
    def validate(params: Dict[str, Any], rules: Dict[str, Dict]):
        for field, rule in rules.items():
            value = params.get(field)
            
            # 必填校验
            if rule.get('required', False) and value is None:
                raise ParamsException(f"参数{field}是必填的")
            # 非必填跳过该字段
            if value is None:
                continue
            # 类型校验
            expect_type = rule.get('type')
            if expect_type is not None and not isinstance(value, expect_type):
                raise ParamsException(f"参数{field}期望类型为{expect_type}")
            
            # 字符串长度校验
            if expect_type == str:
                min_str = rule.get('min_len')
                max_str = rule.get('max_len')
                
                if min_str is not None and max_str is not None and (len(value) < min_str or len(value) > max_str):
                    raise ParamsException(f"参数{field}的长度要在{min_str}和{max_str}之间")
                if min_str is not None and len(value) < min_str:
                    raise ParamsException(f"参数{field}的长度不能小于{min_str}")
                if max_str is not None and len(value) > max_str:
                    raise ParamsException(f"参数{field}的长度不能大于{max_str}")
                
            # 数值校验
            if expect_type == int:
                min_int = rule.get('min')
                max_int = rule.get('max')
                
                if min_int is not None and len(value) < min_int:
                    raise ParamsException(f"参数{field}的值不能小于{min_int}")
                if max_int is not None and len(value) > max_int:
                    raise ParamsException(f"参数{field}的值不能大于{max_int}")