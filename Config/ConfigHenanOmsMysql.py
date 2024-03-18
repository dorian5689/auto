#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2024/3/5 1:33
@Auth ： Xq
@File ：ConfigHenanOmsMysql.py
@IDE ：PyCharm
"""
import os

new_south = os.path.abspath(os.path.join('..', 'DataBaseInfo', 'HenanOmsMysql', 'new_south.yml'))


henan_oms_config_sjts_select ="""

SELECT 
    a.电场名称, 
    a.日期, 
    a.发电量, 
    a.发电量, 
    a.上网电量, 
    ROUND(a.弃电量/10000, 4) AS 弃电量, 
    b.储能最大充电电力, 
    b.储能最大放电电力, 
    b.储能日充电, 
    b.储能日放电, 
    b.充电次数, 
    b.放电次数, 
    a.填报开始时间, 
    a.填报结束时间, 
    CASE 
        WHEN a.是否已完成 = 1 THEN '已填报' 
        ELSE '未填报' 
    END AS 是否已完成
FROM nanfangyunying.data_oms a
LEFT JOIN nanfangyunying.data_oms_c b
ON a.电场名称=b.电场名称 AND a.日期=b.日期
WHERE a.日期 >= CURDATE() - INTERVAL 1 DAY;
"""





