import random
import collections
import time
import sys
start = time.time()
SERVER = True
TIME = False
# while True:
#     line = sy
# A = 3
# B = 0.33
host_dict = {}
# com_host_dict = {}  # 计算密集型服务器
# mid1_host_dict = {}  # 均衡服务器
# mid2_host_dict = {}
# io_host_dict = {}  # I/O密集型服务器
vm_dict = {}
if not SERVER:
    PATH = 'E:\HW_JYTZS\\training-data/training-1.txt'
    with open(PATH) as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    host_num = int(lines[0])
    for i in range(1, host_num+1):
        line = lines[i]
        temp = line.split(',')
        host_name = temp[0][1:]
        val = [int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4][:-1]),
               int(temp[3]), int(temp[4][:-1])]
        # ----------------------------- 分离 计算密集型服务器 和 I/O密集型服务器
        # if val[0] >= A * val[1]:
        #     com_host_dict[host_name] = val  # 是计算密集型服务器3 0.33
        # if A * val[1] > val[0] >=  val[1]:
        #     mid1_host_dict[host_name] = val  # 是均衡密集型服务器
        # if val[1] > val[0] >= B * val[1]:
        #     mid2_host_dict[host_name] = val  # 是均衡密集型服务器
        # if B * val[1] > val[0] :
        #     io_host_dict[host_name] = val  # 是I/O密集型服务器
        # -----------------------------
        host_dict[host_name] = val
    vm_num = int(lines[host_num+1])
    for i in range(host_num+2,host_num+2+vm_num):
        line = lines[i]
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]),int(temp[3][:-1])]
        vm_dict[vm_name] = val
    day_num = int(lines[host_num+2+vm_num])

    data_index = host_num+2+vm_num+1
    data = []

    for i in range(day_num):
        data_i = []
        data_num = int(lines[data_index])
        for item in lines[data_index+1:data_index+1+data_num]:
            data_i.append(item)
        data.append(data_i)
        data_index = data_index+data_num+1

else:
    host_num = sys.stdin.readline().strip()
    host_num = int(host_num)
    # host_num = int(lines[0])
    for i in range(host_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        host_name = temp[0][1:]
        val = [int(temp[1]),int(temp[2]),int(temp[3]),int(temp[4][:-1]),
               int(temp[3]), int(temp[4][:-1])]
        # ----------------------------- 分离 计算密集型服务器 和 I/O密集型服务器
        # if val[0] >= A * val[1]:
        #     com_host_dict[host_name] = val  # 是计算密集型服务器
        # if A * val[1] > val[0] >= val[1]:
        #     mid1_host_dict[host_name] = val  # 是均衡密集型服务器
        # if val[1] > val[0] >= B * val[1]:
        #     mid2_host_dict[host_name] = val  # 是均衡密集型服务器
        # if B * val[1] > val[0] :
        #     io_host_dict[host_name] = val  # 是I/O密集型服务器
        # -----------------------------
        host_dict[host_name] = val

    vm_num = sys.stdin.readline().strip()
    vm_num = int(vm_num)
    for i in range(vm_num):
        line = sys.stdin.readline().strip()
        temp = line.split(',')
        vm_name = temp[0][1:]
        val = [int(temp[1]), int(temp[2]), int(temp[3][:-1])]
        vm_dict[vm_name] = val
    day_num = sys.stdin.readline().strip()
    day_num = int(day_num)

    # data_index = host_num+2+vm_num+1
    data = []

    for i in range(day_num):
        requirement = sys.stdin.readline().strip()
        requirement = int(requirement)
        data_i = []
        for i in range(requirement):
            line = sys.stdin.readline().strip()
            data_i.append(line)
        data.append(data_i)



host_dict_keys_list = list(host_dict.keys())
HOST_DICT_LEN = len(host_dict_keys_list)




class Host:
    def __init__(self, name):
        self.name = name
        self.A_cpu = host_dict[name][0]/2
        self.B_cpu = host_dict[name][0]/2
        self.A_mem = host_dict[name][1]/2
        self.B_mem = host_dict[name][1]/2

        self.AA_cpu = host_dict[name][0] / 2
        self.AA_mem = host_dict[name][1] / 2
    def putvm(self,vm):
        info = vm_dict[vm]
        cpu,mem,core = info
        if core == 0:
            if self.A_cpu >=cpu and self.A_mem>=mem: #优先放A节点
                self.A_cpu -= cpu
                self.A_mem -= mem
                return 'A'
            elif self.B_cpu>=cpu and self.B_mem>=mem:
                self.B_cpu -= cpu
                self.B_mem -= mem
                return 'B'
            else:
                return 'NULL'
        else:
            if self.A_cpu>=cpu/2 and self.A_mem>=mem/2 and self.B_cpu>=cpu/2 and self.B_mem>=mem/2:
                self.A_cpu -= cpu/2
                self.B_cpu -= cpu/2
                self.A_mem -= mem/2
                self.B_mem -= mem/2
                return 'ALL'
            else:
                return 'NULL'

    def available(self,vm):
        info = vm_dict[vm]
        cpu,mem,core = info
        if core == 0:
            if self.A_cpu >=cpu and self.A_mem>=mem: #优先放A节点
                return True
            elif self.B_cpu>=cpu and self.B_mem>=mem:
                return True
            else:
                return False
        else:
            if self.A_cpu>=cpu/2 and self.A_mem>=mem/2 and self.B_cpu>=cpu/2 and self.B_mem>=mem/2:
                return True
            else:
                return False

    def delvm(self,vm,type):
        info = vm_dict[vm]
        cpu, mem, core = info
        if type == 'A':
            self.A_cpu += cpu
            self.A_mem += mem
        elif type == 'B':
            self.B_cpu += cpu
            self.B_mem += mem
        else:
            self.A_cpu += cpu/2
            self.A_mem += mem/2
            self.B_cpu += cpu/2
            self.B_mem += mem/2

class hostList:

    def __init__(self):
        self.allHost = []
        self.id_info = {}
        self.out = []
        self.host0id = [0]
        self.host1id = [1]
        self.hostIDlist = 1

    def addHost(self,vm_name,host_keys1):  # 添加I/O密集型服务器

        host_keys2 = host_keys1[:int(1)]
        host_keysm = host_keys1[int(1):int(6)]
        random.shuffle(host_keysm)
        host_keys3 = host_keys1[int(6):]
        host_keys2.extend(host_keysm)
        host_keys2.extend(host_keys3)

        for i in range(len(host_keys2)):
            host = Host(host_keys2[i][0])
            if host.available(vm_name):
                break
        self.allHost.append(host)

    def search_and_add(self, dayvm, host_keys):  # 添加虚拟机策略
        INDEX = {}
        # ---------------------------- 给虚拟机有大到小排序
        def takeSecond(elem):
            return elem[1]
        dayvm.sort(key=takeSecond)
        dayvm.reverse()
        # ----------------------------
        if len(self.allHost) == 0:
            self.addHost(dayvm[0][0], host_keys)

        dayvm1 = dayvm[:]
        # -------------------------------
        # 给所有的服务器由小到大排序
        allh = []
        allhh = {}
        for i in range(len(self.allHost)):
            vv = self.allHost[i].A_cpu + self.allHost[i].A_mem + self.allHost[i].B_cpu + self.allHost[i].B_mem
            allh.append([i, vv])
            allhh[i] = vv
        allh.sort(key=takeSecond)
        hostlist = [n[0] for n in allh]

        tmp = -1
        for a in range(len(dayvm)):
            tmp = tmp + 1
            cpu, mem, core = vm_dict[dayvm[a][0]]
            # for i in range(len(self.allHost)):
            for i in hostlist:
                if cpu + mem <= allhh[i]:
                    res = self.allHost[i].putvm(dayvm[a][0])
                    if res != 'NULL':
                        INDEX[dayvm[a][2]] = [i, res, dayvm[a][2], dayvm[a][0]]
                        del dayvm1[tmp]
                        tmp = tmp - 1
                        break

        while len(dayvm1) != 0:

            dayvm2 = dayvm1[:]
            self.addHost(dayvm2[0][0], host_keys)
            tmp = -1
            for a in range(len(dayvm1)):
                tmp = tmp + 1
                res = self.allHost[len(self.allHost)-1].putvm(dayvm1[a][0])
                if res != 'NULL':
                    INDEX[dayvm1[a][2]] = [len(self.allHost)-1, res, dayvm1[a][2], dayvm1[a][0]]
                    del dayvm2[tmp]
                    tmp = tmp - 1

            dayvm1 = dayvm2[:]
        return INDEX








    def upate_out(self,i,AorB,vm_id,vm_name):
        if AorB == 'A':
            self.out.append([i,'A'])
            self.id_info[vm_id] = [vm_name, i, 'A']
        elif AorB == 'B':
            self.out.append([i, 'B'])
            self.id_info[vm_id] = [vm_name, i, 'B']
        else:
            self.out.append([i])
            self.id_info[vm_id] = [vm_name, i, 'ALL']

    def del_vm(self, id):
        vm_name,host_id,type = self.id_info[id]
        self.allHost[host_id].delvm(vm_name, type)

    def Price(self): # 计算服务器性价比
        def takeSecond(elem):
            return elem[1]

        host_keys = []

        for key in host_dict_keys_list:
            # host_keys.append([key, host_dict[key][4] + dday_num * host_dict[key][5]])
            host_keys.append([key, host_dict[key][4]])
        host_keys.sort(key=takeSecond)
        return host_keys
    def oout(self, VMID, INDEX):
        for vmid in VMID:
            self.upate_out(INDEX[vmid][0], INDEX[vmid][1], INDEX[vmid][2], INDEX[vmid][3])

def main():
    my_hostList = hostList()
    out = []
    index = 0
    index_id = {}
    ITER = 0
    # dday_num = 3000 + 1
    host_keys = my_hostList.Price()  #将虚拟机进行排序
    for day in data:
        # dday_num = dday_num - 1 # 服务器可用天数
        # host_keys = my_hostList.Price(dday_num)
        VMID = []
        dayvm = []
        for line in day:
            add_or_del = line.split(',')[0][1:]
            ID = int(line.split(',')[-1][:-1])
            if add_or_del == 'add':
                vm_name = line.split(',')[1].strip()
                VMID.append(ID)
                dayvm.append([vm_name,(vm_dict[vm_name][0] + vm_dict[vm_name][1]), ID])
        INDEX = my_hostList.search_and_add(dayvm, host_keys) # 添加虚拟机
        my_hostList.oout(VMID, INDEX)  # 按照初始虚拟机顺序输出
        for line in day:
            add_or_del = line.split(',')[0][1:]
            ID = int(line.split(',')[-1][:-1])
            if add_or_del == 'del':
                my_hostList.del_vm(ID)
        start_id = index
        temp = index
        index = len(my_hostList.allHost)
        name_indies = collections.OrderedDict()
        for idx,item in zip(range(temp,index),my_hostList.allHost[temp:index]):
            if item.name not in name_indies.keys():
                name_indies[item.name] = [idx]
            else:
                name_indies[item.name].append(idx)

        out.append('(purchase,'+' '+str(len(name_indies.keys()))+')')
        for k,v in name_indies.items():
            out.append('('+str(k)+','+' '+str(len(v))+')')

        out.append('(migration, 0)')

        for k,v in name_indies.items():
            for item in v:
                index_id[item] = start_id
                start_id += 1
        operate = my_hostList.out
        new_operate = []
        for line in operate:
            idx = line[0]
            new_index = index_id[idx]
            if len(line) == 1:
                new_operate.append('('+str(new_index)+')')
            else:
                new_operate.append('('+str(new_index)+','+' '+line[1]+')')

        out += new_operate
        my_hostList.out.clear()
        ITER +=1
        if TIME:
            if ITER % 100 == 0:
                print('over')
        # if a%100 == 0:
        #     print('over')

    # with open('result.txt','w')as f:
    #     f.write('\n'.join(out))
    end = time.time()

    sys.stdout.write('\n'.join(out))  # 借
    sys.stdout.flush()
    if TIME:
        print('time consume',end-start)

if __name__ == "__main__":
    main()
