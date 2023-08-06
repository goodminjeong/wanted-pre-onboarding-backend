# 원티드 프리온보딩 백엔드 인턴십 - 사전 과제
## 구민정


## 애플리케이션의 실행 방법 (엔드포인트 호출 방법 포함)
#### 깃허브 클론하기
```
$ git init
$ git clone git@github.com:goodminjeong/wanted-pre-onboarding-backend.git
```
#### 패키지 밎 라이브러리 설치
```
$ pip install -r requirements.txt
```
#### .env 파일 설정
```
DEBUG=True
SECRET_KEY="시크릿키"
SIGNING_KEY="싸이닝키" <-시크릿키랑 같은 유형의 문자열
DB_NAME="데이터베이스명"
DB_USER="사용자명"
DB_PASSWORD=비밀번호
DB_HOST=호스트번호
DB_PORT=포트번호
```
#### DB 연동
```
$ python manage.py makemigrations
$ python manage.py migrate
```
#### 백엔드 서버 실행
```
$ python manage.py runserver
```
#### Swagger 접속 후 엔드포인트 호출
```
http://localhost:8000/swagger
각 API 클릭 -> Try it out 클릭 -> (데이터 작성 후) execute 클릭
```

## 데이터베이스 테이블 구조
![image](https://github.com/goodminjeong/wanted-pre-onboarding-backend/assets/125722304/34dd8804-ba37-42ca-8f80-075cc6fde7f1)

## 구현한 API의 동작을 촬영한 데모 영상 링크
https://youtu.be/jdkjgpdYWlE

## 구현 방법 및 이유에 대한 간략한 설명
- 회원가입
    - 회원가입 시리얼라이저에서 password 필드 min_length를 8로 설정해서 유효하지 않은 비밀번호 입력 시 유효성 검사에 따른 안내 문구가 나옴
    - BaseUserManager를 상속받은 UserManager 클래스에서 유저 객체 생성 시 normalize_email 메서드를 통해 이메일 형식에 맞지 않은 값 입력 시 안내 문구가 나옴
- 로그인
    - 시리얼라이저 validate 메서드를 커스텀 하여, 요구사항을 따르는 이메일과 비밀번호에 대한 유효성 검사 진행함
- 글 목록 조회
    - DRF의 PageNumberPagination을 활용하여 페이지네이션 구현함
- 특정 글 조회
    - url에 특정 글의 id를 받아 해당 id와 일치하는 특정 게시글을 조회함
    - 존재하지 않는 글의 id 입력 시 발생할 에러를 방지하기 위해 get_object_or_404() 메서드를 활용함
- 글 작성
    - 제목, 내용은 필수, 이미지는 선택사항으로 설정함
    - 작성자를 DB에 담긴 데이터로 식별하기 위해 로그인 한 사용자만 게시글 작성할 수 있도록 함
- 글 수정
    - 제목만, 내용만 수정하고 싶은 경우를 고려하여 부분 수정이 가능하게끔 partial=True 옵션을 설정함
    - 게시글 작성자와 request.user를 비교하여 일치하는 경우에만 수정이 가능하도록 함
- 글 삭제
    - 게시글 작성자와 request.user를 비교하여 일치하는 경우에만 삭제가 가능하도록 함

## API 명세(request/response 포함)
| 기능 | method | url | request | response |
| ---- | ---- | ---- | ---- | ---- |
| 회원가입 | `POST` | api/users/signup/ | {"email", "password"} | {"data":유저 정보들,"status", "message"} |
| 로그인 | `POST` | api/users/signin/ | {"email", "password"} | {"data":{"access","refresh"},"status", "message"} |
| 글 목록 조회 | `GET` | api/articles/ | - | {"count":글개수,"next":다음페이지,"previous":이전페이지,"results":글정보} |
| 특정 글 조회 | `GET` | api/articles/<int:article_id> | - | {"data":글 정보들,"status", "message"} |
| 글 작성 | `POST` | api/articles/ | {"title","content","image"} | {"data":글 정보들,"status", "message"} |
| 글 수정 | `PUT` | api/articles/<int:article_id> | {"title","content","image"} | {"data":글 정보들,"status", "message"} |
| 글 삭제 | `DELETE` | api/articles/<int:article_id> | - | {"status", "message"} |