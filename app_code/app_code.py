# 特点：做成MP4 和gif

import numpy as np
import matplotlib.pyplot as plt
import json

import time


def Subfun_Theta_Phi(pa, pb):
    a0 = ((pb - pa) / np.linalg.norm(pb - pa)).flatten()
    a_x = np.array([1, 0, 0])
    a_xy = np.array([a0[0], a0[1], 0])  # o-xy plane
    a_xy = (a_xy / np.linalg.norm(a_xy))
    if a0[1] >= 0:
        theta = np.arccos(a_x.dot(a_xy))
    else:
        theta = - np.arccos(a_x.dot(a_xy))
    if a0[2] >= 0:
        phi = np.arccos(a_xy.dot(a0))
    else:
        phi = - np.arccos(a_xy.dot(a0))
    return list((theta, phi))


class Target():
    """
    Target, including posture(pos), velocity(vel), posture(posture),
    motion(motion_model), acceleratiion(acc),Radar Cross section(RCS),
    appearing_time(time)
    """

    def __init__(self, num, pos, vel, posture, motion_model, acc, t0, MovementMode, parament, DuringTime, attribute):
        '''
        'pos',p_s0,...              % 位置矢量
        'vel',v_s0,...              % 速度矢量
        'posture',[0;0;0],...       % 姿态矢量
        'motion_model',motion,...   % 运动模型
        'acc',a_s0,...         % 加速度值或加速度标准差 (m/s^2)
        'RCS',10^(10/10),...        % RCS值,默认值
        'time',t0 ...        % 目标出现时刻，对应最小可检测信噪比
        '''
        self.num = num
        self.pos = pos
        self.vel = vel
        self.posture = posture
        self.motion_model = motion_model
        self.acc = acc
        # self.RCS = RCS
        self.t0 = t0
        self.MovementMode = MovementMode
        self.parament = parament
        self.DuringTime = DuringTime
        self.attribute = attribute


class Radar():
    """ 
    Radar, a object concluding radar's posture velocity and acceleration.
    All three are three-dimensional x,y,z variables as np.array([x, y, z])
    """

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel


class Platform():
    def __init__(self, time_t, fs, SNRO, res_r, res_v, theta_width, phi_width):
        """
        / 雷达系统参数 /
        'time_t': t , int  , 总时间（s)
        'fs',fs,...               数据率 (Hz)
        'min_SNR',SNR0,...               最小可检测SNR
        'res_r',res_r,...            距离分辨率 (m)
        'res_v',res_v,...              速度分辨率 (m)
        'theta_width',theta_width,...  方位波束宽度 (rad)
        'phi_width',phi_width ...    俯仰波束宽度 (rad)
        'pos'         位置矢量 = [pos_x;pos_y;pos_z]
        'vel'         速度矢量  = [vel_x;vel_y;vel_z]
        """
        self.time_t = time_t  # 实际上用的是t
        self.fs = fs
        self.t = np.linspace(0, time_t, time_t * fs)
        N = len(self.t)
        self.m = 0
        self.SNRO = SNRO
        self.rate_r = res_r
        self.res_v = res_v
        self.theta_width = theta_width
        self.phi_width = phi_width

        self.data_SNR = np.zeros((N, 1))
        self.data_range_r = np.zeros((N, 1))
        self.data_theta = np.zeros((N, 1))
        self.data_phi = np.zeros((N, 1))
        self.data_vel = np.zeros((N, 1))
        self.data_p_s = np.zeros((N, 3))
        self.data_v_s = np.zeros((N, 3))

        self.data_measure_cartesian_x = []
        self.data_measure_cartesian_y = []
        self.data_measure_cartesian_z = []
        self.p_sx = []
        self.p_sy = []
        self.p_sz = []

        # def run_1(self,Target,Radar):
        """
        run_1 : A research method of one radar and one targets

        Parameters
        Target : Moving_Target
            moving target to be discovered 待发现的目标
            -> m_target.T0 : int 
                The number of frames when the object appears 物体出现时的帧数        
        Radar : radar
            1 雷达

        """

    def run_1(self, Target_lst, Radar_lst):
        """
        run_1 : A research method of one radar and one targets

        Parameters
        Target : Moving_Target
            moving target to be discovered 待发现的目标
            -> m_target.T0 : int 
                The number of frames when the object appears 物体出现时的帧数        
        Radar : radar
            1 雷达

        """
        start1 = time.perf_counter()
        t = self.t  # 雷达总时间的列表
        global locate_data
        global target_m0
        locate_data = json.loads(json.dumps({}))
        target_m0 = json.loads(json.dumps({}))

        for target in Target_lst:
            num = target.num
            t0 = target.t0
            p_s0 = target.pos
            v_p0 = np.array(eval(target.vel)).T
            a_s0 = target.acc
            # a_s0 = np.array(eval(target.acc)).T 
            MovementMode = target.MovementMode  # 是一个列表['匀速', '匀速']
            parament = target.parament
            # print(parament)
            DuringTime = target.DuringTime
            attribute = target.attribute

            all_radar_data_list = {}
            for radar_i, radar in enumerate(Radar_lst):
                p_p0 = radar.pos
                v_s0 = radar.vel

                N = len(t)  # 数据帧数
                T = (max(t) - min(t)) / N
                self.m0 = np.where(min(abs(t0 - t)) == abs(t0 - t))[0] + 1
                self.m = int(sum(self.m0) / len(self.m0))
                t0 = t[self.m]
                # print(t0)
                # print(type(p_p0), type(v_s0), type(min(t)))
                p_p = p_p0 + v_s0 * (t0 - min(t))  # 雷达t0时刻的位置
                R0 = np.linalg.norm(p_s0 - p_p)  # 目标出现时刻对应的距离，计算SNR的参考

                self.data_SNR = np.zeros((N, 1))
                self.data_range_r = np.zeros((N, 1))
                self.data_theta = np.zeros((N, 1))
                self.data_phi = np.zeros((N, 1))
                self.data_vel = np.zeros((N, 1))
                self.data_p_s = np.zeros((N, 3))
                self.data_v_s = np.zeros((N, 3))

                self.data_measure_cartesian_x = []
                self.data_measure_cartesian_y = []
                self.data_measure_cartesian_z = []
                self.p_sx = []
                self.p_sy = []
                self.p_sz = []


                Frame_i = 0
                for stage, DuringTime_i in enumerate(DuringTime):
                    while 1:
                        # for i in range(N):
                        while Frame_i < N:
                            if Frame_i > DuringTime_i * self.fs:
                                break
                            else:
                                # 处于第几阶段
                                # stage = DuringTime.index(DuringTime_i)
                                Mode = MovementMode[stage]
                                if Frame_i < self.m:
                                    Frame_i += 1
                                    continue
                                else:
                                    p_p = p_p0 + v_s0 * (t[Frame_i] - min(t))  # 雷达当前位置
                                    if Frame_i == self.m:  # 目标刚出现，信噪比等于于最小可检测信噪比
                                        self.data_p_s[Frame_i] = p_s0
                                        self.data_v_s[Frame_i] = v_p0
                                    else:
                                        if Mode == '匀速':
                                            self.data_v_s[Frame_i] = np.array(eval(parament[stage])).T
                                            self.data_p_s[Frame_i] = self.data_p_s[Frame_i - 1] + self.data_v_s[
                                                Frame_i - 1] * T

                                        elif Mode == '匀加速':
                                            a_s = np.array(eval(parament[stage])).T
                                            # print(a_s, self.data_v_s[Frame_i - 1])
                                            self.data_v_s[Frame_i] = self.data_v_s[Frame_i - 1] + a_s * T
                                            self.data_p_s[Frame_i] = self.data_p_s[Frame_i - 1] + self.data_v_s[
                                                Frame_i - 1] * T + 1 / 2 * a_s * pow(T, 2)

                                        elif Mode == '随机':
                                            a_s = a_s0 * (np.random.rand(1, 3) - 0.5)
                                            self.data_v_s[Frame_i] = self.data_v_s[Frame_i - 1] * (
                                                        np.random.rand(1, 3) - 0.5)
                                            self.data_p_s[Frame_i] = self.data_p_s[Frame_i - 1] + self.data_v_s[
                                                Frame_i - 1] * T + 1 / 2 * a_s * pow(T, 2)

                                        elif Mode == '静止':
                                            # a_s = np.array((0.0, 0.0, 0.0)).T
                                            self.data_v_s[Frame_i] = np.array((0.0, 0.0, 0.0)).T
                                            self.data_p_s[Frame_i] = self.data_p_s[Frame_i - 1]

                                # 目标真实参数
                                R_i = np.linalg.norm(self.data_p_s[Frame_i] - p_p)
                                theta_i, phi_i = Subfun_Theta_Phi(p_p, self.data_p_s[Frame_i])

                                vel_i = self.data_v_s[Frame_i].dot(((self.data_p_s[Frame_i] - p_p) / R_i).T)  # 径向速度
                                self.data_SNR[Frame_i] = self.SNRO * pow((R0 / R_i), 4)
                                #  观测值

                                delta_range = self.rate_r * (np.random.rand(1) - 0.5)[0] * 0.5  # 0.5是为了让误差更小
                                self.data_range_r[Frame_i] = R_i + delta_range
                                accuracy = pow(10, ((-0.6 * (
                                        10 * np.log10(
                                    self.data_SNR[Frame_i]) - 10) - 10) / 10))  # 不同信噪比对应测角精度不同，(10dB对应1/10，15dB对应1/20)

                                delta_theta = accuracy * self.theta_width * (np.random.rand(1) - 0.5)[0]
                                self.data_theta[Frame_i] = theta_i + delta_theta
                                delta_phi = accuracy * self.phi_width * (np.random.rand(1) - 0.5)[0]
                                self.data_phi[Frame_i] = phi_i + delta_phi
                                delta_vel = accuracy * self.res_v * (np.random.rand(1) - 0.5)[0]
                                self.data_vel[Frame_i] = vel_i + delta_vel

                                Frame_i += 1
                        # N个帧执行完就跳出while 1
                        # print("here")
                        # Frame_i += 1
                        # print(Frame_i)
                        break
                    # print("here2")

                self.data_measure_cartesian_x = self.data_range_r * [np.cos(i) for i in self.data_theta] * [np.cos(j)
                                                                                                            for j
                                                                                                            in
                                                                                                            self.data_phi]
                self.data_measure_cartesian_y = self.data_range_r * [np.sin(ii) for ii in self.data_theta] * [np.cos(jj)
                                                                                                              for
                                                                                                              jj in
                                                                                                              self.data_phi]
                self.data_measure_cartesian_z = self.data_range_r * [np.sin(k) for k in self.data_phi]
                self.p_sx, self.p_sy, self.p_sz = self.data_p_s[:, 0], self.data_p_s[:, 1], self.data_p_s[:, 2]

                self.p_deltax = np.abs(self.data_measure_cartesian_x.T - self.p_sx).T
                self.p_deltay = np.abs(self.data_measure_cartesian_y.T - self.p_sy).T
                self.p_deltaz = np.abs(self.data_measure_cartesian_z.T - self.p_sz).T

                all_radar_data_list[str(radar_i + 1) + "_num_radar"] = {
                    "data_measure_cartesian_x": self.data_measure_cartesian_x.tolist(),
                    "data_measure_cartesian_y": self.data_measure_cartesian_y.tolist(),
                    "data_measure_cartesian_z": self.data_measure_cartesian_z.tolist(),
                    "p_sx": self.p_sx.tolist(),
                    "p_sy": self.p_sy.tolist(),
                    "p_sz": self.p_sz.tolist(),
                    "p_deltax": self.p_deltax.tolist(),
                    "p_deltay": self.p_deltay.tolist(),
                    "p_deltaz": self.p_deltaz.tolist()
                }
            # =====================================================================
            m0_and_attribute = {
                "t": self.t.tolist(),
                "m0": int(self.m0),
                "attribute": attribute
            }
            target_m0.update(
                {
                    num: m0_and_attribute
                }
            )
            # =====================================================================

            locate_data.update(
                {
                    num: all_radar_data_list
                }
            )
        with open("target_m0.json", 'w', encoding='utf-8') as file0:
            json.dump(target_m0, file0)
            print("target_m0.json已保存")

        with open("locate_data.json", 'w', encoding='utf-8') as file:
            json.dump(locate_data, file)
            # print("locate_data_new.json已保存")
            # ===========================================
        # START==============构造0_radar=========START
        locate_data_copy = locate_data

        # print(locate_data_copy)
        for target_i in locate_data:
            new_target = {}
            radar_data = locate_data[target_i]
            N = len(radar_data["1_num_radar"]['data_measure_cartesian_x'])
            NN = len(locate_data[target_i])
            data_measure_cartesian_x_all = np.zeros(N)
            data_measure_cartesian_y_all = np.zeros(N)
            data_measure_cartesian_z_all = np.zeros(N)
            p_deltax_all = np.zeros(N)
            p_deltay_all = np.zeros(N)
            p_deltaz_all = np.zeros(N)
            for radar_ii in radar_data:
                data_measure_cartesian_x = np.array([x[0] for x in radar_data[radar_ii]['data_measure_cartesian_x']])
                locate_data_copy[target_i][radar_ii]['data_measure_cartesian_x'] = data_measure_cartesian_x.tolist()
                data_measure_cartesian_y = np.array([y[0] for y in radar_data[radar_ii]['data_measure_cartesian_y']])
                locate_data_copy[target_i][radar_ii]['data_measure_cartesian_y'] = data_measure_cartesian_y.tolist()
                data_measure_cartesian_z = np.array([z[0] for z in radar_data[radar_ii]['data_measure_cartesian_z']])
                locate_data_copy[target_i][radar_ii]['data_measure_cartesian_z'] = data_measure_cartesian_z.tolist()
                # p_sx = np.array(radar_data[radar_ii]['p_sx'])
                # p_sy = np.array(radar_data[radar_ii]['p_sy'])
                # p_sz = np.array(radar_data[radar_ii]['p_sz'])
                p_deltax = np.array([zx[0] for zx in radar_data[radar_ii]['p_deltax']])
                locate_data_copy[target_i][radar_ii]['p_deltax'] = p_deltax.tolist()
                p_deltay = np.array([zy[0] for zy in radar_data[radar_ii]['p_deltay']])
                locate_data_copy[target_i][radar_ii]['p_deltay'] = p_deltay.tolist()
                p_deltaz = np.array([zz[0] for zz in radar_data[radar_ii]['p_deltaz']])
                locate_data_copy[target_i][radar_ii]['p_deltaz'] = p_deltaz.tolist()

                # add all
                data_measure_cartesian_x_all += data_measure_cartesian_x
                data_measure_cartesian_y_all += data_measure_cartesian_y
                data_measure_cartesian_z_all += data_measure_cartesian_z
                p_deltax_all += p_deltax
                p_deltay_all += p_deltay
                p_deltaz_all += p_deltaz
            zero_radar = {
                "data_measure_cartesian_x": (data_measure_cartesian_x_all / NN).tolist(),
                "data_measure_cartesian_y": (data_measure_cartesian_y_all / NN).tolist(),
                "data_measure_cartesian_z": (data_measure_cartesian_z_all / NN).tolist(),
                "p_sx": radar_data["1_num_radar"]['p_sx'],
                "p_sy": radar_data["1_num_radar"]['p_sy'],
                "p_sz": radar_data["1_num_radar"]['p_sz'],
                "p_deltax": (p_deltax_all / NN).tolist(),
                "p_deltay": (p_deltay_all / NN).tolist(),
                "p_deltaz": (p_deltaz_all / NN).tolist()
            }
            # print(zero_radar)
            new_target["0_num_radar"] = zero_radar
            for radar_iii in locate_data_copy[target_i]:
                new_target[radar_iii] = locate_data_copy[target_i][radar_iii]
            locate_data_copy.update(
                {
                    target_i: new_target
                }
            )

        with open("locate_data.json", 'w', encoding='utf-8') as file:
            json.dump(locate_data_copy, file)
            print("locate_data.json已保存")
        # END==============构造0_radar=========END

        start2 = time.perf_counter()
        print("程序用时：", start2 - start1)

if __name__ == '__main__':
    """
    Tests for simulation module.
    """
    t_0 = Target(pos=np.array([50e3, 50e3, 8e3]).T, vel=np.array([-100, 0, 0]).T,
                 posture=np.array([0, 0, 0]).T, motion_model='Singer', acc=5, t0=10)

    r_0 = Radar(pos=np.array([0, 0, 0]).T, vel=np.array([0, 0, 0]).T)

    p_0 = Platform(time=600, fs=10, SNRO=pow(10, 12 / 10), res_r=100,
                   res_v=10, theta_width=5 / 180 * np.pi, phi_width=5 / 180 * np.pi)

    p_0.run_1(t_0, r_0)

    p_0.draw_gif_pic_2d()
    p_0.draw_delta_xyz()
