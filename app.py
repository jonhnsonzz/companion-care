"""
CompanionCare - 陪诊守护
子女视角的陪诊服务平台 MVP

核心逻辑：
- 子女端：创建陪诊需求 → 系统匹配陪诊师 → 服务完成 → AI生成复诊提醒
- 陪诊师端：接受订单 → 查看任务详情（含AI生成的医院攻略） → 完成服务
- 管理端：数据看板
"""

import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'companion-care-secret-2026')
CORS(app)

# ============================================================
# 内存数据存储 (MVP阶段，真实环境替换为数据库)
# ============================================================

# 老人健康档案
# key: elderly_id, value: dict
elderly_db = {}

# 陪诊师数据
# key: companion_id, value: dict
companions_db = {}

# 订单记录
# key: order_id, value: dict
orders_db = {}

# 医院攻略库
# key: hospital_name, value: list[tips]
hospital_tips_db = {
    "华西医院": [
        "内分泌科在4楼，扶梯比电梯快",
        "上午10点后专家号基本约满，建议提前1天",
        "抽血在3楼，B超在2楼，先抽血再B超可以节省时间",
        "心内科住院部门禁需陪诊师备案才能进入",
    ],
    "四川省人民医院": [
        "挂号可现场加号，上午8点前到成功率更高",
        "取药在1楼，有自助取号机",
        "CT和核磁需要预约当天做不了",
    ],
    "成都市第一人民医院": [
        "科室分散在不同楼，通过连廊连接",
        "下午2点后人少，排队时间可减半",
    ]
}

# ============================================================
# AI 模拟函数 (真实环境接入 DeepSeek)
# ============================================================

def ai_match_companion(elderly_info: dict, hospital: str, department: str) -> dict:
    """
    AI匹配陪诊师
    输入：老人信息 + 医院 + 科室
    输出：匹配到的陪诊师 + 推荐理由
    """
    # 简单规则匹配 (MVP阶段)
    available = [c for c in companions_db.values() if c.get('available', True)]
    
    if not available:
        return None
    
    # 优先匹配擅长该医院+科室的陪诊师
    for companion in available:
        expertise = companion.get('expertise', [])
        hospitals = companion.get('hospitals', [])
        if hospital in hospitals and department in expertise:
            score = companion.get('rating', 5.0) + len([t for t in expertise if t == department]) * 0.5
            return {**companion, 'match_score': min(score, 5.0)}
    
    # 次选：同医院
    for companion in available:
        hospitals = companion.get('hospitals', [])
        if hospital in hospitals:
            score = companion.get('rating', 5.0)
            return {**companion, 'match_score': score}
    
    # 默认：评分最高的
    best = max(available, key=lambda x: x.get('rating', 5.0))
    return {**best, 'match_score': best.get('rating', 5.0)}


def ai_generate_reminder(elderly: dict, last_service_date: str, service_type: str) -> dict:
    """
    AI生成复诊提醒
    输入：老人档案 + 上次服务时间 + 服务类型
    输出：下次建议时间 + 提醒内容
    """
    disease = elderly.get('disease', '常规复查')
    
    # 规则映射 (真实环境由AI生成)
    reminder_map = {
        '糖尿病复查': {'interval_months': 3, 'next_check': '糖化血红蛋白+空腹血糖'},
        '高血压复查': {'interval_months': 1, 'next_check': '血压监测+用药调整'},
        '心脑血管复查': {'interval_months': 6, 'next_check': '心电图+血脂检查'},
        '肿瘤复查': {'interval_months': 3, 'next_check': '肿瘤标志物+影像学检查'},
        '常规复查': {'interval_months': 6, 'next_check': '常规体检+血液检查'},
    }
    
    config = reminder_map.get(disease, reminder_map['常规复查'])
    
    last_date = datetime.fromisoformat(last_service_date)
    next_date = last_date + timedelta(days=config['interval_months'] * 30)
    
    return {
        'suggested_date': next_date.strftime('%Y年%m月%d日'),
        'interval': f'每{config["interval_months"]}个月一次',
        'check_items': config['next_check'],
        'ai_message': f"根据{disease}的管理指南，建议{elderly['name']}于{next_date.strftime('%Y年%m月')}进行复查，检查项目包括：{config['next_check']}。如出现不适请随时就诊。"
    }


def ai_generate_task_detail(elderly: dict, companion: dict, hospital: str, department: str) -> str:
    """
    AI生成陪诊任务详情 (陪诊师看到的)
    """
    tips = hospital_tips_db.get(hospital, [])
    existing_tips = "\n".join([f"• {t}" for t in tips[:3]])
    
    disease = elderly.get('disease', '未知')
    medications = elderly.get('medications', '无')
    
    detail = f"""
📋 任务详情（AI生成）

👤 患者：{elderly['name']}
🏥 医院：{hospital} {department}
📅 预约时间：{elderly.get('last_visit', '待确认')}

【健康档案】
• 疾病：{disease}
• 常用药物：{medications}
• 特殊情况：{elderly.get('notes', '无')}

【注意事项】
• 建议到院时间：上午8:00前（如需空腹检查）
{existing_tips}

【联系家属】
• 子女姓名：{elderly.get('child_name', '待联系')}
• 联系电话：{elderly.get('child_phone', '待联系')}
    """
    return detail.strip()


def ai_generate_order_summary(order: dict, companion: dict, elderly: dict) -> str:
    """
    AI生成订单完成摘要
    """
    disease = elderly.get('disease', '常规')
    duration = order.get('duration', '约2小时')
    
    summary = f"""
✅ 陪诊完成

👤 服务对象：{elderly['name']} ({elderly.get('age', '')}岁)
🏥 服务医院：{order.get('hospital', '')} {order.get('department', '')}
📅 服务日期：{order.get('created_at', '')[:10]}
⏱️ 服务时长：{duration}

【服务记录】
• 完成项目：{order.get('services', '常规陪诊')}
• 就医科室：{order.get('department', '')}
• 取药情况：{'已完成' if order.get('medication_collected') else '无需取药'}

【医嘱备注】
• {order.get('medical_notes', '遵医嘱按时服药，定期复查')}

💰 费用结算
• 陪诊费用：{order.get('fee', 400)}元
• 保险：已覆盖（每次服务自动投保）
    """
    return summary.strip()


# ============================================================
# 路由：首页（子女端）
# ============================================================

@app.route('/')
def index():
    """子女端首页"""
    return render_template('index.html')


@app.route('/companion')
def companion_page():
    """陪诊师端"""
    return render_template('companion.html')


@app.route('/dashboard')
def dashboard():
    """管理端数据看板"""
    return render_template('dashboard.html')


# ============================================================
# API：子女端
# ============================================================

@app.route('/api/elderly', methods=['POST'])
def create_elderly_profile():
    """创建老人健康档案"""
    data = request.json
    
    elderly_id = str(uuid.uuid4())
    elderly = {
        'id': elderly_id,
        'name': data.get('name', ''),
        'age': data.get('age', ''),
        'gender': data.get('gender', ''),
        'disease': data.get('disease', ''),        # 疾病类型
        'medications': data.get('medications', ''), # 常用药物
        'allergies': data.get('allergies', ''),    # 过敏史
        'child_name': data.get('child_name', ''),  # 子女姓名
        'child_phone': data.get('child_phone', ''),# 子女电话
        'notes': data.get('notes', ''),            # 特殊备注
        'hospital': data.get('hospital', ''),      # 常去医院
        'department': data.get('department', ''),   # 常去科室
        'created_at': datetime.now().isoformat(),
    }
    
    elderly_db[elderly_id] = elderly
    
    return jsonify({
        'success': True,
        'elderly': elderly,
        'message': '健康档案创建成功'
    })


@app.route('/api/elderly/<elderly_id>', methods=['GET'])
def get_elderly_profile(elderly_id):
    """获取老人健康档案"""
    elderly = elderly_db.get(elderly_id)
    if not elderly:
        return jsonify({'success': False, 'error': '档案不存在'}), 404
    return jsonify({'success': True, 'elderly': elderly})


@app.route('/api/order', methods=['POST'])
def create_order():
    """
    创建陪诊订单（子女端）
    核心：选择老人 → 选择医院科室 → AI匹配陪诊师
    """
    data = request.json
    elderly_id = data.get('elderly_id')
    hospital = data.get('hospital')
    department = data.get('department')
    service_type = data.get('service_type', '普通陪诊')  # 普通/肿瘤/慢病
    appointment_date = data.get('appointment_date')
    
    elderly = elderly_db.get(elderly_id)
    if not elderly:
        return jsonify({'success': False, 'error': '请先创建健康档案'}), 400
    
    # AI匹配陪诊师
    matched_companion = ai_match_companion(elderly, hospital, department)
    
    if not matched_companion:
        return jsonify({
            'success': False, 
            'error': '暂无空闲陪诊师，请稍后再试'
        }), 400
    
    # 创建订单
    order_id = str(uuid.uuid4())
    order = {
        'id': order_id,
        'elderly_id': elderly_id,
        'elderly_name': elderly['name'],
        'hospital': hospital,
        'department': department,
        'service_type': service_type,
        'appointment_date': appointment_date,
        'companion_id': matched_companion['id'],
        'companion_name': matched_companion['name'],
        'companion_phone': matched_companion.get('phone', ''),
        'companion_rating': matched_companion.get('rating', 5.0),
        'match_score': matched_companion.get('match_score', 5.0),
        'fee': data.get('fee', 400),
        'status': 'matched',  # matched -> confirmed -> in_progress -> completed
        'created_at': datetime.now().isoformat(),
        'task_detail': ai_generate_task_detail(elderly, matched_companion, hospital, department),
    }
    
    orders_db[order_id] = order
    
    # 更新老人的上次就医信息
    elderly['last_visit'] = appointment_date
    elderly['hospital'] = hospital
    elderly['department'] = department
    
    return jsonify({
        'success': True,
        'order': order,
        'message': f'已为您匹配陪诊师：{matched_companion["name"]}（{matched_companion.get("rating", 5.0)}分）'
    })


@app.route('/api/order/<order_id>/complete', methods=['POST'])
def complete_order(order_id):
    """完成陪诊订单"""
    data = request.json
    order = orders_db.get(order_id)
    if not order:
        return jsonify({'success': False, 'error': '订单不存在'}), 404
    
    # 更新订单状态
    order['status'] = 'completed'
    order['completed_at'] = datetime.now().isoformat()
    order['services'] = data.get('services', '常规陪诊')
    order['medication_collected'] = data.get('medication_collected', False)
    order['medical_notes'] = data.get('medical_notes', '')
    order['duration'] = data.get('duration', '约2小时')
    
    elderly = elderly_db.get(order['elderly_id'])
    
    # AI生成订单摘要
    companion = companions_db.get(order['companion_id'], {})
    order_summary = ai_generate_order_summary(order, companion, elderly)
    order['summary'] = order_summary
    
    # AI生成复诊提醒
    if elderly:
        reminder = ai_generate_reminder(
            elderly, 
            order['created_at'], 
            elderly.get('disease', '常规复查')
        )
        order['reminder'] = reminder
        elderly['last_visit'] = order['created_at'][:10]
    
    return jsonify({
        'success': True,
        'order': order,
        'summary': order_summary,
        'reminder': reminder if elderly else None
    })


@app.route('/api/reminder/<elderly_id>', methods=['GET'])
def get_reminder(elderly_id):
    """获取老人的复诊提醒"""
    elderly = elderly_db.get(elderly_id)
    if not elderly:
        return jsonify({'success': False, 'error': '档案不存在'}), 404
    
    if not elderly.get('last_visit'):
        return jsonify({
            'success': False, 
            'error': '暂无就诊记录，无法生成提醒'
        }), 400
    
    reminder = ai_generate_reminder(
        elderly,
        elderly['last_visit'],
        elderly.get('disease', '常规复查')
    )
    
    return jsonify({
        'success': True,
        'elderly': elderly,
        'reminder': reminder
    })


# ============================================================
# API：陪诊师端
# ============================================================

@app.route('/api/companion/<companion_id>', methods=['GET'])
def get_companion_profile(companion_id):
    """获取陪诊师信息"""
    companion = companions_db.get(companion_id)
    if not companion:
        return jsonify({'success': False, 'error': '陪诊师不存在'}), 404
    
    # 获取该陪诊师的订单
    companion_orders = [o for o in orders_db.values() 
                       if o.get('companion_id') == companion_id]
    
    return jsonify({
        'success': True,
        'companion': companion,
        'orders': companion_orders
    })


@app.route('/api/companion/<companion_id>/orders', methods=['GET'])
def get_companion_orders(companion_id):
    """获取陪诊师的订单列表"""
    companion_orders = [o for o in orders_db.values() 
                       if o.get('companion_id') == companion_id]
    companion_orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify({
        'success': True,
        'orders': companion_orders
    })


@app.route('/api/companion/login', methods=['POST'])
def companion_login():
    """陪诊师登录"""
    data = request.json
    phone = data.get('phone')
    
    # 简单验证 (真实环境需要密码)
    for c in companions_db.values():
        if c.get('phone') == phone:
            return jsonify({'success': True, 'companion': c})
    
    # 不存在则创建 (演示用)
    companion_id = str(uuid.uuid4())
    companion = {
        'id': companion_id,
        'name': f'陪诊师{phone[-4:]}',
        'phone': phone,
        'rating': 5.0,
        'orders_count': 0,
        'available': True,
        'expertise': [],  # 擅长科室
        'hospitals': [],  # 常跑医院
        'created_at': datetime.now().isoformat(),
    }
    companions_db[companion_id] = companion
    
    return jsonify({'success': True, 'companion': companion})


@app.route('/api/companion/<companion_id>/update', methods=['POST'])
def update_companion(companion_id):
    """更新陪诊师信息"""
    data = request.json
    companion = companions_db.get(companion_id)
    if not companion:
        return jsonify({'success': False, 'error': '陪诊师不存在'}), 404
    
    # 更新字段
    if 'name' in data:
        companion['name'] = data['name']
    if 'expertise' in data:
        companion['expertise'] = data['expertise']
    if 'hospitals' in data:
        companion['hospitals'] = data['hospitals']
    if 'available' in data:
        companion['available'] = data['available']
    
    return jsonify({'success': True, 'companion': companion})


# ============================================================
# API：管理端
# ============================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取数据看板统计"""
    total_elderly = len(elderly_db)
    total_companions = len(companions_db)
    total_orders = len(orders_db)
    completed_orders = len([o for o in orders_db.values() if o.get('status') == 'completed'])
    
    # 收入统计
    total_revenue = sum(o.get('fee', 0) for o in orders_db.values())
    platform_revenue = int(total_revenue * 0.15)  # 15%抽佣
    
    # 各医院订单分布
    hospital_stats = {}
    for order in orders_db.values():
        h = order.get('hospital', '未知')
        hospital_stats[h] = hospital_stats.get(h, 0) + 1
    
    return jsonify({
        'success': True,
        'stats': {
            'total_elderly': total_elderly,
            'total_companions': total_companions,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'completion_rate': f"{completed_orders/total_orders*100:.1f}%" if total_orders else "0%",
            'total_revenue': total_revenue,
            'platform_revenue': platform_revenue,
            'hospital_distribution': hospital_stats,
        }
    })


@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    """获取所有订单"""
    orders = list(orders_db.values())
    orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify({'success': True, 'orders': orders})


@app.route('/api/elderly/list', methods=['GET'])
def list_elderly():
    """获取所有老人档案"""
    elderly_list = list(elderly_db.values())
    elderly_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    return jsonify({'success': True, 'elderly_list': elderly_list})


# ============================================================
# 初始化示例数据
# ============================================================

def init_sample_data():
    """初始化示例陪诊师数据"""
    sample_companions = [
        {
            'id': 'c001',
            'name': '张姐',
            'phone': '13800138001',
            'rating': 4.9,
            'orders_count': 23,
            'available': True,
            'expertise': ['内分泌科', '糖尿病', '高血压'],
            'hospitals': ['华西医院', '四川省人民医院'],
            'tags': ['华西内分泌科专家', '糖尿病照护经验丰富'],
            'created_at': datetime.now().isoformat(),
        },
        {
            'id': 'c002',
            'name': '李师傅',
            'phone': '13800138002',
            'rating': 4.8,
            'orders_count': 45,
            'available': True,
            'expertise': ['心内科', '神经内科'],
            'hospitals': ['华西医院', '成都市第一人民医院'],
            'tags': ['心脑血管专科', '10年陪诊经验'],
            'created_at': datetime.now().isoformat(),
        },
        {
            'id': 'c003',
            'name': '王阿姨',
            'phone': '13800138003',
            'rating': 4.7,
            'orders_count': 31,
            'available': True,
            'expertise': ['肿瘤科', '外科'],
            'hospitals': ['四川省人民医院', '华西医院'],
            'tags': ['肿瘤患者陪诊', '熟悉放化疗流程'],
            'created_at': datetime.now().isoformat(),
        },
    ]
    
    for c in sample_companions:
        companions_db[c['id']] = c
    
    # 示例老人档案
    sample_elderly = {
        'id': 'e001',
        'name': '刘阿姨',
        'age': '72',
        'gender': '女',
        'disease': '糖尿病复查',
        'medications': '二甲双胍 每日2次',
        'allergies': '无',
        'child_name': '李梅',
        'child_phone': '13900001111',
        'notes': '膝盖不好，走路慢，楼层高需扶梯',
        'hospital': '华西医院',
        'department': '内分泌科',
        'last_visit': '2026-02-15',
        'created_at': '2026-01-10T10:00:00',
    }
    elderly_db['e001'] = sample_elderly
    
    # 示例订单
    sample_order = {
        'id': 'o001',
        'elderly_id': 'e001',
        'elderly_name': '刘阿姨',
        'hospital': '华西医院',
        'department': '内分泌科',
        'service_type': '慢病复查',
        'appointment_date': '2026-05-19',
        'companion_id': 'c001',
        'companion_name': '张姐',
        'companion_phone': '13800138001',
        'companion_rating': 4.9,
        'fee': 400,
        'status': 'completed',
        'services': '空腹血糖+糖化血红蛋白+取药',
        'medication_collected': True,
        'medical_notes': '血糖控制良好，三个月后复查',
        'duration': '约3小时',
        'created_at': '2026-05-19T08:30:00',
        'completed_at': '2026-05-19T11:45:00',
    }
    orders_db['o001'] = sample_order


init_sample_data()

# ============================================================
# 启动
# ============================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    print(f"\n🏥 陪诊守护 MVP 启动中...")
    print(f"📍 访问地址: http://localhost:{port}")
    print(f"📊 管理后台: http://localhost:{port}/dashboard")
    print(f"\n示例账号:")
    print(f"  陪诊师: 13800138001 (张姐)")
    print(f"  陪诊师: 13800138002 (李师傅)")
    print(f"  陪诊师: 13800138003 (王阿姨)")
    app.run(host='0.0.0.0', port=port, debug=debug)
