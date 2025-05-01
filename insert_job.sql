-- 插入工作信息
INSERT INTO job (
    title,
    title_zh,
    description,
    description_zh,
    location,
    salary_range,
    requirements,
    requirements_zh,
    job_type,
    headcount,
    created_at,
    is_active,
    company_id
) VALUES (
    'Warehouse Picker (Forklift Operator Preferred)',
    '仓库理货员（叉车工优先）',
    'We are currently seeking warehouse pickers for our Olympic Park facility with immediate start. Two shifts available (morning/afternoon). Forklift license holders will be given priority. Competitive hourly rates: $30/hour for general pickers, $35+/hour for forklift operators (based on experience).

Key Details:
- Location: Olympic Park, Western Sydney
- Morning Shift: Starting at 8:00 AM
- Afternoon Shift: Starting at 2:00 PM
- Immediate start available
- Full working rights required',

    '悉尼Olympic Park工厂招聘仓库理货员，可立即入职。提供早班和晚班两个班次。持有叉车证者优先考虑。具有竞争力的时薪：普通理货员30澳元/小时，叉车工35澳元起（根据经验）。

工作详情：
- 地点：悉尼西区Olympic Park
- 早班：上午8点开始
- 晚班：下午2点开始
- 可立即入职
- 需要合法工作许可',

    'Olympic Park, Western Sydney',
    '$30-35+/hour',
    '- Valid work rights in Australia
- Physical fitness and ability to lift
- Basic English communication skills
- Forklift license preferred
- PR preferred
- Male preferred
- Immediate availability',

    '- 澳洲合法工作许可
- 身体健康，能搬运货物
- 基本英语交流能力
- 叉车证优先
- PR优先
- 男性优先
- 可立即入职',

    'WAREHOUSE',
    2,
    '2025-04-21 09:00:00',
    true,
    1
); 