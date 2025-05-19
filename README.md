# Hackathon_Hairloss-project

#### 2024 빅데이터/AI 해커톤 탈모 및 피부 셀프 점검 프로젝트 - 장려상 :trophy:

## 문제 정의
건강보험관리공단에 따르면 국내 탈모 인구가 10000만명으로 추산되고 10~30대 젊은 탈모 환자가 전체의 50%를 차지하고 있을 정도로 심각한 탈모화 시대
또한 슬로우 에이징이 새로운 뷰티 트렌드로 자리 잡고 있을만큼 유튜브, SNS 등에서 자가 탈모 진단 방법, 피부관리법 등이 큰 인기를 끌고 있다.

<p align="center">
  <img alt="탈모 뉴스" src="https://github.com/user-attachments/assets/0b33d7b0-c80b-4d17-a0ab-36df99a505bd" width="45%"/>
  <img alt="슬로우 에이징 뉴스" src="https://github.com/user-attachments/assets/98d52c21-39d0-4cc7-a9f9-653a0b11fd82" width="45%" />
</p>
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

<img width="434" alt="image" src="https://github.com/user-attachments/assets/e07f9025-89f6-4790-a8b8-80acd0e00efd" />
<img width="441" alt="image" src="https://github.com/user-attachments/assets/0811010a-3275-4196-83fd-539454c9f2c6" />
<img width="396" alt="image" src="https://github.com/user-attachments/assets/be53803c-790d-4f7c-be04-77022482d5da" />
<p align="center">
  <img src="https://github.com/user-attachments/assets/e07f9025-89f6-4790-a8b8-80acd0e00efd" width="30%">
  <img src="https://github.com/user-attachments/assets/0811010a-3275-4196-83fd-539454c9f2c6" width="30%">
  <img src="https://github.com/user-attachments/assets/be53803c-790d-4f7c-be04-77022482d5da" width="30%">
</p>

초기 구성한 데이터 셋은 class도 다르고 class 별 instance 수 또한 데이터 불균형 심각  :arrow_forward: 이미지 검수하여 데이터의 레벨이 균하게 이루어진 데이터로 병합
LOW|MIDDLE|HIGH로  class 재 구성 ==> Low = 정상, Mid = 탈모 진행중, High = 탈모 심각






