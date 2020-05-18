from django.db import models

# Create your models here.


# 用户表
class User(models.Model):
    phone_id = models.CharField(max_length=11, primary_key=True)  #账号换为手机号
    user_password = models.CharField(max_length=15)
    user_level = models.IntegerField(default=4)


# 用户信息表
class UserInfo(models.Model):
    user_id = models.CharField(max_length=15, primary_key=True)
    user_name = models.CharField(max_length=45)
    user_sex = models.CharField(max_length=15)
    user_specialty = models.CharField(max_length=45, null=True)
    # user_phone = models.CharField(max_length=11, null=True)   #
    user_college = models.CharField(max_length=45, null=True)
    user_qq = models.CharField(max_length=12, null=True)
    user_organization = models.CharField(max_length=45, null=True)
    user_hobby = models.CharField(max_length=45, null=True)
    user_autograph = models.CharField(max_length=125, null=True)
    user_instructor = models.CharField(max_length=45, null=True)
    user_picture = models.CharField(max_length=300, null=True)  # 用户头像，存放头像路径
    state = models.IntegerField(default=0)            # 是否安排进排班表，‘1’为安排进排班,‘0’为不参与排班，在下一次排班中将进入排班
    user_phone = models.OneToOneField("User", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey("Department", on_delete="CASCADE", null=True)

    @property
    def __str__(self):
        return self.user_name  # 调用对象时输出名字，方便展示


# 部门表
class Department(models.Model):
    de_name = models.CharField(max_length=45)
    de_college = models.CharField(max_length=45, null=True)
    de_info = models.CharField(max_length=300, null=True)
    de_instructor = models.CharField(max_length=45, null=True)
    de_picture = models.CharField(max_length=300, default='')
    de_address = models.CharField(max_length=45, null=True)

    @property
    def __str__(self):
        return self.de_name  # 调用对象时输出名字，方便展示


# 空闲时间表表项
class FreeTimeTableInfo(models.Model):
    table_name = models.CharField(max_length=155)  # 空闲时间表名
    state = models.IntegerField(default=0)  # 填报状态，‘0’为未开放，‘1’为已开放
    start_time = models.DateTimeField(null=True)  # 开始填报时间
    end_time = models.DateTimeField(null=True)   # 截至填报时间


# 学生空闲时间表,单个学生的空闲信息“11”：星期一第一讲 ----“56”：星期五第六讲
class StudentFreeTime(models.Model):
    free_time = models.CharField(max_length=45, null=True)  # 存放空闲时间编码，从周一第一讲到周五第五讲组成字符串编码，‘1’为空闲,'0'为有课，‘a’为优先
    state = models.IntegerField(null=True)  # 空闲字段
    student = models.ForeignKey("UserInfo", on_delete="CASCADE")
    table_info = models.ForeignKey("FreeTimeTableInfo", on_delete=models.CASCADE, null=True)

    @property
    def __str__(self):
        return self.student  # 调用对象时输出名字，方便展示


# 值班批次表
class DutyBatch(models.Model):
    name = models.CharField(max_length=45)
    start_time = models.DateTimeField()   # 开始日期
    end_time = models.DateTimeField(null=True)     # 截至日期
    state = models.IntegerField()
    admin = models.ForeignKey("UserInfo", on_delete="CASCADE")

    @property
    def __str__(self):
        return self.name  # 调用对象时输出名字，方便展示


# 班次表
class Shifts(models.Model):
    start_time = models.CharField(max_length=25)      # 开始与第几讲
    end_time = models.CharField(max_length=25)        # 结束与第几讲
    address = models.CharField(max_length=45)
    num_people = models.IntegerField()
    duty_batch = models.ForeignKey("DutyBatch", on_delete="CASCADE")

    @property
    def __str__(self):
        return self.duty_batch  # 调用对象时输出名字，方便展示


# 排班表,班次根据班次要求和学生空闲时间进行排班，生成排班表
class ShiftsStudent(models.Model):
    student = models.ForeignKey("UserInfo", on_delete="CASCADE")
    shifts = models.ForeignKey("Shifts", on_delete="CASCADE")


# 签到表
class SignDuty(models.Model):
    sign_in_time = models.DateTimeField()
    sign_off_time = models.DateTimeField()
    late = models.TimeField()  # 迟到时间
    sign_state = models.IntegerField(default=0)  # ‘0’：未开始 ‘1’：未签到  ‘2’：正在值班，显示值班时长  ‘3’：已结束
    evaluate = models.IntegerField()        # 值班结束后根据评价参数（迟到时间）进行 评价，‘1’：优  ‘2’：良  ‘3’：差
    shifts_student = models.ForeignKey("ShiftsStudent", on_delete="CASCADE")


# 岗位批次表
class StationBatch(models.Model):
    name = models.CharField(max_length=45)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField
    content = models.TextField(null=True)  # 批次描述
    limit_num = models.IntegerField(default=2)  # 每人最多可以申请几个岗位，默认为2
    page_views = models.IntegerField()
    state = models.IntegerField()  # 批次招募状态（申请人数）

    @property
    def __str__(self):
        return self.name


# 岗位表
class Station(models.Model):
    name = models.CharField(max_length=45)
    duty = models.TextField()  # 岗位职责或要求
    num_recruit = models.IntegerField()
    department = models.ForeignKey("Department", on_delete="CASCADE")
    station_batch = models.ForeignKey("StationBatch", on_delete="CASCADE")

    @property
    def __str__(self):
        return self.name


#  申请表，学生与岗位是多对多关系，这是中间表
class Apply(models.Model):
    student = models.ForeignKey("UserInfo", on_delete="CASCADE")
    station = models.ForeignKey("Station", on_delete="CASCADE")


# 申请信息表
class ApplyInfo(models.Model):
    birthday = models.DateField()
    image = models.CharField(max_length=300)  # 学生照片，存放头像路径
    political_status = models.CharField(max_length=45)
    sc_address = models.CharField(max_length=120)  # 校内住址
    ho_address = models.CharField(max_length=120)  # 家庭住址
    wechat = models.CharField(max_length=30)
    postal_code = models.IntegerField()  # 邮政编码
    bank_card = models.BigIntegerField()
    degree_of_difficulty = models.IntegerField() # 贫困等级  ‘1’：特别困难  ‘2’：困难  ‘3’：一般困难
    transfer = models.IntegerField(default=1)  # 是否服从调剂岗位   ‘1’：是  ‘0’：否
    go_other = models.IntegerField(default=0)  # 是否愿意去学校其他部门   ‘1’：是 则填写部门名称到other_department字段 ‘0’：否
    other_department = models.CharField(max_length=45, null=True)
    fail_exam = models.IntegerField(default=0)  # 是否挂科   ‘0’：否   ，否则填写挂科数目
    performance = models.TextField()    # 在校表现
    apply_reason = models.TextField()   # 申请理由
    lesson_code = models.CharField(max_length=45)    # 存放有课编码，从周一第一讲到周五第五讲组成字符串编码，‘1’为有课,'0'为无课
    student = models.OneToOneField("UserInfo", on_delete="CASCADE")


# 绩效批次表
class AchievementsBatch(models.Model):
    name = models.CharField(max_length=45)
    check = models.IntegerField(null=True)  # 考核标准，
    wage = models.FloatField()  # 时薪
    overtime_wage = models.FloatField()  # 加班时薪
    start_time = models.DateField()  # 开始计算的日期
    end_time = models.DateField()  # 截至计算的日期
    compute_method = models.IntegerField(default=1)  # 计算方法，‘1’：按排班计算   ‘0’：按签到计算
    ach_state = models.IntegerField()  # 状态：‘0’：未提交审核  ‘1’：已提交审核，未审核  ‘2’：已通过  ‘3’：已审核未通过，可重新提交
    remark = models.CharField(max_length=300)  # 备注
    admin = models.ForeignKey("UserInfo", on_delete="CASCADE")


# 绩效表
class Achievements(models.Model):
    duty_hour = models.FloatField()  # 工时
    overtime_hour = models.FloatField()  # 加班工时
    money = models.FloatField()   # 薪酬
    check = models.IntegerField(default=1)  # 考核：‘1’：优  ‘2’：良  ‘3’：差
    achievementsbatch = models.ForeignKey("AchievementsBatch", on_delete="CASCADE")


# 资源表
class Resource(models.Model):
    re_type = models.CharField(max_length=15)
    theme = models.CharField(max_length=45)
    re_file = models.CharField(max_length=300)
    re_content = models.TextField()
    upload_time = models.DateTimeField()
    num_download = models.IntegerField()
    remark = models.CharField(max_length=255)
    admin = models.ForeignKey("UserInfo", on_delete="CASCADE")

    @property
    def __str__(self):
        return self.theme


# 公告表
class Bulletin(models.Model):
    name = models.CharField(max_length=45)
    bu_file = models.CharField(max_length=300)
    bu_content = models.TextField()
    release_time = models.DateTimeField()
    num_views = models.IntegerField()
    remark = models.CharField(max_length=255)
    admin = models.ForeignKey("UserInfo", on_delete="CASCADE")

    @property
    def __str__(self):
        return self.name
