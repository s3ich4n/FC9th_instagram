# Instagram 카피

## Contents

### 1. 환경설정
### 2. 디렉토리 구조
### 3. 할일

---

### 1. 환경설정.

DB: SQLite3
Python: 3.6.5
Django: 2.1.2
그 외는 requirements.txt 참조 바랍니다.

---

### 2. 디렉토리 구조



---

### 3. 할일

## 모델 설계
    * Post
        * Comment list
        * Photo
    * Comment
        * author
        * contents
        * hashtags
        * mentions
    * Hashtag
        * tag_name
    * User(기본모델)
        * username
        * name
        * profile_image(thumbnail?)
        * website
        * Bio
        
## 화면 설계
    * 프로필
        * 프로필 수정
        * 내 게시물 목록
        * 내 팔로워 목록
        * 내 팔로잉 목록
    * 로그인
    * 팔로우/언팔로우/블락
    * 포스트 디테일
        * 포스트 피드 (포스트 리스트)
        * 포스트 작성
            * 포스트 좋아요/좋아요 취소
        * 포스트에 댓글
            * 작성/수정/삭제
    * 해시태그 검색
