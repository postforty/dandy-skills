---
name: address-geocoding
description: VWorld(국토교통부 국가공간정보) 및 OpenStreetMap을 활용하여 한국 주소(도로명/지번) 및 장소명의 정확한 위도, 경도 좌표와 상세 주소 정보를 조회합니다. 주소의 위경도 좌표 변환(지오코딩)이 필요할 때 사용하세요.
---

# Address Geocoding Skill

한국의 도로명 주소, 지번 주소, 건물명, 주요 랜드마크(POI)의 정확한 위도/경도 좌표를 조회하는 스킬입니다.
**국토교통부 VWorld Geocoder 2.0 및 검색 2.0 API**를 기본 연동하여 국내 건물 번호 및 상호명 단위까지 정밀 지오코딩을 지원하며, 키가 없거나 조회 실패 시 **OpenStreetMap (Nominatim)**으로 자동 폴백합니다.

---

## 🔑 VWorld API 키 설정 방법 (선택 사항 및 권장)

VWorld 인증키가 있는 경우 다음 3가지 방법 중 하나로 설정할 수 있습니다:

1. **`.env` 파일에 등록 (가장 권장)**
   - 프로젝트 루트(`.env`) 또는 스킬 폴더(`.agents/skills/address-geocoding/.env`)에 다음 내용을 추가합니다:
     ```env
     VWORLD_API_KEY=발급받은_VWORLD_인증키
     VWORLD_DOMAIN=http://localhost
     ```

2. **환경 변수 설정**
   - 시스템/쉘 환경 변수로 등록:
     ```powershell
     $env:VWORLD_API_KEY="발급받은_VWORLD_인증키"
     ```

3. **명령어 인자로 전달 (`--key`)**
   - 스크립트 실행 시 `--key [인증키]` 옵션으로 직접 전달할 수 있습니다.

> [!NOTE]
> VWorld API 키가 등록되지 않은 상태에서도 무료 OpenStreetMap (Nominatim)을 통해 기본 좌표 변환이 자동으로 동작합니다.

---

## 🚀 실행 단계

1. 사용자가 조회하고자 하는 주소 또는 장소명을 확인합니다 (예: "부산광역시 남구 문현금융로 40", "부산 남구 남동천로 128", "서울역" 등).
2. `run_command` 도구를 사용하여 파이썬 스크립트를 실행합니다:
   - **기본 실행 (가독성 높은 텍스트 출력)**:
     ```bash
     python .agents/skills/address-geocoding/scripts/get_coordinates.py "[주소 또는 장소명]"
     ```
   - **JSON 포맷 출력 (구조화된 데이터 필요 시)**:
     ```bash
     python .agents/skills/address-geocoding/scripts/get_coordinates.py "[주소 또는 장소명]" --json
     ```
   - **특정 API 키 직접 지정 실행**:
     ```bash
     python .agents/skills/address-geocoding/scripts/get_coordinates.py "[주소 또는 장소명]" --key "[VWORLD_KEY]" --json
     ```
3. 출력된 결과에서 위도(`latitude`), 경도(`longitude`), 도로명/지번 주소(`road_address`, `parcel_address`), 데이터 출처(`source`)를 추출합니다.
4. 사용자에게 친절하고 명확한 한국어로 위도/경도 좌표 및 위치 정보를 안내합니다.

---

## 💡 지원 기능
- **VWorld 도로명 주소 지오코딩**: 건물 번호 단위 100% 정밀 좌표 변환
- **VWorld 지번 주소 지오코딩**: 번지/호수 단위 정밀 좌표 변환
- **VWorld 공간 검색(POI)**: 빌딩명, 상호명, 랜드마크 검색 지원
- **주소 전처리(정제)**: 층수, 호수 등 상세 부가정보 자동 필터링 후 검색
- **OpenStreetMap (Nominatim) 자동 폴백**: API 키 부재 또는 장애 시 끊김 없는 서비스 제공
