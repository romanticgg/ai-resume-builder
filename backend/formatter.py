def format_resume(data):
    basic = data.get("basic_info", {})
    job = data.get("job_intention", {})
    education = data.get("education", {})
    projects = data.get("projects", [])
    internships = data.get("internships", [])
    skills = data.get("skills", [])
    self_eval = data.get("self_evaluation", "")

    target_position = job.get("position", "")

    resume_text = f"""
# 简历预览

## 基本信息
姓名：{basic.get('name', '')}
性别：{basic.get('gender', '')}
出生年月：{basic.get('birth_month', '')}
年龄：{basic.get('age', '')}
电话：{basic.get('phone', '')}
邮箱：{basic.get('email', '')}

## 求职意向
目标行业：{job.get('industry', '')}
目标职位：{target_position}
目标省份/地区：{job.get('location', '')}

## 教育经历
学校：{education.get('school', '')}
专业：{education.get('major', '')}
学历：{education.get('degree', '')}
时间：{education.get('duration', '')}
在校经历：{optimize_general_experience(education.get('campus_experience', ''), target_position)}

## 项目 / 活动 / 竞赛经历
"""

    for idx, project in enumerate(projects, start=1):
        resume_text += f"""
经历{idx}：{project.get('name', '')}
担任角色：{project.get('role', '')}
优化描述：{optimize_experience(project.get('description', ''), target_position)}
"""

    resume_text += "\n## 实习 / 工作经历\n"

    for idx, internship in enumerate(internships, start=1):
        resume_text += f"""
经历{idx}：{internship.get('company', '')} - {internship.get('role', '')}
优化描述：{optimize_experience(internship.get('description', ''), target_position)}
"""

    resume_text += f"\n## 技能 / 证书\n{format_skills(skills)}\n"
    resume_text += f"\n## 自我评价\n{optimize_self_evaluation(self_eval, target_position, skills)}\n"

    return resume_text


EXPERIENCE_PATTERNS = {
    "技术开发": ["开发", "系统", "网站", "小程序", "接口", "前端", "后端", "数据库", "代码", "程序", "软件", "python", "java", "flask", "spring"],
    "数据分析": ["数据", "分析", "统计", "问卷", "调研", "可视化", "excel", "sql", "报表", "图表", "整理数据"],
    "文案宣传": ["文案", "推文", "公众号", "宣传", "海报", "新闻稿", "拍摄", "剪辑", "排版", "新媒体", "短视频"],
    "组织策划": ["策划", "组织", "协调", "沟通", "安排", "对接", "流程", "活动", "会议", "执行"],
    "后勤保障": ["后勤", "物资", "签到", "场地", "秩序", "保障", "接待", "布置", "采购", "分发"],
    "竞赛活动": ["比赛", "竞赛", "挑战杯", "互联网+", "创新创业", "辩论赛", "数学建模", "大创", "参赛"],
    "志愿服务": ["志愿", "公益", "社区", "支教", "服务", "协助", "引导", "讲解", "陪伴"],
    "行政助理": ["行政", "资料整理", "归档", "会议纪要", "报表", "文件", "档案", "录入", "审核"],
    "市场运营": ["运营", "用户", "社群", "推广", "活动推广", "调研", "转化", "拉新", "留存", "品牌"],
    "教育培训": ["教学", "辅导", "培训", "课程", "学生", "讲课", "备课", "答疑", "助教"],
    "财务会计": ["财务", "会计", "凭证", "发票", "预算", "报销", "成本", "账目", "审计"],
    "人力资源": ["招聘", "面试", "简历筛选", "员工", "人事", "培训", "绩效", "考勤", "入职"]
}


def detect_experience_type(text):
    text = text.lower()
    scores = {}

    for exp_type, keywords in EXPERIENCE_PATTERNS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text:
                score += 1
        scores[exp_type] = score

    best_type = max(scores, key=scores.get)

    if scores[best_type] == 0:
        return "通用经历"

    return best_type


def optimize_experience(description, target_position):
    if not description.strip():
        return ""

    desc = clean_text(description)
    exp_type = detect_experience_type(desc)

    templates = {
        "技术开发": f"参与技术开发相关实践，围绕实际需求完成系统功能设计、代码实现与问题排查。{desc}，体现了较强的工程实践能力、逻辑分析能力和问题解决能力。",
        "数据分析": f"围绕数据收集、整理与分析任务开展实践，完成信息归纳、数据处理与结果呈现。{desc}，体现了良好的数据意识、逻辑分析能力和结果表达能力。",
        "文案宣传": f"参与宣传内容策划与文字材料整理工作，负责内容撰写、信息提炼与传播表达。{desc}，体现了较强的文字表达能力、信息整合能力和审美传播意识。",
        "组织策划": f"参与活动组织与流程推进工作，负责沟通协调、任务安排与执行落地。{desc}，保障相关工作有序开展，体现了组织策划能力、沟通协调能力和执行力。",
        "后勤保障": f"参与活动后勤与现场保障工作，负责物资准备、场地协调、秩序维护等支持性任务。{desc}，保障活动顺利开展，体现了责任意识、细节把控能力和执行能力。",
        "竞赛活动": f"参与竞赛或实践活动相关工作，围绕目标任务完成资料准备、团队协作与成果输出。{desc}，体现了学习应用能力、团队协作能力和抗压执行能力。",
        "志愿服务": f"参与志愿服务与公益实践工作，协助完成现场服务、沟通引导与任务执行。{desc}，体现了服务意识、沟通能力和社会责任感。",
        "行政助理": f"参与行政支持与事务性工作，负责资料整理、信息录入、文件归档与流程协助。{desc}，体现了较强的细致度、执行力和事务处理能力。",
        "市场运营": f"参与市场运营与用户相关工作，围绕活动推广、用户沟通与内容运营开展实践。{desc}，体现了用户意识、运营思维和沟通执行能力。",
        "教育培训": f"参与教学辅助与培训支持工作，围绕课程准备、学生沟通与学习辅导开展实践。{desc}，体现了表达能力、责任意识和耐心细致的工作态度。",
        "财务会计": f"参与财务或会计相关辅助工作，围绕凭证整理、数据核对、费用统计等任务开展实践。{desc}，体现了严谨细致的工作习惯、数据敏感度和责任意识。",
        "人力资源": f"参与人力资源相关辅助工作，围绕招聘支持、信息整理、沟通协调与流程跟进开展实践。{desc}，体现了良好的沟通能力、组织协调能力和服务意识。"
    }

    return templates.get(exp_type, optimize_general_experience(desc, target_position))


def optimize_general_experience(description, target_position):
    if not description.strip():
        return ""

    desc = clean_text(description)

    if target_position:
        return f"{desc}，该经历与目标岗位“{target_position}”所需的沟通协作、执行落地和问题解决能力具有一定关联。"

    return f"{desc}，在实践过程中提升了沟通协作能力、执行能力和问题解决能力。"


def optimize_self_evaluation(self_evaluation, target_position, skills):
    if self_evaluation.strip():
        return clean_text(self_evaluation)

    skill_text = "、".join(skills) if skills else "相关专业技能"

    if "开发" in target_position or "工程师" in target_position:
        return f"具备良好的学习能力和工程实践意识，掌握{skill_text}，能够结合实际需求完成相关技术任务。"

    if "数据" in target_position or "分析" in target_position:
        return f"具备较好的逻辑分析能力和数据意识，掌握{skill_text}，能够围绕业务问题开展信息整理与分析工作。"

    if "运营" in target_position or "市场" in target_position:
        return f"具备良好的沟通表达能力和用户意识，掌握{skill_text}，能够参与内容运营、活动执行与用户沟通相关工作。"

    if "行政" in target_position or "人事" in target_position or "人力" in target_position:
        return f"具备较强的责任心、细致度和沟通协调能力，掌握{skill_text}，能够胜任事务处理与流程支持相关工作。"

    return f"学习能力较强，具备良好的沟通能力、执行能力和团队协作意识，掌握{skill_text}，能够快速适应目标岗位工作。"


def format_skills(skills):
    if not skills:
        return "暂无"

    return "、".join(skills)


def clean_text(text):
    return text.strip().replace("\n", " ").replace("  ", " ")