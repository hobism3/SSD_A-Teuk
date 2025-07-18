# A-Teuk Team SSD Project
###### 팀원 : 황웅범님, 이민호님, 최새롬님, 박소정님, 홍승표님, 이준태님 <br>
###### 프로젝트 기간 : 2025-07-14 ~ 2025-07-18
## Introduction
본 프로젝트에서는 소프트웨어로 구현된 SSD(Storage Solid-State Drive)를 대상으로, SSD 동작 검증을 위한 애플리케이션을 개발합니다. <br>
SSD 하드웨어를 대신하는 ssd.py 모듈과, 이를 테스트하는 shell.py Test Shell 프로그램을 포함하여, 다양한 테스트 스크립트를 작성할 수 있는 환경을 제공합니다. 또한, Logger, Runner, Buffer 등의 부가 기능 개발도 함께 수행하여, SSD의 기능 구현 및 검증 전반을 지원하는 통합 테스트 환경을 구축합니다.
<br>
## Purpose
#### • Clean Code / Refactoring / TDD 수행
SSD, Shell 기능 구현시 TDD 를 적용하여 각 Feature들이 Testable하도록 구현하고, 지속적인 Refactoring을 통해 Clean Code를 작성하는 것을 목표로 합니다.
#### • SSD Program 100% 구현
팀 프로젝트를 통한 git 코드 형상 관리 방법을 익히고, 팀 협업, 커뮤니케이션을 활용하여 요구하는 SRS에 맞게 프로그램을 구현을 목표로 합니다.
<br><br><br>

## 팀소개

### A-Teuk Team 이란?  
The A-Team(A-특공대)라는 의미로 Code Review 전문가들의 팀이라는 의미를 담고 있습니다.
저희 팀은 FIRST원칙을 준수하는 코드를 작성하며, 보이스카우트 원칙(Scout Rule)에 따라 이전 보다 Clean한 코드를 Commit한다는 팀의 목표를 가지고 있습니다.
<br>

---

### 팀원 소개 및 역할 할당

| 팀원         | 역할                      | 메일                       |
|--------------|---------------------------|----------------------------|
| 황웅범님     | SSD Feature Developer <br> (팀장)👑슈퍼 긍정으로 항상 팀의 분위기를 밝게 만들어 주는 리더십 마스터 | hobism3@gmail.com          |
| 이민호님     | SSD Feature Developer <br> Clean Code의 아버지로 항상 Clean한 코드만 작성하는 LGTM 수집가, Clean Code 마스터   | oz101@naver.com           |
| 최새롬님     | Shell Feature Developer <br> Refactoring 마스터로 Feature 구현 & Refactoring 모두 훌륭한 실력을 가진 코딩 마스터 | develope.nerd@gmail.com          |
| 박소정님     | SSD Feature Developer <br> Design Pattern 마스터로 SW의 확장성을 고려해 적합한 Pattern을 적용하는 디자인 마스터 | ssjjjjjpppp@gmail.com          |
| 홍승표님     | Shell Feature Developer <br> Code Review 마스터로 팀원들에게 항상 새로운 관점을 제시하는 CR 마스터 | robin5544@naver.com      |
| 이준태님     | Shell Feature Developer <br> TDD 마스터로 조기 버그 발견과 높은 Code Coverage를 유지하는 Test 마스터                 | dlwnsxo98@naver.com       |

---

<br>

## Ground Rule
- 17시 퇴근
- PR 16시 이후 금지
- 2인 이상 승인후, PR merge
- commit message format 은 google conventional commit으로 한다.
- 아침/퇴근 인사하기
- 2시간 안에 리뷰하기
- 점심식사 준수: 11시~12시30분
- git hook(pre-commit) 사용해서 코딩(commit 하기 전에 검열 해주는 친구들)
- Merge 할 때, rebase로 합치기



## 팀 코드리뷰 전략
- self-review 걸치고 pr 올리기
- pr에 설명을 구체적으로, 이해할 수 있을 정도로 작성하기
- pr에 템플릿 정해서 준수
- feature 브랜치의 경우 pr의 크기 300줄 이내로 한다.(refactor 는 알아서)
- 테스트 코드를 함께 작성한다.(테스트 결과도 함께 PR에 캡처해서 올린다)
- (code pearl 스타일로)변경사항이 아니더라도, 좋은 코드에 대해서는 긍정적인 반응과 칭찬을 작성한다.

<br>

## 구현 Feature

### SSD (ssd.py)

- **저장 범위**: 0 ~ 99 인덱스(LBA)에 32비트 16진수 값 저장 가능 (`0x00000000` ~ `0xFFFFFFFF`)  
- **초기 상태**: `ssd_nand.txt`에 0부터 99까지 모두 `0x00000000` 기록  
- **파일 입출력 방식**  
  - 모든 명령(R/W)은 `ssd_nand.txt`를 전부 읽은 후 처리  
  - 읽기(R): 지정 인덱스 값을 `ssd_output.txt`에 기록  
  - 쓰기(W): 지정 인덱스 값 변경 후 전체 내용 `ssd_nand.txt`에 저장, `ssd_output.txt`는 빈 파일로 변경  
  - 에러 발생 시 `ssd_output.txt`에 `ERROR` 기록  
- **명령어 실행 후 프로그램 종료**  
- **추가 명령어**  
  - Erase(E): 지정 LBA부터 SIZE 만큼 `0x00000000`으로 초기화
    - `E [LBA] [SIZE]` (1 ≤ SIZE ≤ 10)
- **Flush(F)**: 버퍼에 저장된 명령 모두 실행, 버퍼 초기화
- **Buffer**: 버퍼 파일을 활용한 SSD 성능 최적화 방안 적용
---



### Test Shell (shell.py)

- **목적**: SSD 기능 테스트를 위한 Interactive Shell
- **지원 명령어**  
  - `read [LBA]` : 특정 인덱스 읽기  
  - `write [LBA] [VALUE]` : 특정 인덱스 쓰기  
  - `erase [LBA] [SIZE]` : 특정 범위 삭제 (삭제 범위 100까지 가능)  
  - `erase_range [ST_LBA] [EN_LBA]` : 구간 삭제 (시작 LBA ≤ 종료 LBA)  
  - `fullread` : 전체 0~99 인덱스 읽기  
  - `fullwrite [VALUE]` : 전체 인덱스 지정 값으로 쓰기  
  - `flush` : SSD 버퍼 비우기 (Flush 기능)  
  - `exit` : 프로그램 종료  
  - `help` : 사용법 출력  
  - `1_`, `2_`, `3_`, `4_` 등으로 테스트 스크립트 실행 가능
- **예외처리**  
  - 없는 Command 입력 시 `INVALID COMMAND` 출력  
  - Parameter 갯수/Type 오류 및 범위 벗어남 시 에러 메시지 처리



---


### Test Script 명령어

- **1_FullWriteAndReadCompare (1_)**  
  - 0~4 LBA에 랜덤값 동일하게 쓰기 후 검증  
  - 5~9 LBA에 다른 랜덤값 동일하게 쓰기 후 검증  
  - 전체 0~99 반복 수행  
- **2_PartialLBAWrite (2_)**  
  - 30회 반복  
  - 0,1,2,3,4 LBA에 동일 랜덤값 쓰기 후 일치 여부 확인  
- **3_WriteReadAging (3_)**  
  - 200회 반복  
  - 0, 99 LBA에 동일 랜덤값 쓰기 및 검증  
- **4_EraseAndWriteAging (4_)**  
  - 반복적으로 일부 LBA 영역 삭제 후 랜덤값 쓰기 및 검증 수행  

- **테스트 실행 시**  
  - `PASS` 또는 `FAIL` 결과 출력  
  - 실패 시 즉시 종료, 다음 테스트 미실행

---



### Logger (Test Shell)

- **로그 파일명 및 관리**  
  - 기본 로그 파일: `latest.log`  
  - 파일 용량 10KB 초과 시 `until_YYMMDD_HHh_MMm_SSs.log`로 이름 변경 후 새 로그 생성  
  - 두 개 이상의 `until_` 파일 존재 시 가장 오래된 파일 확장자 `.zip`으로 변경  
---




### Runner 기능

- Test Shell 실행 시 스크립트 파일 입력 가능  
- 스크립트 내에 테스트 명령어 순차 실행  
- 실행 결과 출력 후 실패 시 즉시 중단  
- 실행 예시
```
python .\shell.py .\path\to\shell_script.txt
```


---


### Command Buffer

- `.\buffer` 폴더 내 5개 파일 (`1_empty` ~ `5_empty`)로 명령어 임시 저장  
- 각 파일명에 명령어 정보를 포함하여 관리 (예: `1_W_20_0xABCDABCD`)  
- 중복되거나 불필요한 명령어는 병합하거나 삭제하여 SSD 파일(`ssd_nand.txt`) 접근 최소화  
- 예시:  
  - 동일 LBA에 여러 번 쓰기 명령이 있을 경우 마지막 명령만 유지  
  - 삭제 명령(Erase)이 있으면 이전 쓰기 명령은 무효화  
- Buffer는 실제 데이터 대신 파일명으로 명령어 상태를 표현  
- 명령어 순서와 효율성을 고려하여 버퍼 상태를 업데이트 함  
- Flush 명령(F)을 통해 버퍼에 저장된 모든 명령을 한꺼번에 실행 가능  
- 목표: 실제 SSD(파일) 변경 최소화로 성능 및 수명 최적화 목적
- Buffer file 예시
```
1_W_01_0x12341234 2_empty  3_empty  4_empty  5_empty
```



### Command Parsing Rule
- Memory 주소 check
  - isdigit() + in range(0, 100)
- value
  - 무조건 10자리, 0x로 시작, 8자리는 0123456789ABCDEF
- address와 value는 ' '(space)로 분리

<br>

## UML
- Top View Structure
<img width="793" height="787" alt="image" src="https://github.com/user-attachments/assets/f95358ee-9986-4abd-8d33-35eeb88938ca" />
<br><br>

---

- Shell UML
<img width="1229" height="848" alt="image" src="https://github.com/user-attachments/assets/5e353dc1-e26f-4dfa-86f7-5cd5e8c8225c" />
<br><br>

- Shell Mixin Structure
<img width="1860" height="643" alt="image" src="https://github.com/user-attachments/assets/cc93a2db-4151-43ad-884f-72d67a0af95c" />
<br><br>

---

- SSD UML
<img width="1746" height="655" alt="image" src="https://github.com/user-attachments/assets/95f9f71d-d52e-42f1-8eb8-0c769a5aaa6d" />
<br><br>

- Buffer Algorithm
<img width="1966" height="755" alt="image" src="https://github.com/user-attachments/assets/8051196a-b143-4781-acaa-809b71d5ddf9" />
<br><br>

---


<br>

## 실행 방법

- ssd 실행 예시
```
python ./ssd.py W 0 0xAAAABBBB 
```

- shell 실행
```
python ./shell.py
```

- Help Document
```
▷ Basic Commands
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
write [lba] [val]         -   writes a val on lba (ex. write 10 0x1234ABCD)
read [lba]                -   reads the val written on lba (ex. read 10)
exit                      -   exits program
help                      -   prints manual to stdout
fullwrite [val]           -   writes val to all lbas ranging from 0 to 99
fullread                  -   reads all vals written on each lba ranging from 0 to 99 and prints to stdout
erase [lba] [size]        -   wipes ssd 'size' amount of lbas starting from lba
erase_range [slba] [elba] -   wipes ssd lbas in range [slba, elba]
flush                     -   executes and clears all buffered commands (run with "flush" or "F")
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
▶ Script Commands
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
1_FullWriteAndReadCompare  -  writes/verifies random vals in 5-LBA blocks across full range; PASS/FAIL (run "1_")
2_PartialLBAWrite          -  writes/verifies same val to LBAs 0-4, 30 times; PASS/FAIL (run "2_")
3_WriteReadAging           -  writes/verifies same val to LBAs 0 and 99, 200 times; PASS/FAIL (run "3_")
4_EraseAndWriteAging       -  erases/writes vals in overlapping LBA ranges, 30 times; PASS/FAIL (run "4_")
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

<br>


## Test Coverage
###### UT Coverage 98%

<img width="599" height="509" alt="image" src="https://github.com/user-attachments/assets/c29b1b2a-ba40-41f7-99dc-2b0c3d225c70" />
<br><br>
