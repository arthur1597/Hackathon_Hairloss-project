# Hackathon_Hairloss-project

#### 2024 빅데이터/AI 해커톤 탈모 및 피부 셀프 점검 프로젝트 - 장려상 :trophy: 수상

## 문제 정의
건강보험관리공단에 따르면 국내 탈모 인구가 10000만명으로 추산되고 10~30대 젊은 탈모 환자가 전체의 50%를 차지하고 있을 정도로 심각한 탈모화 시대
또한 슬로우 에이징이 새로운 뷰티 트렌드로 자리 잡고 있을만큼 유튜브, SNS 등에서 자가 탈모 진단 방법, 피부관리법 등이 큰 인기를 끌고 있다.
<p align="left" style="font-size:12px">
  * 출처: <a href="http://www.biotimes.co.kr" target="_blank">Bio Times</a>
</p>
따라서 스스로 탈모 진단과 피부 상태를 진단할 수 있는 시스템을 개발하여 본인의 탈모 정도를 파악 할 수 있게 하는 것이 목표

# 데이터 선정 및 수집
## 데이터 수집
탈모 정도, 피부 타입 진단을 위한 AI 모델을 구현하기 위해다양한 공개 이미지 데이터셋을 수집하고 목표에 맞게 재라벨링 진행

## 사용한 데이터셋

| [Hair Loss Dataset (UZE)](https://universe.roboflow.com/uze/hair-loss-nq8hh) | [HEXA Dataset (Mohit)](https://universe.roboflow.com/mohit-srivastava/hexa-7bin2) | [SkinProblem](https://universe.roboflow.com/dmrai/skinproblem/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true) |
|:--:|:--:|:--:|

<p align="center">
  <img src="https://github.com/user-attachments/assets/e07f9025-89f6-4790-a8b8-80acd0e00efd" width="30%", height="180">
  <img src="https://github.com/user-attachments/assets/0811010a-3275-4196-83fd-539454c9f2c6" width="30%", height="180">
  <img src="https://github.com/user-attachments/assets/be53803c-790d-4f7c-be04-77022482d5da" width="30%", height="180">
</p>

* 초기 구성한 데이터 셋은 class도 다르고 class 별 instance 수 또한 데이터 불균형 심각
* 이미지 검수하여 데이터의 레벨이 균하게 이루어진 데이터로 병합 및 데이터셋 추가 + 라벨링으로 불균형 다소 해소
* LOW|MIDDLE|HIGH로  class 재 구성 ==> Low = 정상, Mid = 탈모 진행중, High = 탈모 심각

## 사용 모델
Yolo = 객체 탐지 모델
Unet = 이미지 특징 추출

## 탈모 정도 및 피부 진단 모델 결과
* 탈모 정도 파악 모델
<img width="822" alt="image" src="https://github.com/user-attachments/assets/3905ce3b-4fb6-4757-94a4-f101d66a09d7" />

:arrow_forward: 전반적으로 학습이 잘 되는듯 하나 val/box_loss가 초반에 감소하는 듯 하나 변동이 심한 것으로 과적합이 발생하지 않도록 다양성을 학습중인 것으로 보임 

:arrow_forward: mAP 값 증가하는 추세를 보이나 mAP50-95의 결과값이 약 0.4정도로 좋지 않은 모습을 보임

* 피부 진단 모델
<img width="822" alt="image" src="https://github.com/user-attachments/assets/76e89415-9e23-4eb9-b0e9-6394549f891e" />

:arrow_forward: 전반적으로 학습은 잘 진행되나 Presion과 Recall 값이 변동이 심하고 mAP50-95값의 상승 폭이 줄어드는 것으로 보아 epoch이 진행될수록 학습의 효율성 떨어짐

:heavy_exclamation_mark:탈모 발생지가 확실한 이미지에서는 탐지와 정도를 잘 예측하지만 애매한 탈모는 잘 예측하지 못함

따라서 Yolo 단일 모델이 아닌 Unet과 결합한 모델을 구축하기로 계획

#### Yolo + Unet 모델 구조
1.  Yolo를 이용하여 바운딩 박스의 좌표를 계산
2.  계산한 바운딩 박스 면적에 있는 픽셀 Mask 처리
3.  Mask Image를 이용하여 Unet을 이용하여 특징 추출

<p align="center">
  <img src="https://github.com/user-attachments/assets/facb3fd9-c0f6-4217-ac76-d46611bcebdf" width="30%" >
  <img src="https://github.com/user-attachments/assets/9dedb7ee-3543-4344-8608-a7a398201193" width="30%" >
</p>

### 성능 개선 

<p align="center">
  <img src="https://github.com/user-attachments/assets/b5e09910-fef3-438a-beb5-9e99bdc9909a" width="30%" >
  <img src="https://github.com/user-attachments/assets/5acb7bdc-11c2-46b1-b1c3-ee5dd94efe77" width="30%" >
</p>

* Yolo 단일 모델 (왼쪽): 탐지하지 못하는 경우 발생
* Yolo + Unet 결합 모델 (오른쪽) : 탐지 안되던 것까지 탐지가 되는 모습

#### 서비스 구현
![Picture-4](https://github.com/user-attachments/assets/ae392865-7e8e-41da-90e1-ccd088a92dea)

* 서비스 구현은 팀원 중 한분이 진행하여 코드를 깃에 올리지 않고 허락을 받고 실행 결과만 기제(Flask + html)

## 한계
mask 처리가 제대로 되지않으면 모델 성능에 큰 영향 끼짐 /
Yolo 모델의 성능이 해커톤 대회 시간 + 기타 등등의 문제로 성능 향상으로 크게 하지 못함

> 팀장으로 참가하여 모델 구현 + 팀 관리 역할을 맡아서 수행하였음

