# Author:   coneypo
# Created:  08.31

import datetime

# 开始时间
start_time = datetime.datetime.now()
print(start_time)
tmp = 0
# 记录的秒数
sec_cnt = 0

while 1:
    current_time = datetime.datetime.now()

    # second 是以60为周期
    # 将开始时间的秒 second / 当前时间的秒 second 进行对比；
    # 如果发生变化则 sec_cnt+=1；
    if current_time.second >= start_time.second:
        if tmp != current_time.second - start_time.second:
            # print("<no 60>+  ", tmp)
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)
            # 以 10s 为周期
            if sec_cnt % 10 == 0:
                # do something
                pass
        tmp = current_time.second - start_time.second

    # when get 60
    else:
        if tmp != current_time.second + 60 - start_time.second:
            sec_cnt += 1
            print("Time_cnt:", sec_cnt)

            # 比如以 10s 为周期
            if sec_cnt % 10 == 0:
                # do something
                pass
        tmp = current_time.second + 60 - start_time.second