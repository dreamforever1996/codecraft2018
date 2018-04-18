#coding=utf8
from __future__ import division
import parser
import util
import time

InputInfo = 0
'''
case1:
8/8/7
1 flavor3 2 flavor2 3 flavor1 3 flavor6 3 flavor5 9 flavor8 6
2 flavor14 1 flavor8 1 flavor6 2 flavor11 4
3 flavor9 2 flavor14 3
4 flavor9 6 flavor10 1 flavor7 2 flavor1 5 flavor4 3
5 flavor9 1 flavor12 2 flavor10 4
6 flavor13 2 flavor12 3
7 flavor13 1 flavor12 3
8 flavor12 1

case2:
21/20/20
1 flavor3 8 flavor2 17 flavor1 1 flavor5 15
2 flavor3 9 flavor8 3 flavor11 2 flavor5 9
3 flavor3 7 flavor1 1 flavor14 2 flavor11 2
4 flavor14 3 flavor6 4
5 flavor14 3 flavor6 4
6 flavor9 1 flavor14 3 flavor1 2 flavor6 1
7 flavor9 3 flavor14 2 flavor1 12
8 flavor9 6 flavor1 7 flavor4 12
9 flavor9 2 flavor7 3 flavor12 1 flavor4 14
10 flavor15 1 flavor7 10
11 flavor15 1 flavor7 7 flavor10 1
12 flavor15 1 flavor10 5
13 flavor15 1 flavor13 1 flavor10 3
14 flavor15 1 flavor13 2
15 flavor15 1 flavor13 2
16 flavor13 3
17 flavor13 3
18 flavor13 3
19 flavor13 3
20 flavor13 3
21 flavor13 2

case3:
43/42/40
1 flavor3 8 flavor2 48
2 flavor3 8 flavor2 1 flavor1 1 flavor5 23
3 flavor3 8 flavor8 9 flavor5 6
4 flavor3 8 flavor8 8 flavor11 2
5 flavor3 8 flavor11 6
6 flavor3 4 flavor6 2 flavor11 6
7 flavor9 2 flavor11 6
8 flavor9 2 flavor11 6
9 flavor9 2 flavor11 6
10 flavor9 2 flavor11 6
11 flavor9 2 flavor14 1 flavor11 4
12 flavor9 2 flavor14 3
13 flavor9 2 flavor14 3
14 flavor9 2 flavor14 3
15 flavor9 3 flavor14 2 flavor1 7 flavor4 2
16 flavor9 6 flavor7 3 flavor4 9
17 flavor9 6 flavor7 7
18 flavor9 6 flavor10 4
19 flavor9 6 flavor10 4
20 flavor9 5 flavor10 4
21 flavor12 3 flavor10 4
22 flavor12 3 flavor10 4
23 flavor12 3 flavor10 4
24 flavor12 3 flavor10 4
25 flavor15 1 flavor10 5
26 flavor15 1 flavor10 5
27 flavor15 1 flavor10 4
28 flavor15 1 flavor13 2
29 flavor15 1 flavor13 2
30 flavor15 1 flavor13 2
31 flavor15 1 flavor13 2
32 flavor15 1 flavor13 2
33 flavor15 1 flavor13 2
34 flavor15 1 flavor13 2
35 flavor15 1 flavor13 2
36 flavor15 1 flavor13 2
37 flavor15 1 flavor13 2
38 flavor15 1 flavor13 2
39 flavor15 1 flavor13 2
40 flavor15 1 flavor13 2
41 flavor15 1 flavor13 1
42 flavor15 2
43 flavor15 1

case4:
80/ / /77
1 flavor3 8 flavor2 41 flavor1 1 flavor5 3
2 flavor3 7 flavor6 1 flavor5 23
3 flavor8 12 flavor6 4
4 flavor9 1 flavor1 2 flavor6 1 flavor11 6
5 flavor9 2 flavor11 6
6 flavor9 2 flavor11 6
7 flavor9 2 flavor14 2 flavor11 2
8 flavor9 2 flavor14 3
9 flavor9 2 flavor14 3
10 flavor9 2 flavor14 3
11 flavor9 2 flavor14 3
12 flavor9 2 flavor14 3
13 flavor9 2 flavor14 3
14 flavor9 2 flavor14 3
15 flavor9 2 flavor14 3
16 flavor9 2 flavor14 3
17 flavor9 5 flavor14 1 flavor1 5 flavor4 4
18 flavor9 6 flavor4 16
19 flavor9 6 flavor4 16
20 flavor9 6 flavor4 16
21 flavor9 6 flavor7 2 flavor4 11
22 flavor9 6 flavor7 8
23 flavor9 6 flavor7 2 flavor10 3
24 flavor9 6 flavor10 4
25 flavor9 6 flavor10 4
26 flavor9 6 flavor10 4
27 flavor9 6 flavor10 4
28 flavor9 6 flavor10 4
29 flavor9 1 flavor12 2 flavor10 4
30 flavor12 3 flavor10 4
31 flavor12 3 flavor10 4
32 flavor12 3 flavor10 4
33 flavor12 3 flavor10 4
34 flavor12 3 flavor10 4
35 flavor12 3 flavor10 4
36 flavor12 3 flavor10 4
37 flavor12 3 flavor10 4
38 flavor12 3 flavor10 4
39 flavor12 3 flavor10 4
40 flavor12 3 flavor10 4
41 flavor12 3 flavor10 4
42 flavor13 1 flavor12 3 flavor10 1
43 flavor13 2 flavor12 3
44 flavor13 2 flavor12 3
45 flavor13 2 flavor12 3
46 flavor13 2 flavor12 3
47 flavor13 2 flavor12 3
48 flavor13 2 flavor12 3
49 flavor13 2 flavor12 3
50 flavor13 2 flavor12 3
51 flavor13 2 flavor12 3
52 flavor13 2 flavor12 3
53 flavor13 2 flavor12 3
54 flavor13 2 flavor12 3
55 flavor13 2 flavor12 3
56 flavor13 2 flavor12 3
57 flavor13 2 flavor12 3
58 flavor13 2 flavor12 3
59 flavor13 2 flavor12 3
60 flavor13 2 flavor12 3
61 flavor13 2 flavor12 3
62 flavor15 1 flavor13 2 flavor12 1
63 flavor15 1 flavor13 2
64 flavor15 1 flavor13 2
65 flavor13 3
66 flavor13 3
67 flavor13 3
68 flavor13 3
69 flavor13 3
70 flavor13 3
71 flavor13 3
72 flavor13 3
73 flavor13 3
74 flavor13 3
75 flavor13 3
76 flavor13 3
77 flavor13 3
78 flavor13 3
79 flavor13 3
80 flavor13 2

case5:
182/ / /156
1 flavor3 15 flavor2 45
2 flavor3 15 flavor2 45
3 flavor3 15 flavor2 40 flavor1 1 flavor5 2
4 flavor3 15 flavor1 1 flavor5 22
5 flavor3 15 flavor1 1 flavor5 22
6 flavor3 14 flavor8 5 flavor5 13
7 flavor3 6 flavor1 2 flavor8 11 flavor6 4
8 flavor1 2 flavor8 11 flavor6 7
9 flavor1 2 flavor8 11 flavor6 7
10 flavor1 2 flavor8 11 flavor6 7
11 flavor1 2 flavor8 11 flavor6 7
12 flavor1 2 flavor8 11 flavor6 7
13 flavor1 2 flavor8 11 flavor6 7
14 flavor1 2 flavor8 11 flavor6 7
15 flavor1 2 flavor8 11 flavor6 7
16 flavor9 3 flavor8 10 flavor1 4 flavor6 2
17 flavor9 3 flavor8 5 flavor1 4 flavor11 3
18 flavor9 4 flavor1 4 flavor11 5
19 flavor9 4 flavor1 4 flavor11 5
20 flavor9 4 flavor1 4 flavor11 5
21 flavor9 4 flavor1 4 flavor11 5
22 flavor9 4 flavor1 4 flavor11 5
23 flavor9 4 flavor1 4 flavor11 5
24 flavor9 4 flavor1 4 flavor11 5
25 flavor9 4 flavor1 4 flavor11 5
26 flavor9 4 flavor1 4 flavor11 5
27 flavor9 4 flavor1 4 flavor11 5
28 flavor9 4 flavor1 4 flavor11 5
29 flavor9 4 flavor1 4 flavor11 5
30 flavor9 4 flavor1 4 flavor11 5
31 flavor9 4 flavor1 4 flavor11 5
32 flavor9 4 flavor1 4 flavor11 5
33 flavor9 4 flavor1 4 flavor11 5
34 flavor9 4 flavor1 4 flavor11 5
35 flavor9 4 flavor1 4 flavor11 5
36 flavor9 4 flavor1 4 flavor11 5
37 flavor9 4 flavor1 4 flavor11 5
38 flavor9 4 flavor1 4 flavor11 5
39 flavor9 4 flavor1 4 flavor11 5
40 flavor9 4 flavor1 4 flavor11 5
41 flavor9 4 flavor1 4 flavor11 5
42 flavor9 4 flavor1 4 flavor11 5
43 flavor9 2 flavor1 4 flavor12 1 flavor11 5
44 flavor1 4 flavor12 2 flavor11 5
45 flavor1 4 flavor12 2 flavor11 5
46 flavor1 4 flavor12 2 flavor11 5
47 flavor1 4 flavor12 2 flavor11 5
48 flavor1 4 flavor12 2 flavor11 5
49 flavor1 4 flavor12 2 flavor11 5
50 flavor1 4 flavor12 2 flavor11 5
51 flavor1 4 flavor14 1 flavor12 2 flavor11 3
52 flavor1 12 flavor14 2 flavor12 2
53 flavor1 12 flavor14 2 flavor12 2
54 flavor1 10 flavor14 2 flavor12 2 flavor4 1
55 flavor14 2 flavor12 2 flavor4 6
56 flavor12 4 flavor4 8
57 flavor12 4 flavor4 8
58 flavor12 4 flavor4 8
59 flavor12 4 flavor4 8
60 flavor12 4 flavor4 8
61 flavor12 4 flavor4 8
62 flavor12 4 flavor4 8
63 flavor12 4 flavor4 8
64 flavor12 4 flavor4 8
65 flavor12 4 flavor4 8
66 flavor12 4 flavor4 8
67 flavor12 4 flavor4 8
68 flavor12 4 flavor4 8
69 flavor12 4 flavor4 8
70 flavor12 4 flavor4 8
71 flavor12 4 flavor4 8
72 flavor12 4 flavor4 8
73 flavor12 4 flavor4 8
74 flavor12 4 flavor4 8
75 flavor12 4 flavor4 8
76 flavor12 4 flavor4 8
77 flavor7 3 flavor12 4 flavor4 2
78 flavor7 4 flavor12 4
79 flavor7 4 flavor12 4
80 flavor7 4 flavor12 4
81 flavor7 4 flavor12 4
82 flavor7 4 flavor12 4
83 flavor7 4 flavor12 4
84 flavor7 4 flavor12 4
85 flavor7 4 flavor12 4
86 flavor7 4 flavor12 4
87 flavor7 4 flavor12 4
88 flavor7 4 flavor12 4
89 flavor7 4 flavor12 4
90 flavor7 4 flavor12 4
91 flavor7 4 flavor12 4
92 flavor7 4 flavor12 4
93 flavor7 4 flavor12 4
94 flavor7 4 flavor12 4
95 flavor7 4 flavor12 4
96 flavor15 2 flavor7 4
97 flavor15 2 flavor7 4
98 flavor15 2 flavor7 4
99 flavor15 2 flavor7 4
100 flavor15 2 flavor7 4
101 flavor15 2 flavor7 4
102 flavor15 2 flavor7 4
103 flavor15 2 flavor7 4
104 flavor15 2 flavor7 4
105 flavor15 2 flavor7 4
106 flavor15 2 flavor7 4
107 flavor15 2 flavor7 4
108 flavor15 2 flavor7 4
109 flavor15 2 flavor7 4
110 flavor15 2 flavor7 4
111 flavor15 2 flavor7 4
112 flavor15 2 flavor7 4
113 flavor15 2 flavor7 4
114 flavor15 2 flavor7 4
115 flavor15 2 flavor7 4
116 flavor15 2 flavor7 3 flavor10 1
117 flavor15 2 flavor10 2
118 flavor15 2 flavor10 1
119 flavor15 2 flavor13 1
120 flavor15 2 flavor13 1
121 flavor15 2 flavor13 1
122 flavor15 2 flavor13 1
123 flavor15 2 flavor13 1
124 flavor15 2 flavor13 1
125 flavor15 2 flavor13 1
126 flavor15 2 flavor13 1
127 flavor15 2 flavor13 1
128 flavor15 2 flavor13 1
129 flavor15 2 flavor13 1
130 flavor15 2 flavor13 1
131 flavor15 2 flavor13 1
132 flavor15 2 flavor13 1
133 flavor15 2 flavor13 1
134 flavor15 2 flavor13 1
135 flavor15 2 flavor13 1
136 flavor15 2 flavor13 1
137 flavor15 2 flavor13 1
138 flavor15 2 flavor13 1
139 flavor15 1 flavor13 2
140 flavor13 3
141 flavor13 3
142 flavor13 3
143 flavor13 3
144 flavor13 3
145 flavor13 3
146 flavor13 3
147 flavor13 3
148 flavor13 3
149 flavor13 3
150 flavor13 3
151 flavor13 3
152 flavor13 3
153 flavor13 3
154 flavor13 3
155 flavor13 3
156 flavor13 3
157 flavor13 3
158 flavor13 3
159 flavor13 3
160 flavor13 3
161 flavor13 3
162 flavor13 3
163 flavor13 3
164 flavor13 3
165 flavor13 3
166 flavor13 3
167 flavor13 3
168 flavor13 3
169 flavor13 3
170 flavor13 3
171 flavor13 3
172 flavor13 3
173 flavor13 3
174 flavor13 3
175 flavor13 3
176 flavor13 3
177 flavor13 3
178 flavor13 3
179 flavor13 3
180 flavor13 3
181 flavor13 3
182 flavor13 1

case6:
113/ / /124
1 flavor3 15 flavor1 1 flavor5 22
2 flavor3 17 flavor1 1 flavor11 5
3 flavor3 17 flavor1 1 flavor11 5
4 flavor3 17 flavor1 1 flavor11 5
5 flavor3 17 flavor1 1 flavor11 5
6 flavor3 17 flavor1 1 flavor11 5
7 flavor3 17 flavor1 1 flavor11 5
8 flavor3 4 flavor9 3 flavor1 4 flavor11 5
9 flavor9 4 flavor1 4 flavor11 5
10 flavor9 7 flavor1 20 flavor11 1
11 flavor7 5 flavor9 3 flavor1 9 flavor15 1
12 flavor15 2 flavor7 4
13 flavor15 2 flavor7 4
14 flavor15 2 flavor7 4
15 flavor15 2 flavor7 4
16 flavor15 2 flavor7 4
17 flavor15 2 flavor7 4
18 flavor15 2 flavor7 4
19 flavor15 2 flavor7 4
20 flavor15 2 flavor7 4
21 flavor15 2 flavor7 4
22 flavor15 2 flavor7 4
23 flavor15 2 flavor7 4
24 flavor15 2 flavor7 4
25 flavor15 2 flavor7 4
26 flavor15 2 flavor7 4
27 flavor15 2 flavor7 4
28 flavor15 2 flavor7 4
29 flavor15 2 flavor7 4
30 flavor15 2 flavor7 4
31 flavor15 2 flavor7 4
32 flavor15 2 flavor7 4
33 flavor15 2 flavor7 4
34 flavor15 2 flavor7 4
35 flavor15 2 flavor7 4
36 flavor15 2 flavor7 4
37 flavor15 2 flavor7 4
38 flavor15 2 flavor7 4
39 flavor15 2 flavor7 4
40 flavor15 2 flavor7 4
41 flavor15 2 flavor7 4
42 flavor15 2 flavor7 4
43 flavor15 2 flavor7 4
44 flavor15 2 flavor7 4
45 flavor15 2 flavor7 4
46 flavor15 2 flavor7 4
47 flavor15 2 flavor7 4
48 flavor15 2 flavor7 4
49 flavor15 2 flavor7 4
50 flavor15 2 flavor7 4
51 flavor15 2 flavor7 4
52 flavor15 2 flavor7 4
53 flavor15 2 flavor7 4
54 flavor15 2 flavor7 4
55 flavor15 2 flavor7 4
56 flavor15 2 flavor7 4
57 flavor15 2 flavor7 2
58 flavor15 2 flavor13 1
59 flavor15 2 flavor13 1
60 flavor15 2 flavor13 1
61 flavor15 2 flavor13 1
62 flavor15 2 flavor13 1
63 flavor15 2 flavor13 1
64 flavor15 2 flavor13 1
65 flavor15 2 flavor13 1
66 flavor15 2 flavor13 1
67 flavor15 2 flavor13 1
68 flavor15 2 flavor13 1
69 flavor15 2 flavor13 1
70 flavor15 2 flavor13 1
71 flavor15 2 flavor13 1
72 flavor15 2 flavor13 1
73 flavor15 2 flavor13 1
74 flavor15 2 flavor13 1
75 flavor15 2 flavor13 1
76 flavor15 2 flavor13 1
77 flavor15 2 flavor13 1
78 flavor15 2 flavor13 1
79 flavor15 2 flavor13 1
80 flavor15 2 flavor13 1
81 flavor15 2 flavor13 1
82 flavor15 2 flavor13 1
83 flavor15 2 flavor13 1
84 flavor15 2 flavor13 1
85 flavor15 2 flavor13 1
86 flavor15 2 flavor13 1
87 flavor15 2 flavor13 1
88 flavor15 2 flavor13 1
89 flavor15 2 flavor13 1
90 flavor15 2 flavor13 1
91 flavor15 2 flavor13 1
92 flavor15 2 flavor13 1
93 flavor15 2 flavor13 1
94 flavor15 2 flavor13 1
95 flavor15 2 flavor13 1
96 flavor15 2 flavor13 1
97 flavor15 2 flavor13 1
98 flavor15 2 flavor13 1
99 flavor15 2 flavor13 1
100 flavor15 2 flavor13 1
101 flavor15 2 flavor13 1
102 flavor15 2 flavor13 1
103 flavor15 2 flavor13 1
104 flavor15 2 flavor13 1
105 flavor15 2 flavor13 1
106 flavor15 2 flavor13 1
107 flavor15 2 flavor13 1
108 flavor13 3
109 flavor13 3
110 flavor13 3
111 flavor13 3
112 flavor13 3
113 flavor13 2
'''
def predict_vm():
    flavors = []
    flavors.append(('flavor1',1,1))
    flavors.append(('flavor2',1,2))
    flavors.append(('flavor3',1,4))
    flavors.append(('flavor4',2,2))
    flavors.append(('flavor5',2,4))
    flavors.append(('flavor6',2,8))
    flavors.append(('flavor7',4,4))
    flavors.append(('flavor8',4,8))
    flavors.append(('flavor9',4,16))
    flavors.append(('flavor10',8,8))
    flavors.append(('flavor11',8,16))
    flavors.append(('flavor12',8,32))
    flavors.append(('flavor13',16,16))
    flavors.append(('flavor14',16,32))
    flavors.append(('flavor15',16,64))
    predict_flavors = []
    flavor_names = []

    f = open('./deploy_test_cases/case1.txt')
    counter = 0
    for line in f:
        if counter == 0:
            a = line.split(' ')
            ps_cpu_num = int(a[0])
            ps_mem_num = int(a[1])
        if counter == 2:
            target = line.split('\r\n')[0]
        if counter == 4:
            flavor_num = int(line)
        if counter > 5:
            a = line.split(':')
            flavor_name = a[0]
            flavor_names.append(a[0])
            flavor_num = int(a[1])
            predict_flavors.append((flavor_name, flavor_num))
        counter += 1
    f.close()

    num_vs = 0
    for pf in predict_flavors:
        fname, fnum = pf
        num_vs += fnum
    print num_vs

    pServers = []
    if num_vs >= 600:
        pServers, _ = util.ratio_distribute(predict_flavors, ps_cpu_num, ps_mem_num, target, flavor_names, flavors)
    else:
        pServers = util.dp_distribute(predict_flavors, ps_cpu_num, ps_mem_num, target, flavor_names, flavors)
    # 5. Record the result
    print "recording the result"
    result = []

    result.append(len(pServers))
    ratio_array = []
    for i in range(len(pServers)):
        ratio = 0
        total_cpu = 0
        total_mem = 0
        s = ""
        for f, n in pServers[i].items():
            tmp = "%s %d "%(f, n)
            #print i+1, tmp,
            vs_cpu_num = 0
            vs_mem_num = 0
            for each in flavors:
                if each[0] == f:
                    vs_cpu_num = each[1]
                    vs_mem_num = each[2]
                    #print vs_cpu_num, vs_mem_num,
                    break
            total_cpu = total_cpu + n * vs_cpu_num
            total_mem = total_mem + n * vs_mem_num
            #print total_cpu, total_mem
            s = s + tmp
        #print "aaaa",total_cpu, ps_cpu_num
        ratio1 = total_cpu/ps_cpu_num
        ratio2 = total_mem/ps_mem_num
        ratio = 0
        if target == "CPU":
            ratio_array.append(ratio1)
            ratio = ratio1
        elif target == "MEM":
            ratio_array.append(ratio2)
            ratio = ratio2
        #s = "%d %s %f %f %d"%(i+1, s, ratio1, ratio2, ps_mem_num-total_mem)
        s = "%d %s %f %f"%(i+1, s, ratio1, ratio2)
        result.append(s)
    counter = 0
    for each in ratio_array:
        if each > 0.55:
            counter = counter + 1
    if (counter == len(pServers)  and target=="MEM" ) or target=="CPU":
        #while(1):
        #    print "Best boom!!"
        print 'hh'
    for each in result:
        print each

    return result


if __name__ == '__main__':
    t1 = time.time()
    predict_vm()
    t2 = time.time()

    print "time: %s seconds"%(t2-t1)





