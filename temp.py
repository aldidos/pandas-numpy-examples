import numpy as np
import matplotlib.pyplot as plt

# 1. 사용자로부터 데이터 입력 받기
n = int(input("측정 데이터의 개수를 입력하세요: "))

weights = []    # 무게 (kg)
velocities = [] # 속도 (m/s)
powers = []     # 파워 (W)

for i in range(n):
    print(f"\n데이터 {i+1} 입력:")
    weight = float(input("  무게 (kg): "))
    velocity = float(input("  속도 (m/s): "))
    power = float(input("  파워 (W): "))
    weights.append(weight)
    velocities.append(velocity)
    powers.append(power)

# numpy 배열로 변환
weights = np.array(weights)
velocities = np.array(velocities)
powers = np.array(powers)

# 2. F-V 프로파일 선형회귀모델 계산 (모델: V = a - b * weight)
# 일반 선형회귀식: y = A + B*x 에서 A = a, B = -b 로 해석
n_data = len(weights)
sum_x  = np.sum(weights)
sum_y  = np.sum(velocities)
sum_xy = np.sum(weights * velocities)
sum_x2 = np.sum(weights**2)

B_u = ((n_data * sum_xy) - (sum_x * sum_y))
B_b = ((n_data * sum_x2) - sum_x**2)

B = ((n_data * sum_xy) - (sum_x * sum_y)) / ((n_data * sum_x2) - sum_x**2)
A = (sum_y - (B * sum_x)) / n_data

a = A       # 무부하 시 이론적 최대 속도
b = -B      # 하중 1kg당 속도 감소율

print("\n--- 선형회귀 결과 ---")
print(f"회귀모델: V = {a:.4f} - {b:.5f} * weight")

# 3. 최소 임계속도(MVT)를 이용하여 1RM 무게 추정 (MVT = 0.2 m/s)
MVT = 0.2
weight_1RM = (a - MVT) / b
print(f"추정된 1RM 무게: {weight_1RM:.2f} kg (최소 임계속도: {MVT} m/s)")

# 4. 회귀모델에 따른 예측값 계산
# 무게 범위를 데이터 범위에 약간 여유를 두어 설정
weight_range = np.linspace(min(weights)-5, max(weights)+5, 100)
velocity_fit = a - b * weight_range
power_fit = weight_range * velocity_fit  # 파워 = weight * velocity

# 5. 하나의 2D 그래프에 F-V (좌측 y축)와 파워 (우측 y축) 함께 그리기
fig, ax1 = plt.subplots(figsize=(10, 6))

# 좌측: F-V 프로파일 (속도)
color_vel = 'tab:blue'
ax1.set_xlabel('무게 (kg)', fontsize=12)
ax1.set_ylabel('속도 (m/s)', color=color_vel, fontsize=12)
line1 = ax1.plot(weight_range, velocity_fit, color=color_vel, linewidth=2,
                 label=f'회귀선: V = {a:.4f} - {b:.5f}×weight')
sc1 = ax1.scatter(weights, velocities, color='red', s=50, label='측정 데이터 (속도)')
# 추정된 1RM (속도 축)
sc2 = ax1.scatter([weight_1RM], [MVT], color='green', s=100, label='추정 1RM (속도)')
ax1.tick_params(axis='y', labelcolor=color_vel)
ax1.grid(True)

# 우측: 파워 프로파일 (파워)
ax2 = ax1.twinx()
color_power = 'tab:orange'
ax2.set_ylabel('파워 (W)', color=color_power, fontsize=12)
line2 = ax2.plot(weight_range, power_fit, color=color_power, linewidth=2,
                 label='예측 파워: P = weight × (a - b×weight)')
sc3 = ax2.scatter(weights, powers, color='magenta', s=50, label='측정 데이터 (파워)')
# 추정된 1RM 파워: weight_1RM * MVT
sc4 = ax2.scatter([weight_1RM], [weight_1RM * MVT], color='green', s=100,
                  label='추정 1RM 파워')
ax2.tick_params(axis='y', labelcolor=color_power)

# 범례 결합
lines = line1 + line2
scatters = [sc1, sc3]
leg_labels = [l.get_label() for l in lines] + [s.get_label() for s in scatters] + ['추정 1RM (속도)', '추정 1RM 파워']
# ax1.legend()는 두 축의 객체들을 따로 처리해야 하므로, 각각의 범례를 합치는 방법을 사용
labs1 = [line.get_label() for line in line1]
labs2 = [line.get_label() for line in line2]
ax1.legend(line1 + line2, labs1 + labs2, loc='upper right')

plt.title('F-V Profile와 파워 프로파일 (동일 그래프)', fontsize=14)
plt.tight_layout()
plt.show()
