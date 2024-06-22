# 文件时间属性修改器

import os
import time
import random
import win32file
import win32con
import pywintypes


class TimeModifier:
    """
    用于修改指定文件或文件夹下所有文件的时间属性（创建时间、最后访问时间和最后修改时间）。
    这个类提供了方法来处理单个文件或递归处理文件夹中的所有文件。
    参数:
        base_time (float): 用作时间生成基准的UNIX时间戳。所有时间计算都基于这个时间。
        x (float): 创建时间允许的随机增加的最大天数，以天为单位。（可以为小数）
        x1 (float): last_write_time 相对于 creation_time 增加的最小天数。（可以为小数）
        x2 (float): last_write_time 相对于 creation_time 增加的最大天数。（可以为小数）
        y1 (float): last_access_time 相对于 last_write_time 增加的最小天数。（可以为小数）
        y2 (float): last_access_time 相对于 last_write_time 增加的最大天数。（可以为小数）
        forbidden_start (int): 每天禁止设置时间的起始小时（24小时制）。
        forbidden_end (int): 每天禁止设置时间的结束小时（24小时制）。
    使用示例:
        # 设置基准时间为 "2024-04-07 10:09:45"
        base_time = time.mktime(time.strptime("2024-04-07 10:09:45", "%Y-%m-%d %H:%M:%S"))
        # 初始化时间修改器
        modifier = TimeModifier(base_time, 5, 3.7, 7.2, 2, 4.8, 22, 10)
        # 修改单个文件的时间属性
        modifier.change_file_timestamp("example_file.txt")
        # 修改文件夹下所有文件的时间属性
        modifier.change_folder_timestamps("example_folder")
    """

    def __init__(self, base_time, x, x1, x2, y1, y2, forbidden_start, forbidden_end):
        self.base_time = base_time
        self.x = x
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.forbidden_start = forbidden_start
        self.forbidden_end = forbidden_end

    def to_pywintypes_time(self, timestamp):
        """
        将时间戳转换为 pywintypes.Time 对象。
        """
        if timestamp is not None:
            return pywintypes.Time(time.localtime(timestamp))
        return None

    def is_time_allowed(self, timestamp):
        """
        检查给定的时间戳是否在允许的时间段内。
        """
        time_struct = time.localtime(timestamp)
        hour = time_struct.tm_hour
        if self.forbidden_start < self.forbidden_end:
            return not (self.forbidden_start <= hour < self.forbidden_end)
        else:
            return not (self.forbidden_start <= hour or hour < self.forbidden_end)

    def change_file_timestamp(self, file_path):
        """
        修改单个文件的时间属性，确保时间不在禁止时间段内。
        """
        creation_time = self.base_time + int(random.uniform(0, self.x * 86400))
        # 确保生成的时间符合条件
        while not self.is_time_allowed(creation_time):
            creation_time = self.base_time + int(random.uniform(0, self.x * 86400))

        seconds_to_add = random.uniform(self.x1 * 86400, self.x2 * 86400)
        last_write_time = creation_time + int(seconds_to_add)
        while not self.is_time_allowed(last_write_time):
            seconds_to_add = random.uniform(self.x1 * 86400, self.x2 * 86400)
            last_write_time = creation_time + int(seconds_to_add)

        seconds_to_add = random.uniform(self.y1 * 86400, self.y2 * 86400)
        last_access_time = last_write_time + int(seconds_to_add)
        while not self.is_time_allowed(last_access_time):
            seconds_to_add = random.uniform(self.y1 * 86400, self.y2 * 86400)
            last_access_time = last_write_time + int(seconds_to_add)

        # 转换时间戳
        creation_time = self.to_pywintypes_time(creation_time)
        last_write_time = self.to_pywintypes_time(last_write_time)
        last_access_time = self.to_pywintypes_time(last_access_time)

        # 打开文件获取句柄
        handle = win32file.CreateFile(
            file_path, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None
        )

        # 设置文件时间
        win32file.SetFileTime(handle, creation_time, last_access_time, last_write_time)

        # 关闭文件句柄
        handle.Close()

    def change_folder_timestamps(self, folder_path):
        """
        修改指定文件夹下所有文件的创建时间、最后访问时间和最后修改时间。
        确保时间不在每天指定的禁止时间段内。
        """
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                self.change_file_timestamp(full_path)